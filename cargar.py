import pandas as pd
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
import menu

def cargar_stock(proveedor, codigo_produ, nombre_prod, precio, medida, foto, output_label):
    producto = {
        'proveedor': [proveedor],
        'codigo_produ': [codigo_produ],
        'nombre_prod': [nombre_prod],
        'precio': [precio],
        'medida': [medida],
        'foto': [foto]
    }
    df_producto = pd.DataFrame(producto)
    
    try:
        df_stock = pd.read_csv('stock.csv')
        df_stock = pd.concat([df_stock, df_producto], ignore_index=True)
    except FileNotFoundError:
        df_stock = df_producto

    df_stock.to_csv('stock.csv', index=False)
    
    output_label.config(text="Producto cargado exitosamente al stock.", bootstyle="success")

def crear_interfaz():
    app = ttkb.Window(themename="flatly")
    app.title("Cargar Producto")
    app.geometry("800x600")

    ttkb.Label(app, text="Cargar Producto", font=("Arial", 14)).pack(pady=10)
    
    frame_cargar = ttkb.Frame(app)
    frame_cargar.pack(pady=10)

    ttkb.Label(frame_cargar, text="Proveedor").grid(row=0, column=0, padx=5, pady=5)
    proveedor_entry = ttkb.Entry(frame_cargar)
    proveedor_entry.grid(row=0, column=1, padx=5, pady=5)

    ttkb.Label(frame_cargar, text="Código Producto").grid(row=1, column=0, padx=5, pady=5)
    codigo_produ_entry = ttkb.Entry(frame_cargar)
    codigo_produ_entry.grid(row=1, column=1, padx=5, pady=5)

    ttkb.Label(frame_cargar, text="Nombre Producto").grid(row=2, column=0, padx=5, pady=5)
    nombre_prod_entry = ttkb.Entry(frame_cargar)
    nombre_prod_entry.grid(row=2, column=1, padx=5, pady=5)

    ttkb.Label(frame_cargar, text="Precio").grid(row=3, column=0, padx=5, pady=5)
    precio_entry = ttkb.Entry(frame_cargar)
    precio_entry.grid(row=3, column=1, padx=5, pady=5)

    ttkb.Label(frame_cargar, text="Medida").grid(row=4, column=0, padx=5, pady=5)
    medida_entry = ttkb.Entry(frame_cargar)
    medida_entry.grid(row=4, column=1, padx=5, pady=5)

    ttkb.Label(frame_cargar, text="Foto (URL o Ruta)").grid(row=5, column=0, padx=5, pady=5)
    foto_entry = ttkb.Entry(frame_cargar)
    foto_entry.grid(row=5, column=1, padx=5, pady=5)

    output_label = ttkb.Label(app, text="", font=("Arial", 10), bootstyle="info")
    output_label.pack(pady=5)

    def cargar_producto():
        cargar_stock(
            proveedor_entry.get(), 
            codigo_produ_entry.get(), 
            nombre_prod_entry.get(), 
            precio_entry.get(), 
            medida_entry.get(), 
            foto_entry.get(), 
            output_label
        )

    ttkb.Button(app, text="Cargar", command=cargar_producto, bootstyle="success").pack(pady=10)

    def volver_menu():
        app.destroy()
        menu.mostrar_menu()

    ttkb.Button(app, text="Volver al Menú Principal", command=volver_menu, bootstyle="secondary").pack(pady=10)

    app.mainloop()
