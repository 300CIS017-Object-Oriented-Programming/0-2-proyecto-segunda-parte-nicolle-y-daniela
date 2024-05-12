

class Evento:
    def __init__(self, nombre, dia, mes, anio):
        self.nombre = nombre
        self.dia = dia
        self.mes = mes
        self.anio = anio

    def set_mes(self,mes):
        self.mes = mes

    def set_anio(self,anio):
        self.anio = anio

    def set_dia(self,dia):
        self.dia = dia

    def set_nombre(self,nombre):
        self.nombre = nombre

    def get_nombre(self):
        return self.nombre

    def get_dia(self):
        return self.dia
    def get_mes(self):
        return self.mes

    def get_anio(self):
        return self.anio

