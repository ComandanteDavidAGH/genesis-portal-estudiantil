import streamlit as st
import pandas as pd
from supabase import create_client
import time
import base64

# =================================================================
# ⚡ NITRO TURBO: CONFIGURACIÓN INICIAL DE ALTA VELOCIDAD
# =================================================================
st.set_page_config(
    page_title="Génesis - Zona Escolar", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicialización de variables de control en memoria activa
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'datos_alumno' not in st.session_state:
    st.session_state.datos_alumno = None

# --- 🖼️ CACHÉ ULTRARRÁPIDA: PROCESAMIENTO ÚNICO DEL ESCUDO ---
@st.cache_data(show_spinner=False)
def cargar_escudo_local():
    try:
        with open("escudo.png", "rb") as image_file:
            return f"data:image/png;base64,{base64.b64encode(image_file.read()).decode()}"
    except Exception:
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

escudo_seguro = cargar_escudo_local()

# --- ⚙️ SIFÓN DE CONEXIÓN: ENLACE ÚNICO CON EL SERVIDOR ---
@st.cache_resource(show_spinner=False)
def iniciar_conexion():
    return create_client(st.secrets["SUPABASE_URL"].strip(), st.secrets["SUPABASE_KEY"].strip())

supabase = iniciar_conexion()

# --- 🚀 EL TURBO NITRO: DESCARGA MASIVA Y PRECARGA EN CACHÉ LOCAL ---
# Esto descarga toda la tabla una sola vez. Los clics siguientes toman 0 segundos.
@st.cache_data(ttl=300, show_spinner=False)
def descargar_toda_la_data_institucional():
    try:
        respuesta = supabase.table("data_estudiantes").select("*").execute()
        df = pd.DataFrame(respuesta.data)
        # Estandarizamos nombres de columnas a mayúsculas para evitar errores
        df.columns = [str(c).upper() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Error en Sifón de Datos: {e}")
        return pd.DataFrame()

# =================================================================
# 🎨 ESTILOS INSTITUCIONALES PREMIUM Y BLINDAJE ANTI-GATO
# =================================================================
st.markdown("""
<style>
    /* Ocultamiento absoluto de la barra de herramientas Streamlit (Gato, Share, Ajustes) */
    footer {visibility: hidden !important;}
    [data-testid="stToolbarActions"] {display: none !important;}
    [data-testid="stToolbarShareButton"] {display: none !important;}
    .stActionButton {display: none !important;}
    header {visibility: hidden !important;}
    
    /* Contenedor del Cuadro Académico Oficial */
    [data-testid="stDataFrame"] {
        border-left: 3px solid #0d1b2a !important;
        border-right: 3px solid #0d1b2a !important;
        border-bottom: 3px solid #0d1b2a !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        margin-top: -10px !important; 
        box-shadow: 0px 5px 15px rgba(0,0,0,0.15) !important;
    }
    
    /* Panel de Control HUD */
    .hud-box {
        background: linear-gradient(135deg, #0d1b2a 0%, #1a365d 100%);
        border-left: 5px solid #d4af37;
        padding: 15px; border-radius: 8px; 
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.3); margin-bottom: 20px;
    }
    .hud-item { text-align: center; border-right: 1px solid rgba(255,255,255,0.1); }
    .hud-item:last-child { border-right: none; }
    .hud-title { font-size: 11px; color: #a8b2d1; font-family: 'Arial Black', sans-serif; text-transform: uppercase; margin: 0; letter-spacing: 1px; }
    .hud-value { font-size: 24px; color: #ffffff; font-weight: 900; margin: 0; }
    .hud-value-gold { color: #d4af37; }
    .hud-value-green { color: #00ff66; }
    .hud-value-red { color: #ff3333; }

    /* Barra Lateral */
    [data-testid="stSidebar"] { background-color: #0d1b2a; color: white; border-right: 2px solid #d4af37; }
    [data-testid="stSidebar"] * { color: white !important; }
    
    .titulo-seccion { color: #0d1b2a; font-family: 'Arial Black', sans-serif; border-bottom: 2px solid #d4af37; padding-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

# =================================================================
# 🛡️ PANTALLA DE LOGUEO (Verificación Inmediata contra Caché)
# =================================================================
def mostrar_login():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; margin-bottom: 10px;'><img src='{escudo_seguro}' width='140'></div>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #0d1b2a; margin-top: 0; font-family: Arial Black;'>GÉNESIS</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #d4af37; font-weight: bold; margin-top: -10px;'>PORTAL ESCOLAR ESTUDIANTIL</p>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("#### Control de Acceso")
            doc_ingresado = st.text_input("Ingrese su ID Estudiantil o Código Maestro:", placeholder="Ej: 001").strip()
            autenticar = st.button("Acceder a Zona Escolar", type="primary", use_container_width=True)
            
            if autenticar and doc_ingresado:
                clave_secreta = st.secrets.get("CODIGO_MAESTRO", "ADMIN_FALLBACK_2026").strip()
                
                if doc_ingresado == clave_secreta:
                    st.session_state.autenticado = True
                    st.session_state.datos_alumno = {
                        'NOMBRE_COMPLETO': "OPERADOR / ADMIN GENERAL",
                        'GRADO': "ADMIN CORE",
                        'ID_ESTUDIANTE': "MASTER_CONTROL"
                    }
                    st.success("🔓 Acceso de Administrador Supremo Concedido")
                    time.sleep(0.4)
                    st.rerun()
                else:
                    df_global = descargar_toda_la_data_institucional()
                    if not df_global.empty and 'ID_ESTUDIANTE' in df_global.columns:
                        coincidencias = df_global[df_global['ID_ESTUDIANTE'].astype(str).str.lower() == doc_ingresado.lower()]
                        if not coincidencias.empty:
                            st.session_state.autenticado = True
                            st.session_state.datos_alumno = coincidencias.iloc[0].to_dict()
                            st.success(f"Acceso concedido a {st.session_state.datos_alumno['NOMBRE_COMPLETO']}")
                            time.sleep(0.4)
                            st.rerun()
                    st.error("Credencial inválida o no registrada.")

# =================================================================
# 📊 GENERADOR DE BOLETINES COMPLETO (Súper Acelerado en Local)
# =================================================================
def seccion_boletin():
    st.markdown("<h2 class='titulo-seccion'>&#x1F4CA; Mi Boletín de Calificaciones</h2>", unsafe_allow_html=True)
    
    # 🏎️ Llamada al Turbo Nitro: Extraemos la data completa de la memoria instantánea
    df_completo = descargar_toda_la_data_institucional()
    
    if df_completo.empty:
        st.warning("La base de datos institucional está vacía o desconectada.")
        return

    es_admin = (st.session_state.datos_alumno.get('ID_ESTUDIANTE') == "MASTER_CONTROL")

    # 🎛️ CONTROL MAESTRO: DOS SELECTORES INDEPENDIENTES (GRADO Y ALUMNO)
    if es_admin:
        st.info("💡 MODO INSPECTOR GENERAL: Filtre por Grado y Alumno para auditar la libreta académica al instante.")
        
        # Selector 1: Grados únicos disponibles en el DataFrame local (Velocidad: 0 segundos)
        lista_grados = sorted(df_completo['GRADO'].dropna().unique().tolist())
        grado_seleccionado = st.selectbox("📁 1. Seleccione el Grado Escolar:", lista_grados)
        
        # Filtramos la data local solo por ese grado para alimentar el segundo selector
        df_filtrado_grado = df_completo[df_completo['GRADO'] == grado_seleccionado]
        
        # Selector 2: Alumnos pertenecientes únicamente a ese grado seleccionado
        lista_alumnos = sorted(df_filtrado_grado['NOMBRE_COMPLETO'].dropna().unique().tolist())
        alumno_seleccionado = st.selectbox("👤 2. Seleccione el Alumno a Consultar:", lista_alumnos)
        
        # Extraemos el registro exacto del alumno elegido
        registro_alumno = df_filtrado_grado[df_filtrado_grado['NOMBRE_COMPLETO'] == alumno_seleccionado]
    else:
        # Si es un alumno normal, el registro se extrae filtrando directamente por su ID de sesión
        registro_alumno = df_completo[df_completo['ID_ESTUDIANTE'].astype(str) == str(st.session_state.datos_alumno.get('ID_ESTUDIANTE'))]

    if registro_alumno.empty:
        st.error("No se encontraron registros para la selección actual.")
        return

    # =================================================================
    # 🧮 MOTOR DE CÁLCULO LOGÍSTICO (PROMEDIOS Y SEMÁFOROS)
    # =================================================================
    # Convertimos los periodos a numéricos asegurando que no rompan el sistema
    for p in ['P1', 'P2', 'P3', 'P4']:
        if p in registro_alumno.columns:
            registro_alumno[p] = pd.to_numeric(registro_alumno[p], errors='coerce').fillna(0.0)
            
    # Calculamos el Promedio por asignatura de manera local
    registro_alumno['PROMEDIO'] = registro_alumno[['P1', 'P2', 'P3', 'P4']].mean(axis=1).round(1)
    
    # Extraemos variables para los bloques superiores HUD
    promedio_general_colegio = round(registro_alumno['PROMEDIO'].mean(), 1)
    total_materias = len(registro_alumno)
    materias_aprobadas = len(registro_alumno[registro_alumno['PROMEDIO'] >= 6.0])
    
    color_promedio = "hud-value-green" if promedio_general_colegio >= 9.0 else ("hud-value-gold" if promedio_general_colegio >= 6.0 else "hud-value-red")
    nombre_sujeto = alumno_seleccionado if es_admin else st.session_state.datos_alumno['NOMBRE_COMPLETO']

    # 📊 PANEL HUD PREMIUM DINÁMICO
    st.markdown(f"""
    <div class="hud-box">
        <div class="hud-item"><p class="hud-title">Periodo Académico</p><p class="hud-value hud-value-gold">OFICIAL</p></div>
        <div class="hud-item"><p class="hud-title">Tu Promedio Anual</p><p class="hud-value {color_promedio}">{promedio_general_colegio}</p></div>
        <div class="hud-item"><p class="hud-title">Asignaturas Aprobadas</p><p class="hud-value">{materias_aprobadas} / {total_materias}</p></div>
    </div>
    """, unsafe_allow_html=True)

    # 📋 CONSTRUCCIÓN DE LA TABLA MATRIZ ESTILIZADA
    df_tabla = registro_alumno[['MATERIA', 'P1', 'P2', 'P3', 'P4', 'PROMEDIO']].copy()

    def aplicar_color_semaforo(val):
        try:
            n = float(val)
            if n < 6.0: return 'color: #cc0000; font-weight: bold; background-color: #ffe6e6;'
            elif n >= 9.0: return 'color: #00994c; font-weight: bold; background-color: #e6ffe6;'
            return 'color: #0d1b2a; font-weight: bold;'
        except: return ''

    df_estilizado = df_tabla.style.map(aplicar_color_semaforo, subset=['P1', 'P2', 'P3', 'P4', 'PROMEDIO']).format("{:.1f}", subset=['P1', 'P2', 'P3', 'P4', 'PROMEDIO'])

    # Despliegue final simétrico
    st.markdown(f"<div style='background-color:#0d1b2a; color:#d4af37; font-family:Arial Black; font-size:13px; text-align:center; padding:10px; border:3px solid #0d1b2a; border-radius:8px 8px 0 0; letter-spacing:1px;'>TU BOLETÍN DE CALIFICACIONES PERSONAL: {nombre_sujeto.upper()}</div>", unsafe_allow_html=True)
    st.dataframe(df_estilizado, use_container_width=True, hide_index=True)

# =================================================================
# 📥 MÓDULOS SECUNDARIOS (Avisos y Descargas de Reacción Inmediata)
# =================================================================
def seccion_descargas():
    st.markdown("<h2 class='titulo-seccion'>&#x1F4C4; Documentación Institucional</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div style='background:#0d1b2a; padding:15px; border-radius:8px; border-left:4px solid #d4af37; text-align:center;'><h3 style='color:#d4af37; font-size:15px; margin:0;'>&#x1F4D5; MANUAL DE CONVIVENCIA</h3></div>", unsafe_allow_html=True)
        st.download_button(label="Descargar Manual PDF", data=b"PDF", file_name="Manual_Convivencia_2026.pdf", use_container_width=True)
    with col2:
        st.markdown("<div style='background:#0d1b2a; padding:15px; border-radius:8px; border-left:4px solid #d4af37; text-align:center;'><h3 style='color:#d4af37; font-size:15px; margin:0;'>&#x1F4DC; CRONOGRAMA LECTIVO</h3></div>", unsafe_allow_html=True)
        st.download_button(label="Descargar Cronograma PDF", data=b"PDF", file_name="Cronograma_2026.pdf", use_container_width=True)

def seccion_avisos():
    st.markdown("<h2 class='titulo-seccion'>&#x1F514; Comunicados de Rectoría</h2>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("🚨 **URGENTE:** Asamblea General de Padres - Viernes 10 de Julio, 6:30 AM. Asistencia obligatoria.")

# =================================================================
# 🏛️ ORQUESTADOR PRINCIPAL
# =================================================================
def main():
    if not st.session_state.autenticado:
        mostrar_login()
    else:
        # Renderizado estricto del menú de control lateral
        st.sidebar.markdown(f"""
        <div style="text-align: center; color: white;">
            <img src="{escudo_seguro}" width="90" style="margin-bottom: 5px; filter: drop-shadow(0px 2px 4px rgba(212,175,55,0.3));">
            <p style="font-size: 20px; font-family: 'Arial Black', sans-serif; color: #d4af37; margin: 0;">GÉNESIS</p>
            <p style="font-size: 11px; margin-top: 0; color: #a8b2d1;">ZONA ESCOLAR</p>
            <hr style="border: 1px solid rgba(255,255,255,0.1); margin: 8px 0;">
            <p style="font-size: 10px; font-weight: bold; color: #d4af37; margin:0;">OPERADOR ACTIVO:</p>
            <p style="font-size: 12px; margin-bottom: 5px;">{st.session_state.datos_alumno.get('NOMBRE_COMPLETO')}</p>
            <hr style="border: 1px solid rgba(255,255,255,0.1); margin: 8px 0;">
        </div>
        """, unsafe_allow_html=True)
        
        opcion = st.sidebar.radio("MENÚ DE NAVEGACIÓN", ["Mi Boletín", "Descargas", "Avisos"])
        st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
        
        if st.sidebar.button("Cerrar Sesión", use_container_width=True):
            st.session_state.autenticado = False
            st.session_state.datos_alumno = None
            st.clear_cache()
            st.rerun()

        # Despliegue de módulos condicionales instantáneos
        if opcion == "Mi Boletín": seccion_boletin()
        elif opcion == "Descargas": seccion_descargas()
        elif opcion == "Avisos": seccion_avisos()

if __name__ == "__main__":
    main()
