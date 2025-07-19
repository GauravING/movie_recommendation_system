import pandas as pd
import requests
import pickle
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load movie dataset
try:
    movies_df = pd.read_csv("movies.csv")
except FileNotFoundError:
    raise FileNotFoundError("❌ ERROR: 'movies.csv' is missing. Please add it to your project.")

# Load similarity matrix
try:
    with open("similarity.pkl", "rb") as file:
        cosine_sim = pickle.load(file)
except FileNotFoundError:
    raise FileNotFoundError("❌ ERROR: 'similarity.pkl' is missing. Run generate_similarity.py to create it.")

# TMDb API Key (Replace with your actual key)
TMDB_API_KEY = "82d7b2af65c8de549c2958b54dcade89"

def fetch_poster(movie_name):
    """Fetch movie poster URL from TMDb API."""
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("results"):
            poster_path = data["results"][0].get("poster_path")
            return f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
    except requests.exceptions.RequestException as e:
        print(f"⚠️ TMDb API Error: {e}")
        return None

@app.get("/movies")
def get_movies():
    """Fetch all available movies."""
    return {"movies": movies_df["title"].dropna().tolist()}

@app.get("/recommend")
def get_recommendations(title: str = Query(..., description="Movie title to get recommendations for")):
    """Get movie recommendations including the selected movie itself."""
    title = title.strip()
    
    if title not in movies_df["title"].values:
        return {"error": "Movie not found"}
    
    # Get the index of the selected movie
    idx = movies_df[movies_df["title"] == title].index[0]
    
    # Get similarity scores (include selected movie + 4 similar movies)
    sim_scores = sorted(list(enumerate(cosine_sim[idx])), key=lambda x: x[1], reverse=True)[:10]  
    movie_indices = [i[0] for i in sim_scores]

    recommendations = []
    
    for index in movie_indices:
        row = movies_df.iloc[index]
        recommendations.append({
            "title": row["title"],
            "genre": row.get("genre", "Unknown"),
            "language": row.get("original_language", "Unknown"),
            "release_date": row.get("release_date", "Unknown"),
            "rating": row.get("ratings", "N/A"),
            "poster": fetch_poster(row["title"])
        })
    
    return recommendations
