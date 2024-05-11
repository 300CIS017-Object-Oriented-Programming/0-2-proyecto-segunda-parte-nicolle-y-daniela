from Model.Evento import Evento

# Clase para los eventos filantropicos
class Filantropico(Evento):
    def __init__(self, ganancia):
        self.ganancia = ganancia

    # MODIFICADORAS
    def porcentaje(self):