"""Little module for DataBase boot process"""

from sqlmodel import create_engine, SQLModel
from utils.database.models import Usuario, Estudiante, Profesor, Reporte

DB_URL = "mysql+pymysql://frost:CrimsonCC3327-0@localhost:3306/sistema_de_asistencia"

engine = create_engine(DB_URL, echo=True)