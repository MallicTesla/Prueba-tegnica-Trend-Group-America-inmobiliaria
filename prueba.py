from unidecode import unidecode
import mysql.connector

def conexion_db():
    conn = mysql.connector.connect(
        host = '54.219.2.160',
        user = 'postulante',
        password = 'HB<tba!Sp6U2j5CN',
        database = 'prueba_postulantes'
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

for dato in datos [:5]:
    n += 1
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

    return sng, neutros

sng_satisfaccion, neutros = calculo_SNG(datos)
print(f"SNG de satisfacción general: {sng_satisfaccion}")
print (f"Neutros {neutros} \n")


# cauantos esncuestados conosian a la enpresa ---------------------------------------------------------------------------------
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











