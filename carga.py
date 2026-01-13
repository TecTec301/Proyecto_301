from tkinter import *
from tkinter import ttk
import time

from tkinter import *
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
from tkinter import simpledialog
from tkcalendar import DateEntry
import pandas as pd
import os
class CARGA(Tk):
    def __init__(self, titulo="Ventana Base"):
        super().__init__()

        self.config(bg="#000000")
        ancho_ventana = 600
        alto_ventana = 600
    
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()

        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        self.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.title("StockFlow")

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor="#000000",
            bordercolor="#000000",
            background="#FFFFFF",
            lightcolor="#000000",
            darkcolor="#000000",
            thickness=1
        )
        self.progress = ttk.Progressbar(
            self,
            orient="horizontal",
            length=600,
            mode="determinate",
            maximum=100,
            style="Custom.Horizontal.TProgressbar"
        )

        Label(self, text="📦", font=("Impact", 200), fg="#FFFFFF", bg="#000000").pack(anchor="center", expand=True)

        self.progress.place(y=515)

        self.frame = Frame(self, bg="#0F0F0F")
        self.frame.pack(anchor="s", fill="x", side="bottom", expand=True,)

        self.label = Label(self.frame, text="StockFlow", font=("Impact", 30), fg="#FFFFFF", bg="#0F0F0F")
        self.label.grid(row=0, column=0, pady=10, padx=10)

        self.exit = Button(self.frame, text="Cerrar", bg="#000000", fg="#ffffff", font=("Arial", 11), command=self.destroy)
        self.exit.grid(row=0, column=1, padx=300, pady=6)

        # Llamar automáticamente a la barra de carga
        self.after(300, self.barra)

    def barra(self):
        self.progress["value"] = 0
        max_value = 100
        for i in range(max_value + 1):
            self.progress["value"] = i
            self.update_idletasks()
            time.sleep(0.03)
        self.abrir_principal()

    def abrir_principal(self):
        self.destroy()  # Cierra la ventana base
        principal = Principal()
        principal.mainloop()


class Principal(Tk):
    def __init__(self):
        super().__init__()
        self.title("StockFlow - Sistema de Inventario")
        self.config(bg="#2C2C2C")
        self.overrideredirect(False)
        self.state("zoomed")


if __name__ == "__main__":
    app = VentanaBase()
    app.mainloop()

