from tkinter import *
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
from tkinter import simpledialog
from tkcalendar import DateEntry
import pandas as pd
import os
import matplotlib.pyplot as plt

class CARGA(Tk):
    def __init__(self, titulo="Ventana Base"):
        super().__init__()

        self.config(bg="#000000")
        ancho_ventana = 500
        alto_ventana = 500
    
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

        self.progress.place(y=417)

        self.frame = Frame(self, bg="#0F0F0F")
        self.frame.pack(anchor="s", fill="x", side="bottom", expand=True,)

        self.label = Label(self.frame, text="StockFlow", font=("Impact", 30), fg="#FFFFFF", bg="#0F0F0F")
        self.label.grid(row=0, column=0, pady=10, padx=10)

        self.exit = Button(self.frame, text="Cerrar", bg="#000000", fg="#ffffff", font=("Arial", 11), command=self.destroy)
        self.exit.grid(row=0, column=1, padx=200, pady=6)

        # Llamar automáticamente a la barra de carga
        self.after(300, self.barra)

    def barra(self, i=0):
        max_value = 100
        if i <= max_value:
            self.progress["value"] = i
            self.after(1000, self.barra, i + 40)
        else:
            self.Abrir_Login()


    def Abrir_Login(self):
        self.destroy()  # Cierra la ventana base
        principal = Principal()
        principal.mainloop()

class Login(Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Login")
        self.geometry("400x500")
        self.config(bg="#000000")

        # Centrar ventana en pantalla
        self.update_idletasks()
        w = 400
        h = 500
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

        Label(self, text="STOCKFLOW", bg="#000000", fg="#ffffff", font=("Impact", 30)).pack(side="top")
        Label(self, text="🔒", bg="#000000", fg="#ffffff", font=("Impact", 80)).pack(anchor="center")
        self.lf = Frame(self, bg="#000000")
        self.lf.pack(anchor="center", pady=20)
        Label(self.lf, text="👤", bg="#303030", fg="#FFFFFF", font=("Arial", 18)).grid(row=0, column=0, pady=10)
        self.user = Entry(self.lf, bg="#303030", font=(16), fg="#ffffff")
        self.user.grid(row=0, column=1, pady=10)
        Label(self.lf, text="🔒", bg="#303030", fg="#FFFFFF", font=("Arial", 18)).grid(row=2, column=0, pady=10)
        self.password = Entry(self.lf, bg="#303030", font=(16), show="*", fg="#ffffff")
        self.password.grid(row=2, column=1, pady=10)
        self.lf2 = Frame(self, bg="#000000")
        self.lf2.pack(anchor="center", pady=20)
        self.lpws = Label(self.lf2, text="¿Olvidaste tu contraseña?", bg="#000000", fg="#FFFFFF", font=("Arial", 10))
        self.lpws.grid(row=0, column=0,padx=10)
        self.lpws.bind("<Button-1>", lambda e: messagebox.showinfo("Recuperar contraseña", "Contacta al administrador del sistema\nig: @ng_el.am\nTel: 5621852696"))
        self.pwslook = Button(self.lf2, text="Mostrar contraseña", bg="#000000", fg="#FFFFFF", font=("Arial", 10))
        self.pwslook.grid(row=0, column=1)
        self.pwslook.bind("<ButtonPress>", self.mostrar_password)
        self.pwslook.bind("<ButtonRelease>", self.ocultar_password)
        Button(self, text="LOGIN", bg="#ffffff", fg="#000000", font=("Arial", 12), width=30, command=self.verificar_usuario).pack(pady=20)

    def mostrar_password(self, event=None):
        self.password.config(show="")

    def ocultar_password(self, event=None):
        self.password.config(show="*")

    def abrir_principal(self):
        self.destroy()
        ventanaP = Principal()
        ventanaP.mainloop()

    def conectar(self):
        try:
            self.conexion1 = mysql.connector.connect(host="localhost",
                                                user="root",
                                                passwd="",
                                                database="INVENTARIO")
            print("Conexión correcta")
        except (mysql.connector.Error) as e:
            print("Ocurrióun error al conectar: ", e)
        return self.conexion1

    def verificar_usuario(self):
        con = self.conectar()
        cursor = con.cursor()
        usuario = self.user.get()
        contraseña = self.password.get()
        try:
            cursor.execute("""SELECT * FROM users 
                        WHERE username=%s 
                        AND password=%s""", 
                        (usuario, contraseña))
            if cursor.fetchone():
                messagebox.showinfo("Login", f"Bienvenido: {usuario}")
                self.abrir_principal()
                return True
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")
                return False
        except Exception as e:
            messagebox.showerror("Error en la base de datos", str(e))
            return False
        finally:
            con.close()

class Principal(Tk):
    def __init__(self):
        super().__init__()
        self.title("StockFlow - Sistema de Inventario")
        self.config(bg="#2C2C2C")
        self.overrideredirect(False)
        self.state("zoomed")

        self.marco1=Frame(self,bg="#000000",width=200,height=800)
        self.marco1.pack(side="left",fill="both")
        self.marco2=Frame(self,bg="#888888",width=300,height=300)
        self.marco2.pack(expand=True,fill="both")
        et1=Label(self.marco1,text="STOCKFLOW",bg="#000000",fg="#ffffff",font=("Impact",30))
        et1.grid(row=0,column=0,padx=40,pady=10)
        self.b_pro=Button(self.marco1,text="INVENTARIO",font=("Impact",12),width=20,bg="#ffffff",activebackground="#ffffff",command=self.view_inventario)
        self.b_pro.grid(row=1,column=0,padx=10,pady=40)
        self.b_inv=Button(self.marco1,text="GRAFICA",font=("Impact",12),width=20,bg="#ffffff",activebackground="#ffffff",command=self.grafica)
        self.b_inv.grid(row=2,column=0,padx=10,pady=40)
        logout=Button(self.marco1,text="Logout",bg="#ffffff",width=20,height=2,font=("Impact",10),command=self.abrir_login)
        logout.grid(row=3,column=0,pady=30,padx=10)
        Label(self.marco1,text="Dulceria Jireth©\n San Mateo Tequixquiac Edo.Mex",bg="#000000",fg="#ffffff",font=("Arial",12)).grid(row=4,column=0,pady=180,padx=10)
        Label(self.marco2,text="Bienvenido a StockFlow",bg="#888888",fg="#000000",font=("Impact",30)).pack()
        Label(self.marco2,text="Inventory software for a candy store: Jireth Candy Store,located in San Mateo Tequixquiac, State of Mexico.\nThe software comes with two applications.The first manages\nthe entire candy store's inventory using \nbatches, dates, and product codes.The second application is a point-of-sale system \nwhere you can record purchases at the candy store.",bg="#888888",fg="#000000",font=("Arial",15)).pack(pady=20)

    def stock_alert(self):
        con=self.conectar()
        c1=con.cursor()
        c1.execute("""SELECT exi_cantidad, 
                exi_lote 
                FROM existencias 
                WHERE exi_cantidad<5 
                AND exi_cantidad>=0""")
        low_stock=c1.fetchall()
        c1.execute("""SELECT pro_descripcion 
                FROM productos 
                WHERE pro_codigo_k IN 
                (SELECT pro_codigo_k 
                FROM existencias 
                WHERE exi_cantidad<5 
                AND exi_cantidad>=0)""")
        descripciones_low_stock=c1.fetchall()
        if low_stock:
            messagebox.showwarning("Advertencia de inventario bajo",
                                "Los siguientes productos tienen inventario bajo:\n" + "\n".join
                                ([f"Producto: {descripciones_low_stock[low_stock.index(fila)][0]} Lote: {fila[1]} con {fila[0]} unidades" 
                                for fila in low_stock]))
        con.close()

    def abrir_login(self):
        self.destroy() 
        ventana = Login()
        ventana.mainloop()

    def limpiar_marco2(self):
        for dat in self.marco2.winfo_children():
            dat.destroy()

    def conectar(self):
        try:
            self.conexion1 = mysql.connector.connect(host="localhost",
                                                user="root",
                                                passwd="",
                                                database="INVENTARIO")
            print("Conexión correcta")
        except (mysql.connector.Error) as e:
            print("Ocurrióun error al conectar: ", e)
        return self.conexion1

    def view_inventario(self):
        self.limpiar_marco2()
        self.neg=Label(self.marco2,text="DULCERIA JIRETH DEMO",bg="#888888",font=("Impact",20))
        self.neg.pack(anchor="w",padx=15)
        self.action=Frame(self.marco2,bg="#605F5F")
        self.action.pack(fill="x",side="top",padx=15)
        et1=Label(self.action,text="Inventario\t\t\t\t\t\tBodega-1",bg="#605F5F",fg="#000000",font=("Impact",20))
        et1.pack(anchor="w",padx=15,pady=5)

        self.action2=Frame(self.marco2,bg="#605F5F")
        self.action2.pack(fill="x",side="top",padx=15,pady=10)   
        self.cod_E=Entry(self.action2,bg="#B3B3B3",font=(1))
        self.cod_E.grid(row=0,column=0,pady=10,padx=5)
        self.mos=Button(self.action2,text="🔎  Look",bg="#000000",fg="#ffffff",font=("Arial",12),command=self.buscarPro)
        self.mos.grid(row=0,column=1,pady=10)
        self.ins=Button(self.action2,text="+ Create",bg="#000000",fg="#ffffff",font=("Arial",12),command=self.insertar)
        self.ins.grid(row=0,column=2,pady=10,padx=100)
        self.report=Button(self.action2,text="Report",bg="#000000",fg="#ffffff",font=("Arial",12),command=self.report)
        self.report.grid(row=0,column=3,pady=10)        
        self.scrol=ttk.Scrollbar(self.marco2,orient="vertical")
        self.scrol.pack(side="right", fill='y')

        self.inventario=ttk.Treeview(self.marco2,columns=("Cod_producto", 
                                                        "Descripcion", 
                                                        "Precio", 
                                                        "Fecha", 
                                                        "Lote", 
                                                        "existencia"), 
                                    show="headings",yscrollcommand=self.scrol.set)

        self.inventario.heading("Cod_producto",text="Cod_Pro")
        self.inventario.heading("Descripcion",text="Producto")
        self.inventario.heading("Precio",text="Precio")
        self.inventario.heading("Fecha",text="Fecha")
        self.inventario.heading("Lote",text="Lote")
        self.inventario.heading("existencia",text="Unidades")

        self.inventario.column("Cod_producto",width=100)
        self.inventario.column("Descripcion",width=100)
        self.inventario.column("Precio",width=100)
        self.inventario.column("Fecha",width=100)
        self.inventario.column("Lote",width=50)
        self.inventario.column("existencia",width=100)     
        self.inventario.pack(expand=True,anchor="center",fill="both",padx=15)
        self.scrol.config(command=self.inventario.yview)

        self.action4=Frame(self.marco2,bg="#605F5F")
        self.action4.pack(fill="x",side="bottom",padx=15,pady=10)
        self.eli=Button(self.action4,text="Delete",bg="#000000",fg="#ffffff",font=("Arial",12),command=self.eliminarPro)
        self.eli.grid(row=0,column=1,pady=10,padx=10)
        self.act=Button(self.action4,text="Update",bg="#000000",fg="#ffffff",font=("Arial",12),command=self.actualizarPro)
        self.act.grid(row=0,column=2,pady=10,padx=10)

        con = self.conectar()
        c1 = con.cursor()
        c1.execute("select *from view_inventario")
        self.inventario.delete(*self.inventario.get_children())
        for fila in c1:
            self.inventario.insert(parent="", index=END, values=fila)
        con.close()
        self.stock_alert()

    def insertar(self):
        #Ventana para insertar productos y stock
        self.top = Toplevel(self)
        self.top.title("Insertar Producto")
        self.top.geometry("800x400")
        self.top.config(bg="#888888")
        self.top.grab_set() 
        self.top.focus_set()  
        self.top.transient(self)
        self.lf=LabelFrame(self.top,text="Producto",bg="#525252")
        self.lf.pack(side="left",expand=True,padx=20)

        #Nuevos Productos
        Label(self.lf, text="Codigo:",bg="#525252").grid(row=0, column=0)
        self.cod=Entry(self.lf,width=30)
        self.cod.grid(row=0, column=1,padx=5,pady=7)
        Label(self.lf, text="descripcion:",bg="#525252").grid(row=1, column=0)
        self.des=Entry(self.lf,width=30)
        self.des.grid(row=1, column=1,padx=5,pady=7)
        Label(self.lf, text="Cantidad:",bg="#525252").grid(row=2, column=0)
        self.can=Entry(self.lf,width=30)
        self.can.grid(row=2, column=1,padx=5,pady=7)
        Label(self.lf, text="Lote:",bg="#525252").grid(row=3, column=0)
        self.lot=Entry(self.lf,width=30)
        self.lot.grid(row=3, column=1,padx=5,pady=7)
        Label(self.lf,text="Precio:",bg="#525252").grid(row=4,column=0)
        self.pre=Entry(self.lf,width=30)
        self.pre.grid(row=4,column=1,padx=10,pady=7)
        Label(self.lf,text="Fecha",bg="#525252").grid(row=5,column=0)
        self.fec=DateEntry(self.lf,date_pattern="yyyy-mm-dd",bg="#525252",width=30)
        self.fec.grid(row=5,column=1,padx=10,pady=7)
        Button(self.lf, text="Insertar",bg="#bbbbbb",width=20,command=self.insertarPro).grid(row=6, column=1,pady=7)

        #Nuevo Stock
        self.lf2=LabelFrame(self.top,text="Stock",bg="#525252")
        self.lf2.pack(side="right",expand=True)        
        con = self.conectar()
        c1 = con.cursor()
        c1.execute("SELECT pro_codigo_k FROM productos")
        productos = c1.fetchall()
        con.close()
        opciones = [codigo[0] for codigo in productos]

        Label(self.lf2,text="Codigo-Producto:",bg="#525252",anchor="w").grid(row=0,column=0,pady=10)
        self.combo = ttk.Combobox(self.lf2, values=opciones, width=40, state="readonly")
        self.combo.grid(row=0,column=1)
        Label(self.lf2,text="Cantidad",bg="#525252",anchor="w").grid(row=1,column=0,pady=10)
        self.cant2=Entry(self.lf2,width=40)
        self.cant2.grid(row=1,column=1)
        Label(self.lf2,text="Lote:",bg="#525252",anchor="w").grid(row=2,column=0,pady=10)
        self.lot2=Entry(self.lf2,width=40)
        self.lot2.grid(row=2,column=1)
        Label(self.lf2,text="Fecha",bg="#525252").grid(row=3,column=0)
        self.fec=DateEntry(self.lf2,date_pattern="yyyy-mm-dd",bg="#525252",width=30)
        self.fec.grid(row=3,column=1,padx=10,pady=7)
        Button(self.lf2,text="Registrar",width=30,bg="#bbbbbb",command=self.insertarstock).grid(row=4,column=1,pady=30)

    def insertarPro(self):
        con = self.conectar()
        c1 = con.cursor()
        co = self.cod.get()
        de = self.des.get()
        lo = self.lot.get()
        ca = self.can.get()
        pr = self.pre.get()
        fe = self.fec.get()

        if not co or not de or not lo or not ca or not pr or not fe:
            messagebox.showerror("Error", "Llena todos los campos")
            return
        try:
            c1.execute("""SELECT * FROM productos 
                    WHERE pro_codigo_k = %s""", (co,))
            if c1.fetchone():
                messagebox.showerror("Error", "El código ya existe")
                return
            inserta = "INSERT INTO productos VALUES (%s, %s, %s, %s)"
            c1.execute(inserta, (co, de, pr, fe))
            c1.execute("""INSERT INTO existencias 
                    (exi_lote, 
                    exi_cantidad, 
                    pro_codigo_k, 
                    exi_fecha) 
                    VALUES (%s, %s, %s,%s)""", 
                    (lo, ca, co, fe))
            c1.execute("SELECT * FROM view_inventario")
            self.inventario.delete(*self.inventario.get_children())
            for fila in c1:
                self.inventario.insert(parent="", index=END, values=fila)
            con.commit()
            messagebox.showinfo("Éxito", "Producto insertado correctamente")
        except Exception as e:
            messagebox.showerror("Error en la base de datos", str(e))
        finally:
            self.cod.delete(0, END)
            self.des.delete(0, END)
            self.can.delete(0, END)
            self.lot.delete(0, END)
            con.close()
            self.top.destroy()

    def insertarstock(self):
        con = self.conectar()
        c1 = con.cursor()
        com = self.combo.get().strip()
        lot = self.lot2.get().strip()
        can = self.cant2.get().strip()
        fecha = self.fec.get()
        if not com or not lot or not can:
            messagebox.showerror("Error", "Llena todos los campos")
            return
        try:
            can = int(can)
            c1.execute("SELECT * FROM productos WHERE pro_codigo_k = %s", (com,))
            producto = c1.fetchone()
            if not producto:
                messagebox.showerror("Error", "El código de producto no existe en la base de datos")
                return
            c1.execute("""SELECT * FROM existencias 
                    WHERE exi_lote=%s 
                    AND pro_codigo_k=%s""", (lot,com))
            if c1.fetchone():
                messagebox.showerror("Error","EL LOTE YA EXISTE")
                return
            c1.execute("""INSERT INTO existencias 
                    (exi_fecha, 
                    exi_lote, 
                    exi_cantidad, 
                    pro_codigo_k) 
                    VALUES (%s,%s, %s, %s)""", 
                    (fecha,lot, can, com))
            c1.execute("SELECT * FROM view_inventario")
            self.inventario.delete(*self.inventario.get_children())
            for fila in c1:
                self.inventario.insert(parent="", index=END, values=fila)
            con.commit()
            messagebox.showinfo("Éxito", "Producto insertado correctamente")
            self.top.destroy()
        except Exception as e:
            messagebox.showerror("Error en la base de datos", str(e))
        finally:
            self.cod.delete(0, END)
            self.des.delete(0, END)
            self.can.delete(0, END)
            self.lot.delete(0, END)
            con.close()

    def buscarPro(self):
            con = self.conectar()
            c1 = con.cursor()
            co = self.cod_E.get()
            try:
                c1.execute("SELECT * FROM productos WHERE pro_codigo_k = %s", (co,))
                resultado = c1.fetchall()
                self.inventario.delete(*self.inventario.get_children())
                if not resultado:
                    messagebox.showinfo("Sin resultados", "No se encontró ningún producto con ese código")
                    c1.execute("SELECT * FROM view_inventario")
                    for fila in c1:
                        self.inventario.insert(parent="",index=END,values=fila)
                else:
                    for fila in resultado:
                        self.inventario.insert(parent="", index=END, values=fila)
            except Exception as e:
                messagebox.showerror("Error", str(e))
            con.close()
            self.cod_E.delete(0,END)

    def eliminarPro(self):
        self.eli = simpledialog.askstring("Eliminar Producto", "codigo_Producto")
        if not self.eli:
            return 
        try:
            con = self.conectar()
            c1 = con.cursor()
            co = self.eli
            if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este producto?\nSe eliminaran todos los registros del producto"):
                    c1.execute("DELETE FROM existencias WHERE PRO_CODIGO_K = %s", (co,))
                    c1.execute("DELETE FROM productos WHERE PRO_CODIGO_K = %s", (co,))
                    con.commit()
                    c1.execute("SELECT * FROM view_inventario")
                    self.inventario.delete(*self.inventario.get_children())
                    for fila in c1:
                        self.inventario.insert("", END, values=fila)
                    messagebox.showinfo("Éxito", "Producto y existencias eliminados correctamente.")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el producto: {e}")
        finally:
            con.close()

    def actualizarPro(self):
        try:
            item = self.inventario.selection()[0]
        except IndexError:
            messagebox.showerror("Error", "Selecciona un producto para actualizar")
            return
        valores = self.inventario.item(item, "values")
        cod, desc, precio, fecha, lote, existencia = valores

        self.top = Toplevel(self)
        self.top.title("Actualizar Producto")
        self.top.geometry("600x400")
        self.top.config(bg="#888888")

        Label(self.top, text="Código:", bg="#525252").grid(row=0, column=0)
        self.cod_up = Entry(self.top, width=30)
        self.cod_up.insert(0, cod)
        self.cod_up.config(state="readonly")  # no editable
        self.cod_up.grid(row=0, column=1, padx=5, pady=7)
        Label(self.top, text="Descripción:", bg="#525252").grid(row=1, column=0)
        self.des_up = Entry(self.top, width=30)
        self.des_up.insert(0, desc)
        self.des_up.grid(row=1, column=1, padx=5, pady=7)
        Label(self.top, text="Precio:", bg="#525252").grid(row=2, column=0)
        self.pre_up = Entry(self.top, width=30)
        self.pre_up.insert(0, precio)
        self.pre_up.grid(row=2, column=1, padx=5, pady=7)
        Label(self.top, text="Fecha:", bg="#525252").grid(row=3, column=0)
        self.fec_up = DateEntry(self.top, date_pattern="yyyy-mm-dd", width=30)
        self.fec_up.set_date(fecha)
        self.fec_up.grid(row=3, column=1, padx=5, pady=7)
        Label(self.top, text="Lote:", bg="#525252").grid(row=4, column=0)
        self.lot_org=lote
        self.lot_up = Entry(self.top, width=30)
        self.lot_up.insert(0, lote)
        self.lot_up.grid(row=4, column=1, padx=5, pady=7)
        Label(self.top, text="Cantidad:", bg="#525252").grid(row=5, column=0)
        self.can_up = Entry(self.top, width=30)
        self.can_up.insert(0, existencia)
        self.can_up.grid(row=5, column=1, padx=5, pady=7)
        Button(self.top, text="Actualizar", bg="#bbbbbb",command=self.updateDB).grid(row=6, column=1, pady=10)

    def updateDB(self):
        cod = self.cod_up.get()
        desc = self.des_up.get()
        precio = self.pre_up.get()
        fecha = self.fec_up.get()
        lote = self.lot_up.get()
        cantidad = self.can_up.get()
        con = self.conectar()
        c1 = con.cursor()
        try:
            c1.execute("""UPDATE productos 
                    SET pro_descripcion=%s, 
                    pro_precio=%s, 
                    pro_fecha=%s 
                    WHERE pro_codigo_k=%s""",
                    (desc, precio, fecha, cod))
            # Actualizar existencias
            c1.execute("""UPDATE existencias 
                    SET exi_lote=%s, 
                    exi_cantidad=%s, 
                    exi_fecha=%s 
                    WHERE pro_codigo_k=%s 
                    AND exi_lote=%s""",
                    (lote, cantidad, fecha, cod, self.lot_org))
            con.commit()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente")

            # Refrescar tabla
            c1.execute("SELECT * FROM view_inventario")
            self.inventario.delete(*self.inventario.get_children())
            for fila in c1:
                self.inventario.insert(parent="", index=END, values=fila)
            self.top.destroy()
        except Exception as e:
            messagebox.showerror("Error en la base de datos", str(e))
        finally:
            con.close()

    def report(self):
        con = self.conectar()
        c1 = con.cursor()
        c1.execute("SELECT * FROM productos")
        datos = c1.fetchall()
        df1 = pd.DataFrame(datos, columns=["codigo", "producto", "precio", "fecha"])
        c1.execute("SELECT * FROM existencias")
        datos = c1.fetchall()
        df2 = pd.DataFrame(datos, columns=["codigo_producto", 
                                        "lote", 
                                        "cantidad", 
                                        "Fecha"])
        with pd.ExcelWriter("Report_Dulceria.xlsx") as writer:
            df1.to_excel(writer, sheet_name="Productos", index=False)
            df2.to_excel(writer, sheet_name="Existencias", index=False)
        abrir = messagebox.askyesno("Reporte generado correctamente", "¿Desea abrirlo?")
        if abrir:
            os.startfile("Report_Dulceria.xlsx")
        con.close()

    def grafica(self):
        pro=[]
        fech=[]
        con=self.conectar()
        c1=con.cursor()
        c1.execute("SELECT *FROM productos")
        datos=c1.fetchall()
        for fila in datos:
            pro.append(fila[1])
            fech.append(fila[3])
        plt.bar(pro,fech,color="blue")
        plt.xlabel("Productos")
        plt.ylabel("Fechas")
        plt.title("Productos y sus fechas")
        plt.savefig('grafica de productos.png')
        plt.show()

if __name__=="__main__":
    ventanaB=CARGA()
    ventanaB.mainloop()
