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

@app.get("/")
async def read_root():
    return {"Status": "Active"}

@app.get("/user/{username}")
async def get_score(username):
    scores = get_user_ratings(username)
    return get_hot_takes(scores)
#print(user_average_rating(scores))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)