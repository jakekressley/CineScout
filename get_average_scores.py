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
        model = {
            "Title": movie_title,
            "tmdb_id": tmdb_id,
            "Average Score": movie_average,
            "Vote Count": movie_vote_count
        }
        #print(movie_title)
        collection.update_one({'Title' : movie_title}, {'$set' : model}, upsert=True)
        return movie_average, movie_vote_count

    except:
        tmdb_link = ''
        tmdb_id = ''
        return 0, 0
    