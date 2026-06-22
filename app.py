import streamlit as st
import pandas as pd
from supabase import create_client

# =================================================================
# 🔒 CONEXIÓN AL BÚNKER DE DATOS INSTITUCIONAL
# =================================================================
@st.cache_resource(show_spinner=False)
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def ejecutar():
    # 🚀 MOTOR VISUAL PREMIUM CON CONTORNOS INTEGRADOS
    <style>
    [data-testid="stDataFrame"] {
        border-left: 3px solid #0d1b2a !important;
        border-right: 3px solid #0d1b2a !important;
        border-bottom: 3px solid #0d1b2a !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        margin-top: -10px !important; 
        box-shadow: 0px 5px 15px rgba(0,0,0,0.15) !important;
        overflow: hidden !important;
    }
    
    /* CAJA PRINCIPAL (Cuadrícula perfecta) */
    .hud-box {
        background: linear-gradient(135deg, #0d1b2a 0%, #1a365d 100%);
        border-left: 5px solid #d4af37;
        padding: 15px; border-radius: 8px; 
        display: grid; 
        grid-template-columns: repeat(3, 1fr); 
        gap: 15px;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.3); margin-bottom: 20px;
    }
    .hud-item { 
        text-align: center; 
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    .hud-item:last-child { border-right: none; }
    
    /* LUCES ENCENDIDAS PARA LOS TEXTOS (Brillo y Color) */
    .hud-title { font-size: 11px; color: #a8b2d1; font-family: 'Arial Black', sans-serif; text-transform: uppercase; margin: 0; letter-spacing: 1px; }
    .hud-value { font-size: 24px; color: #ffffff; font-weight: 900; margin: 0; font-family: Arial, sans-serif; }
    .hud-value-gold { color: #d4af37; }
    .hud-value-green { color: #00ff66; }
    .hud-value-red { color: #ff3333; }
    </style>
    """, unsafe_allow_html=True)

    # ==========================================
    # 🎓 ENCABEZADO DEL PORTAL ESTUDIANTIL
    # ==========================================
    st.markdown("<h1 style='text-align: center; color: #0d1b2a; font-family: Arial Black;'>🎓 Portal Académico Estudiantil</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #d4af37; font-weight: bold;'>SISTEMA DE AUTENTICACIÓN Y CONSULTA PRIVADA</p>", unsafe_allow_html=True)
    st.markdown("---")

    try:
        supabase = iniciar_conexion()
    except Exception as e:
        st.error(f"🚨 Falla en el enlace satelital con Supabase: {e}")
        return

    # 🔑 PASO 1: BÚNKER DE ACCESO POR DOCUMENTO
    with st.container(border=True):
        st.markdown("#### 🔒 Control de Identidad Estudiantil")
        c_id, c_btn = st.columns([3, 1])
        
        # El estudiante ingresa su número (Ej: EST-001)
        documento_ingresado = c_id.text_input("💳 Ingrese su Documento de Identidad o ID:", placeholder="Ejemplo: EST-001").strip().upper()
        
        st.markdown("<br>", unsafe_allow_html=True)
        autenticar = c_btn.button("📡 Acceder al Sistema", type="primary", use_container_width=True)

    if documento_ingresado:
        with st.spinner("Verificando credenciales en el búnker central..."):
            try:
                # 📡 ESCÁNER 1: Buscamos al estudiante por su ID exacto
                res_estudiante = supabase.table("data_estudiantes").select("Nombre_Completo, Grado").ilike("ID_Estudiante", f"%{documento_ingresado}%").execute()
                alumno_data = res_estudiante.data
            except Exception as e:
                st.error(f"🚨 Error en el escáner de identidad: {e}")
                return

        if not alumno_data:
            st.error(f"❌ EL ID '{documento_ingresado}' NO ESTÁ REGISTRADO. Verifique si lleva mayúsculas o guiones.")
            return

        # 🎯 EXTRACCIÓN DE IDENTIDAD
        nombre_estudiante = str(alumno_data[0]["Nombre_Completo"]).strip().upper()
        grado_estudiante = str(alumno_data[0]["Grado"]).strip().upper()

        st.markdown("### 📋 Coordenadas del Estudiante")
        cs1, cs2 = st.columns(2)
        cs1.selectbox("👤 Estudiante Autenticado:", [nombre_estudiante], disabled=True)
        cs2.selectbox("👥 Curso / Grado Asignado:", [grado_estudiante], disabled=True)

        # 🔑 PASO 2: EXTRACCIÓN DE CALIFICACIONES
        with st.spinner("Descargando historial de notas consolidado..."):
            try:
                # Primero buscamos en la tabla principal de notas
                respuesta_notas = supabase.table("notas_consolidadas").select("*").eq("NOMBRE_COMPLETO", nombre_estudiante).execute()
                datos_notas = respuesta_notas.data
                
                # PLAN B: Si no hay notas consolidadas, sacamos las notas preliminares de data_estudiantes (lo que vi en tus fotos)
                if not datos_notas:
                    res_respaldo = supabase.table("data_estudiantes").select("*").ilike("ID_Estudiante", f"%{documento_ingresado}%").execute()
                    datos_notas = res_respaldo.data

            except Exception as e:
                st.error(f"🚨 Error al descargar boletín: {e}")
                return

        if not datos_notas:
            st.warning(f"⚠️ Identidad confirmada, pero aún no tienes calificaciones asentadas en este periodo.")
            return

        # Procesamos las notas en Pandas
        df_notas = pd.DataFrame(datos_notas)
        
        # Unificamos el nombre de columnas a mayúsculas para evitar problemas (Materia vs MATERIA vs ASIGNATURA)
        df_notas.columns = [str(c).upper() for c in df_notas.columns]
        
        columnas_mostrar = ['ASIGNATURA', 'MATERIA', 'P1', 'P2', 'P3', 'P4', 'PROMEDIO', 'DESEMPEÑO']
        columnas_reales = [col for col in columnas_mostrar if col in df_notas.columns]
        df_mostrar = df_notas[columnas_reales].copy()

        # Si el profesor aún no calcula el PROMEDIO, el sistema lo calcula en vivo
        if 'PROMEDIO' not in df_mostrar.columns:
            cols_promedio = [c for c in ['P1', 'P2', 'P3', 'P4'] if c in df_mostrar.columns]
            if cols_promedio:
                for c in cols_promedio:
                    df_mostrar[c] = pd.to_numeric(df_mostrar[c], errors='coerce').fillna(0.0)
                df_mostrar['PROMEDIO'] = df_mostrar[cols_promedio].mean(axis=1).round(1)

        # 🧮 CÓMPUTO DE RENDIMIENTO VIP HÚD
        if 'PROMEDIO' in df_mostrar.columns:
            df_mostrar['PROMEDIO'] = pd.to_numeric(df_mostrar['PROMEDIO'], errors='coerce').fillna(0.0)
            promedio_general = df_mostrar['PROMEDIO'].mean()
            materias_aprobadas = len(df_mostrar[df_mostrar['PROMEDIO'] >= 6.0])
            total_materias = len(df_mostrar)
            
            if promedio_general >= 9.0: color_promedio = "hud-value-green"
            elif promedio_general >= 6.0: color_promedio = "hud-value-gold"
            else: color_promedio = "hud-value-red"

            # 📊 PANEL HUD PREMIUM PERSONAL
            st.markdown(f"""
            <div class="hud-box">
                <div class="hud-item"><p class="hud-title">Periodo Académico</p><p class="hud-value" style="color:#d4af37;">OFICIAL</p></div>
                <div class="hud-item"><p class="hud-title">Tu Promedio General</p><p class="hud-value {color_promedio}">{promedio_general:.1f}</p></div>
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

        cols_num = [c for c in ['P1', 'P2', 'P3', 'P4', 'PROMEDIO'] if c in df_mostrar.columns]
        df_pintado = df_mostrar.style.map(pintar_celdas, subset=cols_num).format("{:.1f}", subset=cols_num)

        # 📊 DESPLIEGUE DEL BOLETÍN PRIVADO
        st.markdown("<div style='background-color:#0d1b2a; color:#d4af37; font-family:Arial Black; font-size:13px; text-align:center; padding:10px; border:3px solid #0d1b2a; border-radius:8px 8px 0 0; position:relative; z-index:11; letter-spacing:1px;'>TU BOLETÍN DE CALIFICACIONES PERSONAL</div>", unsafe_allow_html=True)
        st.dataframe(df_pintado, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    ejecutar()
