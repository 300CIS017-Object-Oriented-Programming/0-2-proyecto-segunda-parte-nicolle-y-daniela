import streamlit as st





class View:
    def __init__(self):
        st.title('GESTOR DE EVENTOS')

    def menu(self):
        st.header("Menú de opciones")
        option = st.selectbox("Seleccione una opcion:", ["Crear Evento", "Buscar Evento","Reportes Detallados"])
        return option



