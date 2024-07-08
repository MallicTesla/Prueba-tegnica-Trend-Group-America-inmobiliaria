import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io

# Datos para la gráfica circular usando pandas
data = {'Labels': ['Aasdasdasd', 'asdasdB', 'asdasdasdasdC'], 'Values': [30, 4, 30]}
df = pd.DataFrame(data)

# Crear la gráfica circular
fig, ax = plt.subplots()
ax.pie(df['Values'], labels=df['Labels'], autopct='%1.1f%%', startangle=140, colors=['gold', 'lightcoral', 'lightskyblue'])
ax.axis('equal')  # Para que sea un círculo perfecto

# Guardar la gráfica en un objeto BytesIO
img_buffer = io.BytesIO()
plt.savefig(img_buffer, format='png')
img_buffer.seek(0)
plt.close(fig)

# Convertir BytesIO a ImageReader
img = ImageReader(img_buffer)

# Crear el PDF
pdf_buffer = io.BytesIO()
c = canvas.Canvas(pdf_buffer, pagesize=letter)
c.drawImage(img, 100, 100, width=400, height=300)  # Ajustar la posición y tamaño según sea necesario
c.showPage()
c.save()

# Guardar el PDF en un archivo
with open("grafica_circular.pdf", "wb") as f:
    f.write(pdf_buffer.getvalue())
