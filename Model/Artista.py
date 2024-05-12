

class Artista:
    def __init__(self, nombre_art,cod_art,evento_participo):
        self.nombre_art = nombre_art
        self.cod_art = cod_art
        self.evento_participo= evento_participo

    def get_nombre_art(self):
        return self.nombreArt

    def get_mes(self):
        return self.mes

    def get_anio(self):
        return self.anio

    def get_dia(self):
        return self.dia

    def get_cod_art(self):
        return self.codArt

    def get_evento_participo(self):
        return self.evento_participo

    def set_nombre_art(self, nombre_art):
        self.nombreArt = nombre_art

    def set_cod_art(self, cod_art):
        self.codArt = cod_art

    def set_mes(self, mes):
        self.mes = mes

    def set_anio(self, cod_anio):
        self.anio = cod_anio

    def set_dia(self, dia):
        self.dia = dia

    def set_evento_participo(self, evento_participo):
        self.evento_participo = evento_participo
