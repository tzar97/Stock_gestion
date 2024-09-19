import os
import pandas as pd
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import ttkbootstrap as ttkb
import menu

def buscar_stock(criterio, output_label, tree):
    try:
        df_stock = pd.read_csv('stock.csv')
    except FileNotFoundError:
        output_label.config(text="No se encontró el archivo de stock. Por favor, cargue productos primero.", bootstyle="danger")
        return None

    df_stock['proveedor'] = df_stock['proveedor'].astype(str)
    df_stock['codigo_produ'] = df_stock['codigo_produ'].astype(str)
    df_stock['nombre_prod'] = df_stock['nombre_prod'].astype(str)
    
    # Limpiar el árbol de la tabla
    for item in tree.get_children():
        tree.delete(item)

    if criterio.strip() == "":
        output_label.config(text="Ingrese un criterio de búsqueda.", bootstyle="warning")
        return

    resultados = df_stock[
        (df_stock['proveedor'].str.contains(criterio, case=False, na='')) |
        (df_stock['codigo_produ'].str.contains(criterio, case=False, na='')) |
        (df_stock['nombre_prod'].str.contains(criterio, case=False, na=''))
    ]

    if not resultados.empty:
        output_label.config(text="Producto(s) encontrado(s):", bootstyle="info")
        
        for index, row in resultados.iterrows():
            precio_formateado = f"${row['precio']:.2f}"

            # Cargar y redimensionar la imagen
            imagen = None
            if row['foto']:
                try:
                    ruta_imagen = os.path.join('foto', row['fotos'])
                    if os.path.exists(ruta_imagen):
                        img = Image.open(ruta_imagen)
                        img.thumbnail((100, 100))  # Redimensionar la imagen
                        imagen = ImageTk.PhotoImage(img)
                    else:
                        print(f"No se encontró el archivo: {ruta_imagen}")
                except Exception as e:
                    print(f"Error al cargar imagen: {e}")
                    imagen = None
            
            tree.insert("", "end", values=(row['proveedor'], row['codigo_produ'], row['nombre_prod'], precio_formateado, ""), tags=("img",))
            
            # Establecer la imagen en la celda
            if imagen:
                tree.item(tree.get_children()[-1], image=imagen)

        # Mantener una referencia a las imágenes para evitar que sean recolectadas por el recolector de basura
        tree.images = {}

    else:
        output_label.config(text="No se encontraron productos.", bootstyle="danger")

def crear_interfaz():
    app = ttkb.Window(themename="flatly")
    app.title("Buscar Producto")
    app.geometry("1000x600")

    ttkb.Label(app, text="Buscar Producto", font=("Arial", 14)).pack(pady=10)
    
    frame_buscar = ttkb.Frame(app)
    frame_buscar.pack(pady=10)

    ttkb.Label(frame_buscar, text="Criterio de Búsqueda").grid(row=0, column=0, padx=5, pady=5)
    criterio_entry = ttkb.Entry(frame_buscar)
    criterio_entry.grid(row=0, column=1, padx=5, pady=5)

    buscar_button = ttkb.Button(frame_buscar, text="Buscar", command=lambda: buscar_stock(criterio_entry.get(), output_label, tree), bootstyle="info")
    buscar_button.grid(row=0, column=2, padx=5, pady=5)

    output_label = ttkb.Label(app, text="", font=("Arial", 10), bootstyle="info")
    output_label.pack(pady=5)

    # Crear y configurar la tabla
    columns = ('proveedor', 'codigo_produ', 'nombre_prod', 'precio', 'foto')
    tree = ttk.Treeview(app, columns=columns, show='headings')

    tree.heading('proveedor', text='Proveedor')
    tree.heading('codigo_produ', text='Código Producto')
    tree.heading('nombre_prod', text='Nombre Producto')
    tree.heading('precio', text='Precio')
    tree.heading('foto', text='Foto')

    tree.column('proveedor', anchor='center')
    tree.column('codigo_produ', anchor='center')
    tree.column('nombre_prod', anchor='center')
    tree.column('precio', anchor='center')
    tree.column('foto', anchor='center', width=100)

    tree.pack(pady=20, fill='both', expand=True)

    def volver_menu():
        app.destroy()
        menu.mostrar_menu()

    ttkb.Button(app, text="Volver al Menú Principal", command=volver_menu, bootstyle="secondary").pack(pady=10)

    app.mainloop()
