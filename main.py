from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QObject, pyqtSignal
from PyQt5 import QtGui
from model import create as creator
from model import findAll, eliminador, find

import sys    

class Communicate(QObject):
    fileSelected = pyqtSignal(str)  

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
        self.communicate = Communicate()
        self.setup()
                
    def showEvent(self, event):
        self.animation.start()
        super().showEvent(event)
        
    def setup(self):
        self.pushButton.clicked.connect(self.openFile)
        self.buttonBox.accepted.connect(self.fileOppened)
        self.buttonBox.rejected.connect(self.notSelected)
    
    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Select File", "", "Text Files (*.txt);;CSV Files (*.csv);;JSON Files (*.json)", options=options)

    def fileOppened(self):
        try:
            self.communicate.fileSelected.emit(self.fileName)
        finally:
            self.close()

    def notSelected(self):
        self.fileName = 0
        self.close()
        
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(self.mapToGlobal(event.pos() - self.offset))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False


class InitialWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('base.ui', self)
        self.setup()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowIcon(QtGui.QIcon('imgs/hospital.png'))
        
    def setup(self):
        self.updateComboBoxes()
        self.salir_2.clicked.connect(self.saliendo)
        self.aBoton.clicked.connect(self.create)
        self.bBoton.clicked.connect(self.reader)
        self.acBoton.clicked.connect(self.updater)
        self.eBoton.clicked.connect(self.deleter)
        self.minimizar.clicked.connect(self.minimizator)
        self.confirm.clicked.connect(self.eliminarPaciente)
        self.comboBox_3.currentTextChanged.connect(self.asiBuscamos)
        
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        try:
            if self.dragging:
                self.move(self.mapToGlobal(event.pos() - self.offset))
        except:
            pass

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
        
    def updateComboBoxes(self):
        dataToPut = findAll()
        self.comboBox.clear()
        self.comboBox_2.clear()
        self.comboBox_3.clear()
        self.comboBox.addItem('')
        self.comboBox_2.addItem('')
        self.comboBox_3.addItem('')
        self.comboBox.addItems(dataToPut)
        self.comboBox_2.addItems(dataToPut)
        self.comboBox_3.addItems(dataToPut)
        self.comboBox.setCurrentIndex(0)
        self.comboBox_2.setCurrentIndex(0)
        self.comboBox_3.setCurrentIndex(0)
        
    def saliendo(self):
        sys.exit(app.exec_())    
        
    def create(self):
        self.popup = OpenFileUi()
        self.popup.communicate.fileSelected.connect(self.getFile)
        self.popup.show()
        
    def getFile(self, path):
        val = creator([path])
        print(val)
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        if val == "":
            val = "Creado satisfactoriamente"
        msgBox.setText(val)
        msgBox.setWindowTitle('Ventana de información')
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()
        self.updateComboBoxes()
        
    def eliminarPaciente(self):
        id_to_delete = self.comboBox_2.currentText()
        val = eliminador(id_to_delete)
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(val)
        msgBox.setWindowTitle('Aviso Eliminación')
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()
        self.deletedd.setText(val)
        self.updateComboBoxes()
        
    def asiBuscamos(self):
        idBuscar = self.comboBox_3.currentText()
        if idBuscar == '':
            pass
        else:
            result = find(idBuscar)
            info_paciente = f'''
    Paciente: {result['nombre']} {result['apellido']} de genero {result['sexo']} y {result['edad']} años.
    Medico: {result['especialidad']} {result['médico']}.
    Fecha: {result['fecha'][0:4]}-{result['fecha'][4:6]}-{result['fecha'][6:8]}
            '''
            self.textBrowser.setText(info_paciente) 
        
    def reader(self):
        self.stackedWidget.setCurrentIndex(0)

    def updater(self):
        self.stackedWidget.setCurrentIndex(2)

    def deleter(self):
        self.stackedWidget.setCurrentIndex(1)
        
    def minimizator(self):
        self.showMinimized()
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = InitialWindow()
    login_window.show()
    sys.exit(app.exec_())
