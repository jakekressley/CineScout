import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://api.themoviedb.org/3/movie/650"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv('TMDB_API_READ_ACCESS_TOKEN')}"       
}

movie = requests.get(url, headers=headers)

print(movie.json()['poster_path'])
print(movie.json()['release_date'][:4])
#print(response.poster_path.text)