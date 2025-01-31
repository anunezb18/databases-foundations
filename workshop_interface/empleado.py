import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import pg8000

def limpiar_campos():
    entry_codigo.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_usuario.delete(0, tk.END)
    entry_contrasena.delete(0, tk.END)

def guardar_datos():
    codigo = entry_codigo.get()
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    if not codigo or not nombre or not apellido or not usuario or not contrasena:
        messagebox.showerror("Error", "Todos los campos deben estar llenos")
        return

    try:
        conn = pg8000.connect(
            database="taller1",
            user="postgres",
            password="Bullrock",
            host="localhost",
            port=5432
        )
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Empleado (codempleado, nomempleado, apellempleado, "user", password)
            VALUES (%s, %s, %s, %s, %s)
        ''', (codigo, nombre, apellido, usuario, contrasena))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Información", "Datos guardados correctamente")
        limpiar_campos()  
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron guardar los datos: {e}")

def buscar_usuario():
    usuario = entry_usuario.get()

    try:
        conn = pg8000.connect(
            database="taller1",
            user="postgres",
            password="Bullrock",
            host="localhost",
            port=5432
        )
        cursor = conn.cursor()
        cursor.execute('''
            SELECT codempleado, nomempleado, apellempleado, "user"
            FROM Empleado
            WHERE "user" = %s
        ''', (usuario,))
        empleado = cursor.fetchone()
        if empleado:
            entry_codigo.delete(0, tk.END)
            entry_codigo.insert(0, empleado[0])
            entry_nombre.delete(0, tk.END)
            entry_nombre.insert(0, empleado[1])
            entry_apellido.delete(0, tk.END)
            entry_apellido.insert(0, empleado[2])
            messagebox.showinfo("Información", "Usuario encontrado")
        else:
            messagebox.showinfo("Información", "Usuario no encontrado")
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo buscar el usuario: {e}")

ventana = tk.Tk()
ventana.title("Empleado")
ventana.geometry("300x400")

label_titulo = tk.Label(ventana, text="Empleado", font=("Arial", 16))
label_titulo.pack(pady=10)

frame_codigo = tk.Frame(ventana)
frame_codigo.pack(pady=5)

label_codigo = tk.Label(frame_codigo, text="Código:")
label_codigo.pack(side=tk.LEFT, padx=5)
entry_codigo = tk.Entry(frame_codigo)
entry_codigo.pack(side=tk.LEFT, padx=5)

frame_nombre = tk.Frame(ventana)
frame_nombre.pack(pady=5)

label_nombre = tk.Label(frame_nombre, text="Nombre:")
label_nombre.pack(side=tk.LEFT, padx=5)
entry_nombre = tk.Entry(frame_nombre)
entry_nombre.pack(side=tk.LEFT, padx=5)


frame_apellido = tk.Frame(ventana)
frame_apellido.pack(pady=5)

label_apellido = tk.Label(frame_apellido, text="Apellido:")
label_apellido.pack(side=tk.LEFT, padx=5)
entry_apellido = tk.Entry(frame_apellido)
entry_apellido.pack(side=tk.LEFT, padx=5)

frame_usuario = tk.Frame(ventana)
frame_usuario.pack(pady=5)

label_usuario = tk.Label(frame_usuario, text="Usuario:")
label_usuario.pack(side=tk.LEFT, padx=5)
entry_usuario = tk.Entry(frame_usuario)
entry_usuario.pack(side=tk.LEFT, padx=5)

lupa_image = PhotoImage(file="lupa.png")
lupa_image = lupa_image.subsample(2, 2)  

label_lupa = tk.Label(frame_usuario, image=lupa_image)
label_lupa.pack(side=tk.LEFT, padx=5)
label_lupa.bind("<Button-1>", lambda e: buscar_usuario())  

frame_contrasena = tk.Frame(ventana)
frame_contrasena.pack(pady=5)

label_contrasena = tk.Label(frame_contrasena, text="Contraseña:")
label_contrasena.pack(side=tk.LEFT, padx=5)
entry_contrasena = tk.Entry(frame_contrasena, show="*")
entry_contrasena.pack(side=tk.LEFT, padx=5)

boton_guardar = tk.Button(ventana, text="Guardar", command=guardar_datos)
boton_guardar.pack(pady=10)

ventana.mainloop()