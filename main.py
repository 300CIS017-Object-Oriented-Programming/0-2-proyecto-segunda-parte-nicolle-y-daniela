import streamlit as st
from controller import Controlador
from view import EventView



# Definir la función principal de la aplicación
def main():
    # Titulo
    st.title("Gestor de Eventos de Comedia")

    # Crear una instancia de la clase Controlador para gestionar la lógica de la aplicación
    manager = Controlador()


    # Crear una instancia de la clase EventView para manejar la vista de los eventos
    view = EventView(manager)

    # Ejecutar la aplicación
    view.run()
    manager.inicoo()
# Verificar si este archivo es el punto de entrada principal
if __name__ == "__main__":
    # Llamar a la función principal si este archivo es ejecutado directamente
    main()