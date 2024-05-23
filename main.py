import streamlit as st
from event_controller import ComedyEventManager
from event_view import EventView

def main():
    st.title("Gestor de Eventos de Comedia")
    manager = ComedyEventManager()
    view = EventView(manager)
    view.run()

if __name__ == "__main__":
    main()
