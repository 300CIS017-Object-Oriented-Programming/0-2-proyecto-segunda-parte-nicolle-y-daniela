
from Model.Artista import Artista as Art, Artista
from Model.Evento import Evento as Eve

class EveController:

    def __init__(self):
        self.lugar_evento = None #contenedor nombre evento
        self.fecha_evento = None #lista
        self.artista = [] #dicc de artistas


    def agregar_lugar(self, lugar_seleccionado):
        self.lugar_evento = lugar_seleccionado

    def set_num_artista(self,numero):
        self.num_artista = numero

    def get_num_artista(self):
        return self.num_artista

    def encontrar_art(self, nombrex):
        a=0
        for artista in self.artistas:
            if artista.nombre_art == nombrex:
                codigo_art= artista.cod_art
                Eve.agregar_art2(nombrex,codigo_art)
                a=1
        return a

    def agregar_artista(self,cod_Art, nombre_arte=None):
        nombre=Artista(self,nombre_arte,cod_Art)
        self.artista.append(nombre)

