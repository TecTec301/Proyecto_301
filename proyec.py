from tkinter import *
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
from tkinter import simpledialog
from tkcalendar import DateEntry
import pandas as pd
import os
class VentanaBase(Tk):
    def __init__(self, titulo="Ventana Base"):
        super().__init__()
        self.config(bg="#605F5F")
        self.overrideredirect(True)
        self.geometry("500x500+400+70")
        self.title("StockFlow")

        self.frame = Frame(self, bg="#000000")
        self.frame.pack(expand=True,fill="both",padx=20,pady=20)

        self.label = Label(self, text="StockFlow", font=("Impact",40), fg="#605F5F", bg="#000000")
        self.label.place(x=140, y=90)

        Label(self, text="📦", font=("Impact",100), fg="#605F5F", bg="#000000").place(x=170, y=190)
        Label(self, text="Cargando...", font=("Impact",20), fg="#605F5F", bg="#000000").place(x=180, y=400)

        self.after(1000,self.abrir_principal)

    def abrir_principal(self):
        self.destroy()
        Principal().mainloop()

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

        self.b_pro=Button(self.marco1,text="INVENTARIO",font=("Impact",12),width=20,bg="#ffffff",activebackground="#ffffff",command=self.productos)
        self.b_pro.grid(row=1,column=0,padx=10,pady=40)
        self.b_exi=Button(self.marco1,text="MOVIMIENTOS",font=("Impact",12),width=20,bg="#ffffff",activebackground="#ffffff")
        self.b_exi.grid(row=2,column=0,padx=10,pady=40)
        self.b_mov=Button(self.marco1,text="Ventas",font=("Impact",12),width=20,bg="#ffffff",activebackground="#ffffff")
        self.b_mov.grid(row=3,column=0,padx=10,pady=40)
        self.b_inv=Button(self.marco1,text="GRAFICA",font=("Impact",12),width=20,bg="#ffffff",activebackground="#ffffff")
        self.b_inv.grid(row=4,column=0,padx=10,pady=40)
        logout=Button(self.marco1,text="Logout",bg="#ffffff",width=20,height=2,font=("Impact",10))
        logout.grid(row=5,column=0,pady=30,padx=10)

    def limpiar_marco2(self):
        for dat in self.marco2.winfo_children():
            dat.destroy() 

    def productos(self):
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

        self.inventario=ttk.Treeview(self.marco2,columns=("Cod_producto","Descripcion","Precio","Fecha","Lote","existencia"),show="headings",yscrollcommand=self.scrol.set)
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
        self.act=Button(self.action4,text="Update",bg="#000000",fg="#ffffff",font=("Arial",12))
        self.act.grid(row=0,column=2,pady=10,padx=10)

        con = self.conectar()
        c1 = con.cursor()
        c1.execute("select *from vista_productos_existencias")
        self.inventario.delete(*self.inventario.get_children())
        for fila in c1:
            self.inventario.insert(parent="", index=END, values=fila)
        con.close()

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

    def insertar(self):
        self.top = Toplevel(self)
        self.top.title("Insertar Producto")
        self.top.geometry("800x400")
        self.top.config(bg="#888888")
        self.lf=LabelFrame(self.top,text="Producto",bg="#525252")
        self.lf.pack(side="left",expand=True,padx=20)


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
        Button(self.lf, text="Insertar",bg="#bbbbbb", command=self.insertarPro,width=20).grid(row=6, column=1,pady=7)


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
        Button(self.lf2,text="Registrar",width=30,bg="#bbbbbb",command=self.insertarstock).grid(row=3,column=1,pady=30)

    def insertarstock(self):
        con = self.conectar()
        c1 = con.cursor()
        com = self.combo.get().strip()
        lot = self.lot2.get().strip()
        can = self.cant2.get().strip()
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
            c1.execute("SELECT COALESCE(SUM(exi_cantidad), 0) FROM existencias WHERE exi_lote = %s", (lot,))
            cantidad_actual = c1.fetchone()[0]

            if cantidad_actual + can > 5000:
                messagebox.showerror("Error", f"El lote '{lot}' "f"No puedes exceder 5000 unidades.")
                return
            c1.execute("INSERT INTO existencias (exi_lote, exi_cantidad, pro_codigo_k) VALUES (%s, %s, %s)", (lot, can, com))
            c1.execute("select *from vista_productos_existencias")
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
    def insertarPro(self):
        con = self.conectar()
        c1 = con.cursor()
        co = self.cod.get()
        de = self.des.get()
        lo = self.lot.get()
        ca = self.can.get()
        pr = self.pre.get()
        fe = self.fec.get()
        
        if not co or not de:
            messagebox.showerror("Error", "Llena todos los campos")
            self.top.destroy()
            return
        try:
            c1.execute("SELECT * FROM productos WHERE pro_codigo_k = %s", (co,))
            if c1.fetchone():
                messagebox.showerror("Error", "El código ya existe")
                return
            inserta = "INSERT INTO productos VALUES (%s, %s, %s, %s)"
            c1.execute(inserta, (co, de, pr, fe))
            c1.execute("Insert into existencias (exi_lote, exi_cantidad, pro_codigo_k) values (%s, %s, %s)", (lo, ca, co))
            c1.execute("select *from vista_productos_existencias")
            
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
                    c1.execute("select * from vista_productos_existencias")
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
            if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este producto?"):
                c1.execute("DELETE FROM existencias WHERE PRO_CODIGO_K = %s", (co,))
                c1.execute("DELETE FROM productos WHERE PRO_CODIGO_K = %s", (co,))
                con.commit()
                c1.execute("SELECT * FROM vista_productos_existencias")
                self.inventario.delete(*self.inventario.get_children())
                for fila in c1:
                    self.inventario.insert("", END, values=fila)
                messagebox.showinfo("Éxito", "Producto y existencias eliminados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el producto: {e}")
        finally:
            con.close()
    def actualizarPro(self):
            con = self.conectar()
            c1 = con.cursor()
            co = self.cod_E.get()
            de = self.des_E.get()
            actualiza="UPDATE productos SET pro_descripcion=%s WHERE pro_codigo_k =%s"
            c1.execute(actualiza,(de,co))
            con.commit()
            c1.execute("select * from vista_productos_existencias")
            self.inventario.delete(*self.inventario.get_children())
            for fila in c1:
                self.inventario.insert(parent="",index=END, values=fila)
            con.close()
            self.cod_E.delete(0,END)
            self.des_E.delete(0,END)
    def report(self):
        con=self.conectar()
        c1=con.cursor()
        c1.execute("select*from productos")
        datos=c1.fetchall()
        df1=pd.DataFrame(datos,columns=["codigo","producto","precio","fecha"])
        c1.execute("select*from existencias")
        datos=c1.fetchall()
        df2=pd.DataFrame(datos,columns=["codigo_producto","lote","cantidad"])
        with pd.ExcelWriter("Report_Dulceria.xlsx") as writer:
            df1.to_excel(writer, sheet_name="Productos", index=False)
            df2.to_excel(writer, sheet_name="Existencias", index=False)
        messagebox.askyesno("reporte generado correctamente","¿Desea abrirlo?")
        if messagebox.YES:
            os.startfile("Report_Dulceria.xlsx")
            con.close()


if __name__ == "__main__":
    app = VentanaBase()
    app.mainloop()