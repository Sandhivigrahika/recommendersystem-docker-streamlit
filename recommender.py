import pickle
import pandas as pd


def load_data():
    data = pd.read_csv(r"C:\Users\neelh\Jupyter Related\Recsys project\data\movie_data.csv")
    return data


def load_model():
    with open(r"C:\Users\neelh\Jupyter Related\Recsys project\model.pkl", 'rb') as file:
        model = pickle.load(file)
    return model

data = load_data()
model = load_model()

def get_top_n_recommendations(model, user_id, data, n=10):


    # Get a list of all movie IDs
    all_movie_ids = data['movieId'].unique()
    rated_movies = data[data['userId'] == user_id]['movieId'].unique()
    movies_to_predict = [m for m in all_movie_ids if m not in rated_movies]
    # Predict ratings for all movies the user hasn't rated yet
    predictions = []
    for movie_id in movies_to_predict:
        predictions.append((movie_id, model.predict(user_id, movie_id).est))

    # Sort predictions by estimated rating
    predictions.sort(key=lambda x: x[1], reverse=True)

    # Get top N movie IDs
    top_movie_ids = [movie_id for movie_id, _ in predictions[:n]]

    # Get movie titles for the top N movie IDs
    top_movie_titles = data[data['movieId'].isin(top_movie_ids)]['title'].unique().tolist()

    return top_movie_titles


print(get_top_n_recommendations(model, 180, data, n=10))