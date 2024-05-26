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
            elif menu == "Venta de Boleta":
                self.venta_boleta()
            elif menu == "Ver Reportes":
                self.ver_reportes()
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
        aforo = st.number_input("Aforo del evento", min_value=1)
        nuevo_artista = st.text_input("Nombre del nuevo artista")
        if st.button("Añadir Artista") and nuevo_artista:
            id_art = len(st.session_state['temp_artistas']) + 1
            artista = self.manager.crear_artista(nuevo_artista, id_art)
            st.session_state['temp_artistas'].append(artista)
            st.success(f"Artista '{nuevo_artista}' añadido exitosamente")

        tipo_evento = st.selectbox("Tipo de Evento", ["Evento en Bar", "Evento en Teatro", "Evento Filantrópico"])
        estado = st.selectbox("Estado del Evento", ["Por Realizar", "Realizado", "Cancelado", "Aplazado", "Cerrado"])
        costo_alquiler = 0
        if tipo_evento == "Evento Filantrópico":
            sponsor = st.text_input("Patrocinador")
            aporte = st.number_input("Aporte economico", min_value=1)
            if st.button("Añadir patrocinador") and sponsor and aporte:
                self.manager.agregar_sponsor(nombre, sponsor, aporte)
                st.success(f"Patrocinador '{sponsor}' añadido exitosamente")
            precio_gen=0
            precio_prev=0
            fecha_prev=0
            fecha_gen=0
        if tipo_evento == "Evento en Teatro":
            sponsors = None
            costo_alquiler = st.number_input("Costo de Alquiler", min_value=0)
            precio_prev= st.number_input("Precio boleta preventa",min_value=1)
            precio_gen= st.number_input("Precio boleta normal",min_value=1)
            fecha_prev= st.date_input("Fecha maxima de preventa", datetime.now())
            fecha_gen= st.date_input("Fecha maxima de venta de boleta general", datetime.now())
        if tipo_evento == "Evento en Bar":
            sponsors=None
            precio_prev= st.number_input("Precio boleta preventa",min_value=1)
            precio_gen= st.number_input("Precio boleta normal",min_value=1)
            fecha_prev= st.date_input("Fecha maxima de preventa", datetime.now())
            fecha_gen= st.date_input("Fecha maxima de venta de boleta general", datetime.now())

        if st.button("Crear Evento"):
            artistas = [artista.nombre for artista in st.session_state['temp_artistas']]
            evento = self.manager.creacion_general(tipo_evento, nombre, fecha, hora_apertura, hora_del_show, artistas, costo_alquiler, estado, sponsors, aforo, precio_gen, precio_prev, fecha_gen, fecha_prev)
            if evento:
                st.success(f"Evento '{evento.nombre}' creado exitosamente")
                st.session_state['temp_artistas'] = []

    def editar_eventos(self):
        st.header("Editar un evento")
        eventos = self.manager.obtener_lista_nom_eventos()

        if eventos:
            nombre_evento = st.selectbox("Seleccione el evento a editar", eventos)
            evento = self.manager.obtener_evento(nombre_evento)

            if evento:
                if evento.estado != "Realizado":
                    estados = ["Por Realizar", "Realizado", "Cancelado", "Aplazado", "Cerrado"]
                    if evento.estado in estados:
                        estado_index = estados.index(evento.estado)
                    else:
                        st.warning(f"Estado del evento '{evento.estado}' no reconocido, estableciendo por defecto a 'Por Realizar'")
                        estado_index = 0

                    nuevo_estado = st.selectbox("Estado del Evento", estados, index=estado_index)

                    if st.button("Guardar Cambios"):
                        datos_modificados = {
                            "estado": nuevo_estado,
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

    def venta_boleta(self):
        st.header("Venta Boleta")
        eventos = self.manager.obtener_lista_nom_eventos()

        if eventos:
            nombre_evento = st.selectbox("Seleccione el evento de venta de boleteria", eventos)
            evento = self.manager.obtener_evento(nombre_evento)

            # Solicitar información del comprador
            nombre = st.text_input("Nombre")
            edad = st.number_input("Edad", min_value=0, max_value=150)
            correo = st.text_input("Correo Electrónico")
            residencia = st.text_input("Ciudad de residencia")
            cant_boletas = st.number_input("Cantidad de Boletas", min_value=1)
            etapa_de_compra = st.selectbox("ETAPA DE VENTA", ["Preventa", "Regular", "Cortesia"])
            if etapa_de_compra == "Preventa" or etapa_de_compra == "Regular":
                tipo_pago = st.selectbox("Tipo de Pago", ["Efectivo", "Tarjeta de Crédito", "Tarjeta de Débito",
                                                          "Transferencia Bancaria"])
            else:
                tipo_pago = None
            como_se_entero = st.selectbox("¿Cómo se enteró del evento?", ["Redes sociales", "Por un familiar o amigo", "Carteles publicitarios", "Otro"])

            if st.button("Comprar Boletas"):
                usuario = self.manager.crear_usuario(nombre, edad, correo, residencia, cant_boletas, tipo_pago,como_se_entero,etapa_de_compra)
                self.manager.agregar_info_usu(nombre_evento, usuario)
                mensaje_venta = self.manager.vender_boleta(nombre_evento, usuario)
                st.success(mensaje_venta)
        else:
            st.warning("No hay eventos disponibles para la venta de boletas.")

    def ver_reportes(self):
        st.header("Reportes")
        eventos = self.manager.obtener_lista_nom_eventos()


        if eventos:
            nombre_evento = st.selectbox("Seleccione el evento de venta de boleteria", eventos)
            evento = self.manager.obtener_evento(nombre_evento)
            st.write("Seleccione reporte a analizar")
            info, compra, fig_ciudades, fig_edades, excel_file = self.manager.info(nombre_evento)
            sponsors = self.manager.info_sponsor(nombre_evento)

            bol_prev = info["boletas_tot_efe"] + info["boletas_tot_tc"] + info["boletas_tot_td"] + info["boletas_tot_tb"]
            bol_reg = info["boletas_tot_efe_gen"] + info["boletas_tot_tc_gen"] + info["boletas_tot_td_gen"] + info["boletas_tot_tb_gen"]
            bol_total = bol_reg + bol_prev

            ing_prev = bol_prev * evento.precio_prev
            ing_reg = bol_reg * evento.precio_reg
            ing_total = ing_reg + ing_prev
            #BAR
            ing_tot_sin_bar = ing_total * 0.20
            #TEATRO
                #GANANCIAS DEL TEATRO
            ing_tot_sin_teatro = ing_total * 0.93

            tot_sponsors = 0
            for a in sponsors.values():
                tot_sponsors += a

            ing_p_efe = info["boletas_tot_efe"] * evento.precio_prev
            ing_p_tc = info["boletas_tot_tc"] * evento.precio_prev
            ing_p_td = info["boletas_tot_td"] * evento.precio_prev
            ing_p_tb = info["boletas_tot_tb"] * evento.precio_prev
            ing_r_efe = info["boletas_tot_efe_gen"] * evento.precio_reg
            ing_r_tc = info["boletas_tot_tc_gen"] * evento.precio_reg
            ing_r_td = info["boletas_tot_td_gen"] * evento.precio_reg
            ing_r_tb = info["boletas_tot_tb_gen"] * evento.precio_reg

            if st.button("Ventas de boletas"):
                st.subheader("Reporte de ventas de boletas")
                if evento.tipo_evento == "Evento Filantrópico":
                    st.write("Se vendieron una totalidad de ", bol_total, " boletas de cortesia.")

                elif evento.tipo_evento == " Evento en Teatro" or evento.tipo_evento == "Evento en Bar":
                    st.write("Se vendieron una totalidad de ", bol_total, " boletas.")
                    st.write("Se distribuyen de la siguiente forma:")
                    st.write("BOLETAS REGULARES: ", bol_reg, " boletas, con ingresos de ", ing_reg, " pesos.")
                    st.write("BOLETAS DE PREVENTA: ", bol_prev, " boletas, con ingresos de ", ing_prev, " pesos.")
                    st.write("BOLETAS DE CORTESIA: ", info["boletas_tot_cortesia"], " boletas.")

            if st.button("Financiero"):
                st.subheader("Reporte financiero")

                if evento.tipo_evento == "Evento en Bar":
                    st.write("Se obtuvo un ingreso total de ", ing_total, " pesos, y un total de utilidad de ", ing_tot_sin_bar, " pesos.")
                    st.write("Se distribuyen de la siguiente forma:")
                    st.write("BOLETAS REGULARES:")
                    st.write("Efectivo: ", ing_r_efe, " pesos.")
                    st.write("Tarjeta de credito: ", ing_r_tc, " pesos.")
                    st.write("Tarjeta de debito: ", ing_r_td, " pesos.")
                    st.write("Transferencia bancaria: ", ing_r_tb, " pesos.")
                    st.write("BOLETAS DE PREVENTA:")
                    st.write("Efectivo: ", ing_p_efe, " pesos.")
                    st.write("Tarjeta de credito: ", ing_p_tc, " pesos.")
                    st.write("Tarjeta de debito: ", ing_p_td, " pesos.")
                    st.write("Transferencia bancaria: ", ing_p_tb, " pesos.")

                if evento.tipo_evento == " Evento en Teatro":
                    # TEATRO COSTO ALQUILER
                    ing_prev_alq_teatro = ing_tot_sin_teatro - evento.costo_alquiler
                    st.write("Se obtuvo un ingreso total de ", ing_total, " pesos, y un total de utilidad de ", ing_tot_sin_teatro, " pesos.")
                    st.write("Se obtuvo un ingreso total descontando el alquiler de teatro del ", ing_prev_alq_teatro, "pesos")
                    st.write("Se distribuyen de la siguiente forma:")
                    st.write("BOLETAS REGULARES:")
                    st.write("Efectivo: ", ing_r_efe, " pesos.")
                    st.write("Tarjeta de credito: ", ing_r_tc, " pesos.")
                    st.write("Tarjeta de debito: ", ing_r_td, " pesos.")
                    st.write("Transferencia bancaria: ", ing_r_tb, " pesos.")
                    st.write("BOLETAS DE PREVENTA:")
                    st.write("Efectivo: ", ing_p_efe, " pesos.")
                    st.write("Tarjeta de credito: ", ing_p_tc, " pesos.")
                    st.write("Tarjeta de debito: ", ing_p_td, " pesos.")
                    st.write("Transferencia bancaria: ", ing_p_tb, " pesos.")

                if evento.tipo_evento == "Evento Filantrópico":
                    st.write("Se obtuvo un ingreso total de ", tot_sponsors, " pesos.")
                    st.write("Se distribuyen de la siguiente forma:")
                    for nom, ap in sponsors.items():
                        st.write(f"Sponsor: {nom}, Aporte: {ap}")

            if st.button("Datos de compradores"):
                st.subheader("Reporte de datos de compradores")
                st.write("El analisis de datos de compradores arroja la siguiente informacion:")

                st.plotly_chart(fig_ciudades)
                st.plotly_chart(fig_edades)
                st.download_button(
                    label="Descargar Reporte en Excel",
                    data=open(excel_file, "rb").read(),
                    file_name=excel_file,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.write("La mayoría de compradores provienen de la ciudad: ",
                         compra['ciudad_mas_frecuente']['ciudad'])
                st.write("Ocurrencias: ", compra['ciudad_mas_frecuente']['ocurrencias'])

        else:
            st.warning("No hay eventos disponibles para la venta de boletas.")