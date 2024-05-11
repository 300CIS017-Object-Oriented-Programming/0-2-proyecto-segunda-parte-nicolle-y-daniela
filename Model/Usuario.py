# Clase que guarda la informacion de cada usuario que compra boletas
class Usuario:
    # Datos importantes del usuario
    def __init__(self, nombre, edad, ciudad, correo, cant_bols, id_comp, tipo_pago, dia, mes, anio):
        self.nombre = nombre
        self.edad = edad
        self.ciudad = ciudad
        self.correo = correo
        self.cant_bols = cant_bols
        self.id_comp = id_comp
        self.tipo_pago = tipo_pago
        self.dia = dia
        self.mes = mes
        self.anio = anio

    # MODIFICADORAS
    def set_nombre(self, nombre):

    def set_edad(self, edad):

    def set_ciudad(self, ciudad):

    def set_correo(self, correo):

    def set_cant_bols(self, cant_bols):

    def set_id_comp(self, id_comp):

    def set_tipo_pago(self, tipo_pago):

    def set_dia(self, dia):

    def set_mes(self, mes):

    def set_anio(self, anio):

    # ANALIZADORAS
    def get_nombre(self):

    def get_edad(self):

    def get_ciudad(self):

    def get_correo(self):

    def get_cant_bols(self):

    def get_id_comp(self):

    def get_tipo_pago(self):

    def get_dia(self):

    def get_mes(self):

    def get_anio(self):