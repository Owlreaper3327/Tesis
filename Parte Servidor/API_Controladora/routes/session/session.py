"""Api router for session operations"""
from fastapi import APIRouter, status, Response, HTTPException
from utils.database.ops import engine
from utils.database.models import Usuario, Estudiante, Profesor, Reporte
from sqlmodel import Session, select, insert
from fastapi import Form, Cookie
from sqlalchemy.exc import SQLAlchemyError
import hashlib
import os
import jwt
import time

session_router = APIRouter()
clave = "calve_f3327"

#functions go here

def hash_password(password:str, num=None):
    """Utility function to encrypt passwords"""

    if num is None:
        num = os.urandom(16)
    else:
        if isinstance(num, str):
            num = bytes.fromhex(num)

    hashed_obj = hashlib.sha256(num + password.encode())
    hashed_pass = hashed_obj.hexdigest()
    return num.hex(), hashed_pass

def verify_password(password:str, salt:str, stored_pass:str):
    """Utility function to verify encrypted passwords"""

    num = bytes.fromhex(salt)

    _, new_pass = hash_password(password, salt)
    return True if (new_pass == stored_pass) else False

def compose_token(usuario:Usuario):
    """Utility function to create jwt token to be validated on frontend"""

    tipo = "estudiante"

    with Session(engine) as sesion:

        stmt = select(Estudiante).where(Estudiante.id_estudiante == usuario.id_usuario)
        us_i = sesion.exec(stmt).first()
        
        if us_i == None:
            stmt = select(Profesor).where(Profesor.id_profesor == usuario.id_usuario)
            us_i = sesion.exec(stmt).first()
            tipo = "profesor"
    
    expiracion = int(time.time()) + 14400 if tipo == "estudiante" else int(time.time()) + (14400*3)

    un_token = {"username": usuario.username,
            "tipo": tipo,
            "grupo": usuario.grupo,
            "nombre": us_i.nombre,
            "exp": expiracion}
    token = jwt.encode(un_token, clave, algorithm="HS256")

    return token

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

        if us == None:
            return False
        else:
            if verify_password(password, us.salt, us.password):
                token = compose_token(us)
                return token
            else:
                return False


@session_router.post("/register/prof")
async def register_professor(username:str = Form(...),\
                             password:str = Form(...), grupo:str =Form(...),\
                             nombre:str = Form(...), departamento:str = Form(...)):
    
    salt, hashed_pass = hash_password(password)

    with Session(engine) as sesion:

        us = Usuario(
            username= username,
            password= hashed_pass,
            salt= salt,
            grupo= grupo
        )
        sesion.add(us)
        sesion.commit()

        stmt = select(Usuario).where(Usuario.username == username)
        id = sesion.exec(stmt).first().id_usuario

        prof = Profesor(
            id_profesor= id,
            nombre= nombre,
            departamento= departamento
        )

        sesion.add(prof)
        sesion.commit()
    
    return {"status": "successful",
            "message": "Profesor registrado exitosamente"}

@session_router.post("/register/student")
async def register_student(username:str = Form(...),\
                           password:str = Form(...), grupo:str = Form(...),\
                           nombre:str = Form(...), facultad:str = Form(...)):
    
    salt, hashed_pass = hash_password(password)

    with Session(engine) as sesion:
        
        us = Usuario(
            username= username,
            password= hashed_pass,
            salt= salt,
            grupo= grupo
        )

        sesion.add(us)
        sesion.commit()

        stmt = select(Usuario).where(Usuario.username == username)
        id = sesion.exec(stmt).first().id_usuario

        est = Estudiante(
            id_estudiante= id,
            nombre= nombre,
            facultad= facultad
        )

        sesion.add(est)
        sesion.commit()
    
    return {"status": "successful",
            "message": "Estudiante registrado exitosamente"}