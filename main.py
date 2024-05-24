import streamlit as st
from controller import Controlador
from view import EventView

def main():
    st.title("Gestor de Eventos de Comedia")
    manager = Controlador()
    view = EventView(manager)
    view.run()

if __name__ == "__main__":
    main()