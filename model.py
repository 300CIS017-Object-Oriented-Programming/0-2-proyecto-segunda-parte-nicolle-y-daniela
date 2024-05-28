class Evento:
    def __init__(self, nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artista=[], sponsors={}):
        self.nombre = nombre
        self.fecha = fecha
        self.hora_apertura = hora_apertura
        self.hora_del_show = hora_del_show
        self.artista = artista
        self.sponsors = sponsors
        self.estado = estado
        self.aforo = aforo
        self.fecha_prev = fecha_prev
        self.fecha_gen = fecha_gen
        self.precio_prev = precio_prev
        self.precio_gen =precio_gen
    
    def calcula_ingreso_prev(self,numero_boletas,precio_prev):
        ingreso_prev_tot = numero_boletas*precio_prev
        return ingreso_prev_tot
    
    def calcula_ingreso_gen(self,numero_boletas,precio_gen):
        ingreso_prev_tot = numero_boletas * precio_gen
        return ingreso_prev_tot
    
    def calcula_ganacia_total(self, ingreso_prev,ingreso_gen):
        ganancia_total= ingreso_gen + ingreso_prev
        return ganancia_total


class Bar(Evento):
    def __init__(self, nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artista):
        super().__init__(nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artista)

    def calcular_ingresos_artista(self, ganancia_total):
        ingresos_totales = ganancia_total * 0,20  # Utilidad del 20%
        return ingresos_totales
    
    def calcular_porcentaje_bar(self,ganancia_total):
        ingresos_tot = ganancia_total * 0,80
        return ingresos_tot

class Teatro(Evento):
    def __init__(self, nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artista, costo_alquiler):
        super().__init__(nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artista, costo_alquiler)
        self.costo_alquiler = costo_alquiler

    def calcular_ingresos_artista_neto(self, ganancia_total):
        ingresos_netos = ganancia_total * 0,93  # Utilidad del 93%
        return ingresos_netos
    
    def calcular_ingresos_artista_con_alq(self, ganancia_total):
        ingresos_netos=self.calcular_ingresos_artista_neto(ganancia_total)
        ingresos_totales= ingresos_netos - self.costo_alquiler
        return ingresos_totales
    
    def calcular_porcentaje_teatro(self,ganancia_total):
        ingresos_tot = ganancia_total * (7/100)
        return ingresos_tot
    

class Filantropo(Evento):
    def __init__(self, nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artista, patrocinadores):
        super().__init__(nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artista, patrocinadores)
        self.patrocinadores = patrocinadores

    def agregar_patrocinador(self, nombre_patrocinador, valor_aportado):
        self.patrocinadores.append((nombre_patrocinador, valor_aportado))

    def calcular_ingresos(self):
        ingresos_totales = sum([valor for _, valor in self.patrocinadores])
        return ingresos_totales

class Usuario:
    def __init__(self, nombre, edad, correo, residencia, cant_boletas, tipo_pago, etapa_de_compra, como_se_entero):
        self.nombre = nombre
        self.edad = edad
        self.correo = correo
        self.residencia = residencia
        self.cant_boletas = cant_boletas
        self.tipo_pago = tipo_pago
        self.etapa_de_compra = etapa_de_compra
        self.como_se_entero = como_se_entero

class Artista:
    
    def __init__(self,nombre,id_art):
        self.nombre=nombre
        self.id_art=id_art