import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://api.themoviedb.org/3/movie/725201"
genre_url = "https://api.themoviedb.org/3/genre/movie/list?language=en"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv('TMDB_API_READ_ACCESS_TOKEN')}"       
}

genres_list = requests.get(genre_url, headers=headers)
#print(genres_list.json())
genres = {}
for genre in genres_list.json()['genres']:
    genres[genre['id']] = genre['name']

print(genres)

movie = requests.get(url, headers=headers)
#print(movie.json())
print(movie.json()['overview'])
genre_json = movie.json()['genres']
genres = []
for genre in genre_json:
    genres.append(genre['name'])
print(genres)