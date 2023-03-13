import pandas as pd
import streamlit as st
import pickle
import requests


def fetch_poster (movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=17f8b5d3d920842b02b60a894b23a656&language=en-US".format(movie_id))
    data = response.json()

    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])

    recommended_movies_names = []
    recommended_movies_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies_names.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies_names, recommended_movies_posters
st.header('Movie Recommender System')


movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movies_names,recommended_movies_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movies_names[0])
        st.image(recommended_movies_posters[0])
    with col2:
        st.text(recommended_movies_names[1])
        st.image(recommended_movies_posters[1])

    with col3:
        st.text(recommended_movies_names[2])
        st.image(recommended_movies_posters[2])
    with col4:
        st.text(recommended_movies_names[3])
        st.image(recommended_movies_posters[3])
    with col5:
        st.text(recommended_movies_names[4])
        st.image(recommended_movies_posters[4])
