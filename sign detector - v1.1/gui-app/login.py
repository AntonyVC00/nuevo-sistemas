import tkinter as tk
from tkinter import messagebox
import main  


USUARIO_PREDETERMINADO = "admin"
CONTRASENA_PREDETERMINADA = "1234"


def abrir_aplicacion_principal():
    ventana_login.destroy()
    main.iniciar_aplicacion()


def verificar_login():
    usuario = entry_usuario.get()
    clave = entry_contrasena.get()

    if usuario == USUARIO_PREDETERMINADO and clave == CONTRASENA_PREDETERMINADA:
        abrir_aplicacion_principal()
    else:
        messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")


def iniciar_login():
    global ventana_login, entry_usuario, entry_contrasena

    ventana_login = tk.Tk()
    ventana_login.title("Inicio de sesión")
    ventana_login.geometry("320x250")

    ventana_login.configure(bg="#2c2f33")

    tk.Label(ventana_login, text="LISIGHT - LOGIN", font=("Arial", 14, "bold"),
             bg="#2c2f33", fg="white").pack(pady=10)

    tk.Label(ventana_login, text="Usuario", bg="#2c2f33", fg="white").pack()
    entry_usuario = tk.Entry(ventana_login)
    entry_usuario.pack()

    tk.Label(ventana_login, text="Contraseña", bg="#2c2f33", fg="white").pack()
    entry_contrasena = tk.Entry(ventana_login, show="*")
    entry_contrasena.pack()

    tk.Button(ventana_login, text="Ingresar", command=verificar_login,
              bg="#27ae60", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

    ventana_login.mainloop()


if __name__ == "__main__":
    iniciar_login()
