from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
import json
from fastapi import FastAPI
import uvicorn


MONGO_KEY = os.environ["MONGO_KEY"]
MONGO_USER = "jalanfla15_db_user"
MONGO_APP = "Cluster"

uri = f"mongodb+srv://{MONGO_USER}:{MONGO_KEY}@cluster.eeqmwq8.mongodb.net/?appName={MONGO_APP}"

app = FastAPI()

# listando todos os documentos de uma coleção

@app.get("/")
def root():

    with MongoClient(uri, server_api=ServerApi('1')) as client:

        db = client.get_database("flash_cards")
        all_cards = db.cards.find({})

        docs = json.dumps([doc for doc in all_cards], indent=4, default=str, ensure_ascii=False)
            
    return docs
