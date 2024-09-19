import pandas as pd
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
import menu

def buscar_y_mostrar(criterio, tree, output_label):
    try:
        df_stock = pd.read_csv('stock.csv')
    except FileNotFoundError:
        output_label.config(text="No se encontró el archivo de stock. Cargue productos primero.", bootstyle="danger")
        return

    df_stock['proveedor'] = df_stock['proveedor'].astype(str)
    df_stock['codigo_produ'] = df_stock['codigo_produ'].astype(str)
    df_stock['nombre_prod'] = df_stock['nombre_prod'].astype(str)

    # Filtrar productos según el criterio de búsqueda (contiene)
    resultados = df_stock[df_stock['proveedor'].str.contains(criterio, case=False) | 
                          df_stock['codigo_produ'].str.contains(criterio, case=False) | 
                          df_stock['nombre_prod'].str.contains(criterio, case=False)]

    # Limpiar la tabla antes de mostrar nuevos resultados
    for item in tree.get_children():
        tree.delete(item)

    if not resultados.empty:
        for _, row in resultados.iterrows():
            tree.insert("", "end", values=(row['proveedor'], row['codigo_produ'], row['nombre_prod'], row['precio']))
        output_label.config(text="Selecciona un producto para modificar.", bootstyle="info")
    else:
        output_label.config(text="No se encontraron productos con el criterio dado.", bootstyle="danger")

def modificar_producto(tree, nuevo_proveedor, nuevo_codigo_produ, nuevo_nombre_prod, nuevo_precio, output_label):
    seleccion = tree.selection()

    if not seleccion:
        output_label.config(text="Por favor, selecciona un producto para modificar.", bootstyle="danger")
        return

    # Obtener el producto seleccionado
    item = tree.item(seleccion[0])
    valores = item['values']

    # Cargar el CSV
    df_stock = pd.read_csv('stock.csv')

    # Buscar el índice del producto seleccionado en el DataFrame
    index = df_stock[(df_stock['proveedor'].astype(str) == str(valores[0])) &
                     (df_stock['codigo_produ'].astype(str) == str(valores[1])) &
                     (df_stock['nombre_prod'].astype(str) == str(valores[2]))].index

    if not index.empty:
        # Actualizar solo los campos que no estén vacíos
        if nuevo_proveedor:
            df_stock.at[index[0], 'proveedor'] = nuevo_proveedor
        if nuevo_codigo_produ:
            df_stock.at[index[0], 'codigo_produ'] = nuevo_codigo_produ
        if nuevo_nombre_prod:
            df_stock.at[index[0], 'nombre_prod'] = nuevo_nombre_prod
        if nuevo_precio:
            try:
                df_stock.at[index[0], 'precio'] = float(nuevo_precio)
            except ValueError:
                output_label.config(text="El precio debe ser un número válido.", bootstyle="danger")
                return

        # Guardar cambios en el CSV
        df_stock.to_csv('stock.csv', index=False)
        output_label.config(text="Producto modificado exitosamente.", bootstyle="success")
        
        # Actualizar la tabla
        buscar_y_mostrar(valores[2], tree, output_label)
    else:
        output_label.config(text="Error al modificar el producto.", bootstyle="danger")

def crear_interfaz():
    app = ttkb.Window(themename="flatly")
    app.title("Modificar Producto")
    app.geometry("800x800")

    ttkb.Label(app, text="Modificar Producto", font=("Arial", 14)).pack(pady=10)
    
    frame_buscar = ttkb.Frame(app)
    frame_buscar.pack(pady=10)

    ttkb.Label(frame_buscar, text="Criterio de Búsqueda (Proveedor, Código Producto o Nombre)").grid(row=0, column=0, padx=5, pady=5)
    criterio_entry = ttkb.Entry(frame_buscar)
    criterio_entry.grid(row=0, column=1, padx=5, pady=5)

    # Mover el botón de búsqueda al lado derecho del campo de entrada
    ttkb.Button(frame_buscar, text="Buscar", command=lambda: buscar_y_mostrar(criterio_entry.get(), tree, output_label), bootstyle="info").grid(row=0, column=2, padx=5, pady=5)

    output_label = ttkb.Label(app, text="", font=("Arial", 10), bootstyle="info")
    output_label.pack(pady=5)

    columns = ('proveedor', 'codigo_produ', 'nombre_prod', 'precio')
    tree = ttk.Treeview(app, columns=columns, show='headings')
    tree.heading('proveedor', text='Proveedor')
    tree.heading('codigo_produ', text='Código Producto')
    tree.heading('nombre_prod', text='Nombre Producto')
    tree.heading('precio', text='Precio')

    tree.column('proveedor', anchor='center')
    tree.column('codigo_produ', anchor='center')
    tree.column('nombre_prod', anchor='center')
    tree.column('precio', anchor='center')

    tree.pack(pady=10, fill='both', expand=True)

    frame_modificar = ttkb.Frame(app)
    frame_modificar.pack(pady=10)

    ttkb.Label(frame_modificar, text="Nuevo Proveedor (Opcional)").grid(row=0, column=0, padx=5, pady=5)
    nuevo_proveedor_entry = ttkb.Entry(frame_modificar)
    nuevo_proveedor_entry.grid(row=0, column=1, padx=5, pady=5)

    ttkb.Label(frame_modificar, text="Nuevo Código Producto (Opcional)").grid(row=1, column=0, padx=5, pady=5)
    nuevo_codigo_produ_entry = ttkb.Entry(frame_modificar)
    nuevo_codigo_produ_entry.grid(row=1, column=1, padx=5, pady=5)

    ttkb.Label(frame_modificar, text="Nuevo Nombre Producto (Opcional)").grid(row=2, column=0, padx=5, pady=5)
    nuevo_nombre_prod_entry = ttkb.Entry(frame_modificar)
    nuevo_nombre_prod_entry.grid(row=2, column=1, padx=5, pady=5)

    ttkb.Label(frame_modificar, text="Nuevo Precio (Opcional)").grid(row=3, column=0, padx=5, pady=5)
    nuevo_precio_entry = ttkb.Entry(frame_modificar)
    nuevo_precio_entry.grid(row=3, column=1, padx=5, pady=5)

    ttkb.Button(app, text="Modificar Producto", 
                command=lambda: modificar_producto(tree, 
                                                   nuevo_proveedor_entry.get(), 
                                                   nuevo_codigo_produ_entry.get(), 
                                                   nuevo_nombre_prod_entry.get(), 
                                                   nuevo_precio_entry.get(), 
                                                   output_label), 
                bootstyle="warning").pack(pady=10)

    def volver_menu():
        app.destroy()
        menu.mostrar_menu()

    ttkb.Button(app, text="Volver al Menú Principal", command=volver_menu, bootstyle="secondary").pack(pady=10)

    app.mainloop()
