from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
import json
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from pydantic import BaseModel


class Card(BaseModel):

  _id: str | None = None
  termo: str | None = None
  significado: str | None = None

MONGO_KEY = os.environ["MONGO_KEY"]
MONGO_USER = "jalanfla15_db_user"
MONGO_APP = "Cluster"

uri = f"mongodb+srv://{MONGO_USER}:{MONGO_KEY}@cluster.eeqmwq8.mongodb.net/?appName={MONGO_APP}"

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5500/new_card",
    "http://127.0.0.1:59614"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# listando todos os documentos de uma coleção

@app.get("/")
def root():

    with MongoClient(uri, server_api=ServerApi('1')) as client:

        db = client.get_database("flash_cards")
        all_cards = db.cards.find({})

        docs = json.dumps([doc for doc in all_cards], default=str, ensure_ascii=False)
            
    return docs

@app.post("/new_card/")
def new_card(data: Annotated[Card, Form()]):
    print(data)
    print("feito!!!")
    return data
