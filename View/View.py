import streamlit as st
from ..Controllers.EveController import EveController as Eve

def crear_even():
    st.header("Crear un evento")
    st.subheader("Información general")
    nom_even = st.text_input("Ingrese el nombre del evento")
    fecha_even = st.date_input("Ingrese la fecha del evento")
    Eve.agregar_lugar(st.selectbox("Selecciona el lugar del evento:", ["BAR", "TEATRO", "FILANTROPO"]))
    st.success(f"Lugar del evento guardado: {Eve.lugar_evento}")
    st.subheader("Agregar artistas")
    nom_artista = st.text_input("Ingrese el nombre del artista")



def menu_general():
    st.title("Gestor de Eventos")
    if st.button("Crear evento"):
        crear_even()




menu_general()