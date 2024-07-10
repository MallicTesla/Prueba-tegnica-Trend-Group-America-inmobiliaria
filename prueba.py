from dotenv import load_dotenv
import os

from unidecode import unidecode
from datetime import datetime
import mysql.connector


load_dotenv ()

def conexion_db():
    conn = mysql.connector.connect(
        host = os.getenv ("HOST"),
        user = os.getenv ("USER"),
        password = os.getenv ("PASSWORD"),
        database = os.getenv ("DATABSDE")
    )
    return conn


# Conectar y extraer datos
def obtener_datos():
    conn = conexion_db()
    cursor = conn.cursor (dictionary = True)
    cursor.execute ("SELECT * FROM encuesta")
    datos = cursor.fetchall()
    cursor.close()
    conn.close()
    return datos


datos = obtener_datos()
n = 0

# print (datos ["recomendacion_abierta"])
for dato in datos[:5]:
    n += 1
#     print (f"{n}) {dato ['recomendacion_abierta']} \n")  
    print (f"{n}) {dato} \n")


# calculo de SNG --------------------------------------------------------------------------------------------------------------
def calculo_SNG (datos):
    total_respuestas = len (datos)
    satisfaccion = 0
    insatisfaccion = 0
    neutros = 0

    for campo in datos:
        if campo ['satisfeccion_general'] > 5:
            satisfaccion += 1

        elif campo ['satisfeccion_general'] < 5:
            insatisfaccion += 1

        elif campo ['satisfeccion_general'] == 5:
            neutros += 1

    sng = (satisfaccion * 100 / total_respuestas) - (insatisfaccion * 100 / total_respuestas)

    return sng, neutros, satisfaccion, insatisfaccion

sng_satisfaccion, neutros, satisfaccion, insatisfaccion = calculo_SNG(datos)
print ("satisfaccion", satisfaccion, "insatisfaccion", insatisfaccion, "neutros", neutros)
print(f"SNG de satisfacción general: {sng_satisfaccion}")
print (f"Neutros {neutros} \n")


# cauantos encuestados conosian a la enpresa ----------------------------------------------------------------------------------
def conocian_empresa (datos):
    total = sum (1 for campo in datos if unidecode (campo ['conocia_empresa']).lower() == 'si')
    return total

total = conocian_empresa(datos)
print(f"Total de personas que conocían la empresa: {total} \n")


# promedio de si recomendarias la enpresa -------------------------------------------------------------------------------------
def calcualr_recomendacion (datos):
    total_respuestas = len (datos)
    suma_recomendacion = 0
    recomendacion_insatisfaccion = 0
    recomendacion_satisfaccion = 0
    neutros = 0

    for campo in datos:
        suma_recomendacion += campo ['recomendacion']

        if campo ['recomendacion'] > 5:
            recomendacion_insatisfaccion += 1

        elif campo ['recomendacion'] < 5:
            recomendacion_satisfaccion += 1

        elif campo ['recomendacion'] == 5:
            neutros += 1

    recomendacion_promedio = suma_recomendacion / total_respuestas

    sng_recomendacion = (recomendacion_satisfaccion * 100 / total_respuestas) - (recomendacion_insatisfaccion * 100 / total_respuestas)

    return sng_recomendacion, recomendacion_promedio, neutros

sng_recomendacion, recomendacion_promedio, neutros = calcualr_recomendacion (datos)

print (f"SNG de la recomendación: {sng_recomendacion}")
print (f"Nota promedio de la recomendación: {recomendacion_promedio}")
print (f"Neutros: {neutros}\n")


# Todas las personas que hicieron comentarios ---------------------------------------------------------------------------------
def hiciern_comentarios (datos):
    total = sum (1 for campo in datos if campo ['recomendacion_abierta'])

    return total

total = hiciern_comentarios (datos)
print (f"Se hicieron comentarios {total}\n")


# Periodo de encuesta----------------------------------------------------------------------------------------------------------
def periodo_encuesta (datos):
    fecha = []
    for dato in datos :
        fecha += [datetime.strptime (dato ['fecha'][0:10], "%Y-%m-%d")]

    inicio = min(fecha)
    final = max(fecha)
    duracion = (final - inicio).days

    return inicio.strftime('%Y-%m-%d'), final.strftime('%Y-%m-%d'), duracion

inicio, final, duracion = periodo_encuesta (datos)

print (f"La fecha de inicio de la encuesta es: {inicio}")
print (f"La fecha de finalización de la encuesta es: {final}")
print (f"La encuesta duro {duracion} dias")




# como no tengo acseso a a api de openia estas serian las respuestas que me da chadgpt------------------------------------------
sentimientos ={"response": [
    {"id": 1, "sentiment": "Neutral"},
    {"id": 2, "sentiment": "Negative"},
    {"id": 3, "sentiment": "Negative"},
    {"id": 4, "sentiment": "Negative"},
    {"id": 5, "sentiment": "Negative"},
    {"id": 6, "sentiment": "Negative"},
    {"id": 7, "sentiment": "Negative"},
    {"id": 8, "sentiment": "Negative"},
    {"id": 9, "sentiment": "Neutral"},
    {"id": 10, "sentiment": "Neutral"},
    {"id": 11, "sentiment": "Negative"},
    {"id": 12, "sentiment": "Neutral"},
    {"id": 13, "sentiment": "Negative"},
    {"id": 14, "sentiment": "Positivo"},
    {"id": 15, "sentiment": "Negative"},
    {"id": 16, "sentiment": "Neutral"},
    {"id": 17, "sentiment": "Positivo"},
    {"id": 18, "sentiment": "Positivo"},
    {"id": 19, "sentiment": "Neutral"},
    {"id": 20, "sentiment": "Negative"},
    {"id": 21, "sentiment": "Neutral"},
    {"id": 22, "sentiment": "Neutral"},
    {"id": 23, "sentiment": "Neutral"},
    {"id": 24, "sentiment": "Negative"},
    {"id": 25, "sentiment": "Negative"},
    {"id": 26, "sentiment": "Negative"},
    {"id": 27, "sentiment": "Negative"},
    {"id": 28, "sentiment": "Neutral"},
    {"id": 29, "sentiment": "Neutral"},
    {"id": 30, "sentiment": "Neutral"},
    {"id": 31, "sentiment": "Neutral"},
    {"id": 32, "sentiment": "Neutral"},
    {"id": 33, "sentiment": "Negative"},
    {"id": 34, "sentiment": "Neutral"},
    {"id": 35, "sentiment": "Negative"},
    {"id": 36, "sentiment": "Negative"},
    {"id": 37, "sentiment": "Neutral"},
    {"id": 38, "sentiment": "Negative"},
    {"id": 39, "sentiment": "Neutral"},
    {"id": 40, "sentiment": "Negative"},
    {"id": 41, "sentiment": "Positivo"},
    {"id": 42, "sentiment": "Negative"},
    {"id": 43, "sentiment": "Negative"},
    {"id": 44, "sentiment": "Neutral"},
    {"id": 45, "sentiment": "Negative"},
    {"id": 46, "sentiment": "Negative"},
    {"id": 47, "sentiment": "Negative"},
    {"id": 48, "sentiment": "Negative"},
    {"id": 49, "sentiment": "Negative"},
    {"id": 50, "sentiment": "Neutral"},
    {"id": 51, "sentiment": "Neutral"},
    {"id": 52, "sentiment": "Negative"},
    {"id": 53, "sentiment": "Neutral"},
    {"id": 54, "sentiment": "Positivo"},
    {"id": 55, "sentiment": "Neutral"},
    {"id": 56, "sentiment": "Negative"},
    {"id": 57, "sentiment": "Neutral"},
    {"id": 58, "sentiment": "Neutral"},
    {"id": 59, "sentiment": "Negative"},
    {"id": 60, "sentiment": "Negative"},
    {"id": 61, "sentiment": "Negative"}
    ]
}

quejas = {"principales_quejas": [
    "Malo servicio post-venta",
    "Departamentos defectuosos con muchas fallas",
    "Precios elevados de los estacionamientos",
    "Falta de estacionamientos de visita",
    "Mala gestión y administración del condominio",
    "Baja calidad de construcción y materiales",
    "Respuesta lenta e ineficiente a solicitudes de reparación",
    "Información engañosa durante el proceso de venta",
    "Problemas con los cálculos de subsidios y demoras",
    "Mala atención al cliente y personal no profesional"
    ]
}
# def analisis_sentimientos (sentimientos):




