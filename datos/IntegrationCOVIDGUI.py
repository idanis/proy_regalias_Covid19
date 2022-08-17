import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import *
from COVIDGUI import DiagnosticoCovid19
from Model.HistoriaClinicaModel import  HistoriaClinicaModel as HC
from pyH2oMojo import H2oMojoPredictor
import h2o
import pandas as pd
import time
import threading

class DiagnosticoCovidApplication(QDialog):

    def __init__(self):
        super().__init__()

        self.ui = DiagnosticoCovid19()
        self.ui.setupUi(self)

        self.ui.enviar.clicked.connect(self.ejecutar)
        self.show()

    def replace_value (self,value):
        if value:
            return 1
        return 0
    def replace_sexo (self,value):
        if value == 'Femenino':
            return 0
        return 1

    def valid_dict(self):

        for key in self.data.keys():
            value = self.data.get(key)
            if  value !=0 and key != 'sexo':
                return True
        return False

    @pyqtSlot()
    def ejecutar(self):


        self.edad = self.ui.edad.text()
        if self.edad == '0':
            QMessageBox.critical(self, "Error", "Debe diligenciar la edad")
            return

        self.sexo = self.ui.sexo.currentText()
        self.fiebre = self.ui.fiebre.isChecked()
        self.tos = self.ui.tos.isChecked()
        self.dificultad_respiratoria = self.ui.dificultad_respiratoria.isChecked()
        self.fatiga = self.ui.fatiga.isChecked()
        self.odinofagia = self.ui.odinofagia.isChecked()
        self.dolor_cabeza = self.ui.dolor_cabeza.isChecked()
        self.rinorrea = self.ui.rinorrea.isChecked()
        self.diarrea = self.ui.diarrea.isChecked()
        self.data = {'sexo': self.replace_sexo(self.sexo), 'tos': self.replace_value(self.tos),
                'fiebre': self.replace_value(self.fiebre),
                'fatiga': self.replace_value(self.fatiga),
                'dificultad_respiratoria': self.replace_value(self.dificultad_respiratoria),
                'odinofagia': self.replace_value(self.odinofagia),
                'rinorrea': self.replace_value(self.rinorrea),
                'diarrea': self.replace_value(self.diarrea), 'cefalea': self.replace_value(self.dolor_cabeza)}
        if self.valid_dict():
            self.ui.loading.setText("Procesando .........")
            global data_from_thread
            data_from_thread = self.data
            self.worker = WorkerThread()
            self.worker.start()
            self.worker.update_progress.connect(self.finish_message2)
        else:
            QMessageBox.critical(self,"Error","Debe diliginciar al menos un dato")

    def finish_message2(self,value):
        QMessageBox.information(self,"Resultado","La probabilidad de tener COVID {}%".format(value))
        self.ui.loading.setText("")





class WorkerThread (QThread):
    #worker_complete = pyqtSignal(float)
    update_progress = pyqtSignal(float)

    def run(self):
        saved_model = h2o.load_model("Model/GBM_grid_1_AutoML_1_20211218_122220_model_106")
        df = pd.DataFrame(data_from_thread, index=[0])
        data_h2o = h2o.H2OFrame(df)
        prediccion = saved_model.predict(data_h2o)
        data_as_df = prediccion.as_data_frame()
        result = data_as_df.iloc[0, 2]

        round_result = round(float(result) * 100, 2)

        self.update_progress.emit(round_result)

if __name__ == '__main__':
    app  = QApplication(sys.argv)
    h2o.init()
    ventana = DiagnosticoCovidApplication()
    ventana.show()
    sys.exit(app.exec_())
