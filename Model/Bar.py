from Model.Evento import Evento


class Bar(Evento):
    def __init__(self, bar, come,nombre):
        self.bar = bar
        self.come = come
        self.nombre = nombre


