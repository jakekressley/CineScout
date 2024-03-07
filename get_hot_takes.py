import requests
import os
from db_connect import connect_to_db
from dotenv import load_dotenv
from get_average_scores import *
import math

load_dotenv()

hot_takes = []
cluster, db_name, collection_name = connect_to_db()

db = cluster[db_name]
collection = db[collection_name]

def get_hot_takes(scores):
    for movie in scores:
        avg_rating = movie['average']
        user_score = movie['user_rating']
        num_votes = movie['votes']

        weighted_votes = round((3 * math.log10(1 + num_votes / 5000) + 7), 2)

        weighted_average = round(3.57 * avg_rating - 17.68, 2)

        print("Title:", movie['title'], "votes: ", num_votes, "wAvg:", weighted_average, "wVotes:", weighted_votes, "wAvg:", weighted_average)

        weighted_distance = abs(user_score - weighted_average)
        
        hotness = weighted_distance * 6 + weighted_votes * 3

        #hotness = (abs(weighted_average - user_score)) * weighted_average + weighted_votes
        #print("Title:", movie['title'], "votes:", num_votes,  "wVotes:", weighted_votes)

        movie['hotness'] = round(hotness, 2)

    scores.sort(key=lambda x: x['hotness'])
    for movie in scores:
        print("Title:"+ movie['title'], ", User:", movie['user_rating'], "Avg:", movie['average'], "votes:", movie['votes'], ", hotness", movie['hotness'])
    return scores

def mean(arr):
    return sum(arr) / len(arr)

def std_dev(arr):
    mu = mean(arr)
    variance = sum([((x - mu) ** 2) for x in arr]) / len(arr)
    return math.sqrt(variance)

def z_score(x, mu, sigma):
    return (x - mu) / sigma if sigma != 0 else 0