from joblib import load
import difflib

movies_data = load('data.joblib')
title_list = load('title_list.joblib')
similarity_scores = load('similarity_scores.joblib')


def find_closest_string(movie_name, title_list):
  lst = []
  movie_name_lower = movie_name.lower()
  for title in title_list:
    if(title.lower().find(movie_name_lower) >= 0):
      lst.append(title)
  return lst


def recommend_movies():
  movie_name = input('Enter your favourite movie name : ')
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

recommend_movies()