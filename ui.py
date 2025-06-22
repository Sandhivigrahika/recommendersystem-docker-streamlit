# --- ui.py ---
import streamlit as st
from user_auth import authenticate, register_user, load_known_users



def login_ui():
    st.title("Login")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    user_id = st.text_input("Enter your User ID")

    if st.button("Login"):
        if authenticate(user_id):
            st.success("Logged in!")
            st.session_state.logged_in = True
            st.session_state.user_id = user_id
        else:
            st.error("User ID not found in dataset.")

    return st.session_state.get("logged_in", False)


def recommendation_ui(model, movie_data):
    st.subheader("Your Movie Recommendations")

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("Please log in first.")
        return

    if st.button("Get Recommendations"):
        from recommender import get_top_n_recommendations
        movie_titles = movie_data[['movieId', 'title']].drop_duplicates()
        recommendations = get_top_n_recommendations(model, int(user_id), movie_titles)
        st.write(f"Top picks for you:")
        for movie in recommendations:
            st.write("-", movie)

