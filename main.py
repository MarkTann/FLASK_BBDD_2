import os
from flask import Flask,jsonify,request
import pickle
import psycopg2
import pandas as pd
from sqlalchemy import create_engine, text
'''
En esta sección se importan las librerías necesarias para crear la API RESTful y acceder a la base de datos PostgreSQL. 
Flask es la librería principal que se utiliza para crear la aplicación web.
También se importan las librerías Pandas y SQLAlchemy para acceder a la base de datos y manipular los datos.
Además, se importan otras librerías como jsonify y request, que permiten enviar y recibir datos en formato JSON,
y text, que se utiliza para ejecutar consultas SQL.
'''
# Se crea una instancia de la clase Flask y se asigna a la variable app. __name__ es una
# variable especial en Python que indica el nombre del módulo actual.
app=Flask(__name__) 

@app.route("/", methods=["GET"]) # funcion que maneja la solicitud de la ruta principal("/").
#Solo devuelve una cadena de HTML que muestra las rutas disponibles para realizar las consultas.
def home():
    
    return """
    <h1> Pantalla Inicio</h1>
    Rutas:</br>
    Barrios->/api/v1/barrios</br>
    Nombre->/api/v1/barrios/nombre</br> 
    Limites de Areas->/api/v1/barrios/limits
    """

@app.route("/api/v1/barrios", methods=["GET"])
def get_barrios():

    engine = create_engine('postgresql://postgres:pGlmGgTNbTQaEsASuO4Y@containers-us-west-189.railway.app:7863/railway')
    # con el engine conectamos a las BBDD. 
    # datos = pd.read_sql('select * from "Barrios"', con=engine)
    query = text('SELECT * FROM "Barrios"')
    # el query será la consulta que vamos a ejecutar al PostgreSQL, para obtener los datos de la tabla Barrios

    data = pd.read_sql_query(query, engine.connect())
    # esta parte del código mete en un dataframe los datos de la query.

    return jsonify(data.to_json())
# to_jason permite transformar el dataframe creado con los barrios a json.
# Necesario para poder enviar de nuevo al "usuario"
# jsonify, de FLASK, permite retornar los datos como una respuesta HTTP.

@app.route("/api/v1/barrios/nombre", methods=["GET"])
def by_nombre():
    nombre = request.args["Nombre"] # request.args sirve para especificar el criterio de búsqueda de la consulta SQL
    engine = create_engine('postgresql://postgres:pGlmGgTNbTQaEsASuO4Y@containers-us-west-189.railway.app:7863/railway')
    #datos = pd.read_sql('select * from "Barrios"', con=engine)
    query = text(f"""SELECT * FROM "Barrios" WHERE "Nombre"='{nombre}'""")
    data = pd.read_sql_query(query, engine.connect())

    return jsonify(data.to_json())

@app.route("/api/v1/barrios/limits", methods=["GET"])
def by_areas():
    area_min = request.args["area_min"]
    area_max = request.args["area_max"]
    engine = create_engine('postgresql://postgres:pGlmGgTNbTQaEsASuO4Y@containers-us-west-189.railway.app:7863/railway')
    #datos = pd.read_sql('select * from "Barrios"', con=engine)
    query = text(f"""SELECT * FROM "Barrios" WHERE "Areas de barrios">'{area_min}' and "Areas de barrios"<'{area_max}'""")
    data = pd.read_sql_query(query, engine.connect())

    return jsonify(data.to_json())

if __name__=="__main__":
    app.run(debug=True)
