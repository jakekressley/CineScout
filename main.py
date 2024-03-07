from dotenv import load_dotenv
from get_average_scores import *
from get_hot_takes import get_hot_takes
from get_user_ratings import *
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

username = input("Enter username: ")

@app.get("/")
async def read_root():
    return {"Status": "Active"}

@app.get("/user/{username}")
async def get_score():
    scores = get_user_ratings(username)
    get_hot_takes(scores)
    return scores
#scores = get_user_ratings(username)
#get_hot_takes(scores)
#print(user_average_rating(scores))