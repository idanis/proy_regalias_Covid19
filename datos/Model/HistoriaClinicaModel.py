class HistoriaClinicaModel:

    def __init__(self):
        self.edad = 0
        self.menor_18 = 0
        self.entre_18_30 = 0
        self.entre_30_50 = 0
        self.entre_50_70 = 0
        self.mayor_70 = 0
        self.sexo = 0
        self.tos = 0
        self.fiebre = 0
        self.dificultad_respiratoria = 0
        self.fatiga = 0
        self.odinofagia = 0
        self.cefalea = 0
        self.rinorrea = 0
        self.diarrea = 0
        self.hipertension = 0
        self.diabetes = 0
        self.obesidad = 0
        self.enfermedades_respiratorias = 0
        self.asma = 0
        self.fumador = 0
        self.enf_cardiaca = 0
        self.cancer = 0
        self.ins_renal = 0

    def setRangoEdad(self):
        if self.edad < 18:
            self.menor_18 = 1
        elif 18 <= self.edad < 30:
            self.entre_18_30 = 1
        elif 30 <= self.edad < 50:
            self.entre_30_50 = 1
        elif 50 <= self.edad < 70:
            self.entre_50_70 = 1
        elif self.edad >= 70:
            self.mayor_70 = 1



