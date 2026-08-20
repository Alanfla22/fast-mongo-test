from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
import json
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from pydantic import BaseModel
from bson import ObjectId

class Card(BaseModel):

  termo: str | None = None
  significado: str | None = None

class CardUpdate(BaseModel):

    id: str | None = None
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
    "http://127.0.0.1:5500/index.html",
    "http://127.0.0.1:5500/new_card/",
    "http://127.0.0.1:59614"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://flash-card-ycgo.onrender.com", "http://127.0.0.1:5500", "http://127.0.0.1:5500/index.html"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["application/x-www-form-urlencoded"],
)

# listando todos os documentos de uma coleção

@app.get("/")
def root():

    with MongoClient(uri, server_api=ServerApi('1')) as client:

        db = client.get_database("flash_cards")
        all_cards = db.cards.find({})

        docs = json.dumps([doc for doc in all_cards], default=str, ensure_ascii=False)
            
    return docs


@app.post("/")
def new_card(card: Annotated[Card, Form()]):

    with MongoClient(uri, server_api=ServerApi('1')) as client:

        try:
      
            new_card = card.model_dump(by_alias=True)

            db = client.get_database("flash_cards")
            result = db.cards.insert_one(new_card)

            print(f"card iinserido  {result}!")
   
        
        except:

            print("não deu certo!")

    return json.dumps(new_card, default=str, ensure_ascii=False)

@app.patch("/")
def update_card(card: Annotated[CardUpdate, Form()]):

    with MongoClient(uri, server_api=ServerApi('1')) as client:

        try:

            query = card.model_dump(by_alias=True)

            print(query)
            print(query["_id"])

            db = client.get_database("flash_cards")
            result = db.cards.update_one({"_id": ObjectId(query["_id"])}, {"$set": query})

            print("atualizado com sucesso!!")


        except Exception as e:

            print("falha na exclusão")
            print(e)

    return json.dumps(query, default=str, ensure_ascii=False)

    


  
             
    
    

