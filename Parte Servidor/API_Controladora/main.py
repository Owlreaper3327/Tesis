"""This is the center for the controller API"""

#imports and settings go here
import fastapi
from routes.session.session import session_router
from fastapi import FastAPI, APIRouter

app = FastAPI()
app.include_router(session_router, prefix="/session")
#functions go here

#main code goes here

@app.get("/")
async def root():
    return {"mensaje" : "Bienvenido a la api de mi tesis"}