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
            tmdb_id = movie['id']
            dupe_check = collection.find_one({'tmdb_id': tmdb_id})
            if dupe_check is not None:
                continue
            movie_average = movie['vote_average']
            # movie is not out yet
            if (movie_average == 0):
                continue
            movie_vote_count = movie['vote_count']
            movie_year = movie['release_date'][:4]
            movie_poster = movie['poster_path']
            model = {
                    "Title": movie_title,
                    "tmdb_id": tmdb_id,
                    "Average Score": movie_average,
                    "Vote Count": movie_vote_count,
                    "Year": movie_year,
                    "Poster": movie_poster,
            }
            collection.update_one({'tmdb_id' : tmdb_id}, {'$set' : model}, upsert=True)
        page_count += 1

get_top_movies()
# sets year and poster to None for troubleshooting
#collection.update_many({}, {'$set': {'Poster': None, 'Year': None}})
#collection.delete_many({})

def movie_in_db(title):
    movie = collection.find_one({'Title': title})
    return movie is not None