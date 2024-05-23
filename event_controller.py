from event_model import Event

class ComedyEventManager:
    def __init__(self):
        self.events = []
        self.nombre_even=[]

    def get_event_by_name(self, event_name):
        return next((event for event in self.events if event.nombre == event_name), None)
    
    def create_event(self, event):
        self.events.append(event)


    def delete_event(self, event_name):
        event = self.get_event_by_name(event_name)
        if event and event.tickets_sold == 0:
            self.events.remove(event)
            return None
        elif event:
            return "No se puede eliminar un evento con boletería vendida"
        else:
            return "No se encontró el evento"

    def get_events(self):
        return self.events

    def agregar_evento(self, nombre, fecha, hora_apertura, hora_del_show, artista, sponsors=[]):
        evento = Event(nombre, fecha, hora_apertura, hora_del_show, artista, sponsors)
        self.create_event(evento)
        return evento

    def editar_evento(self, nombre, nuevos_datos):
        event = self.get_event_by_name(nombre)
        if event:
            event.nombre = nuevos_datos.get('nombre', event.nombre)
            event.fecha = nuevos_datos.get('fecha', event.fecha)
            event.hora_apertura = nuevos_datos.get('hora_apertura', event.hora_apertura)
            event.hora_del_show = nuevos_datos.get('hora_del_show', event.hora_del_show)
            event.artista = nuevos_datos.get('artista', event.artista)
            event.sponsors = nuevos_datos.get('sponsors', event.sponsors)
            return event
        return None

    def cambiar_estado_evento(self, nombre, nuevo_estado):
        event = self.get_event_by_name(nombre)
        if event:
            return event.cambiar_estado(nuevo_estado)
        return None

