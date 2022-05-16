#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore,QtCore,QtGui,QtWidgets
from PyQt5.QtCore import QT_VERSION_STR
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPixmap, QPainter
# --------------------------------------------------------------------------------------------------------- #
# ╔═════════════════════════════════════════════════════════════════════════════════╤═══════════════════════╗
# ║░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│      UNDO - REDO      ║
# ╚═════════════════════════════════════════════════════════════════════════════════╧═══════════════════════╝
class AddCommand(QtWidgets.QUndoCommand):
    def __init__(self, scene: QtWidgets.QGraphicsScene, item: QtWidgets.QGraphicsItem):
        super().__init__()
        self.scene = scene
        self.item = item

    def undo(self):
        self.scene.removeItem(self.item)

    def redo(self):
        self.scene.addItem(self.item)
# --------------------------------------------------------------------------------------------------------- #
    class MoveCommand(QtWidgets.QUndoCommand):
        def __init__(self, item: QtWidgets.QGraphicsItem, new_pos=None):
            super().__init__()
            self.item = item
            self.old_pos = item.pos()
            self.new_pos = new_pos if new_pos else self.old_pos

        def undo(self):
            self.item.setPos(self.old_pos)

        def redo(self):
            self.item.setPos(self.new_pos)
# --------------------------------------------------------------------------------------------------------- #
    class RemoveCommand(QtWidgets.QUndoCommand):
        def __init__(self, scene: QtWidgets.QGraphicsScene, item: QtWidgets.QGraphicsItem):
            super().__init__()
            self.scene = scene
            self.item = item

        def undo(self):
            self.scene.addItem(self.item)

        def redo(self):
            self.scene.removeItem(self.item)
#                                           ╭────────────────────╮
#───────────────────────────────────────────│   END Undo-Redo    |───────────────────────────────────────────
#                                           ╰────────────────────╯
# --------------------------------------------------------------------------------------------------------- #
class Scene (QtWidgets.QGraphicsScene) :
    def __init__(self,parent,undo_stack):
        QtWidgets.QGraphicsScene.__init__(self, parent)
        self.tool=None
        self.begin,self.end,self.offset=QtCore.QPoint(0,0),QtCore.QPoint(0,0),QtCore.QPoint(0,0)
        self.item=None 
        self.undo_stack = undo_stack
        # Settings for the border and fill color
        self.pen=QtGui.QPen()
        self.pen.setColor(QtCore.Qt.red)
        self.pen.setWidth(3)
        self.brush=QtGui.QBrush(QtCore.Qt.white)
        # -------------------------------------- #
        self.polygon = None
        self.polyclosed = False
        self.move_command = None

    def set_tool(self,tool) :
        print("set_tool(self,tool)",tool)
        self.tool=tool

    def set_pen_color(self,color) :
        print("set_pen_color(self,color)",color)
        self.pen.setColor(color)

    # Added
    def set_pen_width(self,width) :
        print("set_pen_width(self,width)",width)
        self.pen.setWidth(width)

    def set_brush_color(self,color) :
       print("set_brush_color(self,color)",color)
       self.color_brush=color
 
    def mousePressEvent(self, event):
        print("Scene.mousePressEvent()")
        self.begin = self.end = event.scenePos()
        self.item=self.itemAt(self.begin,QtGui.QTransform())
        if self. item :
            self.offset =self.begin-self.item.pos()


    def mouseMoveEvent(self, event):
        # print("Scene.mouseMoveEvent()",self.item)
        if self.item :
            self.item.setPos(event.scenePos() - self.offset)
        self.end = event.scenePos()

 
    def mouseReleaseEvent(self, event):
        print("Scene.mouseReleaseEvent()",self.tool)
        self.end = event.scenePos()
        if self.item :
            self.item.setPos(event.scenePos() - self.offset)
            self.item=None
        elif self.tool=='Line' :
            item = QtWidgets.QGraphicsLineItem(self.begin.x(), self.begin.y(),self.end.x(), self.end.y())
            item.setPen(self.pen)
            self.undo_stack.push(AddCommand(self, item))
        elif self.tool=='Rectangle' :
            x = min(self.begin.x(), self.end.x())
            y = min(self.begin.y(), self.end.y())
            w = max(self.begin.x(), self.end.x()) - x
            h = max(self.begin.y(), self.end.y()) - y
            item = QtWidgets.QGraphicsRectItem(x,y,w,h)
            item.setPen(self.pen)
            item.setBrush(self.brush)
            self.undo_stack.push(AddCommand(self, item))
        else:
            print("No item selected and nothing to draw !")
# --------------------------------------------------------------------------------------------------------- #