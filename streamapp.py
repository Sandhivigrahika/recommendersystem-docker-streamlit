import streamlit as st
import pandas as pd
import pickle
import os
import json
import hashlib
from tmdb_helper import fetch_poster
import random
import numpy

# --- Load Data & Model ---
@st.cache_data
def load_data():
    return pd.read_csv("data/movie_data.csv")

@st.cache_resource
def load_model():
    with open("best_model.pkl", "rb") as file:
        model = pickle.load(file)
    return model

# --- Auth Functions ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists('users.json'):
        return {}
    with open('users.json', 'r') as file:
        return json.load(file)

def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file)

def authenticate(username, password):
    users = load_users()
    return username in users and users[username] == hash_password(password)

def register_user(username, password):
    users = load_users()
    known_users = set(load_data()['userId'].unique().astype(str))
    if username not in known_users or username in users:
        return False
    users[username] = hash_password(password)
    save_users(users)
    return True

data = load_data()
print(data.astype)

# --- Recommender Logic ---
def get_top_n_recommendations(model, user_id, data, n=10):
    #get a list of all unique movie Ids
    all_movie_ids = data['movieId'].unique()
    rated_movies = data[data["userId"]==user_id]['movieId'].values

    #filter the the seen movies
    unseen_movies = []
    for movie in all_movie_ids:
        if movie not in rated_movies:
            unseen_movies.append(movie)

    #predict ratings
    predictions_for_user =  []
    for movieId in unseen_movies:
        predictions = model.predict(uid=user_id,iid=movieId)
        predictions_for_user.append(predictions)

    #get top n-recs
    top_n_recs = sorted(predictions_for_user,key= lambda x: x.est,reverse=True)[:50]

    top_n_sampled = random.sample(top_n_recs, n)

    top_movie_ids = []

    for pred in top_n_sampled:
        top_movie_ids.append(pred.iid)

    # Get movie titles for the top N movie IDs
    top_movie_titles = data[data['movieId'].isin(top_movie_ids)]['title'].unique().tolist()

    return top_movie_titles






model = load_model()
print(get_top_n_recommendations(model,191,data,n=10))






# --- UI ---
st.title("🎬 Neel's Movie Recommender")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    option = st.sidebar.selectbox("Login or Register", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Login":
        if st.button("Login"):
            if authenticate(username, password):
                st.success("Logged in successfully!")
                st.session_state.logged_in = True
                st.session_state.username = username
            else:
                st.error("Invalid username or password.")
    elif option == "Register":
        if st.button("Register"):
            if register_user(username, password):
                st.success("User registered!")
            else:
                st.warning("Username not found in data or already registered.")
else:
    data = load_data()
    model = load_model()
    st.subheader(f"Welcome {st.session_state.username}!")
    user_id = st.session_state.username

    if st.button("Get Recommendations"):
        recommendations = get_top_n_recommendations(model, user_id, data,n=10)
        st.write("Top Recommendations:")
        for movie in recommendations:
            st.write(f"**{movie}**")
            poster_url = fetch_poster(movie)
            if poster_url:
                st.image(poster_url,width=150)
            else:
                st.info("No Poster Available")



