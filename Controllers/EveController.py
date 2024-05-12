
from Model.Artista import Artista as Art, Artista


class EveController:

    def __init__(self):
        self.lugar_evento = None
        self.fecha_evento = None
        self.artista = []
        self.num_artista = None


    def agregar_lugar(self):

        cant_lugar= {
            "BAR",
            "TEATRO",
            "FILANTROPO"
        }
        self.lugar_evento= self.lugar_evento["clave"]

    def set_num_artista(self,numero):
        self.num_artista = numero

    def get_num_artista(self):
        return self.num_artista

    def agregar_artista(self):
        num=self.num_artista
        i=0
        lista_artistas
        for i in range(num):
            self.artista = Artista("clave")
