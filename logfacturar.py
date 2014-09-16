#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import operator
import sys
from PyQt4 import QtCore, QtGui, Qt, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *
import ConfigParser

class MyForm(QtGui.QMainWindow):
	
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui=uic.loadUi('Main.ui',self)
	
    def agregarItem(self):
        with VentanaAgregar() as agregar:
            agregar.exec_()
	
    def abrirPresupuesto(self): #pequeño cambio
        pres = VentanaPresupuesto()
			
    def editarItem(self):
        with VentanaEditar() as editar:
            editar.exec_()
	
    def abrirclientes(self):
        with VentanaClientes() as cliente:
            cliente.exec_()

class VentanaClientes(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.uiLista=uic.loadUi('clientes.ui',self)
        self.show()
    
    def crear(self):
        cliente=self.txbcliente.text()
        self.crear=cliente+".ini"
        archi=open(self.crear,"w")
        self.txbcliente.setText("")
        
    
    def agregar(self):
        producto=self.txbproduc.text()
        cantidad=self.txbcantidad.text()
        abrir=self.txbexist.text()
        abrira=abrir+".ini"
        datos="Stock.ini"
        self.lista=open(datos,'a')
        self.archi=open(abrira,'a')
        config = ConfigParser.ConfigParser()
        config1 = ConfigParser.ConfigParser()
        config.read(datos)
        config1.read(abrira)
        la=config.get(str(producto),'Precio')
        le=config.get(str(producto),'Stock')
        stock=int(le)-int(cantidad)
        if (stock <= 0):
            QtGui.QMessageBox.critical(self, 'Mensaje de sistema', 'No hay Stock!')
        config.set(str(producto),'Stock',stock)
        config1.add_section(str(producto))
        config1.set(str(producto),'Precio',la)
        config1.set(str(producto),'Cantidad',cantidad)
        config.write(self.lista)
        config1.write(self.archi)
        self.lista.close()
        self.archi.close()
        self.txbproduc.setText("")
        self.txbcantidad.setText("")
        self.txbexist.setText("")


class VentanaPresupuesto(QtGui.QWidget):
	
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui=uic.loadUi('presupuesto.ui',self)
        self.show()
        abrir=self.txbprod.text()
        global abrira
        abrira=abrir+".ini"
        self.refreshTable()
        
    
    
    def busca(self):
        abrir=self.txbprod.text()
        self.lala=abrir+".ini"
        self.lista=open(self.lala,'a')
        config= ConfigParser.ConfigParser()
        config.read(self.lala)
        section=config.sections()
        for each in section:
            sec=config.get(each,"Precio")
            self.lista.write(str(sec+","))
        
        self.lista.close()
        self.refreshTable()
        for a in section:
            tot=config.get(section[a],"Precio")
        desc=self.txbdesc.text()
        total=int(total)+int(tot)
        if (desc > 0):
            div=desc/100
            destot=div*total
            self.lcd.display(str(total))
        else:                
            self.lcd.display(str(total))    
            


    def refreshTable(self):
        self.lista=abrira
        header = ["Produco","Precio","Cantidad"]
        self.tablemodel = MyTableModel(self.lista,header, self)
        self.ui.table.setModel(self.tablemodel)
        # enable sorting
        self.ui.table.setSortingEnabled(True)
        hh = self.ui.table.horizontalHeader()
        hh.setStretchLastSection(True)
        self.ui.table.resizeColumnsToContents()



class MyTableModel(QAbstractTableModel):#No entiendo nada (pitri y lauti tampoco dicen que es muy "pythoniano") de esto por eso no pude terminar el trabajo no quiero que lo tomen como una excusa
    def __init__(self,foo, archivo, headerdata, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata=[]   
        self.headerdata = headerdata
        producto=[]
        foo=abrira
        """
        *Adaptado...* gracias Pablo <3 
        """
        datos = ConfigParser.ConfigParser()
        datos.read(foo)

        for p in datos.sections():
            nombre=p
            precio=datos.get(p, 'precio')
            stock=datos.get(p, 'stock')
            producto=[nombre,precio,stock]
            self.arraydata.append(producto)

        """Fin *Adaptado*"""

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))        
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.emit(SIGNAL("layoutChanged()"))

class VentanaAgregar(QtGui.QWidget):
	
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.uiAgregar=uic.loadUi('agregar.ui',self)
        self.show()
        self.config = ConfigParser.ConfigParser()
        self.archivo = "Stock.ini"
        self.config.read(self.archivo)
        
    def agregar(self):        
        nombre=self.txbname.text()
        precio=self.txbprecio.text()
        canti=self.txbstock.text()
        prod=[str(nombre),str(precio),str(canti)]
        with open('Stock.ini','a+r') as f:
            self.txbname.setText("")#config.secction config.items(secction)
            self.txbprecio.setText("")
            self.txbstock.setText("")            
            ifExist = False
            for section in self.config.sections():
                if (prod[0]==section):
                    QtGui.QMessageBox.critical(self, 'Mensaje de sistema', 'Ya existe el producto')
                    ifExist=True
            if (not ifExist):
                QtGui.QMessageBox.information(self, 'Mensaje de sistema', 'Creando el producto')
                self.config.add_section(prod[0])
                self.config.set(prod[0],'Precio',prod[1])
                self.config.set(prod[0],'Stock',prod[2])
                self.config.write(f)
                f.close()    
                       
    
class VentanaEditar(QtGui.QWidget):
	
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.uiEditar=uic.loadUi('editar.ui',self)
        self.show()	
        self.config = ConfigParser.ConfigParser()
        self.archivo = "Stock.ini"
        self.config.read(self.archivo)
   
    def buscar(self):
        nombedit=self.txbnamedit.text()
        newname=self.txbnewname.text()
        newprec=self.txbnewprec.text()
        newstock=self.txbnewstock.text()
        
        with open('Stock.ini','a+r') as f:
            config= ConfigParser.ConfigParser()
            config.read(self.archivo)
            la=config.get(str(nombedit),'precio')
            la2=config.get(str(nombedit),'stock')
            self.txbnewname.setText(nombedit)
            self.txbnewprec.setText(la)
            self.txbnewstock.setText(la2)
            f.close()

    def editar(self):
        nombre=self.txbnewname.text()
        precio=self.txbnewprec.text()
        canti=self.txbnewstock.text()
        prod=[str(nombre),str(precio),str(canti)]   
        with open('Stock.ini','w') as f:
            nombre=self.txbnewname.text()
            precio=self.txbnewprec.text()
            canti=self.txbnewstock.text()
            prod=[str(nombre),str(precio),str(canti)]
            config = ConfigParser.ConfigParser()
            self.config.set(prod[0],'Precio',prod[1])
            self.config.set(prod[0],'Stock',prod[2])
            self.config.write(f)
            self.txbnewname.setText("")
            self.txbnewprec.setText("")
            self.txbnewstock.setText("")
            self.txbnamedit.setText("")
            f.close()
        
if __name__=='__main__':
	app=QtGui.QApplication(sys.argv)
	form=MyForm()
	form.show()
	sys.exit(app.exec_())
