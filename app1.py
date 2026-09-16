import numpy as np
import pandas as pd
import warnings
import re
warnings.filterwarnings('ignore')

from flask import request, render_template, redirect,session
from werkzeug.security import generate_password_hash

import random
import pickle
import sqlite3

from flask import Flask, redirect, render_template, request, url_for

from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
app.secret_key ='secret123'
from datetime import timedelta

# Optional: make session expire after 30 minutes
app.permanent_session_lifetime = timedelta(minutes=30)
from functools import wraps
from flask import session, redirect

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

# =========================
# 📂 LOAD DATASET
# =========================
zomato_df = pd.read_csv(r"C:\Users\kotta\OneDrive\Desktop\Restaurant-recommender\zomato (2).csv", encoding='latin-1')
locations=sorted(zomato_df['City'].dropna().str.title().unique())
zomato_df['Cuisines'] = zomato_df['Cuisines'].fillna('').str.lower()
zomato_df['Restaurant Name'] = zomato_df['Restaurant Name'].str.lower()
 # Make location -> list of cuisines mapping
location_cuisines = {}

for loc in zomato_df['City'].dropna().str.lower().unique():
    cuisines = zomato_df[zomato_df['City'].str.lower() == loc]['Cuisines'].dropna().str.lower().str.split(',')
    # Flatten, strip spaces, remove duplicates
    cuisines_flat = sorted(list({c.strip() for sublist in cuisines for c in sublist}))
    location_cuisines[loc] = cuisines_flat


vectorizer = pickle.load(open('vectorizer.pkl','rb'))
tfidf_matrix = pickle.load(open('tfidf_matrix.pkl','rb'))

# =========================
# 🎲 RANDOM IMAGES
image_list = [
    "/static/RES-1.jpg",
    "/static/RES-2.jpg",
    "/static/RES-3.jpg",
    "/static/res-5.jpg",
    "/static/image.jpeg",
    "/static/res-6.jpeg",
    "/static/res-7.jpeg",
    "/static/res-8.jpeg"



]
# =========================
# 🧠 ML RECOMMENDATION
# =========================
def recommend_ml(query, top_n=10):
    query_vec = vectorizer.transform([query])
    similarity = cosine_similarity(query_vec, tfidf_matrix)

    scores = list(enumerate(similarity[0]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    indices = [i[0] for i in scores[1:top_n+1]]

    results = zomato_df.iloc[indices].copy()
    return results
    if len(images) >= len(results):
        results['image'] = random.sample(images, len(results))
    else:
        results['image'] = [random.choice(images) for _ in range(len(results))]


# =========================
# 👤 USER DATABASE
# =========================
def create_user_table():
    conn = sqlite3.connect('users.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    conn.close()

create_user_table()


# =========================
# 📅 BOOKING DATABASE
# =========================
def create_booking_table():
    conn = sqlite3.connect('bookings.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY,
    name TEXT,
    phone TEXT,
    restaurant TEXT,
    date TEXT,
    time TEXT,
    people TEXT,
    table_type TEXT,
    request TEXT)''')
    conn.close()

create_booking_table()


# =========================
# 🌐 ROUTES
# =========================

@app.route('/')
def home():
    return render_template('index.html')


# 🔐 LOGIN
from werkzeug.security import check_password_hash

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['username'] = username   # store in session
            session.permanent = False        # ends when browser closes
            return redirect('/recommend')    # redirect after login
        else:
            return "Invalid Credentials ❌"

    return render_template('login.html')
from flask import request, render_template, redirect
import sqlite3
from werkzeug.security import generate_password_hash


@app.route('/signup', methods=['GET','POST'])
def signup():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 🔴 Empty check
        if not username or not password:
            return "Please fill all fields ❗"

        conn = sqlite3.connect('users.db')

        # 🔍 Check user already exists
        existing_user = conn.execute(
            "SELECT * FROM users WHERE username=?", (username,)
        ).fetchone()

        if existing_user:
            conn.close()
            return "User already exists ⚠️"

        # 🔐 Hash password
        hashed_password = generate_password_hash(password)

        # 💾 Store user
        conn.execute(
            "INSERT INTO users (username,password) VALUES (?,?)",
            (username, hashed_password)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('signup.html')


# 🔍 SEARCH PAGE
@app.route('/recommend')
@login_required
def recommend():
    return render_template('recommend.html',locations=locations,location_cuisines=location_cuisines)


# 🤖 RESULT (ML BASED)
@app.route('/result', methods=['POST'])
def result():
    query = request.form.get('query')

    if not query:
        return "Please enter a query"

    results = recommend_ml(query)
    results_list = results.to_dict('records')

    return render_template('result.html', recommended_restaurants=results_list)


# Route: Filter results
@app.route('/filter', methods=['POST'])
@login_required
def filter_restaurants():
    # Get form data
    location = request.form.get('location', '')
    cuisines_input = request.form.getlist('cuisine')  # multiple selection
    rating = request.form.get('rating', '')

    filtered = zomato_df.copy()

    # 🔹 Location filter
    if location:
        filtered = filtered[filtered['City'].str.lower().str.contains(location, na=False)]

    # 🔹 Cuisine filter (robust, substring match)
    if cuisines_input:
        import re

        def clean_text(text):
            return re.sub(r'\s+', ' ', text.strip().lower())

        selected_cuisines = [clean_text(c) for c in cuisines_input]

        def match_cuisines(restaurant_cuisines):
            if not restaurant_cuisines:
                return False
            restaurant_cuisines = [clean_text(c) for c in restaurant_cuisines.split(',')]
            return any(sel in r for sel in selected_cuisines for r in restaurant_cuisines)

        filtered = filtered[filtered['Cuisines'].apply(match_cuisines)]

    # 🔹 Rating filter
    if rating:
        try:
            filtered = filtered[filtered['Aggregate rating'] >= float(rating)]
        except:
            pass

    # 🔹 Remove duplicates
    filtered = filtered.drop_duplicates(subset=['Restaurant Name'])

    # 🔥 PASTE HERE 👇
    import random

    filtered = filtered.reset_index(drop=True)

    filtered['image'] = [
        image_list[i % len(image_list)] for i in range(len(filtered))
    ]

    # 🔹 Convert to records
    results_list = filtered.to_dict('records')

    # 🔹 
    # No results message
    if len(results_list) == 0:
        message = "No restaurants found for your filters 😢"
        return render_template('result.html', message=message)
    else:
        return render_template('result.html', recommended_restaurants=results_list)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
# 📅 TABLE BOOKING
@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    phone = request.form['phone']
    date = request.form['date']
    time = request.form['time']
    people = request.form['people']
    table_type = request.form['table_type']
    request_msg = request.form['request']
    conn = sqlite3.connect('bookings.db')
    conn.execute('''
        INSERT INTO bookings (name, phone, restaurant, date, time, people, table_type, request)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, phone, 'Unknown', date, time, people, table_type, request_msg))
    conn.commit()
    conn.close()

    return "✅ Table Booked Successfully!"
@app.route('/logout')
def logout():
    session.pop('username', None)  # remove username from session
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)