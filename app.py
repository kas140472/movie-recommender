import streamlit as st
import pickle
import requests

movies_list = pickle.load(open('movies.pkl', 'rb'))
movies = movies_list['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=3100354135fbba3f21af9946689f2eca&language=en-US'.format(movie_id))
    data = response.json()
    # st.text(data)
    return "https://image.tmdb.org/t/p/w185/" + data['poster_path']

def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list2 = sorted(list(enumerate(distances)), reverse=True, key= lambda x:x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list2:
        rec_movie_index = i[0]

        recommended_movies.append(movies_list.iloc[rec_movie_index].title)
        # fetch poster from api
        movie_id = movies_list.iloc[rec_movie_index].movie_id
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Movie?',
    movies
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])