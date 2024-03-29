from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve

import sys      

class OpenFileUi(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('buscando.ui', self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowOpacity(0)
        
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(500) 
        self.animation.setStartValue(0)  
        self.animation.setEndValue(1)   
        self.animation.setEasingCurve(QEasingCurve.InOutQuad) 
                
    def openAnimation(self, event):
        self.animation.start()
        super().showEvent(event)
   

class InitialWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('base.ui', self)
        self.setup()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
    def setup(self):
        self.salir_2.clicked.connect(self.saliendo)
        self.aBoton.clicked.connect(self.create)
        self.bBoton.clicked.connect(self.reader)
        self.acBoton.clicked.connect(self.updater)
        self.eBoton.clicked.connect(self.deleter)
        
    def saliendo(self):
        sys.exit(app.exec_())    
        
    def create(self):
        self.popup = OpenFileUi()
        self.popup.show()
        
    def reader(self):
        self.stackedWidget.setCurrentIndex(0)

    def updater(self):
        self.stackedWidget.setCurrentIndex(2)

    def deleter(self):
        self.stackedWidget.setCurrentIndex(1)
 
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = InitialWindow()
    login_window.show()
    sys.exit(app.exec_())
