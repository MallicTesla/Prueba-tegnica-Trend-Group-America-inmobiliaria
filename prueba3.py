import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import os

class InformeEncuesta:
    def __init__(self, titulo):
        self.titulo = titulo
        self.pdf_buffer = io.BytesIO()
        self.c = canvas.Canvas (self.pdf_buffer, pagesize = letter)
        self.image_width = 400
        self.image_height = 300
        self.x_position = 100

    def crear_grafica(self, data, labels, title, colors, startangle = 0):
        fig, ax = plt.subplots()
        ax.pie (data, labels = labels, autopct = '%1.1f%%', startangle = startangle, colors = colors)
        ax.axis ('equal')
        ax.set_title (title, fontsize = 16, weight = 'bold')

        img_buffer = io.BytesIO()
        plt.savefig (img_buffer, format = 'png')
        img_buffer.seek(0)
        plt.close (fig)
        return ImageReader (img_buffer)

    def agregar_texto (self, texto):
        text_y_position = self.y_position1 - 50
        self.c.setFont ("Helvetica", 12)
        self.c.drawString (self.x_position, text_y_position, texto)
        return text_y_position

    def generar_pdf(self, img1, img2, texto):
        self.c.setFont ("Helvetica-Bold", 16)
        self.c.drawCentredString (letter[0] / 2.0, letter[1] - 30, self.titulo)

        self.y_position1 = 450
        self.c.drawImage (img1, self.x_position, self.y_position1, width = self.image_width, height = self.image_height)

        text_y_position = self.agregar_texto (texto)

        y_position2 = text_y_position - self.image_height - 50
        self.c.drawImage (img2, self.x_position, y_position2, width = self.image_width, height = self.image_height)

        self.c.showPage()
        self.c.save()

        script_dir = os.path.dirname (os.path.abspath (__file__))
        output_path = os.path.join (script_dir, "informe_encuesta.pdf")
        with open (output_path, "wb") as f:
            f.write (self.pdf_buffer.getvalue())


# Titulo
titulo = "Informe de la encuesta realizada por MK"
informe = InformeEncuesta (titulo)

# Datos para la primera gráfica
data_grafica_01 = {'Labels': ['satisfacción', 'insatisfacción', 'neutros'], 'Values': [23, 25, 13]}
img1 = informe.crear_grafica (data_grafica_01 ['Values'], data_grafica_01 ['Labels'], "SNG de satisfacción general", ['green', 'red', 'lightskyblue'], startangle = 134)

# Texto intermedio
sng = -3.28
neutros = 13
total = 61
texto_01 = f"La encuesta dio un SNG de {'%.2f' % sng} con {neutros} respuestas neutras de un total de {total}"

# Datos para la segunda gráfica
data_grafica_02 = {'Labels': ['X', 'Y', 'Z'], 'Values': [20, 50, 30]}
img2 = informe.crear_grafica (data_grafica_02 ['Values'], data_grafica_02 ['Labels'], "Gráfica Circular 2", ['lightgreen', 'lightblue', 'lightpink'], startangle = 140)

# Generar el PDF
informe.generar_pdf (img1, img2, texto_01)


print ("pronto")
