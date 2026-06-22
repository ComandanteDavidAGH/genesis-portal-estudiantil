import streamlit as st
import pandas as pd
from supabase import create_client
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

# --- Inyección de Estilos Omega Pro y Recuperación de Menú Hamburguesa ---
st.markdown("""
<style>
    /* 1. Blindaje Principal y Contornos de Tabla */
    [data-testid="stDataFrame"] {
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

    /* 5. ⚙️ INYECCIÓN CSS: CAMUFLAJE Y VISIBILIDAD DE HAMBURGUESA */
    footer {visibility: hidden;} /* Oculta logo de Streamlit abajo */
    
    /* 🚫 FULMINAR AL GATO Y BOTONES EXTRAS (Share, Star, Edit) */
    header [data-testid="stToolbarShareButton"] {display: none !important;}
    header [data-testid="stToolbarFavoriteButton"] {display: none !important;}
    header a {display: none !important;} /* Elimina el enlace directo a GitHub */
    header button[title="View source"] {display: none !important;}
    header button[title="Deploy"] {display: none !important;}
    
    /* Mantener viva la Hamburguesa */
    #MainMenu {visibility: visible;}
    [data-testid="collapsedControl"] {visibility: visible;}
# =================================================================
# 🔒 ENLACE AL BÚNKER DE DATOS (Supabase)
# =================================================================
@st.cache_resource(show_spinner=False)
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def cerrar_sesion():
    st.session_state.autenticado = False
    st.session_state.datos_alumno = None
    st.rerun()

# =================================================================
# 🛡️ PANTALLA DE LOGUEO (Centralizada y con Escudo)
# =================================================================
def mostrar_login(supabase):
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        # --- 🛡️ INYECCIÓN DEL ESCUDO EN EL LOGIN ---
        st.markdown("""
        <div style='text-align: center; margin-bottom: 10px;'>
            <img src="https://raw.githubusercontent.com/ComandanteDavidAGH/genesis-portal-estudiantil/main/escudo.png" width="140" style="filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.3));">
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h1 style='text-align: center; color: #0d1b2a; margin-top: 0; font-family: Arial Black;'>GÉNESIS</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #d4af37; font-weight: bold; margin-top: -10px;'>PORTAL ESCOLAR ESTUDIANTIL</p>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("#### Control de Acceso")
            doc_ingresado = st.text_input("Ingrese su ID Estudiantil (sin letras):", placeholder="Ej: 001").strip()
            
            autenticar = st.button("Acceder a Zona Escolar", type="primary", use_container_width=True)
            
            if autenticar and doc_ingresado:
                with st.spinner("Escaneando credenciales..."):
                    try:
                        respuesta = supabase.table("data_estudiantes").select("Nombre_Completo, Grado, ID_Estudiante").ilike("ID_Estudiante", f"%{doc_ingresado}%").limit(1).execute()
                        alumno_found = respuesta.data
                        
                        if alumno_found:
                            st.session_state.autenticado = True
                            st.session_state.datos_alumno = alumno_found[0]
                            st.success(f"Acceso concedido a {alumno_found[0]['Nombre_Completo']}")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Credencial inválida o no registrada.")
                    except Exception as e:
                        st.error(f"Falla en escáner: {e}")

# =================================================================
# 📊 MÓDULO 1: MI BOLETÍN 
# =================================================================
def seccion_boletin(supabase):
    st.markdown("<h2 class='titulo-seccion'>&#x1F4CA; Mi Boletín de Calificaciones</h2>", unsafe_allow_html=True)
    
    id_real = st.session_state.datos_alumno['ID_Estudiante']
    nombre = st.session_state.datos_alumno['Nombre_Completo']

    with st.spinner("Descargando historial de notas..."):
        try:
            respuesta_notas = supabase.table("data_estudiantes").select("*").eq("ID_Estudiante", id_real).execute()
            datos_notas = respuesta_notas.data
        except Exception as e:
            st.error(f"Error al descargar boletín: {e}")
            return

    if not datos_notas:
        st.warning(f"Atención {nombre}, aún no tienes calificaciones asentadas.")
        return

    df_notas = pd.DataFrame(datos_notas)
    df_notas.columns = [str(c).upper() for c in df_notas.columns] 
    
    cols_promedio = [c for c in ['P1', 'P2', 'P3', 'P4'] if c in df_notas.columns]
    for c in cols_promedio:
        df_notas[c] = pd.to_numeric(df_notas[c], errors='coerce').fillna(0.0)
    
    df_notas['PROMEDIO'] = df_notas[cols_promedio].mean(axis=1).round(1)

    columnas_mostrar = ['MATERIA', 'P1', 'P2', 'P3', 'P4', 'PROMEDIO']
    df_mostrar = df_notas[[c for c in columnas_mostrar if c in df_notas.columns]].copy()
    
    promedio_general = df_notas['PROMEDIO'].mean()
    promedio_redondeado = round(promedio_general, 1) 
    materias_aprobadas = len(df_notas[df_notas['PROMEDIO'] >= 6.0])
    total_materias = len(df_notas)
    
    color_promedio = "hud-value-green" if promedio_general >= 9.0 else ("hud-value-gold" if promedio_general >= 6.0 else "hud-value-red")

    st.markdown(f"""
    <div class="hud-box">
        <div class="hud-item"><p class="hud-title">Periodo Académico</p><p class="hud-value hud-value-gold">OFICIAL</p></div>
        <div class="hud-item"><p class="hud-title">Tu Promedio Anual</p><p class="hud-value {color_promedio}">{promedio_redondeado}</p></div>
        <div class="hud-item"><p class="hud-title">Asignaturas Aprobadas</p><p class="hud-value">{materias_aprobadas} / {total_materias}</p></div>
    </div>
    """, unsafe_allow_html=True)

    def pintar_celdas(val):
        try:
            n = float(val)
            if n < 6.0: return 'color: #cc0000; font-weight: bold; background-color: #ffe6e6;'
            elif n >= 9.0: return 'color: #00994c; font-weight: bold; background-color: #e6ffe6;'
            return 'color: #0d1b2a; font-weight: bold;'
        except: return ''

    cols_num = [c for c in ['P1', 'P2', 'P3', 'P4', 'PROMEDIO'] if c in df_mostrar.columns]
    df_pintado = df_mostrar.style.map(pintar_celdas, subset=cols_num).format("{:.1f}", subset=cols_num)

    st.markdown("<div style='background-color:#0d1b2a; color:#d4af37; font-family:Arial Black; font-size:13px; text-align:center; padding:10px; border:3px solid #0d1b2a; border-radius:8px 8px 0 0; position:relative; z-index:11; letter-spacing:1px;'>TU BOLETÍN DE CALIFICACIONES PERSONAL</div>", unsafe_allow_html=True)
    st.dataframe(df_pintado, use_container_width=True, hide_index=True)

# =================================================================
# 📄 MÓDULO 2: ZONA DE DESCARGAS Y DOCUMENTOS
# =================================================================
def seccion_descargas():
    st.markdown("<h2 class='titulo-seccion'>&#x1F4C4; Documentación Institucional</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #6c757d; font-size: 14px;'>Consulte los lineamientos y fechas clave del periodo lectivo 2026.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #0d1b2a 0%, #1a365d 100%); padding:20px; border-radius:8px; border-left:5px solid #d4af37; text-align:center; box-shadow: 2px 4px 10px rgba(0,0,0,0.3); margin-bottom: 10px;'>
            <h3 style='color:#d4af37; font-family:Arial Black; font-size:16px; margin-top:0;'>&#x1F4D5; MANUAL DE CONVIVENCIA</h3>
            <p style='color:#a8b2d1; font-size:13px; margin-bottom:0;'>Marco legal, derechos y deberes del estudiante Génesis.</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("Ver Artículos Principales (Vista Rápida)"):
            st.markdown("""
            **Normativa Académica y Disciplinaria 2026:**
            * **Jornada Académica:** Ingreso a las 6:30 AM. Retardos injustificados afectarán la nota de convivencia.
            * **Presentación Personal:** Uso estricto del uniforme oficial según el cronograma semanal. No se permiten alteraciones.
            * **Dispositivos Electrónicos:** Restringidos durante bloques académicos salvo autorización expresa del docente.
            * **Faltas Tipo I, II y III:** Tipificadas en el Capítulo IV. Toda acción que vulnere la integridad será sancionada.
            """)
            
        st.download_button(
            label="Descargar Manual en PDF",
            data=b"Archivo no disponible temporalmente",
            file_name="Manual_Convivencia_Genesis_2026.pdf",
            mime="application/pdf",
            use_container_width=True
        )
            
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #0d1b2a 0%, #1a365d 100%); padding:20px; border-radius:8px; border-left:5px solid #d4af37; text-align:center; box-shadow: 2px 4px 10px rgba(0,0,0,0.3); margin-bottom: 10px;'>
            <h3 style='color:#d4af37; font-family:Arial Black; font-size:16px; margin-top:0;'>&#x1F4DC; CRONOGRAMA LECTIVO 2026</h3>
            <p style='color:#a8b2d1; font-size:13px; margin-bottom:0;'>Ruta académica, evaluaciones y comisiones de evaluación.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Ver Fechas Críticas (Vista Rápida)"):
            st.markdown("""
            **Hitos del Semestre Actual:**
            * **Semana de Exámenes Parciales:** 15 al 19 de Marzo.
            * **Corte de Notas / Plataforma:** 26 de Marzo.
            * **Comisión de Evaluación y Promoción:** 2 de Abril.
            * **Entrega de Boletines a Padres:** 9 de Abril.
            * **Simulacro Tipo Estado:** 28 de Mayo.
            """)
        
        st.download_button(
            label="Descargar Cronograma PDF",
            data=b"Archivo no disponible temporalmente",
            file_name="Cronograma_Academico_Genesis_2026.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# =================================================================
# 🔔 MÓDULO 3: TABLERO DE AVISOS 
# =================================================================
def seccion_avisos():
    st.markdown("<h2 class='titulo-seccion'>&#x1F514; Comunicados de Rectoría</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #6c757d; font-size: 14px;'>Información de última hora y directrices institucionales.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("""
        <div style="border-left: 5px solid #ff3333; padding-left: 10px;">
            <h4 style="margin: 0; color: #0d1b2a;">&#x1F534; URGENTE: Asamblea General de Padres</h4>
            <p style="margin-top: 5px; font-size: 14px;"><b>Fecha:</b> Viernes, 10 de Julio de 2026 | <b>Hora:</b> 6:30 AM.<br>
            Se requiere asistencia de carácter obligatorio para socializar los resultados del periodo anterior.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("""
        <div style="border-left: 5px solid #d4af37; padding-left: 10px;">
            <h4 style="margin: 0; color: #0d1b2a;">&#x1F7E1; SIMULACRO DE EVALUACIONES OMR</h4>
            <p style="margin-top: 5px; font-size: 14px;"><b>Objetivo:</b> Preparación para pruebas estandarizadas.<br>
            La próxima semana se habilitará el uso de las nuevas hojas de respuesta OMR. Traer lápiz Mirado No. 2 y borrador.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("""
        <div style="border-left: 5px solid #1a365d; padding-left: 10px;">
            <h4 style="margin: 0; color: #0d1b2a;">&#x1F535; Plataforma Génesis Actualizada</h4>
            <p style="margin-top: 5px; font-size: 14px;">Estimada comunidad, bienvenidos a la nueva interfaz del <b>Portal Académico Génesis v1.0 Omega</b>.</p>
        </div>
        """, unsafe_allow_html=True)

# =================================================================
# 🏛️ MOTOR DE EJECUCIÓN PRINCIPAL
# =================================================================
def main():
    try:
        supabase = iniciar_conexion()
    except Exception as e:
        st.error(f"Falla en enlace satelital Supabase: {e}")
        return

    if not st.session_state.autenticado:
        mostrar_login(supabase)
    else:
        # --- CONFIGURACIÓN DEL MENÚ LATERAL TÁCTICO CON ESCUDO ---
        st.sidebar.markdown(f"""
        <div style="text-align: center; color: white;">
            <img src="https://raw.githubusercontent.com/ComandanteDavidAGH/genesis-portal-estudiantil/main/escudo.png" width="90" style="margin-bottom: 10px; filter: drop-shadow(0px 2px 5px rgba(212,175,55,0.4));">
            <p style="font-size: 22px; font-family: 'Arial Black', sans-serif; color: #d4af37; margin-bottom: 0; line-height: 1;">GÉNESIS</p>
            <p style="font-size: 13px; margin-top: 0; color: #a8b2d1;">ZONA ESCOLAR</p>
            <hr style="border: 1px solid rgba(255,255,255,0.1); margin: 10px 0;">
            <p style="font-size: 11px; font-weight: bold; text-transform: uppercase; color: #d4af37; margin:0;">Estudiante:</p>
            <p style="font-size: 13px; margin-bottom: 10px;">{st.session_state.datos_alumno['Nombre_Completo']}</p>
            <p style="font-size: 11px; font-weight: bold; text-transform: uppercase; color: #d4af37; margin:0;">Curso:</p>
            <p style="font-size: 13px; margin-bottom: 5px;">{st.session_state.datos_alumno['Grado']}</p>
            <hr style="border: 1px solid rgba(255,255,255,0.1); margin: 10px 0;">
        </div>
        """, unsafe_allow_html=True)
        
        menu_principal = st.sidebar.radio(
            "MENÚ DE NAVEGACIÓN",
            ["Mi Boletín", "Descargas", "Avisos"]
        )
        
        st.sidebar.markdown("<br><br><br><br>", unsafe_allow_html=True)
        
        if st.sidebar.button("Cerrar Sesión", type="secondary", use_container_width=True):
            cerrar_sesion()

        # FOOTER 2026 SANITIZADO Y BLINDADO
        st.sidebar.markdown("""
        <div style="position: fixed; bottom: 10px; width: 100%; text-align: center; font-size: 10px; color: #6c757d;">
            &copy; Agroa&eacute;reo T&aacute;ctico 2026<br>G&eacute;nesis v1.0.Omega
        </div>
        """, unsafe_allow_html=True)

        # --- ENRUTADOR DE SECCIONES ---
        if menu_principal == "Mi Boletín": seccion_boletin(supabase)
        elif menu_principal == "Descargas": seccion_descargas()
        elif menu_principal == "Avisos": seccion_avisos()

if __name__ == "__main__":
    main()
