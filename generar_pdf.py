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
satisfaccion = 23
insatisfaccion = 25
neutros = 13

data_grafica_01 = {'Labels': ['satisfacción', 'insatisfacción', 'neutros'], 'Values': [satisfaccion, insatisfaccion, neutros]}
grafica_01 = Grafica(data_grafica_01['Values'], data_grafica_01['Labels'], "SNG de satisfacción general", ['green', 'red', 'lightskyblue'], startangle=134)
grafica_01.x = 100
grafica_01.y = 460


# Texto 01 --------------------------------------------------------------------
texto_01_x = 100
texto_01_y = 480
sng_satisfaccion = -3.28
neutros = 13
total = 61

texto_01 = Texto(f"La encuesta dio un SNG de {'%.2f' % sng_satisfaccion} con {neutros} respuestas neutras de un total de {total}.", texto_01_x, texto_01_y)


# Datos para la segunda gráfica ------------------------------------------------
no_conocian = 52
conocian = 9

grafica_2_titulo = "Conocian a la empresa"
data_grafica_02 = {'Labels': ['Conocian', 'Desconocian'], 'Values': [conocian, no_conocian]}
grafica_02 = Grafica (data_grafica_02 ['Values'], data_grafica_02 ['Labels'], grafica_2_titulo, ['green', 'red'], startangle = 150)
grafica_02.x = 100
grafica_02.y = 150


# Texto 02 --------------------------------------------------------------------
texto_02_x = 120
texto_02_y = 170

texto_02 = Texto(f"{conocian} personas concian previamente a la compania y {no_conocian} la desconocian.", texto_02_x, texto_02_y)


# Tercera gráfica ----------------------------------------------
recomienda = 27
no_recomienda = 29
recomendacion_neutros = 5

data_grafica_03 = {'Labels': ['recomienda', 'no recomienda', 'neutros'], 'Values': [recomienda, no_recomienda, recomendacion_neutros]}
grafica_03 = Grafica(data_grafica_03['Values'], data_grafica_03 ['Labels'], "Recomendacion", ['green', 'red', 'lightskyblue'], startangle=111)
grafica_03.x = 100
grafica_03.y = 460


# Texto 03 --------------------------------------------------------------------
texto_03_x = 70
texto_03_y = 480
recomendacion_neutros = 5
recomendacion_promedio = 4.47540983605574

texto_03 = Texto(f"Nota promedio de la recomendación: {'%.2f' % recomendacion_promedio} con {recomendacion_neutros} recomendacion neutras de un total de {total}.", texto_03_x, texto_03_y)


# Texto 04 --------------------------------------------------------------------
texto_04_x = 160
texto_04_y = 450
sng_recomendacion = -3.278688524590166

texto_04 = Texto(f"La encuesta dio un SNG de recomendacion de {'%.2f' % sng_recomendacion}.", texto_04_x, texto_04_y)


# Texto 05 --------------------------------------------------------------------
texto_05_x = 120
texto_05_y = 380
inicio = "31/05/2023"
final = "23/08/2023"
duracion = 84

texto_05 = Texto(f"La encuesta inicio el {inicio} y final el {final} durando {duracion} días.", texto_05_x, texto_05_y)


# Texto 06 --------------------------------------------------------------------
texto_06_x = 50
texto_06_y = 310

gpt_quejas = {"principales_quejas": [
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

def respuesta_gpt(gpt_quejas):
    prinsipales_quejas = gpt_quejas["principales_quejas"]
    quejas_formateadas = "Las principales quejas son:\n"
    for i, queja in enumerate(prinsipales_quejas, start=1):
        quejas_formateadas += f"    {i}) {queja}\n"
    return quejas_formateadas

quejas = respuesta_gpt(gpt_quejas)

texto_06 = Texto(quejas, texto_06_x, texto_06_y)


# Agregar elementos a la primera página --------------------------------------------------------
informe.agregar_elemento (grafica_01, pagina = 0)
informe.agregar_elemento (texto_01, pagina = 0)
informe.agregar_elemento (grafica_02, pagina = 0)
informe.agregar_elemento (texto_02, pagina = 0)

# Agregar elementos a la segunda página --------------------------------------------------------
informe.agregar_elemento (grafica_03, pagina = 1)
informe.agregar_elemento (texto_03, pagina = 1)
informe.agregar_elemento (texto_04, pagina = 1)
informe.agregar_elemento (texto_05, pagina = 1)
informe.agregar_elemento (texto_06, pagina = 1)

# Generar el PDF con múltiples páginas
informe.generar_pdf()
print ("pronto")
