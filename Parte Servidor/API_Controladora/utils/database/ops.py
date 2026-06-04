"""This module defines generic operations for the database"""

#imports and global variables go here
from mysql.connector import connect, Error
from sqlmodel import create_engine, Session, select, update, delete, insert, desc
import models

bd_url = "mysql+pymysql://api:systemAccess_749@localhost:3306/sistema_de_asistencia"

con_eng = create_engine(bd_url, echo=True)

#functions go here
def bd_connect():
    """This method establishes a connection with mysql server and returns it"""
    with Session(con_eng) as sesion:
        stmt = select(models.Usuario)
        result = sesion.exec(stmt)
        usuarios = result.all()
        print(usuarios)


#main code (I think none) goes here
print(bd_connect())