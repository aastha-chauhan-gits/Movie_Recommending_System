import streamlit as st
import pickle
import pandas as pd
import requests

#function to fetch movie poster
def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]


#function to recommend the first 5 most similar movies
def recommend(movie):
    # catch the index of given movie
    movie_index = movies[movies['title'] == movie].index[0]

    # calculate the cosine distances of the given movie from all other movies
    distances = similarity[movie_index]

    # sort the list in decreasing order on the basis of distances, keeping their index number with them
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies_posters = []
    recommended_movies = []

    for i in movies_list:
        #fetching the movies id
        movie_id = movies.iloc[i[0]].movie_id


        # to get the first 5 most similar movies
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters




# extracting the title names from pickle file
movies_dict = pickle.load(open('movie_dict', 'rb'))
#making a dataframe from pickle file
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))


st.title('Movie Recommender System')

import streamlit as st

Selected_movie_name = st.selectbox(
    'Select the Movie Name',
    movies['title'].values)

st.write('You selected:', Selected_movie_name)


if st.button('Recommend'):
    names,posters = recommend(Selected_movie_name)


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
