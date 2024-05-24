import streamlit as st
from datetime import datetime
import streamlit as st
from datetime import datetime
from model import  Evento
from model import  Bar
from model import  Teatro
from model import  Filantropo
from model import Artista

class EventView:
    def __init__(self, manager):
        self.manager = manager

    def run(self):
        if not st.session_state['logged_in']:
            self.login()
        else:
            st.sidebar.title("Menú")
            menu = st.sidebar.selectbox("Seleccione una opción", ["Crear Evento", "Editar Evento", "Eliminar Evento", "Venta de Boleta", "Ver Reportes"])

            if menu == "Crear Evento":
                self.crear_eventos()
            elif menu == "Editar Evento":
                self.editar_eventos()
            elif menu == "Eliminar Evento":
                self.eliminar_eventos()
            elif menu == "Ver Reportes":
                self.ver_reportes()
            elif menu == "Venta de Boleta":
                self.venta_boleta()
            if st.sidebar.button("Cerrar sesión"):
                st.session_state['logged_in'] = False

    def login(self):
        st.header("Inicio de Sesión")
        username = st.text_input("Nombre de Usuario")
        password = st.text_input("Contraseña", type="password")
        if st.button("Iniciar Sesión"):
            if self.manager.iniciar_sesion(username, password):
                st.success("Inicio de sesión exitoso")
            else:
                st.error("Nombre de usuario o contraseña incorrectos")

    def crear_eventos(self):
        st.header("Crear un nuevo evento")
        nombre = st.text_input("Nombre del Evento")
        fecha = st.date_input("Fecha del Evento", datetime.now())
        hora_apertura = st.time_input("Hora de Apertura de Puertas", datetime.now().time())
        hora_del_show = st.time_input("Hora del Show", datetime.now().time())
        nuevo_artista = st.text_input("Nombre del nuevo artista")
        if st.button("Añadir Artista"):  # Verificar si se proporcionó un nombre de artista
            verf_art=self.manager.verificar_artistas_por_evento(nombre,nuevo_artista) #COMPROBAR VERIFICACION NO ESTA FUNCIONANDO BIEN
            if verf_art:
                st.error("El artista ya está añadido al evento")
            elif verf_art==False:
                # Asignar un código único al artista (longitud actual de la lista de artistas)
                id_art = len(self.manager.obtener_lista_artistas(nombre)) + 1
                # Crear un nuevo objeto Artista y agregarlo a la lista de artistas
                artista = self.manager.crear_artista(nuevo_artista, id_art)
                self.manager.agregar_artista_eve(nuevo_artista) # Agregar el nombre del artista al conjunto
                st.success(f"Artista '{nuevo_artista}' añadido exitosamente")

        tipo_evento = st.selectbox("Tipo de Evento", ["Evento en Bar", "Evento en Teatro", "Evento Filantrópico"])
        estado = st.selectbox("Estado del Evento", ["Por Realizar", "Realizado", "Cancelado", "Aplazado", "Cerrado"])
        sponsors = []
        costo_alquiler = 0
        if tipo_evento == "Evento Filantrópico":
            sponsors = st.text_area("Patrocinadores (nombre:valor)").split(",")
        if tipo_evento == "Evento en Teatro":
            costo_alquiler = st.number_input("Costo de Alquiler", min_value=0)

        if st.button("Crear Evento"):
            evento = self.manager.creacion_general(tipo_evento, nombre, fecha, hora_apertura, hora_del_show, artista, costo_alquiler, estado, sponsors)
            if evento:
                st.success(f"Evento '{evento.nombre}' creado exitosamente")

    def editar_eventos(self):
        st.header("Editar un evento")
        eventos = self.manager.obtener_lista_nom_eventos()

        if eventos:
            nombre_evento = st.selectbox("Seleccione el evento a editar", eventos)
            evento = self.manager.obtener_evento(nombre_evento)

            if evento:
                if evento.estado != "Realizado":
                    nuevo_estado = st.selectbox("Estado del Evento", ["Por Realizar", "Realizado", "Cancelado", "Aplazado", "Cerrado"], index=["Por Realizar", "Realizado", "Cancelado", "Aplazado", "Cerrado"].index(evento.estado))
                    nueva_fecha = st.date_input("Nueva Fecha", evento.fecha)
                    nuevos_artistas = st.text_input("Nuevo Artista(s)", ",".join(evento.artista)).split(",")

                    if st.button("Guardar Cambios"):
                        datos_modificados = {
                            "estado": nuevo_estado,
                            "fecha": nueva_fecha,
                            "artista": nuevos_artistas,
                        }
                        evento_modificado, actualizado = self.manager.editar_evento(nombre_evento, datos_modificados)
                        if actualizado:
                            st.success(f"Evento '{evento_modificado.nombre}' actualizado exitosamente")
                        else:
                            st.error("Error al actualizar el evento")
                else:
                    st.error("No se puede modificar un evento ya realizado.")
            else:
                st.error("No se encontró el evento seleccionado.")
        else:
            st.warning("No hay eventos disponibles para editar.")

    def eliminar_eventos(self):
        st.header("Eliminar un evento")
        eventos = self.manager.obtener_lista_nom_eventos()

        if eventos:
            nombre_evento = st.selectbox("Seleccione el evento a eliminar", eventos)

            if st.button("Eliminar Evento"):
                mensaje = self.manager.eliminar_evento(nombre_evento)
                if mensaje == "Eliminado":
                    st.success(f"Evento '{nombre_evento}' eliminado exitosamente")
                else:
                    st.error(mensaje)
        else:
            st.warning("No hay eventos disponibles para eliminar.")

