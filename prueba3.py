import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import os

# Variable para el texto intermedio
texto_01 = "La encuesta dio como resultado que la mayoria de la personas "

# Datos para la primera gráfica circular usando pandas
data_grafica_01 = {'Labels': ['satisfaccion', 'insatisfaccion', 'neutros'], 'Values': [23, 25, 13]}
df1 = pd.DataFrame(data_grafica_01)

# Crear la primera gráfica circular
fig1, ax1 = plt.subplots()
ax1.pie(df1['Values'], labels=df1['Labels'], autopct='%1.1f%%', startangle=134, colors=['green', 'red', 'lightskyblue'])
ax1.axis('equal')  # Para que sea un círculo perfecto

# Título de la primera gráfica
ax1.set_title("SNG de satisfacción general", fontsize=16, weight='bold')

# Guardar la primera gráfica en un objeto BytesIO
img_buffer1 = io.BytesIO()
plt.savefig(img_buffer1, format='png')
img_buffer1.seek(0)
plt.close(fig1)

# Convertir BytesIO a ImageReader para la primera gráfica
img1 = ImageReader(img_buffer1)


# Datos para la segunda gráfica circular usando pandas
data2 = {'Labels': ['X', 'Y', 'Z'], 'Values': [20, 50, 30]}
df2 = pd.DataFrame(data2)

# Crear la segunda gráfica circular
fig2, ax2 = plt.subplots()
ax2.pie(df2['Values'], labels=df2['Labels'], autopct='%1.1f%%', startangle=140, colors=['lightgreen', 'lightblue', 'lightpink'])
ax2.axis('equal')  # Para que sea un círculo perfecto

# Título de la segunda gráfica
ax2.set_title("Gráfica Circular 2", fontsize=16, weight='bold')

# Guardar la segunda gráfica en un objeto BytesIO
img_buffer2 = io.BytesIO()
plt.savefig(img_buffer2, format='png')
img_buffer2.seek(0)
plt.close(fig2)

# Convertir BytesIO a ImageReader para la segunda gráfica
img2 = ImageReader(img_buffer2)


# Crear el PDF
pdf_buffer = io.BytesIO()
c = canvas.Canvas(pdf_buffer, pagesize=letter)

# Agregar el título en la parte superior del documento
title = "Informe de la encuesta realisada por MK"
c.setFont("Helvetica-Bold", 16)
c.drawCentredString(letter[0] / 2.0, letter[1] - 50, title)

# Ajustar la posición y tamaño de la primera imagen en el PDF
image_width = 400
image_height = 300
x_position = 100
y_position1 = 400  # Ajusta esta variable para cambiar la altura de la primera gráfica

c.drawImage(img1, x_position, y_position1, width=image_width, height=image_height)

# Agregar el texto entre las dos gráficas
text_y_position = y_position1 - 50
c.setFont("Helvetica", 12)
c.drawString(x_position, text_y_position, texto_01)

# Ajustar la posición y tamaño de la segunda imagen en el PDF
y_position2 = text_y_position - image_height - 50  # Ajusta esta variable para cambiar la altura de la segunda gráfica
c.drawImage(img2, x_position, y_position2, width=image_width, height=image_height)

c.showPage()
c.save()

# Guardar el PDF en un archivo en la misma carpeta del script
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "grafica_circular.pdf")
with open(output_path, "wb") as f:
    f.write(pdf_buffer.getvalue())
