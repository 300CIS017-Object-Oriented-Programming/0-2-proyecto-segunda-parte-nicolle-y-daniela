import streamlit as st
from datetime import datetime
import streamlit as st
from datetime import datetime
from event_model import Event

class EventView:
    def __init__(self, manager):
        self.manager = manager

    def run(self):
        st.sidebar.title("Menú")
        menu = st.sidebar.selectbox("Seleccione una opción", ["Crear Evento", "Editar Evento", "Eliminar Evento", "Ver Reportes"])

        if menu == "Crear Evento":
            self.create_event_view()
        elif menu == "Editar Evento":
            self.edit_event_view()
        elif menu == "Eliminar Evento":
            self.delete_event_view()
        elif menu == "Ver Reportes":
            self.view_reports()

    def create_event_view(self):
        st.header("Crear un nuevo evento")

        # Entrada del usuario
        nombre = st.text_input("Nombre del Evento")
        fecha = st.date_input("Fecha del Evento", datetime.now())
        hora_apertura = st.time_input("Hora de Apertura de Puertas", datetime.now().time())
        hora_del_show = st.time_input("Hora del Show", datetime.now().time())
        artista = st.text_input("Artista(s)").split(",")
        event_type = st.selectbox("Tipo de Evento", ["Evento en Bar", "Evento en Teatro", "Evento Filantrópico"])

        sponsors = []
        if event_type == "Evento Filantrópico":
            sponsors_input = st.text_area("Patrocinadores (nombre:valor)").split(",")
            sponsors = [s.split(":") for s in sponsors_input]

        # Creación del evento y almacenamiento
        if st.button("Crear Evento"):
            evento = self.manager.agregar_evento(nombre, fecha, hora_apertura, hora_del_show, artista, sponsors)
            st.success(f"Evento '{evento.nombre}' creado exitosamente")

    def edit_event_view(self):
        st.header("Editar un evento")
        eventos = self.manager.get_events()

        if eventos!=None:
            # Mostrar la lista de eventos
            st.write("Lista de eventos:")
            event_names = [evento.nombre for evento in eventos]
            for event_name in event_names:
                st.write(event_name)

            # Entrada de texto para buscar un evento por nombre
            event_name_to_edit = st.text_input("Ingrese el nombre del evento a editar")

            # Botón para buscar el evento
            if st.button("Buscar Evento"):
                event_found = False
                for evento in eventos:
                    if evento.nombre.lower() == event_name_to_edit.lower():
                        event_found = True
                        # Aquí puedes continuar con el resto de tu lógica para editar el evento usando el nombre del evento
                        st.success(f"Evento '{evento.nombre}' encontrado. Puedes continuar con la edición.")
                        nuevos_datos = {
                            "nombre": st.text_input("Nuevo Nombre", evento.nombre),
                            "fecha": st.date_input("Nueva Fecha", evento.fecha),
                            "hora_apertura": st.time_input("Nueva Hora de Apertura", evento.hora_apertura),
                            "hora_del_show": st.time_input("Nueva Hora del Show", evento.hora_del_show),
                            "artista": st.text_input("Nuevo Artista(s)", ",".join(evento.artista)).split(","),
                            "sponsors": st.text_area("Nuevos Patrocinadores (nombre:valor)", ",".join([":".join(s) for s in evento.sponsors])).split(",")
                        }
                        # Botón para guardar los cambios
                        if st.button("Guardar Cambios"):
                            event = self.manager.editar_evento(event_name_to_edit, nuevos_datos)
                            if event:
                                st.success(f"Evento '{event.nombre}' actualizado exitosamente")
                            else:
                                st.error("Error al actualizar el evento")
                        break
                
                if not event_found:
                    st.error(f"No se encontró ningún evento con el nombre '{event_name_to_edit}'. Por favor, inténtelo de nuevo.")
        else:
            st.warning("No hay eventos disponibles para editar.")


    def delete_event_view(self):
        st.header("Eliminar un evento")
        event_name = st.text_input("Nombre del Evento a Eliminar")
        if st.button("Eliminar Evento"):
            mensaje = self.manager.delete_event(event_name)
            if mensaje is None:
                st.success(f"Evento '{event_name}' eliminado exitosamente")
            else:
                st.error(mensaje)

    def view_reports(self):
        st.header("Ver reportes")
        eventos = self.manager.get_events()
        if eventos:
            for evento in eventos:
                st.subheader(evento.nombre)
                st.text(f"Fecha: {evento.fecha}")
                st.text(f"Hora de Apertura: {evento.hora_apertura}")
                st.text(f"Hora del Show: {evento.hora_del_show}")
                st.text(f"Artista(s): {', '.join(evento.artista)}")
                st.text(f"Estado: {evento.estado}")
                st.text(f"Boletas Vendidas: {evento.tickets_sold}")
                if evento.sponsors:
                    st.text("Patrocinadores:")
                    for sponsor in evento.sponsors:
                        st.text(f"  - {sponsor[0]}: {sponsor[1]}")
        else:
            st.text("No hay eventos para mostrar.")
