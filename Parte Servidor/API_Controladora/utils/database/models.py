"""Models for the ORM, nth attemp"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import date

class Usuario(SQLModel, table=True):
    """Clase de usuario básica"""
    __tablename__ = "usuario"
    id_usuario: Optional[int] = Field(primary_key=True, default=None)
    username: str = Field(unique=True)
    password:str
    salt:str
    grupo:str
    estudiante: "Estudiante"  = Relationship(back_populates="usuario", cascade_delete=True)
    profesor: "Profesor" = Relationship(back_populates="usuario", cascade_delete=True)

class Estudiante(SQLModel, table=True):
    """Clase para el rol de estudiante"""
    __tablename__ = "estudiante"
    id_estudiante: Optional[int] = Field(default=None, foreign_key="usuario.id_usuario", primary_key=True)
    nombre:str
    facultad:str
    usuario: Usuario = Relationship(back_populates="estudiante")

class Profesor(SQLModel, table=True):
    """Clase para el rol de profesor"""
    __tablename__ = "profesor"
    id_profesor: Optional[int] = Field(default=None, foreign_key="usuario.id_usuario", primary_key=True)
    nombre:str
    departamento:str
    usuario: Usuario = Relationship(back_populates="profesor")

class Reporte(SQLModel, table=True):
    """Tabla para guardar los reportes"""
    __tablename__ = "reporte"
    id_reporte: Optional[int] = Field(primary_key=True, default=None)
    id_profesor: Optional[int] = Field(foreign_key="profesor.id_profesor", default=None)
    contenido:str
    fecha:date