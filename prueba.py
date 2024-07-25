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
        database = os.getenv ("DATABSE")
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

sng_satisfaccion, neutros, satisfaccion, insatisfaccion = calculo_SNG (datos)
print (f"satisfaccion: {satisfaccion}, insatisfaccion: {insatisfaccion}, neutros: {neutros}")
print (f"SNG de satisfacción general: {sng_satisfaccion}\n.")


# cauantos encuestados conosian a la enpresa ----------------------------------------------------------------------------------
def conocian_empresa (datos):
    total = len (datos)
    conocian = sum (1 for campo in datos if unidecode (campo ['conocia_empresa']).lower() == 'si')
    no_conocian = total - conocian
    return conocian, no_conocian, total

conocian, no_conocian, total = conocian_empresa (datos)
print (f"Total de personas que no conocían la empresa: {no_conocian}")
print (f"Total de personas que conocían la empresa: {conocian} \n")


# promedio de si recomendarias la enpresa -------------------------------------------------------------------------------------
def calcular_recomendacion (datos):
    total_respuestas = len (datos)
    suma_recomendacion = 0
    no_recomienda = 0
    recomienda = 0
    recomendacion_neutros = 0

    for campo in datos:
        suma_recomendacion += campo ['recomendacion']

        if campo ['recomendacion'] > 5:
            no_recomienda += 1

        elif campo ['recomendacion'] < 5:
            recomienda += 1

        elif campo ['recomendacion'] == 5:
            recomendacion_neutros += 1

    recomendacion_promedio = suma_recomendacion / total_respuestas

    sng_recomendacion = (recomienda * 100 / total_respuestas) - (no_recomienda * 100 / total_respuestas)

    return sng_recomendacion, recomendacion_promedio, recomendacion_neutros, recomienda, no_recomienda

sng_recomendacion, recomendacion_promedio, recomendacion_neutros, recomienda, no_recomienda = calcular_recomendacion (datos)

print (f"recomienda {recomienda}, no recomienda {no_recomienda}, neutro {recomendacion_neutros} ")
print (f"SNG de la recomendación: {sng_recomendacion}")
print (f"Nota promedio de la recomendación: {recomendacion_promedio}")
print (f"Neutros: {recomendacion_neutros}\n")


# Todas las personas que hicieron comentarios ---------------------------------------------------------------------------------
def hicieron_comentarios (datos):
    comentarios_totales = sum (1 for campo in datos if campo ['recomendacion_abierta'])

    return comentarios_totales

comentarios_totales = hicieron_comentarios (datos)
print (f"Se hicieron comentarios {comentarios_totales}\n")


# Periodo de encuesta----------------------------------------------------------------------------------------------------------
def periodo_encuesta (datos):
    fecha = []
    for dato in datos :
        fecha.append (datetime.strptime (dato ['fecha'][0:10], "%Y-%m-%d"))

    inicio = min(fecha)
    final = max(fecha)
    duracion = (final - inicio).days

    return inicio.strftime ('%d/%m/%Y'), final.strftime ('%d/%m/%Y'), duracion

inicio, final, duracion = periodo_encuesta (datos)

print (f"La fecha de inició de la encuesta es: {inicio}")
print (f"La fecha de finalización de la encuesta es: {final}")
print (f"La encuesta duró {duracion} días\n")


# como no tengo acseso a la api de openia estas serian las respuestas que me da chadgpt------------------------------------------
quejas_y_sentimientos = [{
    "principales_quejas": [
        "Malo servicio post-venta",
        "Departamentos defectuosos con muchas fallas",
        "Precios elevados de los estacionamientos",
        "Falta de estacionamientos de visita",
        "Mala gestión y administración del condominio",
        "Baja calidad de construcción y materiales",
        "Respuesta lenta e ineficiente a solicitudes de reparación",
        "Información engañosa durante el proceso de venta",
        "Problemas con los cálculos de subsidios y demoras",
        "Mala atención al cliente y personal no profesional"]
    },{
    "sentimientos": [
        "Neutral","Negative","Negative","Negative","Negative","Negative","Negative","Negative","Neutral","Neutral","Negative","Neutral","Negative","Positivo","Negative","Neutral","Positivo",
        "Positivo","Neutral","Negative","Neutral","Neutral","Neutral","Negative","Negative","Negative","Negative","Neutral","Neutral","Neutral","Neutral","Neutral","Negative","Neutral","Negative",
        "Negative","Neutral","Negative","Neutral","Negative","Positivo","Negative","Negative","Neutral","Negative","Negative","Negative","Negative","Negative","Neutral","Neutral","Negative",
        "Neutral","Positivo","Neutral","Negative","Neutral","Neutral","Negative","Negative","Negative"]}
]

def respuesta_gpt(quejas_y_sentimientos):
    principales_quejas = quejas_y_sentimientos[0]["principales_quejas"]
    sentimientos = quejas_y_sentimientos[1]["sentimientos"]

    quejas_formateadas = "Las principales quejas son:\n"
    positivo = 0
    negativo = 0
    neutral = 0

    for i, queja in enumerate (principales_quejas, start=1):
        quejas_formateadas += f"    {i}) {queja}\n"

    for sentimiento in sentimientos:
        if sentimiento == "Positivo":
            positivo += 1

        elif sentimiento == "Negative":
            negativo += 1

        elif sentimiento == "Neutral":
            neutral += 1

    return quejas_formateadas, positivo, negativo, neutral

quejas, positivo, negativo, neutral = respuesta_gpt (quejas_y_sentimientos)


# -------------------------------------------------------------------------------------------------------------------------------------------------------
# generacion automatica del informe en pdf
# -------------------------------------------------------------------------------------------------------------------------------------------------------
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import os

class Grafica:
    def __init__ (self, data, labels, title, colors, startangle = 0):
        self.data = data
        self.labels = labels
        self.title = title
        self.colors = colors
        self.startangle = startangle
        self.image = self.crear_grafica()

    def crear_grafica (self):
        fig, ax = plt.subplots()
        ax.pie (self.data, labels = self.labels, autopct = '%1.1f%%', startangle = self.startangle, colors = self.colors)
        ax.axis ('equal')
        ax.set_title (self.title, fontsize = 16, weight = 'bold')

        img_buffer = io.BytesIO()
        plt.savefig (img_buffer, format = 'png')
        img_buffer.seek (0)
        plt.close (fig)
        return ImageReader (img_buffer)


class Texto:
    def __init__(self, contenido, x, y):
        self.contenido = contenido
        self.x = x
        self.y = y

    def dibujar (self, canvas):
        text_object = canvas.beginText(self.x, self.y)
        text_object.setFont("Helvetica", 12)

        for line in self.contenido.split("\n"):
            text_object.textLine(line)

        canvas.drawText(text_object)

class InformeEncuesta:
    def __init__(self, titulo):
        self.titulo = titulo
        self.pdf_buffer = io.BytesIO()
        self.c = canvas.Canvas(self.pdf_buffer, pagesize=letter)
        self.paginas = [[]]

    def agregar_elemento(self, elemento, pagina=0):
        while len(self.paginas) <= pagina:
            self.paginas.append([])
        self.paginas[pagina].append(elemento)

    def generar_pdf(self):
        self.c.setFont("Helvetica-Bold", 16)
        self.c.drawCentredString(letter[0] / 2.0, letter[1] - 30, self.titulo)

        for pagina in self.paginas:
            for elemento in pagina:
                if isinstance(elemento, Grafica):
                    self.c.drawImage(elemento.image, elemento.x, elemento.y, width=400, height=300)
                elif isinstance(elemento, Texto):
                    elemento.dibujar(self.c)
            self.c.showPage()
        self.c.save()

        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, "informe_encuesta.pdf")
        with open(output_path, "wb") as f:
            f.write(self.pdf_buffer.getvalue())

# Titulo --------------------------------------------------------------------
titulo = "Informe de la encuesta realizada por MK"
informe = InformeEncuesta(titulo)


# Datos para la primera gráfica ----------------------------------------------
data_grafica_01 = {'Labels': ['Satisfacción', 'Insatisfacción', 'Neutrales'], 'Values': [satisfaccion, insatisfaccion, neutros]}
grafica_01 = Grafica(data_grafica_01['Values'], data_grafica_01['Labels'], "SNG de satisfacción general", ['green', 'red', 'lightskyblue'], startangle=134)
grafica_01.x = 100
grafica_01.y = 460


# Texto 01 --------------------------------------------------------------------
texto_01_x = 100
texto_01_y = 480

texto_01 = Texto(f"La encuesta dio un SNG de {'%.2f' % sng_satisfaccion} con {neutros} respuestas neutras de un total de {total}.", texto_01_x, texto_01_y)


# Datos para la segunda gráfica ------------------------------------------------
grafica_2_titulo = "Conocian a la empresa"
data_grafica_02 = {'Labels': ['Conocian', 'Desconocian'], 'Values': [conocian, no_conocian]}
grafica_02 = Grafica (data_grafica_02 ['Values'], data_grafica_02 ['Labels'], grafica_2_titulo, ['green', 'red'], startangle = 150)
grafica_02.x = 100
grafica_02.y = 150


# Texto 02 --------------------------------------------------------------------
texto_02_x = 120
texto_02_y = 170

texto_02 = Texto(f"{conocian} personas conocían previamente a la compañía y {no_conocian} la desconocian.", texto_02_x, texto_02_y)


# Tercera gráfica ----------------------------------------------
data_grafica_03 = {'Labels': ['recomienda', 'no recomienda', 'neutros'], 'Values': [recomienda, no_recomienda, recomendacion_neutros]}
grafica_03 = Grafica(data_grafica_03['Values'], data_grafica_03 ['Labels'], "Recomendacion", ['green', 'red', 'lightskyblue'], startangle=111)
grafica_03.x = 100
grafica_03.y = 490


# Texto 03 --------------------------------------------------------------------
texto_03_x = 70
texto_03_y = 515

texto_03 = Texto(f"Nota promedio de la recomendación: {'%.2f' % recomendacion_promedio} con {recomendacion_neutros} recomendación neutras de un total de {total}.", texto_03_x, texto_03_y)


# Texto 04 --------------------------------------------------------------------
texto_04_x = 160
texto_04_y = 500

texto_04 = Texto(f"La encuesta dio un SNG de recomendación de {'%.2f' % sng_recomendacion}.", texto_04_x, texto_04_y)


# grafica_04 --------------------------------------------------------------------
grafica_4_titulo = "Sentimientos de los comentarios"
data_grafica_04 = {'Labels': ['Neutral', 'Negativo', 'Positivo' ], 'Values': [neutral, negativo, positivo]}
grafica_04 = Grafica (data_grafica_04 ['Values'], data_grafica_04 ['Labels'], grafica_4_titulo, ['lightskyblue', 'red', 'green'], startangle = 120)
grafica_04.x = 100
grafica_04.y = 200

# Texto 05 --------------------------------------------------------------------
texto_05_x = 228
texto_05_y = 225

texto_05 = Texto (f"Se hicieron {comentarios_totales} comentarios", texto_05_x, texto_05_y)


# Texto 06 --------------------------------------------------------------------
texto_06_x = 50
texto_06_y = 200

texto_06 = Texto (quejas, texto_06_x, texto_06_y)


# Texto 07 --------------------------------------------------------------------
texto_07_x = 120
texto_07_y = 20

texto_07 = Texto(f"La encuesta inicio el {inicio} y finalizó el {final} durando {duracion} días.", texto_07_x, texto_07_y)

# Agregar elementos a la primera página --------------------------------------------------------
informe.agregar_elemento (grafica_01, pagina = 0)
informe.agregar_elemento (texto_01, pagina = 0)
informe.agregar_elemento (grafica_02, pagina = 0)
informe.agregar_elemento (texto_02, pagina = 0)

# Agregar elementos a la segunda página --------------------------------------------------------
informe.agregar_elemento (grafica_03, pagina = 1)
informe.agregar_elemento (texto_03, pagina = 1)
informe.agregar_elemento (texto_04, pagina = 1)
informe.agregar_elemento (grafica_04, pagina = 1)
informe.agregar_elemento (texto_05, pagina = 1)
informe.agregar_elemento (texto_06, pagina = 1)
informe.agregar_elemento (texto_07, pagina = 1)

# Generar el PDF
informe.generar_pdf()
print ("pronto")


