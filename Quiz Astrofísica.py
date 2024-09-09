import customtkinter as ctk
import random

# Función para cargar preguntas desde un archivo de texto
def cargar_preguntas_txt(nombre_archivo):
    preguntas = []
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
            preguntas_raw = contenido.split("----------")
            for pregunta_raw in preguntas_raw:
                lineas = pregunta_raw.strip().split("\n")
                if len(lineas) >= 4:
                    pregunta = lineas[0].replace("Pregunta: ", "").strip()
                    opciones = [linea.replace("✔", "").strip() for linea in lineas[1:5]]  # Considerar hasta 4 opciones
                    respuesta_correcta = [linea for linea in lineas[1:5] if "✔" in linea]
                    if respuesta_correcta:
                        respuesta_correcta = respuesta_correcta[0].replace("✔", "").strip()
                    else:
                        respuesta_correcta = None
                    # Traducción para preguntas de verdadero/falso
                    if "true" in opciones[0].lower():
                        opciones = ["verdadero", "falso"]
                        respuesta_correcta = "verdadero" if "true" in respuesta_correcta.lower() else "falso"
                    preguntas.append((pregunta, opciones, respuesta_correcta))
    except FileNotFoundError:
        print("Error: no se encontró el archivo.")
    except Exception as e:
        print(f"Error inesperado: {e}")
    return preguntas

# Función para verificar si la respuesta seleccionada es correcta
def verificar_respuesta(opcion_seleccionada, respuesta_correcta, resultado_label, boton_siguiente, botones_opciones):
    global contador_respuestas_correctas, contador_total_preguntas
    contador_total_preguntas += 1  # Incrementar el contador de preguntas respondidas

    # Deshabilitar todos los botones después de seleccionar una respuesta
    for boton in botones_opciones:
        boton.configure(state="disabled")

    if opcion_seleccionada == respuesta_correcta:
        resultado_label.configure(text="¡Respuesta correcta!", fg_color="green")
        contador_respuestas_correctas += 1  # Incrementar el contador de respuestas correctas
    else:
        resultado_label.configure(text=f"Incorrecto. La respuesta correcta era: {respuesta_correcta}", fg_color="red")
    
    # Actualizar el contador en la GUI
    contador_label.configure(text=f"Correctas: {contador_respuestas_correctas} / Total: {contador_total_preguntas}")
    boton_siguiente.configure(state="normal")  # Habilitar el botón para la siguiente pregunta

# Función para cargar una nueva pregunta
def mostrar_pregunta():
    global pregunta_actual
    if preguntas_restantes:
        pregunta_actual = random.choice(preguntas_restantes)
        preguntas_restantes.remove(pregunta_actual)

        pregunta_label.configure(text=pregunta_actual[0])
        for i, boton in enumerate(boton_opciones):
            boton.configure(text=pregunta_actual[1][i], state="normal", fg_color="#3B8ED0")
        resultado_label.configure(text="")
        boton_siguiente.configure(state="disabled")
    else:
        pregunta_label.configure(text="¡Quiz completado!")
        for boton in boton_opciones:
            boton.configure(state="disabled")
        resultado_label.configure(text="")

# Configuración de la ventana principal usando customtkinter
app = ctk.CTk()
app.geometry("800x600")
app.title("Quiz de Astrofísica")

# Contadores
contador_respuestas_correctas = 0
contador_total_preguntas = 0

pregunta_label = ctk.CTkLabel(app, text="", font=("Arial", 18), wraplength=450)
pregunta_label.pack(pady=20)

boton_opciones = []
for i in range(4):
    boton = ctk.CTkButton(app, text="", font=("Arial", 14), width=300, command=lambda i=i: verificar_respuesta(boton_opciones[i].cget("text"), pregunta_actual[2], resultado_label, boton_siguiente, boton_opciones))
    boton.pack(pady=5)
    boton_opciones.append(boton)

resultado_label = ctk.CTkLabel(app, text="", font=("Arial", 14))
resultado_label.pack(pady=20)

boton_siguiente = ctk.CTkButton(app, text="Siguiente", font=("Arial", 14), state="disabled", command=mostrar_pregunta)
boton_siguiente.pack(pady=10)

# Etiqueta para mostrar el contador de preguntas
contador_label = ctk.CTkLabel(app, text="Correctas: 0 / Total: 0", font=("Arial", 14))
contador_label.pack(pady=10)

# Cargar preguntas y comenzar el quiz
nombre_archivo = "Juegos de astrofísica\\PRINCIPIANTE.txt"  # Ajusta esta ruta según tu archivo de preguntas
preguntas = cargar_preguntas_txt(nombre_archivo)
preguntas_restantes = preguntas[:]
pregunta_actual = None

mostrar_pregunta()

app.mainloop()
