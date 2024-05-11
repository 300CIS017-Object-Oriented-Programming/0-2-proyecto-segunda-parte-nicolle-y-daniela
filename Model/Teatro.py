from Model.Evento import Evento

# Clase para los eventos en el teatro
class Teatro(Evento):
    def __init__(self, alquiler, teatro, come):
        self.alquiler = alquiler
        self.teatro = teatro
        self.come = come

    # MODIFICADORAS
    def porcentaje(self):

    def set_alquiler(self, alquiler):

    # ANALIZADORAS
    def get_alquiler(self):