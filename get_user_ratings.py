import requests
from bs4 import BeautifulSoup
from db_connect import connect_to_db

import os
from dotenv import load_dotenv
from get_average_scores import *
from get_hot_takes import get_hot_takes
import math

load_dotenv()

cluster, db_name, collection_name = connect_to_db()

db = cluster[db_name]
collection = db[collection_name]

tmdb_api_headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv('TMDB_API_READ_ACCESS_TOKEN')}"
}

genre_url = "https://api.themoviedb.org/3/genre/movie/list?language=en"

genres_list = requests.get(genre_url, headers=tmdb_api_headers)

genres_dict = {}
for genre in genres_list.json()['genres']:
    genres_dict[genre['id']] = genre['name']

def get_user_ratings(username):
    scores = []
    user_pages = get_page_count(username)
    current_page = 1
    while current_page <= user_pages:
        url = "https://letterboxd.com/{}/films/page/{}/"
        page = requests.get(url.format(username, current_page))
        soup = BeautifulSoup(page.content, "html.parser")


        results = soup.find(class_="poster-list")
        movies = results.findAll("li", class_="poster-container")
        for movie in movies:
            movie_title = movie.find("img")['alt']
            movie_link = movie.find("div", class_="film-poster")['data-film-slug']
            # get the last character of last class name
            try:
                user_rating = movie.find("span", class_="rating")['class'][-1]
                user_rating = int(user_rating.split("-")[-1])
            except: 
                continue
            if user_rating != 0:
                if not movie_in_db(movie_title):
                    try:
                        average, votes = get_average_scores(movie_link)
                        if (average == 0):
                            continue
                    except:
                        continue
                else:
                    movie = collection.find_one({'Title': movie_title})
                    print("getting movie:", movie_title)
                    tmdb_id = movie['tmdb_id']
                    average = movie['Average Score']
                    votes = movie['Vote Count']
                    poster_path = movie['Poster']
                    year_released = movie['Year']
                    if poster_path is None:
                        tmdb_url = "https://api.themoviedb.org/3/movie/{}"
                        tmdb_url = tmdb_url.format(tmdb_id)
                        movie = requests.get(tmdb_url, headers=tmdb_api_headers)

                        poster_path = movie.json()['poster_path']
                        year_released = movie.json()['release_date'][:4]
                        collection.update_one({'tmdb_id' : tmdb_id}, {'$set' : {'Poster': poster_path, 'Year': year_released}}, upsert=True)
                    movie_genres = movie['Genres']
                    genres = []
                    for genre in movie_genres:
                        genres.append(genre)
                    movie_overview = movie['Overview']

                score_data = {
                    "title": movie_title,
                    "user_rating": user_rating,
                    "average": average,
                    "votes": votes,
                    "poster": poster_path,
                    "year": year_released,
                    "genres": genres,
                    "overview": movie_overview,
                    "hotness" : 0,
                }
                scores.append(score_data)
                #print("Title", movie_title, "Average: ", average, "User rated: ", user_rating)
        current_page += 1
    return scores


def get_page_count(username):
    url = "https://letterboxd.com/{}/films/"
    page = requests.get(url.format(username))
    soup = BeautifulSoup(page.content, "html.parser")
    try:
        # get last paginated page
        try:
            page_data = soup.findAll("li", class_="paginate-page")[-1]
        except:
            print("user not found")
        num_pages = int(page_data.find("a").text.replace(",", ""))
    except IndexError:
        num_pages = 1

    return num_pages

def user_average_rating(scores):
    total = 0
    for score in scores:
        total += score['user_rating']
    return round(total / len(scores), 2)

def movie_in_db(title):
    movie = collection.find_one({'Title': title})
    return movie is not None

