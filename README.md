# 🎮 Steam Game Discovery System
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An interactive **Streamlit-based game recommendation and analytics dashboard** designed to help users discover Steam games based on their preferences. The application combines filtering, recommendation techniques, comparison tools, and visual analytics to provide an engaging game exploration experience.

---

## 📌 Project Overview

The **Steam Game Discovery System** is a single-page web application built entirely using **Python and Streamlit**. Unlike traditional websites, the user interface is dynamically generated from Python code without requiring separate HTML, CSS, or JavaScript files.

The application enables users to:

* Discover popular, trending, and hidden gem games.
* Filter games by genre, player style, price, and ratings.
* Receive personalized game recommendations.
* Compare two games side-by-side.
* Explore game trends through interactive visualizations.
* Analyze game similarities using dimensionality reduction techniques.

---

## ✨ Features

### 🔍 Advanced Filtering

* Filter games by genre.
* Choose player styles such as:

  * Casual
  * Hardcore
  * Competitive
  * Story Lover
* Adjust price range (INR).
* Filter by positive ratings.
* View only free-to-play games.

### 🎯 Game Recommendation Engine

* Generates recommendations based on:

  * Genre overlap
  * Positive ratings
  * Price similarity
* Displays the top recommended games with match scores.

### 📈 Popular, Trending & Hidden Gems

* Popular games based on positive ratings.
* Trending games using a custom trending score.
* Hidden gems identified through rating-based scoring.

### 🤖 AI-Style Game Description

* Produces dynamic descriptions for selected games using game metadata and genre information.

### 🧬 Game DNA Visualization

* Interactive radar chart representing genre characteristics of a game.

### 🗺️ Game Similarity Map

* Uses **Principal Component Analysis (PCA)** to project games into a 2D similarity space.

### ⚖️ Compare Two Games

Compare games based on:

* Price
* Positive Ratings
* Average Playtime

### 📊 Interactive Dashboard

Visualizations include:

* Price Distribution Histogram
* Ratings Distribution Histogram
* Price vs Popularity Scatter Plot

---

## 🛠️ Tech Stack

### Frontend

* Streamlit
* Custom CSS

### Backend & Data Processing

* Python
* Pandas

### Data Visualization

* Plotly Express
* Plotly Graph Objects

### Machine Learning

* Scikit-learn (PCA)

### Utilities

* urllib
* functools (lru_cache)

---

## 📂 Project Structure

```text
Game Recommendation System/
├── app.py                 # Main Streamlit application
├── main.py
├── steam.csv              # Steam dataset
├── .streamlit/
├── artifacts/
├── attached_assets/
├── lib/
├── scripts/
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/Game-Recommendation-System.git
```

### 2. Navigate to the Project Folder

```bash
cd Game-Recommendation-System
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

### 5. Open in Browser

Streamlit will provide a local URL similar to:

```text
http://localhost:8501
```

Open it in your browser to access the application.

---

## 📊 Dataset

The application uses the **Steam Dataset (`steam.csv`)** containing information such as:

* App ID
* Game Name
* Genres
* Positive Ratings
* Negative Ratings
* Average Playtime
* Price

---

## 🔄 User Workflow

1. Launch the application.
2. Apply filters from the sidebar.
3. Select a game of interest.
4. View popular, trending, and hidden gem recommendations.
5. Generate personalized recommendations.
6. Explore game DNA and similarity maps.
7. Compare games side-by-side.
8. Analyze market trends using visual dashboards.

---

## 🚀 Future Enhancements

* Integration with the Steam API.
* User authentication and profiles.
* Collaborative filtering recommendation models.
* Deep learning-based recommendation systems.
* Cloud deployment for public access.
* Real-time game updates and analytics.

---

## 📚 Libraries Used

* Streamlit
* Pandas
* Plotly
* Scikit-learn
* urllib
* functools

---

## 👨‍💻 Author

**Pradeep Yedage**

Aspiring Developer passionate about Python, data-driven applications, and creating interactive user experiences.

---

---

## 📄 License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for more information.

© 2026 Pradeep Yedage
