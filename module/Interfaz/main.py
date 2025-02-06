import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from datetime import datetime

# Configuración de la base de datos
DB_HOST = "localhost"
DB_NAME = "modulo-final"
DB_USER = "postgres"
DB_PASSWORD = "Bullrock"

# Conectar a la base de datos
def conectar_bd():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        conn.set_client_encoding('UTF8')
        return conn
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
def buscar_cliente(entry_codigo, entry_cliente):
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
        entry_cliente.delete(0, tk.END)
        entry_cliente.insert(0, cliente[0])
    else:
        messagebox.showerror("Error", "Cliente no encontrado")

# Función para buscar productos
def buscar_producto(entry_producto, tabla, entry_cantidad, entry_descuento):
    nombre_busqueda = entry_producto.get().strip()
    if not nombre_busqueda:
        messagebox.showerror("Error", "Debe ingresar el nombre del producto")
        return

    # Validar cantidad y descuento
    try:
        cantidad = int(entry_cantidad.get().strip())
        descuento = float(entry_descuento.get().strip())
    except ValueError:
        messagebox.showerror("Error", "Cantidad y Descuento deben ser valores numéricos")
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
        total = "Pendiente"

        # Verificar si la cantidad es mayor al stock disponible
        if cantidad > stock:
            messagebox.showerror("Error", f"La cantidad solicitada ({cantidad}) excede el stock disponible ({stock})")
            return

        # Verificar si el producto ya existe en la tabla, para no agregarlo duplicado
        for item in tabla.get_children():
            if tabla.item(item)['values'][0] == idpro:
                messagebox.showinfo("Info", "Producto ya está en la tabla")
                return
        
        # Insertar el producto encontrado en la tabla
        tabla.insert(
            "",
            "end",
            values=(str(idpro).zfill(4), nompro, cantidad, precio, descuento, total, stock)
        )

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al buscar el producto:\n{e}")
    finally:
        conn.close()

# Función para calcular el total
def calcular_total(tabla):
    for item in tabla.get_children():
        values = tabla.item(item)['values']
        cantidad = int(values[2])
        precio = float(values[3])
        descuento = float(values[4])
        total = cantidad * precio - (descuento / 100) * precio
        tabla.set(item, column=5, value=total)

# Función para guardar los datos
def guardar_datos(entry_factura, entry_cliente_codigo, entry_empleado, entry_fecha, tabla):
    factura = entry_factura.get().strip()
    cliente_codigo = entry_cliente_codigo.get().strip()[:20]  # Ajusta el tamaño según la longitud máxima permitida
    empleado = entry_empleado.get().strip()[:10]  # Ajusta el tamaño según la longitud máxima permitida
    fecha = entry_fecha.get().strip()

    if not factura or not cliente_codigo or not empleado or not fecha:
        messagebox.showerror("Error", "Todos los campos deben estar llenos")
        return

    conn = conectar_bd()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        print(f"Factura: {factura}, Empleado: {empleado}, Cliente: {cliente_codigo}, Fecha: {fecha}")
        cursor.execute('''
            INSERT INTO venta (noventa, codempleado, rutcli, fecventa)
            VALUES (%s, %s, %s, %s)
        ''', (factura, empleado, cliente_codigo, fecha))
        conn.commit()

        item_number = 1
        for item in tabla.get_children():
            values = tabla.item(item)['values']
            idpro = str(values[0]).zfill(4)
            cantidad = int(values[2])
            precio = float(values[3])
            descuento = float(values[4]) * 100  # Multiplicar por 100 para guardar como entero
            total = round(float(values[5]), 2)  # Redondea el total a 2 decimales

            # Asegurarse de que el total no exceda el valor permitido
            if abs(total) >= 100000000:
                messagebox.showerror("Error", f"El total ({total}) excede el valor permitido")
                return

            print(f"Detalle Venta - Factura: {factura}, Item: {item_number}, ID Producto: {idpro}, Precio: {precio}, Cantidad: {cantidad}, Descuento: {descuento}, Total: {total}")

            cursor.execute('''
                INSERT INTO detalleventa (noventa, item, idpro, precio, cantidad, descuento, preciototal)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (factura, item_number, idpro, precio, cantidad, descuento, total))
            cursor.execute('''
                UPDATE producto
                SET stock = stock - %s
                WHERE idpro = %s
            ''', (cantidad, idpro))
            item_number += 1
        conn.commit()
        messagebox.showinfo("Información", "Datos guardados correctamente")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron guardar los datos: {e}")
        print(e)
    finally:
        conn.close()

# Función para abrir la ventana principal
def abrir_ventana_principal(codempleado):
    ventana_principal = tk.Tk()  # Crear la ventana principal como Tk()
    ventana_principal.title("Factura")
    ventana_principal.geometry("600x400")

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
    entry_cliente = tk.Entry(marco, width=20)
    entry_cliente.grid(row=0, column=4, padx=5, pady=2)
    btn_buscar_cliente = tk.Button(marco, text="🔍", width=2, command=lambda: buscar_cliente(entry_cliente_codigo, entry_cliente))
    btn_buscar_cliente.grid(row=0, column=5, padx=5, pady=2)

    # Segunda fila
    tk.Label(marco, text="Empleado").grid(row=1, column=0, padx=5, pady=2, sticky="w")
    entry_empleado = tk.Entry(marco, width=20)
    entry_empleado.grid(row=1, column=1, columnspan=2, padx=5, pady=2)
    entry_empleado.insert(0, codempleado)  # Insertar el código del empleado

    tk.Label(marco, text="Fecha").grid(row=1, column=2, padx=5, pady=2, sticky="w")
    entry_fecha = tk.Entry(marco, width=15)
    entry_fecha.grid(row=1, column=3, padx=5, pady=2)
    cargar_fecha_actual(entry_fecha)

    # Tercera fila: Producto
    tk.Label(marco, text="Producto").grid(row=2, column=0, padx=5, pady=2, sticky="w")
    entry_producto = tk.Entry(marco, width=15)
    entry_producto.grid(row=2, column=1, padx=5, pady=2)
    btn_buscar_producto = tk.Button(marco, text="🔍", width=2, command=lambda: buscar_producto(entry_producto, tabla, entry_cantidad, entry_descuento))
    btn_buscar_producto.grid(row=2, column=2, padx=5, pady=2)

    # Campos de entrada para cantidad y descuento
    tk.Label(marco, text="Cantidad").grid(row=2, column=3, padx=5, pady=2, sticky="w")
    entry_cantidad = tk.Entry(marco, width=10)
    entry_cantidad.grid(row=2, column=4, padx=5, pady=2)

    tk.Label(marco, text="Descuento (%)").grid(row=2, column=5, padx=5, pady=2, sticky="w")
    entry_descuento = tk.Entry(marco, width=10)
    entry_descuento.grid(row=2, column=6, padx=5, pady=2)

    # Tabla
    columnas = ["idpro", "producto", "Cantidad", "Precio", "Descuento", "Total", "stock"]
    tabla = ttk.Treeview(marco, columns=columnas, show="headings", height=5)

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=60, anchor="center")

    tabla.grid(row=3, column=0, columnspan=7, padx=5, pady=5)

    # Botón Calcular Total
    btn_calcular_total = tk.Button(marco, text="Calcular Total", command=lambda: calcular_total(tabla))
    btn_calcular_total.grid(row=4, column=0, columnspan=7, pady=5)

    # Botón Guardar
    btn_guardar = tk.Button(marco, text="Guardar", command=lambda: guardar_datos(entry_factura, entry_cliente_codigo, entry_empleado, entry_fecha, tabla))
    btn_guardar.grid(row=5, column=0, columnspan=7, pady=5)

    ventana_principal.mainloop()

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
        codigo = entry_codigo.get().strip()[:10]  # Ajusta el tamaño según la longitud máxima permitida
        nombre = entry_nombre.get().strip()[:50]  # Ajusta el tamaño según la longitud máxima permitida
        apellido = entry_apellido.get().strip()[:50]  # Ajusta el tamaño según la longitud máxima permitida
        usuario = entry_usuario_reg.get().strip()[:20]  # Ajusta el tamaño según la longitud máxima permitida
        contrasena = entry_contrasena_reg.get().strip()[:20]  # Ajusta el tamaño según la longitud máxima permitida

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
            print(e)
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