import streamlit as st
import time
import base64
from supabase import create_client, Client

# =================================================================
# ⚡ CONFIGURACIÓN DE PÁGINA (Debe ser el primer comando de Streamlit)
# =================================================================
st.set_page_config(
    page_title="Génesis - Zona Escolar",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =================================================================
# ⚙️ 1. OPTIMIZACIÓN DE VELOCIDAD: CONEXIÓN CACHEDA A SUPABASE
# =================================================================
@st.cache_resource
def inicializar_conexion():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Error crítico de configuración de llaves: {e}")
        return None

supabase = inicializar_conexion()

# =================================================================
# 🖼️ 2. OPTIMIZACIÓN DE VELOCIDAD: PROCESAMIENTO ÚNICO DE IMAGEN
# =================================================================
@st.cache_data
def cargar_escudo_base64():
    try:
        with open("escudo.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            return f"data:image/png;base64,{encoded_string}"
    except Exception:
        # Fallback de emergencia si la imagen local no se encuentra
        return "https://via.placeholder.com/140"

escudo_seguro = cargar_escudo_base64()

# =================================================================
# ⚡ 3. CACHÉ DE DATOS ACADÉMICOS (Adiós a los 30 segundos de espera)
# =================================================================
@st.cache_data
def descargar_toda_la_data():
    if not supabase:
        return []
    try:
        respuesta = supabase.table("data_estudiantes").select("*").execute()
        return respuesta.data
    except Exception as e:
        st.error(f"Error al sincronizar datos: {e}")
        return []

# Carga masiva en caché ultrarrápida
toda_la_data = descargar_toda_la_data()

# =================================================================
# 🎨 4. DISEÑO CORPORATIVO Y OCULTAMIENTO DE ICONOS INVASORES (GATO/SHARE)
# =================================================================
st.markdown("""
<style>
    /* Ocultar barra de herramientas nativa de Streamlit (Gato GitHub, Estrella, Lápiz, Share) */
    footer {visibility: hidden !important;}
    [data-testid="stToolbarActions"] {display: none !important;}
    [data-testid="stToolbarShareButton"] {display: none !important;}
    header {visibility: hidden !important;}
    
    /* Personalización del Menú Lateral */
    [data-testid="stSidebar"] {
        background-color: #0d1b2a !important;
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* Estilización del Botón de Cerrar Sesión Contractado (Oro e Institucional) */
    .stButton>button {
        background-color: #d4af37 !important;
        color: #0d1b2a !important;
        font-weight: bold !important;
        border: 2px solid #d4af37 !important;
        border-radius: 5px !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #ffffff !important;
        color: #0d1b2a !important;
        border-color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# =================================================================
# 🔄 ESTADOS DE SESIÓN (Control de Estado de Logueo)
# =================================================================
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'datos_alumno' not in st.session_state:
    st.session_state.datos_alumno = None

# =================================================================
# 🛡️ PANTALLA DE LOGUEO INTELIGENTE Y SEGURO
# =================================================================
def mostrar_login():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='text-align: center; margin-bottom: 10px;'>
            <img src="{escudo_seguro}" width="140" style="filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.3));">
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h1 style='text-align: center; color: #0d1b2a; margin-top: 0; font-family: Arial Black;'>GÉNESIS</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #d4af37; font-weight: bold; margin-top: -10px;'>PORTAL ESCOLAR ESTUDIANTIL</p>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("#### Control de Acceso")
            doc_ingresado = st.text_input("Ingrese su ID Estudiantil o Código Maestro:", placeholder="Ej: 001").strip()
            autenticar = st.button("Acceder a Zona Escolar", type="primary", use_container_width=True)
            
            if autenticar and doc_ingresado:
                clave_secreta = st.secrets.get("CODIGO_MAESTRO", "ADMIN_FALLBACK_2026").strip()
                
                # Acceso Administrador Supremo (Saltando Base de Datos)
                if doc_ingresado == clave_secreta:
                    st.session_state.autenticado = True
                    st.session_state.datos_alumno = {
                        'Nombre_Completo': "OPERADOR / ADMIN GENERAL",
                        'Grado': "ADMIN CORE",
                        'ID_Estudiante': "ADMIN"
                    }
                    st.success("🔓 Acceso de Administrador General Concedido")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    # Búsqueda instantánea en la caché cargada
                    alumno_found = [a for a in toda_la_data if str(a.get('ID_Estudiante')).lower() == doc_ingresado.lower()]
                    if alumno_found:
                        st.session_state.autenticado = True
                        st.session_state.datos_alumno = alumno_found[0]
                        st.success(f"Acceso concedido a {alumno_found[0]['Nombre_Completo']}")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("Credencial inválida o no registrada.")

# =================================================================
# 🌌 ENTORNO DE OPERACIÓN PRINCIPAL (Una vez logueado)
# =================================================================
if not st.session_state.autenticado:
    mostrar_login()
else:
    alumno = st.session_state.datos_alumno
    es_admin = (alumno['ID_Estudiante'] == "ADMIN")
    
    # 📌 PANEL LATERAL DE SEGUIMIENTO
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align: center;'>
            <img src="{escudo_seguro}" width="90">
            <h3 style='margin-bottom: 2px;'>GÉNESIS</h3>
            <p style='color: #d4af37; font-size: 12px; font-weight: bold; margin-top: 0;'>ZONA ESCOLAR</p>
        </div>
        <hr style='border-color: #d4af37; margin: 10px 0;'>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**ROL / ESTUDIANTE:**<br><span style='color: #d4af37; font-weight: bold;'>{alumno['Nombre_Completo']}</span>", unsafe_allow_html=True)
        st.markdown(f"**CURSO / ASIGNACIÓN:**<br>{alumno['Grado']}")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # MENÚ TÁCTICO DE NAVEGACIÓN
        opcion = st.radio("MENÚ DE NAVEGACIÓN", ["Mi Boletín", "Descargas", "Avisos"])
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Cerrar Sesión", use_container_width=True):
            st.session_state.autenticado = False
            st.session_state.datos_alumno = None
            st.rerun()

    # 📌 ÁREA DE DESPLIEGUE CENTRAL (Dependiendo de la opción elegida)
    if opcion == "Mi Boletín":
        st.markdown(f"## 📊 {opcion}")
        
        # 👑 COMPORTAMIENTO ADAPTADO PARA EL ADMINISTRADOR SUPREMO
        if es_admin:
            st.info("💡 Modo Inspector General Activado. Puede auditar la información de cualquier estudiante.")
            
            if toda_la_data:
                # 1. Selector de Grados Únicos
                grados_disponibles = sorted(list(set([str(a.get('Grado')) for a in toda_la_data])))
                grado_seleccionado = st.selectbox("Seleccione el Grado a Inspeccionar:", grados_disponibles)
                
                # 2. Filtrar Alumnos del Grado Seleccionado
                alumnos_filtrados = [a for a in toda_la_data if str(a.get('Grado')) == grado_seleccionado]
                nombres_alumnos = {a['Nombre_Completo']: a for a in alumnos_filtrados}
                
                alumno_seleccionado_nombre = st.selectbox("Seleccione el Alumno para ver su Boletín:", list(nombres_alumnos.keys()))
                
                # Datos del alumno auditado en tiempo real
                datos_auditoria = nombres_alumnos[alumno_seleccionado_nombre]
                
                # Desplegar Boletín del alumno seleccionado de forma inmediata
                st.markdown(f"### 📋 Historial Académico de: {datos_auditoria['Nombre_Completo']}")
                st.json(datos_auditoria) # Cambia esto por tus tablas estéticas de notas
            else:
                st.warning("No hay registros en la base de datos para mostrar en este momento.")
                
        else:
            # 🎒 VISTA ESTÁNDAR PARA EL ESTUDIANTE COMÚN
            st.markdown(f"### 📋 Historial de Calificaciones de {alumno['Nombre_Completo']}")
            st.json(alumno) # Aquí despliegas tus tablas específicas

    elif opcion == "Descargas":
        st.markdown(f"## 📥 {opcion}")
        st.write("Zona de descargas de documentos institucionales y guías académicas.")

    elif opcion == "Avisos":
        st.markdown(f"## 📢 {opcion}")
        st.info("📌 **Comunicado Oficial:** Bienvenidos al tercer periodo académico del sistema Génesis v1.0 Omega.")
