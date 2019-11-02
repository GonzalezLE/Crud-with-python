from tkinter import ttk
from tkinter import *

import sqlite3

class producto:
    db_name='database.db'
    def __init__(self,window):
        self.wind=window
        self.wind.title('Producto aplicacion')
        #creamos frame container
        Frame=LabelFrame(self.wind,text='Registra nuevo producto')
        Frame.grid(row=0,column=0,columnspan=3,pady=20)
        
        #entrada de un nombre (input)
        Label(Frame,text='Nombre: ').grid(row=1,column=0)
        self.name=Entry(Frame)
        self.name.focus()
        self.name.grid(row=1,column=1)

        #entrada para el precio (input)
        Label(Frame,text='Precio: ').grid(row=2,column=0)
        self.precio=Entry(Frame)
        self.precio.grid(row=2,column=1)

        #creacion del boton
        ttk.Button(Frame,text='Guardar producto',command=self.addProductos).grid(row=3,columnspan=2,sticky=W + E)

        #table
        self.tree=ttk.Treeview(height=10,column=2)
        self.tree.grid(row=4,column=0,columnspan=2)
        self.tree.heading('#0',text='nombre',anchor=CENTER)
        self.tree.heading('#1',text='Precio',anchor=CENTER)
        self.get_productos()

    def run_query(self,query,parametros=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor=conn.cursor()
            result = cursor.execute(query, parametros)
            conn.commit()
        return result
        

    def get_productos(self):
        #limpiando la tabla
        records=self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #consultando los datos
        query='select * from producto ORDER BY id DESC'
        db_rows=self.run_query(query)
        #rellenando los datos
        for row in db_rows:
            #print(row)
            self.tree.insert('',0,text=row[1],values=row[2])
    
    #validar los inputs
    def validadCampos(self):
        return len(self.name.get())!=0 and len(self.precio.get())!=0
    
    def addProductos(self):
        if self.validadCampos():
            query='insert into producto values(null,?,?)'
            parametros=(self.name.get,self.precio.get())
            self.run_query(query,parametros)
            print('datos guardados')
        else:
            print('El nombre y precio es requerido')
        self.get_productos()
if __name__=='__main__':
    window=Tk()
    aplicacion=producto(window)
    window.mainloop()