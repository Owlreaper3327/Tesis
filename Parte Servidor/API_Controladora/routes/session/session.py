"""Api router for session operations"""
from fastapi import APIRouter, status, Response, HTTPException
from utils.database.ops import engine
from utils.database.models import Usuario, Estudiante, Profesor, Reporte
from sqlmodel import Session, select, insert
from fastapi import Form, Cookie
from sqlalchemy.exc import SQLAlchemyError
import hashlib
import os

session_router = APIRouter()

#functions go here

#main code goes here
@session_router.get("/")
async def hello():
    return "Bienvenido, esta ruta estí aquí sólo para probar\
        \n Ya que cada endpoint debería tener al menos un get básico\
        \n PD: Hello World!"

@session_router.post("/auth")
async def try_auth(username:str = Form(...), password:str = Form(...)):
    
    
    with Session(engine) as sesion:

        stmt = select(Usuario).where(Usuario.username == username)
        result = sesion.exec(stmt)
        us = result.first()        

        if us.salt == "testing":
            
            if us.password == password:
                return "Lograste iniciar sesión, ahora lárgate"
            else:
                return False
        else:
            pass_hash = hashlib.sha256(us.salt + password.encode()).hexdigest()

            if pass_hash == us.password:
                return "El usuario en JSon XDD"
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)