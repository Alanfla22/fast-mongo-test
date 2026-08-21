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

app = FastAPI(strict_content_type=False)

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
    allow_methods=["GET", "POST", "PUT", "PATCH"],
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


@app.post("/")
def new_card(card: Card):

    with MongoClient(uri, server_api=ServerApi('1')) as client:

        try:
      
            new_card = card.model_dump()

            db = client.get_database("flash_cards")
            result = db.cards.insert_one(new_card)

            print(f"card iinserido  {result}!")
   
        
        except:

            print("não deu certo!")

    return json.dumps(new_card, default=str, ensure_ascii=False)

@app.patch("/")
def update_card(card: CardUpdate):

    print("1")

    with MongoClient(uri, server_api=ServerApi('1')) as client:

        try:

            print("2")

            card_update = card.model_dump()

            print(card_update)

            id = card_update["id"]
            query = {
              "termo": card_update["termo"],
              "significado": card_update["significado"]
            }            

            print(query)
            print(id)

            db = client.get_database("flash_cards")
            result = db.cards.update_one({"_id": ObjectId(id)}, {"$set": query})

            print("atualizado com sucesso!!")


        except Exception as e:

            print("falha na exclusão")
            print(e)

    return json.dumps(query, default=str, ensure_ascii=False)

    


  
             
    
    

