import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=9ee43d7c277686bcb8fe646905a4053c&language=en-US"
    )
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Load data
movies = pickle.load(open('movies.pkl', 'rb'))  # Ensure this has 'title' and 'movie_id' columns
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# Streamlit UI
st.title('🎬 Movie Recommender System')

selected_movie = st.selectbox(
    'Select a movie you like:',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    st.subheader("Recommended Movies for You:")

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.caption(names[i])
