import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from datetime import datetime

# Configuración de la base de datos
DB_HOST = "localhost"
DB_NAME = "Modulo"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

# Conectar a la base de datos
def conectar_bd():
    try:
        return psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
    except Exception as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {e}")
        return None

# Función para obtener el nombre del empleado y mostrarlo en la celda correspondiente
def cargar_nombre_empleado(codempleado, entry_empleado):
    conn = conectar_bd()
    if conn is None:
        return
    
    cursor = conn.cursor()
    cursor.execute("SELECT nomempleado FROM empleado WHERE codempleado = %s", (codempleado,))
    empleado = cursor.fetchone()
    conn.close()
    
    if empleado:
        entry_empleado.insert(0, empleado[0])

# Función para obtener la fecha del sistema y mostrarla en la celda correspondiente
def cargar_fecha_actual(entry_fecha):
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    entry_fecha.insert(0, fecha_actual)

# Función para obtener el número de factura y mostrarlo en la celda correspondiente
def obtener_numero_factura(entry_factura):
    conn = conectar_bd()
    if conn is None:
        return
    
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(noventa) FROM venta")
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado and resultado[0] is not None:
        nuevo_numero = resultado[0] + 1
    else:
        nuevo_numero = 1
    
    entry_factura.insert(0, str(nuevo_numero))

# Función para buscar el nombre del cliente y reemplazar el código en la misma celda
def buscar_cliente(entry_codigo):
    codigo_cliente = entry_codigo.get().strip()
    
    if not codigo_cliente:
        messagebox.showerror("Error", "Debe ingresar un código de cliente")
        return
    
    conn = conectar_bd()
    if conn is None:
        return
    
    cursor = conn.cursor()
    cursor.execute("SELECT nomcli FROM cliente WHERE rutcli = %s", (codigo_cliente,))
    cliente = cursor.fetchone()
    conn.close()
    
    if cliente:
        entry_codigo.delete(0, tk.END)
        entry_codigo.insert(0, cliente[0])  # Reemplazar el código con el nombre del cliente
    else:
        messagebox.showerror("Error", "Cliente no encontrado")

# -------------------------
# Función para buscar productos
def buscar_producto(entry_producto, tabla):
    nombre_busqueda = entry_producto.get().strip()
    if not nombre_busqueda:
        messagebox.showerror("Error", "Debe ingresar el nombre del producto")
        return

    conn = conectar_bd()  
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        query_producto = """
            SELECT idpro, nompro, stock 
            FROM producto 
            WHERE nompro ILIKE %s
        """
        cursor.execute(query_producto, (f"%{nombre_busqueda}%",))
        producto = cursor.fetchone()
        
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado")
            return

        idpro, nompro, stock = producto
        query_precio = """
            SELECT valorprecio 
            FROM precio 
            WHERE idpro = %s 
            ORDER BY fechaprecio DESC 
            LIMIT 1
        """
        cursor.execute(query_precio, (idpro,))
        precio_reg = cursor.fetchone()
        if not precio_reg:
            messagebox.showerror("Error", "No se encontró precio para el producto")
            return

        precio = precio_reg[0]

        # Valores por defecto
        cantidad = 1
        descuento = 0     
        total = "Pendiente"  # Aquí puedes cambiar a un cálculo real de Total si lo necesitas

        # Verificar si el producto ya existe en la tabla, para no agregarlo duplicado
        for item in tabla.get_children():
            if tabla.item(item)['values'][0] == idpro:
                messagebox.showinfo("Info", "Producto ya está en la tabla")
                return
        
        # Insertar el producto encontrado en la tabla
        tabla.insert(
            "",
            "end",
            values=(idpro, nompro, cantidad, precio, descuento, total, stock)
        )

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al buscar el producto:\n{e}")
    finally:
        conn.close()

def configurar_edicion_tabla(tabla, parent):
    def on_double_click(event):
        # Identificar la región, fila y columna en la que se hizo clic
        region = tabla.identify("region", event.x, event.y)
        if region != "cell":
            return
        columna = tabla.identify_column(event.x)
        fila = tabla.identify_row(event.y)
        
        if not fila:
            return

        # Obtener la posición y tamaño de la celda
        x, y, width, height = tabla.bbox(fila, columna)
        # Valor actual de la celda
        valor_actual = tabla.set(fila, columna)

        # Crear un Entry para editar el valor y posicionarlo sobre la celda
        entry_edit = tk.Entry(parent)
        entry_edit.place(x=x, y=y, width=width, height=height)
        entry_edit.insert(0, valor_actual)
        entry_edit.focus_set()

        def guardar_edicion(event):
            nuevo_valor = entry_edit.get().strip()
            # Actualizar el valor de la celda
            tabla.set(fila, columna, nuevo_valor)
            # Lógica para guardar el cambio, si es necesario en la base de datos
            entry_edit.destroy()

        entry_edit.bind("<Return>", guardar_edicion)
        entry_edit.bind("<FocusOut>", guardar_edicion)

    tabla.bind("<Double-1>", on_double_click)

# -------------------------
# Función para abrir la ventana principal
def abrir_ventana_principal(codempleado):
    ventana_principal = tk.Toplevel()
    ventana_principal.title("Factura")
    ventana_principal.geometry("450x300")

    marco = tk.Frame(ventana_principal, bd=2, relief="solid")
    marco.pack(padx=5, pady=5, fill="both", expand=True)

    # Primera fila
    tk.Label(marco, text="No. Factura", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=2, sticky="w")
    entry_factura = tk.Entry(marco, width=10)
    entry_factura.grid(row=0, column=1, padx=5, pady=2)
    obtener_numero_factura(entry_factura)

    tk.Label(marco, text="Cliente").grid(row=0, column=2, padx=5, pady=2, sticky="w")
    entry_cliente_codigo = tk.Entry(marco, width=10)
    entry_cliente_codigo.grid(row=0, column=3, padx=5, pady=2)

    btn_buscar_cliente = tk.Button(marco, text="🔍", width=2, command=lambda: buscar_cliente(entry_cliente_codigo))
    btn_buscar_cliente.grid(row=0, column=4, padx=5, pady=2)

    # Segunda fila
    tk.Label(marco, text="Empleado").grid(row=1, column=0, padx=5, pady=2, sticky="w")
    entry_empleado = tk.Entry(marco, width=20)
    entry_empleado.grid(row=1, column=1, columnspan=2, padx=5, pady=2)
    cargar_nombre_empleado(codempleado, entry_empleado)

    tk.Label(marco, text="Fecha").grid(row=1, column=2, padx=5, pady=2, sticky="w")
    entry_fecha = tk.Entry(marco, width=15)
    entry_fecha.grid(row=1, column=3, padx=5, pady=2)
    cargar_fecha_actual(entry_fecha)

    # Tercera fila: Producto
    tk.Label(marco, text="Producto").grid(row=2, column=0, padx=5, pady=2, sticky="w")
    entry_producto = tk.Entry(marco, width=15)
    entry_producto.grid(row=2, column=1, padx=5, pady=2)
    btn_buscar_producto = tk.Button(marco, text="🔍", width=2, 
                                    command=lambda: buscar_producto(entry_producto, tabla))
    btn_buscar_producto.grid(row=2, column=2, padx=5, pady=2)

    # Tabla
    # Se agrega una columna extra "stock" para almacenar el stock (oculto al usuario)
    columnas = ["item", "producto", "Cantidad", "Precio", "Descuento", "Total", "stock"]
    tabla = ttk.Treeview(marco, columns=columnas, show="headings", height=5)

    for col in columnas:
        # Configurar la cabecera
        if col == "stock":
            # Columna oculta: sin cabecera y ancho cero
            tabla.heading(col, text="")
            tabla.column(col, width=0, minwidth=0, stretch=False)
        else:
            tabla.heading(col, text=col)
            tabla.column(col, width=60, anchor="center")

    tabla.grid(row=4, column=0, columnspan=6, padx=5, pady=5)

    # (Opcional) Agregar filas vacías iniciales
    for _ in range(5):
        valores = ["" for _ in columnas]
        tabla.insert("", "end", values=valores)

    # Configurar la edición directa en las columnas "Cantidad" y "Descuento"
    configurar_edicion_tabla(tabla, marco)

    # Botón Guardar
    tk.Button(ventana_principal, text="Guardar").pack(pady=5)

# Función para el login
def login():
    usuario = entry_usuario.get().strip()
    contrasena = entry_contrasena.get().strip()

    if not usuario or not contrasena:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    conn = conectar_bd()
    if conn is None:
        return

    cursor = conn.cursor()
    cursor.execute("SELECT codempleado, nomempleado FROM empleado WHERE usuario=%s AND contrasena=%s", (usuario, contrasena))
    empleado = cursor.fetchone()
    conn.close()

    if empleado:
        messagebox.showinfo("Login exitoso", f"Bienvenido {empleado[1]}")
        ventana_login.destroy()
        abrir_ventana_principal(empleado[0])
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# Función para registrar empleados
def registrar():
    ventana_registro = tk.Toplevel()
    ventana_registro.title("Registro de Empleado")

    tk.Label(ventana_registro, text="Código de Empleado:").pack()
    entry_codigo = tk.Entry(ventana_registro)
    entry_codigo.pack()

    tk.Label(ventana_registro, text="Nombre:").pack()
    entry_nombre = tk.Entry(ventana_registro)
    entry_nombre.pack()

    tk.Label(ventana_registro, text="Apellido:").pack()
    entry_apellido = tk.Entry(ventana_registro)
    entry_apellido.pack()

    tk.Label(ventana_registro, text="Usuario:").pack()
    entry_usuario_reg = tk.Entry(ventana_registro)
    entry_usuario_reg.pack()

    tk.Label(ventana_registro, text="Clave:").pack()
    entry_contrasena_reg = tk.Entry(ventana_registro, show="*")
    entry_contrasena_reg.pack()

    def guardar_usuario():
        codigo = entry_codigo.get().strip()
        nombre = entry_nombre.get().strip()
        apellido = entry_apellido.get().strip()
        usuario = entry_usuario_reg.get().strip()
        contrasena = entry_contrasena_reg.get().strip()

        if not codigo or not nombre or not apellido or not usuario or not contrasena:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        conn = conectar_bd()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO empleado (codempleado, nomempleado, apellempleado, usuario, contrasena) VALUES (%s, %s, %s, %s, %s)",
                           (codigo, nombre, apellido, usuario, contrasena))
            conn.commit()
            messagebox.showinfo("Registro", "Usuario registrado exitosamente")
            ventana_registro.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el usuario: {e}")
        finally:
            conn.close()

    tk.Button(ventana_registro, text="Registrar", command=guardar_usuario).pack()

# Ventana de login
ventana_login = tk.Tk()
ventana_login.title("Login de Empleado")

tk.Label(ventana_login, text="Usuario:").pack()
entry_usuario = tk.Entry(ventana_login)
entry_usuario.pack()

tk.Label(ventana_login, text="Clave:").pack()
entry_contrasena = tk.Entry(ventana_login, show="*")
entry_contrasena.pack()

tk.Button(ventana_login, text="Iniciar sesión", command=login).pack()
tk.Button(ventana_login, text="Registrar", command=registrar).pack()

ventana_login.mainloop()