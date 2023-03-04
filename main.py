import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies_data = pd.read_csv('movies.csv')

selected_features = ['genres', 'keywords', 'cast', 'director']
for feature in selected_features:
    movies_data[feature] = movies_data[feature].fillna('')

combined_features = movies_data['keywords'] + movies_data['genres'] + movies_data['cast'] + movies_data['director']

vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)

similarity_scores = cosine_similarity(feature_vectors)

title_list = movies_data['title'].tolist()

def find_closest_string(movie_name, title_list):
  lst = []
  movie_name_lower = movie_name.lower()
  for title in title_list:
    title = str(title)
    if(title.lower().find(movie_name_lower) >= 0):
      lst.append(title)
  return lst


def recommend_movies(movie_name, title_list):
  close_matches = find_closest_string(movie_name, title_list)

  if(len(close_matches) == 0):
      close_matches = difflib.get_close_matches(movie_name, title_list)

  movie_index = movies_data[movies_data['title'] == close_matches[0]].index.values[0]
  similar_movies = list(enumerate(similarity_scores[movie_index]))
  sorted_similar_movies = sorted(similar_movies, key = lambda x:x[1], reverse = True)
  sorted_similar_movies = sorted_similar_movies[1:]
  i=1
  for movie in sorted_similar_movies:
    index = movie[0]
    movie_name = movies_data[movies_data.index == index]['title'].values[0]
    if(i <= 10):
      print(i, '.', movie_name)
      i += 1

movie_name = input('Enter your favourite movie name : ')
recommend_movies(movie_name, title_list)