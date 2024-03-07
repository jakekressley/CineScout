import requests
import os
from db_connect import connect_to_db
from dotenv import load_dotenv
from get_average_scores import *

load_dotenv()

scores = []
cluster, db_name, collection_name = connect_to_db()

db = cluster[db_name]
collection = db[collection_name]

def get_top_movies():
    page_count = 1

    # total stored 250 * 20 = 5000
    while page_count < 250:
        url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page={}"
        url = url.format(page_count)

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {os.getenv('TMDB_API_READ_ACCESS_TOKEN')}"
        }
        movie_response = requests.get(url, headers=headers)

        for movie in movie_response.json()['results']:
            print(movie['title'], movie['vote_average'], movie['vote_count'])
            movie_title = movie['title']
            movie_average = movie['vote_average']
            movie_vote_count = movie['vote_count']
            tmdb_id = movie['id']
            model = {
                    "Title": movie_title,
                    "tmdb_id": tmdb_id,
                    "Average Score": movie_average,
                    "Vote Count": movie_vote_count
            }
            collection.update_one({'Title' : movie_title}, {'$set' : model}, upsert=True)
        page_count += 1

get_top_movies()

def movie_in_db(title):
    movie = collection.find_one({'Title': title})
    return movie is not None