import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import datetime
import time

# =================================================================
# 🔒 CONFIGURACIÓN CRÍTICA Y BLINDAJE VISUAL
# =================================================================
st.set_page_config(page_title="Génesis - Zona Escolar", page_icon="🎓", layout="wide")

# Inicializamos el estado de la sesión táctica
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'datos_alumno' not in st.session_state:
    st.session_state.datos_alumno = None

# --- Inyección de Estilos Omega Pro (Actualizado con Sidebar) ---
st.markdown("""
<style>
    /* 1. Blindaje Principal y Contornos de Tabla */
    [data-testid="stDataFrame"], .styled-table-container {
        border-left: 3px solid #0d1b2a !important;
        border-right: 3px solid #0d1b2a !important;
        border-bottom: 3px solid #0d1b2a !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        margin-top: -10px !important; 
        box-shadow: 0px 5px 15px rgba(0,0,0,0.15) !important;
    }
    
    /* 2. Estilos del HUD (Panel Superior) */
    .hud-box {
        background: linear-gradient(135deg, #0d1b2a 0%, #1a365d 100%);
        border-left: 5px solid #d4af37;
        padding: 15px; border-radius: 8px; 
        display: grid; 
        grid-template-columns: repeat(3, 1fr); 
        gap: 15px;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.3); margin-bottom: 20px;
    }
    .hud-item { text-align: center; border-right: 1px solid rgba(255,255,255,0.1); }
    .hud-item:last-child { border-right: none; }
    .hud-title { font-size: 11px; color: #a8b2d1; font-family: 'Arial Black', sans-serif; text-transform: uppercase; margin: 0; letter-spacing: 1px; }
    .hud-value { font-size: 24px; color: #ffffff; font-weight: 900; margin: 0; font-family: Arial, sans-serif; }
    .hud-value-gold { color: #d4af37; }
    .hud-value-green { color: #00ff66; }
    .hud-value-red { color: #ff3333; }

    /* 3. Estilos del Panel Lateral (Sidebar Institucional) */
    [data-testid="stSidebar"] {
        background-color: #0d1b2a;
        color: white;
        border-right: 2px solid #d4af37;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] .stRadio > label {
        color: #d4af37 !important;
        font-family: 'Arial Black', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* 4. Títulos Globales Estilizados */
    .titulo-seccion { color: #0d1b2a; font-family: 'Arial Black', sans-serif; border-bottom: 2px solid #d4af37; padding-bottom: 5px; }

    /* 5. 🚫 OPERACIÓN CAMUFLAJE (Eliminar Gato y Menú Streamlit) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =================================================================
# 🔒 ENLACE AL BÚNKER DE DATOS (Supabase)
# =================================================================
@st.cache_resource(show_spinner=False)
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

# Función táctica para cerrar sesión
def cerrar_sesion():
    st.session_state.autenticado = False
    st.session_state.datos_alumno = None
    st.rerun()

# =================================================================
# 🛡️ PANTALLA DE LOGUEO (Centralizada)
# =================================================================
def mostrar_login(supabase):
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        # Logo placeholder o texto institucional
        st.markdown("<h1 style='text-align: center; color: #0d1b2a;'>GÉNESIS</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #d4af37; font-weight: bold;'>PORTAL ESCOLAR ESTUDIANTIL</p>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("#### 🔒 Control de Acceso")
            doc_ingresado = st.text_input("💳 Ingrese su ID Estudiantil (sin letras):", placeholder="Ej: 001").strip()
            
            autenticar = st.button("📡 Acceder a Zona Escolar", type="primary", use_container_width=True)
            
            if autenticar and doc_ingresado:
                with st.spinner("Escaneando credenciales..."):
                    try:
                        # Búsqueda por coincidencia (lo que acordamos anteriormente)
                        respuesta = supabase.table("data_estudiantes").select("Nombre_Completo, Grado, ID_Estudiante").ilike("ID_Estudiante", f"%{doc_ingresado}%").limit(1).execute()
                        alumno_found = respuesta.data
                        
                        if alumno_found:
                            # Fijamos la sesión táctica
                            st.session_state.autenticado = True
                            st.session_state.datos_alumno = alumno_found[0]
                            st.success(f"🔓 Acceso concedido a {alumno_found[0]['Nombre_Completo']}")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Credencial inválida o no registrada.")
                    except Exception as e:
                        st.error(f"🚨 Falla en escáner: {e}")

# =================================================================
# 📊 MÓDULO 1: MI BOLETÍN (Código que ya funcionaba)
# =================================================================
def seccion_boletin(supabase):
    st.markdown("<h2 class='titulo-seccion'>📊 Mi Boletín de Calificaciones</h2>", unsafe_allow_html=True)
    
    id_real = st.session_state.datos_alumno['ID_Estudiante']
    nombre = st.session_state.datos_alumno['Nombre_Completo']

    with st.spinner("Descargando historial de notas..."):
        try:
            # Traemos todo sobre el estudiante de data_estudiantes
            respuesta_notas = supabase.table("data_estudiantes").select("*").eq("ID_Estudiante", id_real).execute()
            datos_notas = respuesta_notas.data
        except Exception as e:
            st.error(f"🚨 Error al descargar boletín: {e}")
            return

    if not datos_notas:
        st.warning(f"⚠️ {nombre}, aún no tienes calificaciones asentadas.")
        return

    # Procesamiento táctico con Pandas
    df_notas = pd.DataFrame(datos_notas)
    df_notas.columns = [str(c).upper() for c in df_notas.columns] # Normalizamos
    
    # Aseguramos columnas numéricas
    cols_promedio = [c for c in ['P1', 'P2', 'P3', 'P4'] if c in df_notas.columns]
    for c in cols_promedio:
        df_notas[c] = pd.to_numeric(df_notas[c], errors='coerce').fillna(0.0)
    
    # Calculamos PROMEDIO simple (lo que acordamos)
    df_notas['PROMEDIO'] = df_notas[cols_promedio].mean(axis=1).round(1)

    # Filtrado y orden visual
    columnas_mostrar = ['MATERIA', 'P1', 'P2', 'P3', 'P4', 'PROMEDIO']
    df_mostrar = df_notas[[c for c in columnas_mostrar if c in df_notas.columns]].copy()
    
    # 🧮 CÓMPUTO DE RENDIMIENTO VIP HÚD
    promedio_general = df_notas['PROMEDIO'].mean()
    materias_aprobadas = len(df_notas[df_notas['PROMEDIO'] >= 6.0])
    total_materias = len(df_notas)
    
    color_promedio = "hud-value-green" if promedio_general >= 9.0 else ("hud-value-gold" if promedio_general >= 6.0 else "hud-value-red")

    # 📊 PANEL HUD PREMIUM (Nivel Táctico)
    st.markdown(f"""
    <div class="hud-box">
        <div class="hud-item"><p class="hud-title">Periodo Académico</p><p class="hud-value hud-value-gold">OFICIAL</p></div>
        <div class="hud-item"><p class="hud-title">Tu Promedio Anual</p><p class="hud-value {color_promedio}">{promedio_general:.1f}</p></div>
        <div class="hud-item"><p class="hud-title">Asignaturas Aprobadas</p><p class="hud-value">{materias_aprobadas} / {total_materias}</p></div>
    </div>
    """, unsafe_allow_html=True)

    # 🎨 SEMÁFORO DE CELDAS DINÁMICO
    def pintar_celdas(val):
        try:
            n = float(val)
            if n < 6.0: return 'color: #cc0000; font-weight: bold; background-color: #ffe6e6;'
            elif n >= 9.0: return 'color: #00994c; font-weight: bold; background-color: #e6ffe6;'
            return 'color: #0d1b2a; font-weight: bold;'
        except: return ''

    # Aplicamos estilos a la matriz
    cols_num = [c for c in ['P1', 'P2', 'P3', 'P4', 'PROMEDIO'] if c in df_mostrar.columns]
    df_pintado = df_mostrar.style.map(pintar_celdas, subset=cols_num).format("{:.1f}", subset=cols_num)

    st.markdown("<div style='background-color:#0d1b2a; color:#d4af37; font-family:Arial Black; font-size:13px; text-align:center; padding:10px; border:3px solid #0d1b2a; border-radius:8px 8px 0 0; position:relative; z-index:11; letter-spacing:1px;'>TU BOLETÍN DE CALIFICACIONES PERSONAL</div>", unsafe_allow_html=True)
    st.dataframe(df_pintado, use_container_width=True, hide_index=True)

# =================================================================
# 📄 MÓDULO 2: ZONA DE DESCARGAS (Estilo Premium 2026)
# =================================================================
def seccion_descargas():
    st.markdown("<h2 class='titulo-seccion'>📄 Zona de Descargas</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Tarjeta con el estilo HUD (Azul Oscuro y Dorado)
        st.markdown("""
        <div style='background: linear-gradient(135deg, #0d1b2a 0%, #1a365d 100%); padding:20px; border-radius:8px; border-left:5px solid #d4af37; text-align:center; box-shadow: 2px 4px 10px rgba(0,0,0,0.3); margin-bottom: 10px;'>
            <h3 style='color:#d4af37; font-family:Arial Black; font-size:16px; margin-top:0;'>📕 MANUAL DE CONVIVENCIA</h3>
            <p style='color:#a8b2d1; font-size:13px; margin-bottom:0;'>Documento oficial en PDF. Lineamientos institucionales.</p>
        </div>
        """, unsafe_allow_html=True)
        # Botón de Descarga
        st.button("⏬ Descargar Manual", key="btn_manual", use_container_width=True)
            
    with col2:
        # Tarjeta con el estilo HUD (Azul Oscuro y Dorado)
        st.markdown("""
        <div style='background: linear-gradient(135deg, #0d1b2a 0%, #1a365d 100%); padding:20px; border-radius:8px; border-left:5px solid #d4af37; text-align:center; box-shadow: 2px 4px 10px rgba(0,0,0,0.3); margin-bottom: 10px;'>
            <h3 style='color:#d4af37; font-family:Arial Black; font-size:16px; margin-top:0;'>📜 CRONOGRAMA 2026</h3>
            <p style='color:#a8b2d1; font-size:13px; margin-bottom:0;'>Fechas de exámenes, vacaciones y entrega de boletines.</p>
        </div>
        """, unsafe_allow_html=True)
        # Botón de Descarga
        st.button("⏬ Descargar Cronograma", key="btn_crono", use_container_width=True)
# =================================================================
# 🔔 MÓDULO 3: AVISOS (Placeholders)
# =================================================================
def seccion_avisos():
    st.markdown("<h2 class='titulo-seccion'>🔔 Avisos y Recordatorios</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("##### 💡 Entrega de Boletines II Periodo")
        st.warning("Señores padres de familia, la entrega será el próximo viernes 30 de Julio de 7:00 AM a 10:00 AM.")
        
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("##### 📅 Próximo Simulacro de Evaluación")
        st.info("Grados 2° a 5° tendrán simulacro de Matemáticas el día miércoles.")

# =================================================================
# 🏛️ MOTOR DE EJECUCIÓN PRINCIPAL
# =================================================================
def main():
    try:
        supabase = iniciar_conexion()
    except Exception as e:
        st.error(f"🚨 Falla en enlace satelital Supabase: {e}")
        return

    # Si no está autenticado, mostramos login central
    if not st.session_state.autenticado:
        mostrar_login(supabase)
    else:
        # --- CONFIGURACIÓN DEL MENÚ LATERAL TÁCTICO (SOLO LOGIN OK) ---
        st.sidebar.markdown(f"""
        <div style="text-align: center; color: white;">
            <p style="font-size: 24px; font-family: 'Arial Black', sans-serif; color: #d4af37; margin-bottom: 0;">GÉNESIS</p>
            <p style="font-size: 14px; margin-top: 0;">Zona Escolar</p>
            <hr style="border: 1px solid rgba(255,255,255,0.1);">
            <p style="font-size: 11px; font-weight: bold; text-transform: uppercase;">Estudiante:</p>
            <p style="font-size: 12px;">{st.session_state.datos_alumno['Nombre_Completo']}</p>
            <p style="font-size: 11px; font-weight: bold; text-transform: uppercase;">Curso: {st.session_state.datos_alumno['Grado']}</p>
            <hr style="border: 1px solid rgba(255,255,255,0.1);">
        </div>
        """, unsafe_allow_html=True)
        
        menu_principal = st.sidebar.radio(
            "📍 MENÚ",
            ["📊 Mi Boletín", "📄 Descargas", "🔔 Avisos"]
        )
        
        st.sidebar.markdown("<br><br><br><br>", unsafe_allow_html=True)
        
        # Botón de Cerrar Sesión (Destruye estado y reinicia)
        if st.sidebar.button("🔒 Cerrar Sesión", type="secondary", use_container_width=True):
            cerrar_sesion()

        st.sidebar.markdown(f"""
        <div style="position: fixed; bottom: 10px; width: 100%; text-align: center; font-size: 10px; color: #6c757d;">
            © Agroaéreo Táctico 2024<br>Génesis v1.0.Omega
        </div>
        """, unsafe_allow_html=True)

        # --- ENRUTADOR DE SECCIONES (MAIN AREA) ---
        if menu_principal == "📊 Mi Boletín":seccion_boletin(supabase)
        elif menu_principal == "📄 Descargas": seccion_descargas()
        elif menu_principal == "🔔 Avisos": seccion_avisos()

if __name__ == "__main__":
    main()
