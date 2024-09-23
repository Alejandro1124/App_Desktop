import tkinter as tk
import requests
from threading import Thread
import time

# URL de la API MockAPI
API_URL = "http://127.0.0.1:5000/cars"

# Función para obtener y mostrar los últimos 10 registros
def obtener_registros():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            registros = response.json()[-10:]  # Obtener los últimos 10 registros
            mostrar_registros(registros)
        else:
            label_status.config(text=f"Error al obtener registros: {response.status_code}")
    except Exception as e:
        label_status.config(text=f"Error al obtener registros: {e}")

# Función para mostrar los registros en el listbox
def mostrar_registros(registros):
    listbox_registros.delete(0, tk.END)  # Limpiar el contenido anterior
    encabezado = f"{'ID':<5} {'Nombre':<20} {'Status':<10} {'Fecha':<20} {'IP':<15}"
    listbox_registros.insert(tk.END, encabezado)
    listbox_registros.insert(tk.END, "-"*65)

    for registro in registros:
        fecha_formateada = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(registro['date']))
        registro_formateado = f"{registro['id']:<5} {registro['name']:<20} {registro['status']:<10} {fecha_formateada:<15} {registro['ipClient']:<15}"
        listbox_registros.insert(tk.END, registro_formateado)

# Función para refrescar los registros periódicamente
def actualizar_registros():
    while True:
        obtener_registros()
        time.sleep(1)  # Esperar 5 segundos antes de la siguiente actualización

# Crear la interfaz de usuario con Tkinter
app = tk.Tk()
app.title("Visualización de Registros")

# Etiqueta para el estado de la aplicación
label_status = tk.Label(app, text="Últimos 10 registros", font=("Arial", 18))
label_status.pack(pady=10)

# Listbox para mostrar los últimos 10 registros con formato
listbox_registros = tk.Listbox(app, font=("Courier", 10), width=100, height=15)
listbox_registros.pack(pady=5)

# Usar threading para actualizar los registros en segundo plano sin bloquear la interfaz
Thread(target=actualizar_registros, daemon=True).start()

# Ejecutar la aplicación
app.mainloop()
