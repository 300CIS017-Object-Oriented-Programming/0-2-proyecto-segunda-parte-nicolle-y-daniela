import streamlit as st
from model import Evento, Bar, Teatro, Filantropo,Artista,Usuario
from fpdf import FPDF
from collections import Counter
import pandas as pd
from collections import Counter
import plotly.express as px
import xlsxwriter
import plotly.graph_objs as go

class Controlador:
    if 'events' not in st.session_state:
            st.session_state['events'] = []
    if 'artistas_por_evento' not in st.session_state:
        st.session_state['artistas_por_evento'] = {}
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'temp_artistas' not in st.session_state:
        st.session_state['temp_artistas'] = []
    if 'aforo' not in st.session_state:
            st.session_state['aforo'] = 0
    if 'info_usu' not in st.session_state:
        st.session_state['info_usu'] = {}
    if 'sponsors' not in st.session_state:
        st.session_state['sponsors'] = {}

    def iniciar_sesion(self, username, password):
        # Aquí puedes agregar la lógica para validar el usuario
        # Por ahora, solo validaremos con un usuario y contraseña fijo
        if username == 'admin' and password == '1':
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
            evento.estado = datos_modificados.get('estado', evento.estado)
            a=True
        return evento,a

    def crear_evento_bar(self, nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artista):
        evento = Bar(nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artista)
        st.session_state['events'].append(evento)
        self.artistas_por_evento[nombre] = set(artista)
        return evento
    
    def crear_evento_teatro(self, nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artista, costo_alquiler):
        evento = Teatro(nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artista, costo_alquiler)
        st.session_state['events'].append(evento)
        self.artistas_por_evento[nombre] = set(artista)
        return evento
    
    def crear_evento_filantropo(self, nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artista, sponsors):
        evento = Filantropo(nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artista, sponsors)
        st.session_state['events'].append(evento)
        self.artistas_por_evento[nombre] = set(artista)
        return evento

    def creacion_general(self, opcion, nombre, fecha, hora_apertura, hora_del_show, costo_alquiler, estado, aforo, precio_gen, precio_prev, fecha_gen, fecha_prev, artistas=[], sponsors={}):
        a=None
        if opcion == "Evento en Bar":
            a= self.crear_evento_bar(nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artistas)
        elif opcion == "Evento en Teatro":
            a= self.crear_evento_teatro(nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artistas, costo_alquiler)
        elif opcion == "Evento Filantrópico":
            a= self.crear_evento_filantropo(nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artistas, sponsors)
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
        a = True
        artistas_evento = self.artistas_por_evento.get(nombre, [])  # Obtener la lista de artistas para el evento
        artistas_nombres = [a.nombre if isinstance(a, Artista) else a for a in artistas_evento]  # Convertir objetos Artista a sus nombres
        for artista in artistas:
            if artista in artistas_nombres:
                a = False
        return a

    def crear_artista(self, nombre, id_art):
        return Artista(nombre, id_art)
    
    def obtener_lista_artistas(self, nombre):
        return self.artistas_por_evento.get(nombre, set())
    
    def agregar_artista(self, nombre_evento, nuevo_artista):
        if nombre_evento not in self.artistas_por_evento:
            self.artistas_por_evento[nombre_evento] = set()
        self.artistas_por_evento[nombre_evento].add(nuevo_artista.nombre)
        st.session_state['temp_artistas'].append(nuevo_artista)

    def agregar_sponsor(self, nombre_evento, nombre_sponsor, aporte):
        if nombre_evento not in st.session_state['sponsors']:
            st.session_state['sponsors'][nombre_evento] = set()
        info = {
            'nombre': nombre_sponsor,
            'aporte': aporte
        }
        st.session_state['sponsors'][nombre_evento].add(info)

    def info_sponsor(self, nombre_evento):
        info = {}

        if nombre_evento in st.session_state['sponsors']:
            for sponsor in st.session_state['sponsors'][nombre_evento]:
                info[sponsor['nombre']] = sponsor['aporte']

        return info

    def agregar_info_usu(self, nombre_evento, usuario):
        if nombre_evento not in st.session_state['info_usu']:
            st.session_state['info_usu'][nombre_evento] = set()
        st.session_state['info_usu'][nombre_evento].add(usuario)

    def info(self,nombre_evento):
        info_espe={}
        info_compra={}
        boletas_tot_efe= 0
        boletas_tot_tc=0
        boletas_tot_td=0
        boletas_tot_tb=0
        boletas_tot_efe_gen = 0
        boletas_tot_tc_gen = 0
        boletas_tot_td_gen = 0
        boletas_tot_tb_gen = 0
        boletas_tot_cortesia = 0

        ciudades_counter = Counter()
        edades_counter = Counter()
        enterado_counter = Counter()

        ciudades = []
        edades = []
        enteradas = []

        for i in st.session_state['info_usu'][nombre_evento]:

            ciudades.append(i.residencia)
            edades.append(i.edad)
            enteradas.append(i.como_se_entero)

            if i.etapa_de_compra == "Preventa":
                if i.tipo_pago == "Efectivo":
                    boletas_tot_efe += i.cant_boletas
                if i.tipo_pago == "Tarjeta de Crédito":
                    boletas_tot_tc += i.cant_boletas
                if i.tipo_pago == "Tarjeta de Débito":
                    boletas_tot_td += i.cant_boletas
                if i.tipo_pago == "Transferencia Bancaria":
                    boletas_tot_tb += i.cant_boletas

            elif i.etapa_de_compra == "Regular":
                if i.tipo_pago == "Efectivo":
                    boletas_tot_efe_gen += i.cant_boletas
                if i.tipo_pago == "Tarjeta de Crédito":
                    boletas_tot_tc_gen += i.cant_boletas
                if i.tipo_pago == "Tarjeta de Débito":
                    boletas_tot_td_gen += i.cant_boletas
                if i.tipo_pago == "Transferencia Bancaria":
                    boletas_tot_tb_gen += i.cant_boletas

            elif i.etapa_de_compra == "Cortesia":
                boletas_tot_cortesia += i.cant_boletas

        for ciu in ciudades:
            ciudades_counter[ciu] += 1

        for eda in edades:
            edades_counter[eda] += 1

        for ent in enteradas:
            enterado_counter[ent] += 1
        ciudad_mas_frecuente = ciudades_counter.most_common(1)[0]
        resultados = {
            "boletas_tot_efe": boletas_tot_efe,
            "boletas_tot_tc": boletas_tot_tc,
            "boletas_tot_td": boletas_tot_td,
            "boletas_tot_tb": boletas_tot_tb,
            "boletas_tot_efe_gen": boletas_tot_efe_gen,
            "boletas_tot_tc_gen": boletas_tot_tc_gen,
            "boletas_tot_td_gen": boletas_tot_td_gen,
            "boletas_tot_tb_gen": boletas_tot_tb_gen,
            "boletas_tot_cortesia": boletas_tot_cortesia
        }

        resultados_compra = {
            "ciudad_mas_frecuente": {
                "ciudad": ciudad_mas_frecuente[0],
                "ocurrencias": ciudad_mas_frecuente[1]
            },
            "edades": dict(edades_counter),
            "enterado": dict(enterado_counter)
        }
        info_espe = resultados
        info_compra = resultados_compra

        df_ciudades = pd.DataFrame(list(ciudades_counter.items()), columns=["Ciudad", "Cantidad"])
        df_edades = pd.DataFrame(list(edades_counter.items()), columns=["Edad", "Cantidad"])
        df_enterado = pd.DataFrame(list(enterado_counter.items()), columns=["Enterado", "Cantidad"])

        # Crear gráficos con Plotly
        fig_ciudades = px.bar(df_ciudades, x="Ciudad", y="Cantidad", title="Distribución de Compradores por Ciudad")
        fig_edades = px.bar(df_edades, x="Edad", y="Cantidad", title="Distribución de Compradores por Edad")

        # Exportar datos a Excel
        with pd.ExcelWriter('reporte_compradores.xlsx', engine='xlsxwriter') as writer:
            df_ciudades.to_excel(writer, sheet_name='Ciudades', index=False)
            df_edades.to_excel(writer, sheet_name='Edades', index=False)
            df_enterado.to_excel(writer, sheet_name='Enterado', index=False)
            writer.close()

        return info_espe, info_compra, fig_ciudades, fig_edades, 'reporte_compradores.xlsx'

    def crear_usuario(self, nombre, edad, correo, residencia, cant_boletas, tipo_pago, etapa_de_compra, como_se_entero):
        return Usuario(nombre, edad, correo, residencia, cant_boletas, tipo_pago, etapa_de_compra, como_se_entero)
    
    def verificar_aforo(self,nombre):
        a=True
        evento=self.obtener_evento(nombre)
        if st.session_state['aforo']< evento.aforo:
            a=False
        return a

    def actualizar_aforo(self, evento, cantidad_boletas):
        st.session_state['aforo'] += cantidad_boletas

    def generar_pdf_boleta(self, usuario, evento):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Boleta para el evento {evento.nombre}", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Nombre: {usuario.nombre}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Correo: {usuario.correo}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Residencia: {usuario.residencia}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Cantidad de Boletas: {usuario.cant_boletas}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Tipo de Pago: {usuario.tipo_pago}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Evento: {evento.nombre}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Fecha: {evento.fecha}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Hora del Show: {evento.hora_del_show}", ln=True, align='L')
        pdf_file_name = f"{usuario.nombre}_boleta.pdf"
        pdf.output(pdf_file_name)
        
        return pdf_file_name

    def vender_boleta(self, nombre, usuario):
        x = ""
        evento = self.obtener_evento(nombre)
        if evento:
            verifico = self.verificar_aforo(nombre)
            if not verifico:
                if usuario.etapa_de_compra == "Preventa":
                    total_precio = evento.calcula_ingreso_prev(usuario.cant_boletas, evento.precio_prev)
                else:
                    total_precio = evento.calcula_ingreso_gen(usuario.cant_boletas, evento.precio_gen)

                self.actualizar_aforo(evento, usuario.cant_boletas)
                boleta_pdf_file = self.generar_pdf_boleta(usuario, evento)
                mensaje_venta = f"¡Venta completada para el evento {evento.nombre}! Precio total: {total_precio}"

                if mensaje_venta:
                    st.success(mensaje_venta)
                    st.write("Información de la boleta:")
                    st.download_button(
                        label="Descargar Boleta",
                        data=open(boleta_pdf_file, "rb").read(),  # Lee el archivo PDF como bytes
                        file_name=f"{usuario.nombre}_boleta.pdf",  # Asigna el nombre del archivo PDF
                        mime="application/pdf"
                    )
            else:
                x = "No hay suficiente disponibilidad de aforo para la cantidad de boletas solicitadas."
        else:
            x = "El evento no existe."
        return x
    
    def determinar_tipo_evento(self,evento):
        x=""
        if isinstance(evento, Bar):
            x= 'Bar'
        elif isinstance(evento, Teatro):
            x= 'Teatro'
        elif isinstance(evento, Filantropo):
            x= 'Filantropo'
        return x
        
    def obtener_eventos_por_artista(self,artista, eventos):
        eventos_artista = []
        for evento in eventos:
            if artista in evento.artista:
                eventos_artista.append(evento)
        return eventos_artista
    
    def imprimir_artistas(self,eventos):
        artistas_set = set()
        for evento in eventos:
            artistas_evento = evento.artista
            for artisti in artistas_evento:
                artistas_set.add(artisti)
        return artistas_set
    
    def dash_board(self,eventos):
        data = {
        'Tipo de Evento': [evento.tipo for evento in eventos],
        'Ingresos Totales': [evento.ingresos_totales() for evento in eventos]
        }
        df = pd.DataFrame(data)
        
        return df
        #FALTA COMPLETAR
