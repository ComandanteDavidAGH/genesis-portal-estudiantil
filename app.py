import streamlit as st
import pandas as pd
from supabase import create_client

# =================================================================
# 🔒 CONEXIÓN AL BÚNKER DE DATOS (Mismo acceso, función de lectura)
# =================================================================
@st.cache_resource(show_spinner=False)
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    return create_client(url, key)

def ejecutar():
    # 🚀 MOTOR VISUAL PREMIUM (Heredado de la matriz maestra)
    st.markdown("""
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
    .hud-box {
        background: linear-gradient(135deg, #0d1b2a 0%, #1a365d 100%);
        border-left: 5px solid #d4af37;
        padding: 15px; border-radius: 8px; display: flex;
        justify-content: space-around; align-items: center;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.3); margin-bottom: 20px;
    }
    .hud-item { text-align: center; }
    .hud-title { font-size: 12px; color: #a8b2d1; font-family: 'Arial Black', sans-serif; text-transform: uppercase; margin: 0; }
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
    st.markdown("<p style='text-align: center; color: #d4af37; font-weight: bold;'>CONSULTA DE RENDIMIENTO EN TIEMPO REAL</p>", unsafe_allow_html=True)
    st.markdown("---")

    # 🔍 BUSCADOR DE RASTREO
    col_busqueda, col_btn = st.columns([3, 1])
    with col_busqueda:
        nombre_buscar = st.text_input("🔍 Ingresa tu Nombre Completo:", placeholder="Ej: JUAN PABLO PEREZ...").strip().upper()
    
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        buscar = st.button("📡 Rastrear Notas", type="primary", use_container_width=True)

    if buscar and nombre_buscar:
        try:
            supabase = iniciar_conexion()
            with st.spinner("Conectando con el búnker de calificaciones..."):
                # 🎯 DISPARO AL BÚNKER: Traemos solo las notas de este estudiante
                respuesta = supabase.table("notas_consolidadas").select("*").ilike("NOMBRE_COMPLETO", f"%{nombre_buscar}%").execute()
                datos = respuesta.data
                
            if not datos:
                st.warning(f"⚠️ No se encontraron calificaciones registradas para: {nombre_buscar}")
                return
                
            # Procesamos la data en Pandas
            df_notas = pd.DataFrame(datos)
            
            # Limpiamos las columnas para mostrar solo lo relevante al alumno
            columnas_mostrar = ['ASIGNATURA', 'P1', 'P2', 'P3', 'P4', 'PROMEDIO', 'DESEMPEÑO']
            # Filtramos solo las columnas que existan realmente en la tabla
            columnas_reales = [col for col in columnas_mostrar if col in df_notas.columns]
            df_mostrar = df_notas[columnas_reales].copy()
            
            # Aseguramos que el promedio sea numérico para sacar métricas
            if 'PROMEDIO' in df_mostrar.columns:
                df_mostrar['PROMEDIO'] = pd.to_numeric(df_mostrar['PROMEDIO'], errors='coerce').fillna(0.0)
                promedio_general = df_mostrar['PROMEDIO'].mean()
                materias_aprobadas = len(df_mostrar[df_mostrar['PROMEDIO'] >= 6.0])
                total_materias = len(df_mostrar)
                
                # Semáforo de rendimiento general
                if promedio_general >= 9.0: color_promedio = "hud-value-green"
                elif promedio_general >= 6.0: color_promedio = "hud-value-gold"
                else: color_promedio = "hud-value-red"

                # 📊 RENDERIZADO DEL HUD ESTUDIANTIL
                st.markdown(f"""
                <div class="hud-box">
                    <div class="hud-item"><p class="hud-title">Estudiante</p><p class="hud-value" style="font-size:16px;">{nombre_buscar}</p></div>
                    <div class="hud-item"><p class="hud-title">Promedio General</p><p class="hud-value {color_promedio}">{promedio_general:.1f}</p></div>
                    <div class="hud-item"><p class="hud-title">Materias Aprobadas</p><p class="hud-value">{materias_aprobadas} / {total_materias}</p></div>
                </div>
                """, unsafe_allow_html=True)

            # Estilos dinámicos para las notas (Semáforo de Celdas)
            def pintar_celdas(val):
                try:
                    n = float(val)
                    if n < 6.0: return 'color: #cc0000; font-weight: bold; background-color: #ffe6e6;'
                    elif n >= 9.0: return 'color: #00994c; font-weight: bold; background-color: #e6ffe6;'
                    return 'color: #0d1b2a; font-weight: bold;'
                except: return ''

            # Aplicamos el semáforo a las columnas numéricas
            cols_num = [c for c in ['P1', 'P2', 'P3', 'P4', 'PROMEDIO'] if c in df_mostrar.columns]
            df_pintado = df_mostrar.style.map(pintar_celdas, subset=cols_num).format("{:.1f}", subset=cols_num)

            st.markdown("<div style='background-color:#d4af37; color:#0d1b2a; font-family:Arial Black; font-size:13px; text-align:center; padding:10px; border:3px solid #0d1b2a; border-radius:8px 8px 0 0; position:relative; z-index:11; letter-spacing:1px;'>BOLETÍN OFICIAL DE CALIFICACIONES</div>", unsafe_allow_html=True)
            
            # Mostramos la tabla como MODO LECTURA (dataframe, no data_editor)
            st.dataframe(df_pintado, use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"🚨 Falla en el sistema de rastreo: {e}")

if __name__ == "__main__":
    ejecutar()
