import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://api.themoviedb.org/3/movie/650?language=en-US"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv('TMDB_API_READ_ACCESS_TOKEN')}"       
}

response = requests.get(url, headers=headers)

for movie in response.json():
    print(movie)
#print(response.poster_path.text)