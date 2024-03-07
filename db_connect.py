def connect_to_db():
    import os
    from pymongo import MongoClient
    from dotenv import load_dotenv
    import certifi

    load_dotenv()

    cluster = MongoClient(os.getenv('MONGO_URI'), tlsCAFile=certifi.where())
    db_name = "CineScout"
    db = cluster["db_name"]

    collection_name = "Letterboxd Averages"
    collection = db[collection_name]

    return cluster, db_name, collection_name