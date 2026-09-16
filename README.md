# 🍽️ Restaurant Recommendation System

A web-based restaurant recommendation system that helps users discover restaurants based on their preferences such as **location, cuisine, ratings, and other restaurant details**.

The application uses a content-based recommendation approach with **TF-IDF and cosine similarity** to identify restaurants that are relevant to user preferences.

---

## 📌 Project Overview

Finding a suitable restaurant can be difficult when users have different preferences for cuisine, location, and ratings.

This project provides a simple web application where users can:

- Create an account and log in
- Select restaurant preferences
- Filter restaurants based on available criteria
- View recommended restaurants
- Check restaurant details
- Book a table by providing booking information

The recommendation component uses text-based restaurant information and similarity techniques to generate relevant recommendations.

---

## ✨ Features

- 🔐 User Registration and Login
- 🍴 Restaurant Recommendations
- 📍 Location-based filtering
- 🍜 Cuisine-based filtering
- ⭐ Rating-based filtering
- 🔎 Restaurant search and filtering
- 🖼️ Restaurant images and details
- 📅 Table booking functionality
- 💾 SQLite database for user and booking information
- 🌐 Web-based interface using Flask

---

## 🛠️ Technologies Used

### Backend
- Python
- Flask

### Machine Learning / Data Processing
- Pandas
- NumPy
- Scikit-learn
- NLTK
- TF-IDF Vectorization
- Cosine Similarity

### Frontend
- HTML5
- CSS3
- Bootstrap

### Database
- SQLite

### Model/Data Files
- Pickle (`.pkl`)
- CSV dataset

---

## 🧠 Recommendation Approach

The recommendation system follows a content-based approach.

### Workflow

1. Restaurant information is collected from the dataset.
2. Relevant restaurant attributes are processed.
3. Text information such as cuisine details is converted into numerical vectors using **TF-IDF**.
4. Similarity between restaurants is calculated using **cosine similarity**.
5. User preferences are used to identify relevant restaurants.
6. Recommended restaurants are displayed through the Flask web application.

### Basic Flow

```text
User Preferences
       ↓
Preference Processing
       ↓
TF-IDF Vectorization
       ↓
Cosine Similarity
       ↓
Restaurant Ranking
       ↓
Recommended Restaurants
## 📂 Project Structure
Restaurant-Recommendation-System/
│
├── app1.py
├── model.pkl
├── vectorizer.pkl
├── tfidf_matrix.pkl
├── req.txt
├── zomato (2).csv
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── recommend.html
│   ├── result.html
│   └── booking.html
│
├── static/
│   ├── RES-1.jpg
│   ├── RES-2.jpg
│   ├── RES-3.jpg
│   └── ...
│
└── .gitignore
The Python virtual environment and other generated files are excluded from the repository using .gitignore.
---
## ⚙️ Installation and Setup
1. Clone the repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
2. Navigate to the project directory
cd Restaurant-Recommendation-System
3. Create a virtual environment
python -m venv .venv
4. Activate the virtual environment
Windows:
.venv\Scripts\activate
Linux/macOS:
source .venv/bin/activate
5. Install dependencies
If your dependency file is named req.txt:
pip install -r req.txt
6. Run the Flask application
python app1.py
Then open the local URL displayed by Flask in your browser.
---
## 🗃️ Dataset
The project uses a restaurant dataset containing information such as:
Restaurant Name
City
Cuisine
Rating
Average Cost
Area
The dataset is processed using Pandas before being used by the recommendation system.
---
##🗄️ Database
SQLite is used to store application-related information such as:
User details
Login-related information
Restaurant booking details
---
## 🔮 Future Improvements
Possible future enhancements include:
Adding a larger and more diverse restaurant dataset
Adding user-specific recommendation history
Improving recommendation personalization
Adding restaurant availability information
Deploying the application to a cloud platform
Adding map/location integration
Improving the UI and mobile responsiveness
---
## 👩‍💻 My Contribution
V. Mohana Durga — Team Lead
Developed the Flask-based web application
Worked on the restaurant recommendation logic
Integrated the recommendation model with the web application
Worked with restaurant data preprocessing
Implemented filtering and recommendation functionality
Worked on the user and booking workflow
Integrated the frontend with the Flask backend
---
## 🎓 Academic Project
This project was developed as part of the B.Tech – Artificial Intelligence & Machine Learning academic project.
Project Title:
###  Restaurant Recommendation System Using User Preferences and Ratings
---
## 🌐 Demo

🔗 **Live Demo:** Coming Soon

###🚀 Run Locally

After starting the Flask application, open:

`http://127.0.0.1:5000`
