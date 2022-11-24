

from PyQt5 import QtCore, QtGui, QtWidgets

import json
import matplotlib.pyplot as plt
import numpy as np
import math as ma
import tkinter as tk
from tkinter import filedialog

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


import matplotlib.pyplot as plt

from struct import *
import sys

#show message
import win32api

class Ui_txtRotate(object):
    def setupUi(self, txtRotate):
        # For plotting
        self.figure = Figure()
        self.graphicsView = FigureCanvas(self.figure)
        self.graphicsView.setParent(txtRotate)
        #


        txtRotate.setObjectName("txtRotate")
        txtRotate.resize(927, 714)
        self.centralwidget = QtWidgets.QWidget(txtRotate)
        self.centralwidget.setObjectName("centralwidget")
        self.btnOpenShape = QtWidgets.QPushButton(self.centralwidget)
        self.btnOpenShape.setGeometry(QtCore.QRect(220, 40, 151, 61))
        self.btnOpenShape.setObjectName("btnOpenShape")
        self.btnOpenJson = QtWidgets.QPushButton(self.centralwidget)
        self.btnOpenJson.setGeometry(QtCore.QRect(520, 40, 151, 61))
        self.btnOpenJson.setObjectName("btnOpenJson")
        #self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(100, 150, 711, 341))
        self.graphicsView.setObjectName("graphicsView")
        self.btnSaveShape = QtWidgets.QPushButton(self.centralwidget)
        self.btnSaveShape.setEnabled(False)
        self.btnSaveShape.setGeometry(QtCore.QRect(660, 520, 151, 61))
        self.btnSaveShape.setObjectName("btnSaveShape")
        self.btnSavJson = QtWidgets.QPushButton(self.centralwidget)
        self.btnSavJson.setEnabled(False)
        self.btnSavJson.setGeometry(QtCore.QRect(660, 590, 151, 61))
        self.btnSavJson.setObjectName("btnSavJson")

        self.btnSavJson2 = QtWidgets.QPushButton(self.centralwidget)
        self.btnSavJson2.setVisible(False)
        self.btnSavJson2.setGeometry(QtCore.QRect(660, 590, 151, 61))
        self.btnSavJson2.setObjectName("btnSavJson2")

        self.lblrotate = QtWidgets.QLabel(self.centralwidget)
        self.lblrotate.setGeometry(QtCore.QRect(100, 570, 81, 31))
        self.lblrotate.setObjectName("lblrotate")
        self.lblDegree = QtWidgets.QLabel(self.centralwidget)
        self.lblDegree.setGeometry(QtCore.QRect(330, 570, 61, 31))
        self.lblDegree.setObjectName("lblDegree")
        self.btnRotate = QtWidgets.QPushButton(self.centralwidget)
        self.btnRotate.setEnabled(False)
        self.btnRotate.setGeometry(QtCore.QRect(400, 570, 101, 31))
        self.btnRotate.setObjectName("btnRotate")
        self.btnRotate2 = QtWidgets.QPushButton(self.centralwidget)
        self.btnRotate2.setVisible(False)
        self.btnRotate2.setGeometry(QtCore.QRect(400, 570, 101, 31))
        self.btnRotate2.setObjectName("btnRotate2")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(210, 570, 91, 31))
        self.textEdit.setObjectName("textEdit")
        txtRotate.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(txtRotate)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 927, 26))
        self.menubar.setObjectName("menubar")
        txtRotate.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(txtRotate)
        self.statusbar.setObjectName("statusbar")
        txtRotate.setStatusBar(self.statusbar)

        self.retranslateUi(txtRotate)
        QtCore.QMetaObject.connectSlotsByName(txtRotate)

        #connect click
        self.btnOpenShape.clicked.connect(self.onOpenClickedShape)
        self.btnRotate.clicked.connect(self.onRotationClickedShape)
        self.btnSaveShape.clicked.connect(self.onSaveClickedShape)
        self.btnSavJson2.clicked.connect(self.onSaveClickedShapeForJson)
        self.btnOpenJson.clicked.connect(self.onOpenClickedJson)
        self.btnRotate2.clicked.connect(self.onRotationClickedJson)
        self.btnSavJson.clicked.connect(self.onSaveClickedJson)
        #

    def retranslateUi(self, txtRotate):
        _translate = QtCore.QCoreApplication.translate
        txtRotate.setWindowTitle(_translate("txtRotate", "My Shapefile & Json read"))
        self.btnOpenShape.setText(_translate("txtRotate", "Open shape file"))
        self.btnOpenJson.setText(_translate("txtRotate", "Open Json file"))
        self.btnSaveShape.setText(_translate("txtRotate", "Save as shape file"))
        self.btnSavJson.setText(_translate("txtRotate", "Save as Json file"))
        self.btnSavJson2.setText(_translate("txtRotate", "Save as Json file"))
        self.lblrotate.setText(_translate("txtRotate", "Rotate Angle :"))
        self.lblDegree.setText(_translate("txtRotate", "Degree"))
        self.btnRotate.setText(_translate("txtRotate", "Rotate"))
        self.btnRotate2.setText(_translate("txtRotate", "Rotate"))



    # open shape file
    def onOpenClickedShape(self):
        root = tk.Tk()
        file_path = filedialog.askopenfilename(title="Open ShapeFile",filetypes = (("Shape Files","*.shp"),("all files","*.*")))
        l=open(file_path,"rb")
        root.destroy()

        self.ax = self.figure.add_subplot(111)
        self.ax.clear()
        

        self.write_l = l
        l.seek(24)
        file_lenght=unpack( ">i", l.read(4))
        #print("file_lenght2 = ",file_lenght2)
        l.seek(32)
        self.shapetype = unpack( "<i", l.read(4))
        print("self.shapetype = ",self.shapetype)
        l.seek(100)
        if self.shapetype[0] == 0: #empty
            print("File is empty")
        elif self.shapetype[0] == 1: #point
            self.pp = int((file_lenght[0] * 2 - 100) / 28)
            self.px = []
            self.py = []
            self.number=[]
            for i in range(self.pp):
                a=l.seek(112 + 28 * i)
                X, Y = unpack('<2d', l.read(2*8))
                self.px.append(X)
                self.py.append(Y)
                self.number+=[1]


            self.ax.plot(self.px, self.py, '*')
            #self.ax.show()
            self.graphicsView.draw()


        elif self.shapetype[0] == 3 or self.shapetype[0] == 5: #polyline and polygon


            self.pp=file_lenght[0]*2-100
            self.px=[]
            self.py=[]
            self.number=[]
            self.startPoint=[]
            while self.pp>1:
                l.seek(l.tell()+4)
                ContentL2 = unpack(">i", l.read(4))
                print("ContentL = ", ContentL2)
                l.seek(l.tell() + 40)

                self.numpoint = unpack("<i", l.read(4))
                self.number+=(self.numpoint)
                print("numpoint = ", self.numpoint)

                self.startPoint.append(l.seek(l.tell() + 4))
                for i in range(self.numpoint[0]):
                    self.px1, self.py1 = unpack('<2d', l.read(2*8))
                    self.px.append(self.px1)
                    self.py.append(self.py1)


                self.pp=self.pp-ContentL2[0]*2-8
            ii=0
            for i in range(len(self.number)):
                self.ax.plot(self.px[ii:ii+self.number[i]],self.py[ii:ii+self.number[i]])
                ii+=self.number[i]

            #self.ax.show()
            self.graphicsView.draw()

        else:
            print("Format can't support")


        # for enable and disable
        self.btnRotate.setEnabled(True)
        self.btnOpenJson.setEnabled(False)
        self.btnOpenShape.setEnabled(False)
        #






    #FOR ROTATE shape
    def onRotationClickedShape(self):
        rotate=float(self.textEdit.toPlainText())

        self.ax.clear()
        
        point=np.array([self.px,self.py])
        R=([[ma.cos(rotate*ma.pi/180),ma.sin(rotate*ma.pi/180)],
        [ -ma.sin(rotate * ma.pi / 180),ma.cos(rotate * ma.pi / 180)]])
        self.ll=R@point

        ii=0
        if self.shapetype[0] == 1:
            self.ax.plot(self.ll[0],self.ll[1],'*')
        elif self.shapetype[0] == 3 or self.shapetype[0] == 5:
            for i in range(len(self.number)):
                self.ax.plot(self.ll[0,ii:ii+self.number[i]],self.ll[1,ii:ii+self.number[i]])
                ii+=self.number[i]

        self.graphicsView.draw()

        # for enable and disable
        self.btnRotate.setEnabled(False)
        self.btnSaveShape.setEnabled(True)
        self.btnSavJson2.setVisible(True)





    #save shape from shape
    def onSaveClickedShape(self):
        root = tk.Tk()
        file_path2 = filedialog.asksaveasfile(mode='w',defaultextension=".shp", title = "Save shape file",filetypes = (("Shape Files","*.shp"),("all files","*.*")))
        root.destroy()
        with open(file_path2.name, 'rb+') as t:
            self.write_l.seek(0)
            t.write(self.write_l.read(100)) #for header1

            if self.shapetype[0] == 1: #for point
                for i_pp in range(self.pp):
                    t.write(self.write_l.read(12))
                    t.write(pack("<d",self.ll[0,i_pp]))
                    t.write(pack("<d",self.ll[1,i_pp]))
                    self.write_l.seek(self.write_l.tell()+16)
            elif self.shapetype[0] == 3 or self.shapetype[0] ==5: #for polyline or polygon
                i1=0
                for i2 in range (len(self.startPoint)):
                    self.write_l.seek(t.tell())
                    t.write(self.write_l.read(56)) #for header 2
                    for i3 in range(self.number[i2]):
                        t.write(pack("<d",self.ll[0,i1]))
                        t.write(pack("<d",self.ll[1,i1]))
                        i1+=1

            t.close()

        win32api.MessageBox(0, 'Save was success', 'OK' , 0x00001000)





    #for save Json from shape
    def onSaveClickedShapeForJson(self):
        js2={}
        js2["type"]="FeatureCollection"
        js2["crs"]={"type":"name","properties":{"name":"EPSG:32639"}}

        if self.shapetype[0] == 1:
            types1 = "Point"
        elif self.shapetype[0] == 3:
            types1 = "LineString"
        elif self.shapetype[0] == 5:
            types1 = "Polygon"


        featureJson=[]
        for i_creat in range (len(self.number)):
            featureJson.append (dict(type="Feature", id=i_creat, geometry=dict(type=types1,coordinates=[0,0]),properties=dict(FID=i_creat,Id=0)))

        js2["features"]=featureJson

        new_point=[]
        ii_replace=0
        for i_replace in range (len(self.number)):
            for i_replace_p in range (self.number[i_replace]):
                new_point.append([self.ll[0,ii_replace],self.ll[1,ii_replace]])

                ii_replace += 1
            if  types1 == "Point":
                new_point = new_point[0]
            elif types1 == "Polygon":
                new_point = [new_point]
            js2['features'][i_replace]['geometry']['coordinates']= new_point
            new_point=[]



        root = tk.Tk()
        file_path2 = filedialog.asksaveasfile(mode='w',defaultextension=".json", title = "Save json file",filetypes = (("json Files","*.json"),("all files","*.*")))
        root.destroy()
        with open(file_path2.name,'w') as t:
            json.dump(js2, t)
            t.close


        win32api.MessageBox(0, 'Save was success', 'OK' , 0x00001000)
            


    
    #open json files
    def onOpenClickedJson(self):

        self.ax = self.figure.add_subplot(111)
        self.ax.clear()


        root = tk.Tk()
        file_path = filedialog.askopenfilename(title="Open jason file",filetypes = (("Jason Files","*.json"),("all files","*.*")))
        root.destroy()
        with open(file_path, 'r') as f:
            js = json.load(f)
            self.js2=js
        
        self.px=[]
        self.py=[]
        self.px2=[]
        self.py2=[]
        self.number=[]
        self.number2=[]
        i=0

        try:
            
            while True:
                self.type = js['features'][i]['geometry']['type']
                coords=js['features'][i]['geometry']['coordinates']
                if self.type == "Point":
                    coords=[[coords]] 
                if self.type== "LineString":
                    coords=[coords]

                
                #if self.type== "LineString":
                 #   self.number2.append(len(coords2[0]))
                #else:
                self.number.append(len(coords[0]))


                
                for i_num in range (self.number[i]):
                    self.px.append(coords[0][i_num][0])
                    self.py.append(coords[0][i_num][1])

                #for i_num2 in range (self.number[i]):
                 #   self.px2.append(coords2[0][i_num2][0])
                  #  self.py2.append(coords2[0][i_num2][1])
                i += 1
        except:
            ii=0
            for i_plot in range(len(self.number)):
                if  self.type == "Point":
                    self.ax.plot(self.px[ii:ii+self.number[i_plot]],self.py[ii:ii+self.number[i_plot]],"*")
                if  self.type == "LineString":
                    self.ax.plot(self.px[ii:ii+self.number[i_plot]],self.py[ii:ii+self.number[i_plot]])
                if self.type == "Polygon":
                    self.ax.plot(self.px[ii:ii+self.number[i_plot]],self.py[ii:ii+self.number[i_plot]])


                ii+=self.number[i_plot]

            self.graphicsView.draw()

        # for enable and disable
        self.btnRotate2.setVisible(True)
        self.btnOpenJson.setEnabled(False)
        self.btnOpenShape.setEnabled(False)
        #

    



    #rotate json
    def onRotationClickedJson(self):
        rotate=float(self.textEdit.toPlainText())

        self.ax.clear()
        
        point=np.array([self.px,self.py])
        #rotate=float (rotate)
        R=([[ma.cos(rotate*ma.pi/180),ma.sin(rotate*ma.pi/180)],
        [ -ma.sin(rotate * ma.pi / 180),ma.cos(rotate * ma.pi / 180)]])
        self.ll=R@point

        ii=0
        for i_plot_rotate in range(len(self.number)):
            if  self.type == "Point":
                self.ax.plot(self.ll[0],self.ll[1],'*')
            elif  self.type == "LineString":
                self.ax.plot(self.ll[0,ii:ii+self.number[i_plot_rotate]],self.ll[1,ii:ii+self.number[i_plot_rotate]])
            elif self.type == "Polygon":
                self.ax.fill(self.ll[0,ii:ii+self.number[i_plot_rotate]],self.ll[1,ii:ii+self.number[i_plot_rotate]])


            ii+=self.number[i_plot_rotate]

      

        self.graphicsView.draw()   

        # for enable and disable
        self.btnRotate2.setEnabled(False)
        self.btnSavJson.setEnabled(True)






    #save json from json
    def onSaveClickedJson(self):
        new_point=[]
        ii_replace=0
        for i_replace in range (len(self.number)):
            for i_replace_p in range (self.number[i_replace]):
                new_point.append([self.ll[0,ii_replace],self.ll[1,ii_replace]])

                ii_replace += 1
            if  self.type == "Point":
                new_point = new_point[0]
            elif self.type == "Polygon":
                new_point = [new_point]
            self.js2['features'][i_replace]['geometry']['coordinates']= new_point
            new_point=[]

        root = tk.Tk()
        file_path2 = filedialog.asksaveasfile(mode='w',defaultextension=".json", title = "Save json file",filetypes = (("json Files","*.json"),("all files","*.*")))
        root.destroy()
        with open(file_path2.name,'w') as t:
            json.dump(self.js2, t)
            t.close 

        win32api.MessageBox(0, 'Save was success', 'OK' , 0x00001000)





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    txtRotate = QtWidgets.QMainWindow()
    ui = Ui_txtRotate()
    ui.setupUi(txtRotate)
    txtRotate.show()
    sys.exit(app.exec_())
