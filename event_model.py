class Event:
    def __init__(self, nombre, fecha, hora_apertura, hora_del_show, artista, sponsors=[]):
        self.nombre = nombre
        self.fecha = fecha
        self.hora_apertura = hora_apertura
        self.hora_del_show = hora_del_show
        self.artista = artista
        self.sponsors = sponsors
        self.estado = "por realizar"
        self.tickets_sold = 0

    def cambiar_estado(self, nuevo_estado):
        if self.estado != "realizado":
            self.estado = nuevo_estado
        else:
            return "No se puede cambiar el estado de un evento realizado"
        
    def get_nombre(self):
        return self.nombre

    def vender_boleta(self, cantidad):
        self.tickets_sold += cantidad

