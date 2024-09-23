import tkinter as tk
import requests
import socket
import time
from threading import Thread

# URL de la API MockAPI
API_URL = "http://127.0.0.1:5000/cars"

# Función para obtener la IP del cliente
def obtener_ip_cliente():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

# Función para obtener la fecha actual en formato Unix
def obtener_fecha_actual():
    return int(time.time())

# Función para enviar datos a MockAPI
def enviar_datos(status):
    nombre = "Alejandro"  # El nombre por defecto es Alejandro
    data = {
        "status": status,  # Enviar el status seleccionado
        "date": obtener_fecha_actual(),
        "ipClient": obtener_ip_cliente(),
        "name": nombre,
        "id": "5"  # ID estático como ejemplo
    }

    def enviar_peticion():
        try:
            response = requests.post(API_URL, json=data)
            if response.status_code == 201:  # Verificar si la creación fue exitosa
                label_status.config(text=f"Datos enviados: {status}")
            else:
                label_status.config(text=f"Error: {response.status_code}")
        except Exception as e:
            label_status.config(text=f"Error al enviar datos: {e}")

    # Usar threading para enviar la petición sin bloquear la interfaz
    Thread(target=enviar_peticion).start()

# Función para manejar los eventos de teclado
def controlar_teclado(event):
    tecla = event.char.lower()
    if tecla == "w":
        enviar_datos("adelante")
    elif tecla == "s":
        enviar_datos("atras")
    elif tecla == "a":
        enviar_datos("izquierda")
    elif tecla == "d":
        enviar_datos("derecha")

# Crear la interfaz de usuario con Tkinter
app = tk.Tk()
app.title("Control de Carrito")

# Mostrar el nombre "Alejandro" en la ventana sin campo de texto
label_default_name = tk.Label(app, text="Nombre: Alejandro", font=("Arial", 12))
label_default_name.pack(pady=5)

# Crear una etiqueta para mostrar el estado
label_status = tk.Label(app, text="Selecciona una dirección para el carrito", font=("Arial", 12))
label_status.pack(pady=10)

# Crear un frame para los botones de control
frame_botones = tk.Frame(app)
frame_botones.pack()

# Crear botones de control en forma de cruz usando grid layout
btn_adelante = tk.Button(frame_botones, text="↑ Adelante",background="Red", width=10, height=2, command=lambda: enviar_datos("adelante"))
btn_adelante.grid(row=0, column=1, padx=5, pady=5)

btn_atras = tk.Button(frame_botones, text="↓ Atrás", background="Red", width=10, height=2, command=lambda: enviar_datos("atras"))
btn_atras.grid(row=2, column=1, padx=5, pady=5)

btn_izquierda = tk.Button(frame_botones, text="← Izquierda", background="#25eb1f", width=10, height=2, command=lambda: enviar_datos("izquierda"))
btn_izquierda.grid(row=1, column=0, padx=5, pady=5)

btn_derecha = tk.Button(frame_botones, text="→ Derecha", background="#25eb1f", width=10, height=2, command=lambda: enviar_datos("derecha"))
btn_derecha.grid(row=1, column=2, padx=5, pady=5)

# Etiqueta para mostrar el estado
label_status.pack(pady=5)

# Asociar los eventos de teclado a las teclas 'W', 'A', 'S', 'D'
app.bind('<Key>', controlar_teclado)

# Ejecutar la aplicación
app.mainloop()
