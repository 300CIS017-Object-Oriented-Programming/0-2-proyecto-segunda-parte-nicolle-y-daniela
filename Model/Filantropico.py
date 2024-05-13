from Model.Evento import Evento

# Clase para los eventos filantropicos
class Filantropico(Evento):
    def __init__(self, ganancia,nombre):
        self.ganancia = ganancia
        self.nombre = nombre

    # MODIFICADORAS
    #def porcentaje(self):