import streamlit as st
from model import Evento, Bar, Teatro, Filantropo,Artista

class Controlador:
    def __init__(self):
        if 'events' not in st.session_state:
            st.session_state['events'] = []
        if 'artistas_por_evento' not in st.session_state:
            st.session_state['artistas_por_evento'] = {}
        if 'logged_in' not in st.session_state:
            st.session_state['logged_in'] = False

    def iniciar_sesion(self, username, password):
        # Aquí puedes agregar la lógica para validar el usuario
        # Por ahora, solo validaremos con un usuario y contraseña fijo
        if username == 'admin' and password == 'password':
            st.session_state['logged_in'] = True
            return True
        return False

    @property
    def artistas_por_evento(self):
        return st.session_state['artistas_por_evento']
    
    def obtener_nombre(self, nombre):
        a=""
        for evento in st.session_state['events']:
            if evento.nombre == nombre:
                a=evento.nombre
        return a

    def obtener_evento(self, nombre):
        a=None
        for evento in st.session_state['events']:
            if evento.nombre==nombre:
                a=evento
        return a

    def obtener_lista_nom_eventos(self):
        return [evento.nombre for evento in st.session_state['events']]
    
    def obtener_eventos(self):
        return st.session_state['events']
    
    def comprobar_si_esta_vacio(self):
        return len(st.session_state['events']) == 0
    
    def editar_evento(self, nombre, datos_modificados):
        a=False
        evento = self.obtener_evento(nombre)
        if evento and evento.estado!="Realizado":
            evento.artista = datos_modificados.get('artista', evento.artista)
            evento.estado = datos_modificados.get('estado', evento.estado)
            evento.fecha = datos_modificados.get('fecha', evento.fecha)
            a=True
        return evento,a

    def crear_evento_bar(self, nombre, fecha, hora_apertura, hora_del_show, artista, estado):
        evento = Bar(nombre, fecha, hora_apertura, hora_del_show, artista, estado)
        st.session_state['events'].append(evento)
        self.artistas_por_evento[nombre] = set(artista)
        return evento
    
    def crear_evento_teatro(self, nombre, fecha, hora_apertura, hora_del_show, artista, costo_alquiler, estado):
        evento = Teatro(nombre, fecha, hora_apertura, hora_del_show, artista, costo_alquiler, estado)
        st.session_state['events'].append(evento)
        self.artistas_por_evento[nombre] = set(artista)
        return evento
    
    def crear_evento_filantropo(self, nombre, fecha, hora_apertura, hora_del_show, artista, sponsors, estado):
        evento = Filantropo(nombre, fecha, hora_apertura, hora_del_show, artista, sponsors, estado)
        st.session_state['events'].append(evento)
        self.artistas_por_evento[nombre] = set(artista)
        return evento

    def creacion_general(self, opcion, nombre, fecha, hora_apertura, hora_del_show, artista, costo_alquiler, estado, sponsors=[]):
        a=None
        if opcion == "Evento en Bar":
            a= self.crear_evento_bar(nombre, fecha, hora_apertura, hora_del_show, artista, estado)
        elif opcion == "Evento en Teatro":
            a= self.crear_evento_teatro(nombre, fecha, hora_apertura, hora_del_show, artista, costo_alquiler, estado)
        elif opcion == "Evento Filantrópico":
            a= self.crear_evento_filantropo(nombre, fecha, hora_apertura, hora_del_show, artista, sponsors, estado)
        return a

    def cambiar_estado_evento(self, nombre, nuevo_estado):
        a=None
        evento = self.obtener_evento(nombre)
        if evento:
            a= evento.cambiar_estado(nuevo_estado)
        return a
    
    def eliminar_evento(self, nombre):
        x=" "
        evento = self.obtener_evento(nombre)
        if evento and evento.estado != "Realizado":
            st.session_state['events'].remove(evento)
            x="Eliminado"
        elif evento:
            x="No se puede eliminar un evento con boletería vendida"
        elif evento==False:
            x="No se encontró el evento"
        return x
    
    def verificar_artistas_por_evento(self, nombre, artistas):
        a=True
        artistas_evento = self.artistas_por_evento.get(nombre, [])  # Obtener la lista de artistas para el evento
        for artista in artistas:
            if artista in artistas_evento:
                a=False
        return a

    def crear_artista(self,nombre,id_art):
        artista = Artista(nombre, id_art)
        return artista
    
    def obtener_lista_artistas(self, nombre):
        return self.artistas_por_evento.get(nombre, set())
    
    def agregar_artista(self, nombre_evento, artista):
        # Verificar si ya existe el evento en el diccionario
        if nombre_evento not in self.artistas_por_evento:
            self.artistas_por_evento[nombre_evento] = []  # Inicializar lista de artistas si es necesario
        # Agregar el artista a la lista de artistas del evento
        self.artistas_por_evento[nombre_evento].append(artista)

        