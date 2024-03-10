import requests
from statistics import mean
from bs4 import BeautifulSoup
from db_connect import connect_to_db

import os
from dotenv import load_dotenv

load_dotenv()

scores = []
cluster, db_name, collection_name = connect_to_db()

db = cluster[db_name]
collection = db[collection_name]

def get_average_scores(movie_title):
    url = "https://letterboxd.com/film/{}/"
    page = requests.get(url.format(movie_title))
    soup = BeautifulSoup(page.content, 'html.parser')
    tmdb_api_headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.getenv('TMDB_API_READ_ACCESS_TOKEN')}"
    }
    try:
        imdb_link = soup.find("a", attrs={"data-track-action": "IMDb"})['href']
        imdb_id = imdb_link.split('/')[4]
    except:
        imdb_link = ''
        imdb_id = ''

    try:
        tmdb_link = soup.find("a", attrs={"data-track-action": "TMDb"})['href']
        tmdb_id = tmdb_link.split('/')[4] 
        movie_response = requests.get(f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={os.getenv('TMDB_API_KEY')}")
        movie_title = movie_response.json()['title']
        movie_average = movie_response.json()['vote_average']
        movie_vote_count = movie_response.json()['vote_count']

        tmdb_url = "https://api.themoviedb.org/3/movie/{}"
        tmdb_url = tmdb_url.format(tmdb_id)
        movie_response = requests.get(tmdb_url, headers=tmdb_api_headers)
        year = movie_response.json()['release_date'][:4]
        poster_path = movie_response.json()['poster_path']
        genre_json = movie_response.json()['genres']
        genres = []
        for genre in genre_json:
            genres.append(genre['name'])
        movie_overview = movie_response.json()['overview']
        #print(year)
        #print(poster_path)

        model = {
            "Title": movie_title,
            "tmdb_id": tmdb_id,
            "Average Score": movie_average,
            "Vote Count": movie_vote_count,
            "Poster": poster_path,
            "Year": year,
            "Genres": genres,
            "Overview": movie_overview,
        }
        #print(movie_title)
        collection.update_one({'tmdb_id' : tmdb_id}, {'$set' : model}, upsert=True)
        return movie_average, movie_vote_count

    except:
        tmdb_link = ''
        tmdb_id = ''
        return 0, 0