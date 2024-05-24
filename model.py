class Evento:
    def __init__(self, nombre, fecha, hora_apertura, hora_del_show, estado,artista=[], sponsors=[]):
        self.nombre = nombre
        self.fecha = fecha
        self.hora_apertura = hora_apertura
        self.hora_del_show = hora_del_show
        self.artista = artista
        self.sponsors = sponsors
        self.estado = estado

    def cambiar_estado(self, nuevo_estado):
        if self.estado != "Realizado":
            self.estado = nuevo_estado
        else:
            return "No se puede cambiar el estado de un evento realizado"
        
    def get_nombre(self):
        return self.nombre

    #def agregar_art(self,nombre_art,codigo_art):
    #  nombre_art=Art(nombre_art,codigo_art)

class Bar(Evento):
    def __init__(self, nombre, fecha, hora_apertura, hora_del_show, artista,estado):
        super().__init__(nombre, fecha, hora_apertura, hora_del_show, artista,estado)

    def calcular_ingresos(self, numero_boletas_vendidas):
        ingresos_totales = numero_boletas_vendidas * 20  # Utilidad del 20%
        return ingresos_totales

class Teatro(Evento):
    def __init__(self, nombre, fecha, hora_apertura, hora_del_show, artista, costo_alquiler,estado):
        super().__init__(nombre, fecha, hora_apertura, hora_del_show, artista,costo_alquiler,estado)
        self.costo_alquiler = costo_alquiler

    def calcular_ingresos(self, numero_boletas_vendidas):
        ingresos_totales = numero_boletas_vendidas * 0.93  # Retención del 7%
        return ingresos_totales

class Filantropo(Evento):
    def __init__(self, nombre, fecha, hora_apertura, hora_del_show, artista,estado,patrocinadores=[]):
        super().__init__(nombre, fecha, hora_apertura, hora_del_show, artista,estado)
        self.patrocinadores = patrocinadores

    def agregar_patrocinador(self, nombre_patrocinador, valor_aportado):
        self.patrocinadores.append((nombre_patrocinador, valor_aportado))

    def calcular_ingresos(self):
        ingresos_totales = sum([valor for _, valor in self.patrocinadores])
        return ingresos_totales

class Usuario:
    def __init__(self,nombre,edad,correo,residencia,cant_boletas,id_compra,tipo_pago):
        self.nombre=nombre
        self.edad=edad
        self.correo=correo
        self.residencia=residencia
        self.cant_boletas=cant_boletas
        self.id_compra=id_compra
        self.tipo_pago=tipo_pago


class Artista:
    
    def __init__(self,nombre,id_art):
        self.nombre=nombre
        self.id_art=id_art