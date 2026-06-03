"""This module defines generic operations for the database"""

#imports go here
from mysql.connector import connect, Error

#functions go here
def bd_connect():
    """This method establishes a connection with mysql server and returns it"""
    results = "pinga"

    try:
        connection = connect(
            host="localhost",
            user="api",
            password="systemAccess_749",
            database="sistema_de_asistencia")
        
        cursor = connection.cursor(dictionary=True)
        consulta = "describe estudiantes;"
        cursor.execute(consulta)
        results = cursor.fetchall()
        connection.commit()
    except Error as e:
        print(e)
    finally:
        connection.close()
    
    return results
    


#main code (I think none) goes here
print(bd_connect())