from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QMessageBox, QVBoxLayout, QLabel, QLineEdit, QScrollArea
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QObject, pyqtSignal, QDate
from PyQt5 import QtGui
from infosss import create as creator
from infosss import findAll, eliminador, find, updateDB

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
        self.folderName = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)

    def fileOppened(self):
        try:
            self.communicate.fileSelected.emit(self.folderName)
        except:
            self.communicate.fileSelected.emit('')
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
        try:
            if self.dragging:
                self.move(self.mapToGlobal(event.pos() - self.offset))
        except:
            print("???")

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
        self.comboBox.currentTextChanged.connect(self.asiActualizamos)
        self.updaterr.clicked.connect(self.actualizadorrr)
        
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
        try:
            val = creator(path)
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            if val == "":
                val = "Importado satisfactoriamente"
            msgBox.setText(val)
            msgBox.setWindowTitle('Ventana de información')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
            self.updateComboBoxes()
        except TypeError:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Error al importar el archivo, intente nuevamente')
            msgBox.setWindowTitle('Error')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        
        
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
            self.textBrowser.setText('')
        else:
            result = find(idBuscar)[0]
            info_paciente = f'''
    Paciente: {result['nombre']} {result['apellido']} de genero {result['sexo']} y {result['edad']} años.
    Medico: {result['médico']} - {result['especialidad']}
    Fecha: {result['fecha'][0:4]}-{result['fecha'][4:6]}-{result['fecha'][6:8]}
    IPS: {result['ips']}
    Diagnóstico: {result['dx']}
    
    Examenes:\n'''

            for key in result['examen']:
                info_paciente += f'   - {key}: {result["examen"][key]}\n'
            info_paciente+='\n  Comorbilidades:\n'
            for comorbilidad in result['Comorbilidades']:
                info_paciente+=f'   - {comorbilidad}\n'
            
            self.textBrowser.setText(info_paciente) 
        
    def asiActualizamos(self):
        idBuscar = self.comboBox.currentText()
        if idBuscar == '':
            pass
        else:    
            result = find(idBuscar)[0]
            list_res = [(self.nombre, 'nombre'), (self.apellidos, 'apellido'), (self.edad, 'edad'), (self.medico, 'médico'),(self.ips, 'ips'), (self.diagnostico, 'dx')]
            for i,j in list_res:
                i.setText(str(result[j]))
            dateNew = QDate(int(result['fecha'][0:4]), int(result['fecha'][4:6]), int(result['fecha'][6:8]))
            self.fecha.setDate(dateNew)
            text=''
            for key in result['examen']:
                text += f'-   {key}: {result["examen"][key]}\n'
            text+='\n\nPara añadir un nuevo resultado de examen, por favor ingresarlas con un guión (-) al inicio'
            self.examte.setText(text)
            text = ''
            for comorbilidad in result['Comorbilidades']:
                print(comorbilidad)
                text+=f'-   {comorbilidad}\n'
            text+='\n\nPara añadir una nueva comorbilidad, por favor ingresarlas con un guión (-) al inicio'
            self.combte.setText(text)
            
    def actualizadorrr(self):
        idpaciente = self.comboBox.currentText()
        if idpaciente == '':
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('No hay una identificación para editar')
            msgBox.setWindowTitle('Error')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        else:
            nombre = self.nombre.text()
            apellidos = self.apellidos.text()
            edad = self.edad.text()
            medico = self.medico.text()
            ips = self.ips.text()
            diagnostico = self.diagnostico.text()
            fecha = ''.join(self.fecha.date().toString('yyyy-MM-dd').split('-'))
            comorbilidades = [i for i in self.combte.toPlainText().splitlines() if (i.startswith('-'))]
            comorbilidades = [' '.join([i for i in comorbilidad.replace('-', '').split(' ') if i != '']) for comorbilidad in comorbilidades]
            examenes = [i for i in self.examte.toPlainText().splitlines() if (i.startswith('-') and ":" in i)]
            examenes = {examen.replace('-', '').replace(' ', '').split(':')[0]: examen.replace('-', '').replace(' ', '').split(':')[1] for examen in examenes}
            updateDB(idpaciente, nombre, apellidos, edad, medico, ips, diagnostico, fecha, comorbilidades, examenes)
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText('Actualización satisfactoria')
            msgBox.setWindowTitle('Aviso de actualización')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        
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
