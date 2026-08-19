from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
import json
from fastapi import FastAPI, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated, Optional
from pydantic import BaseModel, BeforeValidator, Field

PyObjectId = Annotated[str, BeforeValidator(str)]

class Card(BaseModel):

  id: Optional[PyObjectId] = Field(alias="_id", default=None)
  termo: Optional[str] = None
  significado: Optional[str] = None

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


@app.post(
    "/new_card/",
    response_description="Add new card",
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
def new_card(card: Card = Body(...)):

    print(card)
    print("feito!!!")

    with MongoClient(uri, server_api=ServerApi('1')) as client:
      
      new_card = card.model_dump(by_alias=True, exclude=["id"])
      db = client.get_database("flash_cards")
  
      result = db.cards.insert_one(new_card)

      new_card["_id"] = result.inserted_id

    return new_card
  
             
    
    

