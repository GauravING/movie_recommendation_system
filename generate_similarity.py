import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load movie dataset
try:
    movies_df = pd.read_csv("movies.csv")
    movies_df.columns = movies_df.columns.str.strip()  # Remove unwanted spaces
except Exception as e:
    print(f"Error loading movies.csv: {e}")
    exit()

# Check if 'title' and 'genre' exist
if "title" not in movies_df.columns or "genre" not in movies_df.columns:
    print("Error: 'title' and 'genre' columns are required in movies.csv.")
    exit()

# Fill missing values
movies_df["genre"] = movies_df["genre"].fillna("")

# Convert text data into numerical vectors using TF-IDF
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(movies_df["genre"])

# Compute cosine similarity matrix
similarity = cosine_similarity(tfidf_matrix)

# Save similarity matrix
with open("similarity.pkl", "wb") as file:
    pickle.dump(similarity, file)

print("✅ similarity.pkl has been successfully created!")
