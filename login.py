# login.py

import tkinter as tk
from tkinter import messagebox
from config import ROLES_NOMBRES
from database import validar_credenciales


class VentanaLogin:

  def __init__(self, ventana_raiz):
    # Configuración de la ventana emergente de inicio de sesión
    self.ventana_raiz = ventana_raiz
    self.ventana_raiz.title("Inicio de Sesión - Sistema de Gestión")
    self.ventana_raiz.geometry("320x220")
    self.ventana_raiz.resizable(False, False)

    self.usuario_validado = None

    # Título de la interfaz
    tk.Label(
        self.ventana_raiz,
        text="Acceso al Sistema",
        font=("Arial", 12, "bold"),
    ).pack(pady=10)

    # Campo de texto para el Usuario
    frame_usr = tk.Frame(self.ventana_raiz)
    frame_usr.pack(pady=5)
    tk.Label(frame_usr, text="Usuario:    ", width=10, anchor="e").pack(
        side="left"
    )
    self.txt_usuario = tk.Entry(frame_usr, width=20)
    self.txt_usuario.pack(side="left")
    self.txt_usuario.focus()

    # Campo de texto para la Contraseña
    frame_pass = tk.Frame(self.ventana_raiz)
    frame_pass.pack(pady=5)
    tk.Label(frame_pass, text="Contraseña:", width=10, anchor="e").pack(
        side="left"
    )
    self.txt_contrasena = tk.Entry(frame_pass, width=20, show="*")
    self.txt_contrasena.pack(side="left")

    # Botón para Ingresar
    tk.Button(
        self.ventana_raiz,
        text="Ingresar",
        command=self.autenticar,
        width=15,
        bg="#007ACC",
        fg="white",
    ).pack(pady=15)

    # Permite presionar Enter en el teclado para accionar el botón Ingresar
    self.ventana_raiz.bind("<Return>", lambda event: self.autenticar())

  def autenticar(self):
    usr = self.txt_usuario.get().strip()
    pas = self.txt_contrasena.get().strip()

    # Validar que los campos no estén vacíos
    if not usr or not pas:
      messagebox.showerror(
          "Campos Incompletos",
          "Por favor ingrese usuario y contraseña.",
          parent=self.ventana_raiz,
      )
      return

    # Consultar a la base de datos si las credenciales son válidas
    datos_usuario = validar_credenciales(usr, pas)

    if datos_usuario:
      self.usuario_validado = datos_usuario
      rol_tecnico = datos_usuario["rol"]
      nombre_rol = ROLES_NOMBRES.get(rol_tecnico, rol_tecnico)

      messagebox.showinfo(
          "Bienvenido",
          f"Acceso concedido como: {nombre_rol}",
          parent=self.ventana_raiz,
      )

      # Cierra la ventana de login para dar paso a la pantalla principal
      self.ventana_raiz.destroy()
    else:
      # Si falla la validación, muestra el mensaje de error por pantalla
      messagebox.showerror(
          "Acceso Denegado",
          "Usuario o contraseña incorrectos.",
          parent=self.ventana_raiz,
      )