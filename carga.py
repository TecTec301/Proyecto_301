from tkinter import *
from tkinter import ttk
import time

class VentanaBase(Tk):
    def __init__(self, titulo="Ventana Base"):
        super().__init__()
        self.config(bg="#000000")
        self.geometry("600x600+400+70")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.title("StockFlow")

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor="#000000",      # canal de fondo
            bordercolor="#000000",
            background="#FFFFFF",       # color de progreso
            lightcolor="#000000",
            darkcolor="#000000",
            thickness=1                 # altura de la barra
        )
        self.progress = ttk.Progressbar(
            self,
            orient="horizontal",
            length=400,
            mode="determinate",
            maximum=100,
            style="Custom.Horizontal.TProgressbar"
        )
        

        

        Label(self, text="📦", font=("Impact", 200), fg="#605F5F", bg="#000000").pack(anchor="center")
        
        self.progress.pack(fill="x",anchor="s",expand=True)
        
        self.frame = Frame(self, bg="#0F0F0F")
        self.frame.pack(anchor="s", fill="x", side="bottom", expand=True,)
        
        self.label = Label(self.frame, text="StockFlow", font=("Impact", 30), fg="#FFFFFF", bg="#0F0F0F")
        self.label.grid(row=0, column=0, pady=10, padx=10)

        self.exit = Button(self.frame, text="Cerrar", bg="#000000", fg="#ffffff", font=("Arial", 11), command=self.destroy)
        self.exit.grid(row=0, column=1, padx=300, pady=6)

        # Llamar automáticamente a la barra de carga
        self.after(100, self.barra)

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
