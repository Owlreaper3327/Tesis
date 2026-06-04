"""Models for current solution"""

import sqlmodel
from typing import Optional
from sqlmodel import SQLModel, Field 
import datetime

class Usuario(SQLModel, table=True):
    """Main user class"""
    __tablename__ = "usuarios"
    id_usuario: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    password: str
    grupo: str = Field(max_length=6, min_length=6)

class Profesor(Usuario, table=True):
    """Professor model class"""
    __tablename__ = "profesores"
    id_profesor: Optional[int] = Field(foreign_key="usuarios.id_usuario", primary_key=True)
    nombre: str
    departamento: str

class Estudiante(Usuario, table=True):
    """Student model class"""
    __tablename__ = "estudiantes"
    id_estudiante: Optional[int] = Field(foreign_key="usuarios.id_usuario", primary_key=True)
    nombre: str
    facultad: str

class Reporte(SQLModel, table=True):
    """Report model class"""
    __tablename__ = "reportes"
    id_reporte: Optional[int] = Field(primary_key=True, default=None)
    id_profesor: Optional[int] = Field(foreign_key="profesores.id_profesor")
    contenido: str
    fecha: datetime.date