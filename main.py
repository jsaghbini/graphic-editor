#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
import json
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtCore import QT_VERSION_STR

from scene import Scene

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.resize(500, 500)
        self.setWindowTitle("H&J Editor v0.1")
        self.undo_stack = QtWidgets.QUndoStack(self)
        self.create_scene()
        self.create_actions()
        self.create_menus()
        self.connect_actions()
        self.saveFileName = ""
    
    def create_scene(self) :
        view=QtWidgets.QGraphicsView()
        view.setSceneRect(QtCore.QRectF(-200,-200,400,400))
        self.scene=Scene(self, self.undo_stack)
        # text= self.scene.addText("Johnny & Hassan!")
        # text.setPos(100,200)
        view.setScene(self.scene) 
        self.setCentralWidget(view)

    def create_actions(self) :
        # File menu
        self.action_file_new = QtWidgets.QAction(QtGui.QIcon('icons/new.png'), 'New', self)
        self.action_file_new.setShortcut('Ctrl+N')
        self.action_file_new.setStatusTip('New')

        self.action_file_open = QtWidgets.QAction(QtGui.QIcon('icons/open.png'), 'Open', self)
        self.action_file_open.setShortcut('Ctrl+O')
        self.action_file_open.setStatusTip('Open File')

        self.action_file_save = QtWidgets.QAction(QtGui.QIcon('icons/save.png'), 'Save', self)
        self.action_file_save.setShortcut('Ctrl+S')
        self.action_file_save.setStatusTip('Save File')

        self.action_file_save_as = QtWidgets.QAction(QtGui.QIcon('icons/saveas.png'), 'Save As...', self)
        self.action_file_save_as.setShortcut('Ctrl+Shift+S')
        self.action_file_save_as.setStatusTip('Save File As')

        self.action_file_exit = QtWidgets.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        self.action_file_exit.setShortcut('Ctrl+Q')
        self.action_file_exit.setStatusTip('Exit Application')

        # Edit Menu
        self.action_edit_undo = self.undo_stack.createUndoAction(self)
        self.action_edit_undo.setShortcut('Ctrl+Z')
        self.action_edit_redo = self.undo_stack.createRedoAction(self)
        self.action_edit_redo.setShortcut('Ctrl+Y')

        # Tools menu
        self.group_action_tools = QtWidgets.QActionGroup(self)
        self.action_tools_line = QtWidgets.QAction(QtGui.QIcon('icons/line.png'),self.tr("&Line"), self)
        self.action_tools_line.setCheckable(True)
        self.action_tools_line.setShortcut('Ctrl+L')
        self.group_action_tools.addAction(self.action_tools_line)

        self.action_tools_rect = QtWidgets.QAction(QtGui.QIcon('icons/rec.png'),self.tr("&Rectangle"), self)
        self.action_tools_rect.setCheckable(True)
        self.action_tools_rect.setShortcut('Ctrl+R')
        self.group_action_tools.addAction(self.action_tools_rect)

        self.action_tools_ellipse = QtWidgets.QAction(QtGui.QIcon('icons/eli.png'),self.tr("&Ellipse"), self)
        self.action_tools_ellipse.setCheckable(True)
        self.action_tools_ellipse.setShortcut('Ctrl+E')
        self.group_action_tools.addAction(self.action_tools_ellipse)

        self.action_tools_poly = QtWidgets.QAction(QtGui.QIcon('icons/poly.png'),self.tr("&Polygone"), self)
        self.action_tools_poly.setCheckable(True)
        self.action_tools_poly.setShortcut('Ctrl+P')
        self.group_action_tools.addAction(self.action_tools_poly)

        self.action_tools_text = QtWidgets.QAction(QtGui.QIcon('icons/text.png'),self.tr("&Text"), self)
        self.action_tools_text.setCheckable(True)
        self.action_tools_poly.setShortcut('Ctrl+T')
        self.group_action_tools.addAction(self.action_tools_text)

        self.action_tools_eraser = QtWidgets.QAction(QtGui.QIcon('icons/erase.png'),self.tr("&Eraser"), self)
        self.action_tools_eraser.setShortcut('Ctrl+d')
        self.action_tools_eraser.setCheckable(True)
        self.group_action_tools.addAction(self.action_tools_eraser)

        # Style menu
        self.action_style_pen_color = QtWidgets.QAction(QtGui.QIcon('icons/color.png'),self.tr("&Pen Color"), self)
        self.action_style_brush_color = QtWidgets.QAction(QtGui.QIcon('icons/brushcolor.png'),self.tr("&Color"), self)
        self.action_style_pen_width = QtWidgets.QAction(QtGui.QIcon('icons/width.png'),self.tr("&Pen Width"), self)

        # Help  menu

    def create_menus(self) :
        #statusbar=self.statusBar()
        menubar = self.menuBar()
        menu_file = menubar.addMenu('&File')
        menu_file.addAction(self.action_file_new)
        menu_file.addSeparator()
        menu_file.addAction(self.action_file_open)
        menu_file.addAction(self.action_file_save)
        menu_file.addAction(self.action_file_save_as)
        menu_file.addSeparator()
        menu_file.addAction(self.action_file_exit)
        
        menu_edit = menubar.addMenu('&Edit')
        menu_edit.addAction(self.action_edit_undo)
        menu_edit.addAction(self.action_edit_redo)

        menu_tools = menubar.addMenu('&Tools')
        menu_tools.addAction(self.action_tools_line)
        menu_tools.addAction(self.action_tools_rect)
        menu_tools.addAction(self.action_tools_ellipse)
        menu_tools.addAction(self.action_tools_poly)

        menu_style=menubar.addMenu('&Style')
        menu_style_pen=menu_style.addMenu('&Pen')
        menu_style_pen.addAction(self.action_style_pen_color)
        menu_style_brush=menu_style.addMenu('&Brush')
        menu_style_brush.addAction(self.action_style_brush_color)
        menu_style_pen_width=menu_style.addMenu('&width')
        menu_style_pen_width.addAction(self.action_style_pen_width)

        menu_help=menubar.addMenu(self.tr("&Help"))
        self.action_about = menu_help.addAction(self.tr("& About this Editor"))

        # ToolBar Items
        toolbar = self.addToolBar('&Exit')
        toolbar.addAction(self.action_file_exit)

        toolbar = self.addToolBar('&Tools')
        toolbar.addAction(self.action_tools_line)
        toolbar.addAction(self.action_tools_rect)
        toolbar.addAction(self.action_tools_ellipse)
        toolbar.addAction(self.action_tools_poly)
        toolbar.addAction(self.action_tools_text)


    def connect_actions(self) :
        # File menu
        self.action_file_new.triggered.connect(self.file_new)
        self.action_file_open.triggered.connect(self.file_open)
        self.action_file_save.triggered.connect(self.file_save)
        self.action_file_save_as.triggered.connect(self.file_save_as)
        self.action_file_exit.triggered.connect(self.file_exit)
        
        # Tool menu
        self.action_tools_line.triggered.connect(lambda checked, tool="Line": self.tool_selection(checked,tool))
        self.action_tools_rect.triggered.connect(lambda checked, tool="Rectangle": self.tool_selection(checked,tool))
        self.action_tools_ellipse.triggered.connect(lambda checked, tool="Ellipse": self.tool_selection(checked,tool))
        self.action_tools_poly.triggered.connect(lambda checked, tool="Polygone": self.tool_selection(checked,tool))
        self.action_tools_text.triggered.connect(lambda checked, tool="Text": self.tool_selection(checked,tool))

        # Style menu 
        self.action_style_pen_color.triggered.connect(self.pen_color_selection)
        self.action_style_brush_color.triggered.connect(self.brush_color_selection)
        self.action_style_pen_width.triggered.connect(self.pen_width_selection)
        # Help menu

    ## File slots
    def file_new(self) :
        msg = QMessageBox.question(self,"H&J Editor v0.1", "Are you sure you want to create a new file?")
        if(msg == QMessageBox.Yes):
            self.scene.clear()
        else:
            pass

    def file_open(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', os.getcwd())
        fileopen=QtCore.QFile(filename[0])
        if fileopen.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)==None :
            print("Failed to open the file: '" +filename + "'")
            return -1
        else :
            print("File '" +filename+ "' opened successfully!")
            print("'" + filename + "' opened!")
    
    def file_save_as(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', os.getcwd())
        filesave=QtCore.QFile(filename[0])
        
        if filename[0] is None or filename[0]=='' or filesave.open(QtCore.QIODevice.WriteOnly)==None :
            msg = "Failed to save the file: '" +filename[0] + "'"
            if filename[0] is None or filename[0]=='' :
                msg = "Save Operation Cancelled."
                msgbox = QMessageBox.information(self,"Info",msg)
            else:
                msgbox = QMessageBox.warning(self,"Info",msg)
            
            # print("Failed to save the file: "+filename[0])
            return -1
        else :
            msgbox = QMessageBox.information(self,"Info","File '" +filename[0] + "' saved successfully!")
            # print("File " +filename[0] + " saved successfully!")  

    def file_save(self):
        # Testing if there is a chosen save path first
        if self.saveFileName == "" or not os.path.exists(self.saveFileName):
            filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', os.getcwd())
            self.saveFileName = filename[0]
        else:
            filename = []
            filename.append(self.saveFileName)

        filesave=QtCore.QFile(filename[0])
            
        if filename[0] is None or filename[0]=='' or filesave.open(QtCore.QIODevice.WriteOnly)==None :
            msg = "Failed to save the file: '" +filename[0] + "'"
            if filename[0] is None or filename[0]=='' :
                msg = "Save Operation Cancelled!"
            msgbox = QMessageBox.information(self,"Info",msg)
            # print("Failed to save the file: "+filename[0])
            return -1
        else :
            msgbox = QMessageBox.information(self,"Notice","File '" +filename[0] + "' saved successfully!")
            # print("File " +filename[0] + " saved successfully!")  
    
    def file_exit(self):
        msgBox = QMessageBox.question(self, 'Warning',"Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No)
        if(msgBox == QMessageBox.Yes):
            exit(0)

    ## Tools  slots
    def tool_selection(self,checked, tool) :
        print("lamda checked, tool : ",checked, tool)
        todraw=self.action_tools_line.isChecked()
        print(todraw)
        # self.action_line.setChecked(todraw)
        self.scene.set_tool(tool)
    ## Style slots
    def pen_color_selection(self):
        color = QtWidgets.QColorDialog.getColor(QtCore.Qt.yellow, self )
        if color.isValid() :
            print("Chosen Pen Color : ",color.name())
        else :
            print("Not a valid color !")

    def brush_color_selection(self):
        color = QtWidgets.QColorDialog.getColor(QtCore.Qt.yellow, self )
        if color.isValid() :
            print("Chosen Brush Color : ",color.name())
        else :
            print("Not a valid color !") 

    def pen_width_selection(self):
        num,ok = QtWidgets.QInputDialog.getInt(self,"Pen Width","Enter the Pen's width")
        if ok:
            self.scene.set_pen_width(num)
            print("Chosen Width: ",num)
        else :
            print("Not a valid width !")
    
    ## Help slots
    def help_about(self):
        QtWidgets.QMessageBox.information(self, self.tr("About Me"),
                                self.tr("Dupond/Dupont\n copyright ENIB 2022P"))
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

if __name__ == "__main__" :  
    print(QT_VERSION_STR)
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
