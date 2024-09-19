import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
import menu
import cargar
import buscar
import modificar


def mostrar_menu():
    global app
    app = ttkb.Window(themename="flatly")
    app.title("El Gigante Stock")
    app.geometry("300x400")

    ttkb.Label(app, text="Menú Principal", font=("Arial", 16)).pack(pady=20)

    def cargar_stock():
        app.destroy()
        import cargar
        cargar.crear_interfaz()

    def buscar_stock():
        app.destroy()
        import buscar
        buscar.crear_interfaz()

    def modificar_datos():
        app.destroy()
        import modificar
        modificar.crear_interfaz()

    ttkb.Button(app, text="Cargar Producto", command=cargar_stock, bootstyle="primary").pack(pady=10)
    ttkb.Button(app, text="Buscar Producto", command=buscar_stock, bootstyle="info").pack(pady=10)
    ttkb.Button(app, text="Modificar Producto", command=modificar_datos, bootstyle="warning").pack(pady=10)

    app.mainloop()

def volver_menu():
    global app
    app.destroy()
    menu.mostrar_menu()

if __name__ == "__main__":
    mostrar_menu()
