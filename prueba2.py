import pandas as pd
from dotenv import load_dotenv
import os
from unidecode import unidecode
from datetime import datetime
import mysql.connector

load_dotenv()

def conexion_db():
    conn = mysql.connector.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABSDE")
    )
    return conn

# Conectar y extraer datos
def obtener_datos():
    conn = conexion_db()
    query = "SELECT * FROM encuesta"
    datos = pd.read_sql(query, conn)
    conn.close()
    return datos

datos = obtener_datos()

# Mostrar comentarios de recomendación abierta
datos['recomendacion_abierta'] = datos['recomendacion_abierta'].fillna('')
for i, recomendacion in enumerate(datos['recomendacion_abierta'], start=1):
    print(f"{i}) {recomendacion} \n")

# Calculo de SNG
def calculo_SNG(datos):
    total_respuestas = len(datos)
    satisfaccion = (datos['satisfaccion_general'] > 5).sum()
    insatisfaccion = (datos['satisfaccion_general'] < 5).sum()
    neutros = (datos['satisfaccion_general'] == 5).sum()
    sng = (satisfaccion * 100 / total_respuestas) - (insatisfaccion * 100 / total_respuestas)
    return sng, neutros

sng_satisfaccion, neutros = calculo_SNG(datos)
print(f"SNG de satisfacción general: {sng_satisfaccion}")
print(f"Neutros: {neutros} \n")

# Total de personas que conocían la empresa
def conocian_empresa(datos):
    total = (datos['conocia_empresa'].apply(lambda x: unidecode(x).lower()) == 'si').sum()
    return total

total = conocian_empresa(datos)
print(f"Total de personas que conocían la empresa: {total} \n")

# Promedio de si recomendarías la empresa
def calcular_recomendacion(datos):
    total_respuestas = len(datos)
    suma_recomendacion = datos['recomendacion'].sum()
    recomendacion_satisfaccion = (datos['recomendacion'] > 5).sum()
    recomendacion_insatisfaccion = (datos['recomendacion'] < 5).sum()
    neutros = (datos['recomendacion'] == 5).sum()
    recomendacion_promedio = suma_recomendacion / total_respuestas
    sng_recomendacion = (recomendacion_satisfaccion * 100 / total_respuestas) - (recomendacion_insatisfaccion * 100 / total_respuestas)
    return sng_recomendacion, recomendacion_promedio, neutros

sng_recomendacion, recomendacion_promedio, neutros = calcular_recomendacion(datos)
print(f"SNG de la recomendación: {sng_recomendacion}")
print(f"Nota promedio de la recomendación: {recomendacion_promedio}")
print(f"Neutros: {neutros}\n")

# Todas las personas que hicieron comentarios
def hicieron_comentarios(datos):
    total = datos['recomendacion_abierta'].apply(lambda x: bool(x.strip())).sum()
    return total

total = hicieron_comentarios(datos)
print(f"Se hicieron comentarios: {total}\n")

# Periodo de encuesta
def periodo_encuesta(datos):
    datos['fecha'] = pd.to_datetime(datos['fecha'].str[:10])
    inicio = datos['fecha'].min()
    final = datos['fecha'].max()
    duracion = (final - inicio).days
    return inicio.strftime('%Y-%m-%d'), final.strftime('%Y-%m-%d'), duracion

inicio, final, duracion = periodo_encuesta(datos)
print(f"La fecha de inicio de la encuesta es: {inicio}")
print(f"La fecha de finalización de la encuesta es: {final}")
print(f"La encuesta duró {duracion} días")