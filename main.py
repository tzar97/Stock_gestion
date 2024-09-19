"""
import pandas as pd
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb

def cargar_stock(codigo_warnes, codigo_produ, nombre_prod, precio, output_label):
    producto = {
        'codigo_warnes': [codigo_warnes],
        'codigo_produ': [codigo_produ],
        'nombre_prod': [nombre_prod],
        'precio': [precio]
    }
    df_producto = pd.DataFrame(producto)
    
    try:
        df_stock = pd.read_csv('stock.csv')
        df_stock = pd.concat([df_stock, df_producto], ignore_index=True)
    except FileNotFoundError:
        df_stock = df_producto

    df_stock.to_csv('stock.csv', index=False)
    
    output_label.config(text="Producto cargado exitosamente al stock.", bootstyle="success")

def buscar_stock(criterio, output_label, tree):
    try:
        df_stock = pd.read_csv('stock.csv')
    except FileNotFoundError:
        output_label.config(text="No se encontró el archivo de stock. Por favor, cargue productos primero.", bootstyle="danger")
        return None

    df_stock['codigo_warnes'] = df_stock['codigo_warnes'].astype(str)
    df_stock['codigo_produ'] = df_stock['codigo_produ'].astype(str)
    df_stock['nombre_prod'] = df_stock['nombre_prod'].astype(str)
    
    # Limpiar el árbol de la tabla
    for item in tree.get_children():
        tree.delete(item)

    # Mostrar resultados en la tabla
    if not df_stock.empty:
        output_label.config(text="Producto(s) encontrado(s):", bootstyle="info")
        
        for index, row in df_stock.iterrows():
            # Formatear el precio con el símbolo de dólar
            precio_formateado = f"${row['precio']}"  # Solo se agrega el símbolo $
            tree.insert("", "end", values=(row['codigo_warnes'], row['codigo_produ'], row['nombre_prod'], precio_formateado))
    else:
        output_label.config(text="No se encontraron productos.", bootstyle="danger")

def crear_interfaz():
    app = ttkb.Window(themename="flatly")
    app.title("Gestión de Stock")
    app.geometry("800x600")

    # Cargar Stock
    ttkb.Label(app, text="Cargar Producto", font=("Arial", 14)).pack(pady=10)
    
    frame_cargar = ttkb.Frame(app)
    frame_cargar.pack(pady=10)

    ttkb.Label(frame_cargar, text="Código Warnes").grid(row=0, column=0, padx=5, pady=5)
    codigo_warnes_entry = ttkb.Entry(frame_cargar)
    codigo_warnes_entry.grid(row=0, column=1, padx=5, pady=5)

    ttkb.Label(frame_cargar, text="Código Producto").grid(row=1, column=0, padx=5, pady=5)
    codigo_produ_entry = ttkb.Entry(frame_cargar)
    codigo_produ_entry.grid(row=1, column=1, padx=5, pady=5)

    ttkb.Label(frame_cargar, text="Nombre Producto").grid(row=2, column=0, padx=5, pady=5)
    nombre_prod_entry = ttkb.Entry(frame_cargar)
    nombre_prod_entry.grid(row=2, column=1, padx=5, pady=5)

    ttkb.Label(frame_cargar, text="Precio").grid(row=3, column=0, padx=5, pady=5)
    precio_entry = ttkb.Entry(frame_cargar)
    precio_entry.grid(row=3, column=1, padx=5, pady=5)

    output_label = ttkb.Label(app, text="", font=("Arial", 10), bootstyle="info")
    output_label.pack(pady=5)

    def cargar_producto():
        cargar_stock(codigo_warnes_entry.get(), codigo_produ_entry.get(), nombre_prod_entry.get(), precio_entry.get(), output_label)

    ttkb.Button(app, text="Cargar", command=cargar_producto, bootstyle="success").pack(pady=10)

    # Buscar Stock
    ttkb.Label(app, text="Buscar Producto", font=("Arial", 14)).pack(pady=10)
    
    frame_buscar = ttkb.Frame(app)
    frame_buscar.pack(pady=10)

    ttkb.Label(frame_buscar, text="Criterio de Búsqueda").grid(row=0, column=0, padx=5, pady=5)
    criterio_entry = ttkb.Entry(frame_buscar)
    criterio_entry.grid(row=0, column=1, padx=5, pady=5)

    def buscar_producto():
        buscar_stock(criterio_entry.get(), output_label, tree)

    ttkb.Button(app, text="Buscar", command=buscar_producto, bootstyle="info").pack(pady=10)

    # Crear y configurar la tabla
    columns = ('codigo_warnes', 'codigo_produ', 'nombre_prod', 'precio')
    tree = ttk.Treeview(app, columns=columns, show='headings')

    tree.heading('codigo_warnes', text='Código Warnes')
    tree.heading('codigo_produ', text='Código Producto')
    tree.heading('nombre_prod', text='Nombre Producto')
    tree.heading('precio', text='Precio')

    # Definir el estilo
    style = ttk.Style()
    style.configure("Treeview",
                    font=("Arial", 12))  # Tamaño de fuente para el contenido
    style.configure("Treeview.Heading",
                    font=("Arial", 12, "bold"))  # Tamaño de fuente y negrita para los encabezados

    tree.column('codigo_warnes', anchor='center')
    tree.column('codigo_produ', anchor='center')
    tree.column('nombre_prod', anchor='center')
    tree.column('precio', anchor='center')

    tree.pack(pady=20, fill='both', expand=True)

    # Ejecutar la aplicación
    app.mainloop()

crear_interfaz()
"""