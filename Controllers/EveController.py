from Model.Bar import Bar
from Model.Teatro import Teatro
from Model.Filantropico import Filantropico as Filan
from Model.Artista import Artista as Art, Artista
from Model.Evento import Evento as Eve
from View.View import View

import streamlit as st

class EveController:

    def __init__(self):
        self.view = view
        self.nom_even = nom_even
        self.fecha = fecha
        self.artista = artista #dicc de artistas
        self.lugar_evento = lugar

    def vermenu(self, ):
        opcion=self.View.menu()
        if opcion=='Crear Evento':
            st.write('Crear Evento')
            ans = st.selectbox("Elige un lugar para el evento", ("BAR", "TEATRO", "FILANTROPO"))
            nombre = st.text_input("Nombre del evento:")
            fecha = st.date_input("Fecha del evento:")
            hora = st.time_input("Hora del evento:")
            if ans=='BAR':
                self.lugar_evento = Bar(self,1, 2, nombre)
            elif ans=='TEATRO':
                self.lugar_evento = Teatro(self,1, 2, nombre)
            elif ans=='FILANTROPO':
                self.lugar_evento = Filan(self,1,nombre)
            if st.button("Enviar Evento"):
                self.guardar_mostrar_evento()


    def guardar_mostrar_evento(self):
        print(self.lugar_evento)
        st.write('Evento agregado con exito')
    

