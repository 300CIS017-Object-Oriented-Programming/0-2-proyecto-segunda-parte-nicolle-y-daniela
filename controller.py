import streamlit as st
from model import Evento, Bar, Teatro, Filantropo,Artista,Usuario
from fpdf import FPDF
from collections import Counter
import pandas as pd
from collections import Counter
import plotly.express as px
import xlsxwriter
import plotly.graph_objs as go
#Clase que se encarga de la funciones principales y relaciona los tipos de eventos, los usuarios y los artistas
class Controlador:
    #contenedores para guardar datos globales de artistas, eventos y guardar informacion importante de los eventos
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
    # metodo que se encarga de iniciar sesion
    def iniciar_sesion(self, username, password):
        # Aquí puedes agregar la lógica para validar el usuario
        # Por ahora, solo validaremos con un usuario y contraseña fijo
        if username == 'admin' and password == '1':
            st.session_state['logged_in'] = True
            return True
        return False
    # Metodo para facilitar el llamado del contenedor de artistas
    @property
    def artistas_por_evento(self):
        return st.session_state['artistas_por_evento']
    # metodo que facilita la obtencion de los nombre de los eventos
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
    # retorna una lista con todos los nombres de los eventos existentes
    def obtener_lista_nom_eventos(self):
        return [evento.nombre for evento in st.session_state['events']]
    # retorna todo el contenedor de eventos
    def obtener_eventos(self):
        return st.session_state['events']
    # retorna true si el contednedor si está vacio, (que no tiene eventos)
    def comprobar_si_esta_vacio(self):
        return len(st.session_state['events']) == 0
    # Verifica si está permitido editar un evento
    def editar_evento(self, nombre, datos_modificados):
        a=False
        evento = self.obtener_evento(nombre)
        if evento and evento.estado!="Realizado":
            evento.estado = datos_modificados.get('estado', evento.estado)
            a=True
        return evento,a
    # Facilita la construccion de un objeto tipo bar con todos los atributos generales de la clase evento
    def crear_evento_bar(self, nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artista):
        evento = Bar(nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artista)
        st.session_state['events'].append(evento)
        self.artistas_por_evento[nombre] = set(artista)
        return evento
    # Facilita la construccion de un objeto tipo bar con todos los atributos generales de la clase teatro
    def crear_evento_teatro(self, nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artista, costo_alquiler):
        evento = Teatro(nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artista, costo_alquiler)
        st.session_state['events'].append(evento)
        self.artistas_por_evento[nombre] = set(artista)
        return evento
    # Facilita la construccion de un objeto tipo bar con todos los atributos generales de la clase filantropo
    def crear_evento_filantropo(self, nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artista, sponsors):
        evento = Filantropo(nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artista, sponsors)
        st.session_state['events'].append(evento)
        self.artistas_por_evento[nombre] = set(artista)
        return evento
    # DEpendiendo del tipo de evento permite crear cualquiera de los eventos sin errores
    def creacion_general(self, opcion, nombre, fecha, hora_apertura, hora_del_show, costo_alquiler, estado, aforo, precio_gen, precio_prev, fecha_gen, fecha_prev, artistas=[], sponsors={}):
        a=None
        if opcion == "Evento en Bar":
            a= self.crear_evento_bar(nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artistas)
        elif opcion == "Evento en Teatro":
            a= self.crear_evento_teatro(nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artistas, costo_alquiler)
        elif opcion == "Evento Filantrópico":
            a= self.crear_evento_filantropo(nombre, fecha, hora_apertura, hora_del_show, estado, precio_prev, precio_gen, fecha_prev, fecha_gen, aforo, artistas, sponsors)
        return a
    #permite cambiar internamente el estado del evento
    def cambiar_estado_evento(self, nombre, nuevo_estado):
        a=None
        evento = self.obtener_evento(nombre)
        if evento:
            a= evento.cambiar_estado(nuevo_estado)
        return a
    # Quita el evento del contenedor de todos los eventos
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
    # Revia si el nombre del artista ingresado ya está ingresado en la lista
    def verificar_artistas_por_evento(self, nombre, artistas):
        a = True
        artistas_evento = self.artistas_por_evento.get(nombre, [])  # Obtener la lista de artistas para el evento
        artistas_nombres = [a.nombre if isinstance(a, Artista) else a for a in artistas_evento]  # Convertir objetos Artista a sus nombres
        for artista in artistas:
            if artista in artistas_nombres:
                a = False
        return a
    # Crea un nuevo objeto de tipo artista
    def crear_artista(self, nombre, id_art):
        return Artista(nombre, id_art)
    # Retorna la lista de los artistas
    def obtener_lista_artistas(self, nombre):
        return self.artistas_por_evento.get(nombre, set())
    # Despues de verificar si el artista está en la lista crea uno nuevo o si está en la lista solo lo agrega al evento
    def agregar_artista(self, nombre_evento, nuevo_artista):
        if nombre_evento not in self.artistas_por_evento:
            self.artistas_por_evento[nombre_evento] = set()
        self.artistas_por_evento[nombre_evento].add(nuevo_artista.nombre)
        st.session_state['temp_artistas'].append(nuevo_artista)
    # Verifica si el sponsor ya está en la lista y si no lo agrega y agrega su aporte economica al evento
    def agregar_sponsor(self, nombre_evento, nombre_sponsor, aporte):
        if 'sponsors' not in st.session_state:
            st.session_state['sponsors'] = {}

        if nombre_evento not in st.session_state['sponsors']:
            st.session_state['sponsors'][nombre_evento] = set()

        # Convert the dictionary to a tuple of tuples
        info = tuple(sorted({'nombre': nombre_sponsor, 'aporte': aporte}.items()))

        st.session_state['sponsors'][nombre_evento].add(info)
    # Retorna un diccionario con la informacion de los patrocinadores de un evento en especifico
    def info_sponsor(self, nombre_evento):
        info = {}

        if nombre_evento in st.session_state['sponsors']:
            for sponsor in st.session_state['sponsors'][nombre_evento]:
                print("Sponsor dictionary:", sponsor)  # Add this line for debugging
                if 'nombre' in sponsor and 'aporte' in sponsor:
                    info[sponsor['nombre']] = sponsor['aporte']
                else:
                    print("Missing keys in sponsor dictionary:", sponsor)  # Add this line for debugging

        return info
    # Agrega un usuario a la ista de usuarios
    def agregar_info_usu(self, nombre_evento, usuario):
        if nombre_evento not in st.session_state['info_usu']:
            st.session_state['info_usu'][nombre_evento] = set()
        st.session_state['info_usu'][nombre_evento].add(usuario)
    #retorna la informacion de los compradores
    def info(self, nombre_evento):
    # Check if 'info_usu' and the event name key exists in the session state
        if 'info_usu' not in st.session_state:
            st.session_state['info_usu'] = {}

        if nombre_evento not in st.session_state['info_usu']:
            st.session_state['info_usu'][nombre_evento] = []

        info_espe = {}
        info_compra = {}
        boletas_tot_efe = 0
        boletas_tot_tc = 0
        boletas_tot_td = 0
        boletas_tot_tb = 0
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

        ciudad_mas_frecuente = ciudades_counter.most_common(1)[0] if ciudades_counter else ("None", 0)
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
        excel_file = 'reporte_compradores.xlsx'
        with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
            df_ciudades.to_excel(writer, sheet_name='Ciudades', index=False)
            df_edades.to_excel(writer, sheet_name='Edades', index=False)
            df_enterado.to_excel(writer, sheet_name='Enterado', index=False)

        return info_espe, info_compra, fig_ciudades, fig_edades, excel_file
    # Retorna ell objeto nuevo de usuario
    def crear_usuario(self, nombre, edad, correo, residencia, cant_boletas, tipo_pago, etapa_de_compra, como_se_entero):
        return Usuario(nombre, edad, correo, residencia, cant_boletas, tipo_pago, etapa_de_compra, como_se_entero)
    # Verifica si hay disponibilidad de aforo en el evento
    def verificar_aforo(self,nombre):
        a=True
        evento=self.obtener_evento(nombre)
        if st.session_state['aforo']< evento.aforo:
            a=False
        return a
    # Suma al contador de aforo
    def actualizar_aforo(self, evento, cantidad_boletas):
        st.session_state['aforo'] += cantidad_boletas
    # Genera un pdf con toda la informaacion del usuario al comprar la boleta
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
    # Maneja la venta de la boleta internamente para que la informacion financiera se actualice correctamente
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
    # identifica el lugar donde se realizará el evento
    def determinar_tipo_evento(self,evento):
        x=""
        if isinstance(evento, Bar):
            x= 'Bar'
        elif isinstance(evento, Teatro):
            x= 'Teatro'
        elif isinstance(evento, Filantropo):
            x= 'Filantropo'
        return x
    #retorna los eventos en los que un artista participa
    def obtener_eventos_por_artista(self,artista, eventos):
        eventos_artista = []
        for evento in eventos:
            if artista in evento.artista:
                eventos_artista.append(evento)
        return eventos_artista
    # Retorn una lista con los artistas de un evento en especifico
    def imprimir_artistas(self,eventos):
        artistas_set = set()
        for evento in eventos:
            artistas_evento = evento.artista
            for artisti in artistas_evento:
                artistas_set.add(artisti)
        return artistas_set
    
    #Maneja el filtrado de eventos por fechas
    def obtener_eventos_filtrados(self, eventos, fecha_inicio, fecha_fin):
        return [evento for evento in eventos if fecha_inicio <= evento.fecha <= fecha_fin]
    # maneja el dash board
    def dash_board(self, eventos, fecha_inicio, fecha_fin):
        eventos_filtrados = self.obtener_eventos_filtrados(eventos, fecha_inicio, fecha_fin)
        
        tipo_evento_list = []
        ingresos_totales_list = []

        for evento in eventos_filtrados:
            tipo_evento = self.determinar_tipo_evento(evento)
            info_espe, info_compra, fig_ciudades, fig_edades, excel_file = self.info(evento.nombre)

            boletas_tot_efe = info_espe.get("boletas_tot_efe", 0)
            boletas_tot_tc = info_espe.get("boletas_tot_tc", 0)
            boletas_tot_td = info_espe.get("boletas_tot_td", 0)
            boletas_tot_tb = info_espe.get("boletas_tot_tb", 0)
            boletas_tot_efe_gen = info_espe.get("boletas_tot_efe_gen", 0)
            boletas_tot_tc_gen = info_espe.get("boletas_tot_tc_gen", 0)
            boletas_tot_td_gen = info_espe.get("boletas_tot_td_gen", 0)
            boletas_tot_tb_gen = info_espe.get("boletas_tot_tb_gen", 0)

            precio_prev = evento.precio_prev
            precio_gen = evento.precio_gen

            ing_prev = (boletas_tot_efe + boletas_tot_tc + boletas_tot_td + boletas_tot_tb) * precio_prev
            ing_reg = (boletas_tot_efe_gen + boletas_tot_tc_gen + boletas_tot_td_gen + boletas_tot_tb_gen) * precio_gen
            ingresos_totales = ing_prev + ing_reg

            tipo_evento_list.append(tipo_evento)
            ingresos_totales_list.append(ingresos_totales)

        data = {
            'Tipo de Evento': tipo_evento_list,
            'Ingresos Totales': ingresos_totales_list
        }

        df = pd.DataFrame(data)

        # Gráfico de cantidad de eventos por tipo
        fig1 = px.histogram(df, x='Tipo de Evento', title='Cantidad de Eventos por Tipo')

        # Gráfico de ingresos totales por evento
        fig2 = px.bar(df, x='Tipo de Evento', y='Ingresos Totales', title='Ingresos Totales por Tipo de Evento')

        # Crear el dashboard con ambos gráficos
        dashboard = go.Figure(data=fig1.data + fig2.data)

        # Personalizar diseño del dashboard
        dashboard.update_layout(title='Dashboard - Gestión de Eventos',
                                xaxis_title='Tipo de Evento',
                                yaxis_title='Cantidad / Ingresos Totales')

        # Mostrar el dashboard
        st.plotly_chart(dashboard)