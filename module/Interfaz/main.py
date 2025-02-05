import tkinter as tk
from tkinter import messagebox
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
    entry_usuario = tk.Entry(ventana_registro)
    entry_usuario.pack()
    
    tk.Label(ventana_registro, text="Clave:").pack()
    entry_contrasena = tk.Entry(ventana_registro, show="*")
    entry_contrasena.pack()
    
    def guardar_usuario():
        codigo = entry_codigo.get().strip()
        nombre = entry_nombre.get().strip()
        apellido = entry_apellido.get().strip()
        usuario = entry_usuario.get().strip()
        contrasena = entry_contrasena.get().strip()
        
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

def consultar_cliente(codigo_cliente):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cliente WHERE rutcli = %s", (codigo_cliente,))
    cliente = cursor.fetchone()
    conn.close()
    return cliente

def obtener_ultimo_numero_factura():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(noventa) FROM venta")
    ultimo_numero = cursor.fetchone()[0] or 0
    conn.close()
    return ultimo_numero + 1

def registrar_venta(numero_factura, codigo_cliente, codigo_empleado, fecha):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Venta (noventa, rutcli, codempleado, fecventa) VALUES (%s, %s, %s, %s)",
                   (numero_factura, codigo_cliente, codigo_empleado, fecha))
    conn.commit()
    conn.close()

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