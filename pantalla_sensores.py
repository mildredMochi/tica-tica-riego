# ═══════════════════════════════════════════════════════
#   pantalla_sensores.py — Sistema de Riego Tica-Tica
# ═══════════════════════════════════════════════════════

import streamlit as st
from datetime import date

from utils_imagenes import tag_imagen

INVERNADEROS = [
    "Escuela Elizardo Pérez A",
    "Colegio Elizardo Pérez B"
]

# Imágenes — mismos nombres que en la laptop
IMG_ESCUELA = "imagenes/E1.jpg"
IMG_COLEGIO = "imagenes/E2.jpg"

# ── CSS ─────────────────────────────────────────────────
CSS_SENSORES = """
<style>
    .stApp {
        background: linear-gradient(135deg, #1a7a2e 0%, #0d4a6b 50%, #03053A 100%) !important;
        min-height: 100vh;
    }
    [data-testid="stAppViewContainer"] { background: transparent !important; }
    [data-testid="stMain"]             { background: transparent !important; }

    /* Header */
    .header-sensores {
        background: #03053A;
        color: white;
        padding: 16px 30px;
        text-align: center;
        font-family: Arial Black, Arial, sans-serif;
        font-size: 1.2rem;
        font-weight: 900;
        letter-spacing: 2px;
        border-bottom: 3px solid #1a7a2e;
        margin-bottom: 20px;
    }

    /* Tarjetas seleccion invernadero */
    .inv-card-a {
        background: #e8f5e8;
        border: 3px solid #2E7D32;
        border-radius: 20px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }
    .inv-card-b {
        background: #e3f2fd;
        border: 3px solid #1565C0;
        border-radius: 20px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }
    .inv-card-img {
        width: 100%;
        border-radius: 10px;
        margin-bottom: 12px;
        max-height: 160px;
        object-fit: cover;
    }
    .inv-nombre {
        font-weight: bold;
        font-size: 1.1rem;
        color: #1a2e0a;
        margin: 8px 0 4px 0;
        font-family: Arial, sans-serif;
    }

    /* Panel sensores — columna izquierda */
    .panel-titulo {
        color: white;
        border-radius: 10px;
        padding: 8px;
        text-align: center;
        font-weight: bold;
        font-family: Arial Black, Arial, sans-serif;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }
    .sub-seccion {
        color: white;
        font-weight: bold;
        font-size: 0.95rem;
        margin: 14px 0 6px 0;
        text-shadow: 0 1px 3px rgba(0,0,0,0.4);
    }
    .sensor-fila {
        background: white;
        border: 1.5px solid #a5d6a7;
        border-radius: 12px;
        padding: 10px 14px;
        margin-bottom: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .sensor-nombre {
        color: #2d3a1e;
        font-size: 0.9rem;
        font-family: Arial, sans-serif;
    }
    .sensor-valor-verde  { font-weight: bold; font-size: 1.1rem; color: #2e7d32; }
    .sensor-valor-naranja{ font-weight: bold; font-size: 1.1rem; color: #e65100; }
    .sensor-valor-rojo   { font-weight: bold; font-size: 1.1rem; color: #d32f2f; }

    /* Bomba */
    .bomba-on {
        background: #e8fff0;
        border: 3px solid #2e7d32;
        border-radius: 14px;
        padding: 14px;
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
        color: #2e7d32;
        margin-bottom: 6px;
    }
    .bomba-off {
        background: #fff0f0;
        border: 3px solid #ed7f7f;
        border-radius: 14px;
        padding: 14px;
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
        color: #c62828;
        margin-bottom: 6px;
    }
    .bomba-subtexto {
        font-size: 0.82rem;
        color: #6b7c5a;
        margin-top: 4px;
        font-weight: normal;
    }

    /* Botones */
    .stButton > button {
        background-color: #2d6e1a !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: bold !important;
        font-size: 1rem !important;
        padding: 10px 24px !important;
        width: 100% !important;
        letter-spacing: 0.5px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
    }
    .stButton > button:hover {
        background-color: #1a5010 !important;
        color: white !important;
    }

    /* Ocultar elementos Streamlit */
    /* Textos nativos de Streamlit (subheader, labels) en blanco */
    h1, h2, h3, .stMarkdown p, label, .stSelectbox label,
    .stDateInput label, .stTextInput label, .stNumberInput label {
        color: white !important;
    }
    .stSelectbox div[data-baseweb="select"] *,
    .stDateInput input,
    .stTextInput input,
    .stNumberInput input {
        color: #1a2e0a !important;
    }

    #MainMenu                 { visibility: hidden; }
    footer                    { visibility: hidden; }
    header                    { visibility: hidden; }
    [data-testid="stToolbar"] { visibility: hidden; }
</style>
"""


# ════════════════════════════════════════════════════════
#  VISTA 1 — SELECCION DE INVERNADERO
#  (igual que _mostrar_seleccion en la laptop)
# ════════════════════════════════════════════════════════
def mostrar_seleccion_invernadero():
    st.markdown(CSS_SENSORES, unsafe_allow_html=True)

    st.markdown("""
    <div class="header-sensores">SENSORES Y CONTROL DE RIEGO</div>
    """, unsafe_allow_html=True)

    if st.button("Volver al menu", key="btn_volver_sel"):
        st.session_state.pagina = "principal"
        st.rerun()

    st.markdown("---")
    st.markdown('<div style="text-align:center;font-size:1.4rem;font-weight:bold;color:white;margin-bottom:6px;">Selecciona la zona de riego</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;color:#c8e6c9;margin-bottom:28px;">Los sensores son compartidos. Cada zona tiene su propio tanque y bomba.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    # ── Zona A ────────────────────────────────────
    with c1:
        img_html = tag_imagen(IMG_ESCUELA, "inv-card-img")
        tarjeta = (
            f'<div class="inv-card-a">{img_html}'
            f'<div class="inv-nombre">Escuela Elizardo Pérez A</div>'
            f'<div style="color:#6b7c5a;font-size:0.88rem;">Zona A — Verduras y Papa</div>'
            f'</div>'
        )
        st.markdown(tarjeta, unsafe_allow_html=True)
        st.write("")
        if st.button("Ingresar", key="inv_a", use_container_width=True):
            st.session_state.sensor_invernadero = INVERNADEROS[0]
            st.session_state.invernadero        = INVERNADEROS[0]
            st.rerun()

    # ── Zona B ────────────────────────────────────
    with c2:
        img_html = tag_imagen(IMG_COLEGIO, "inv-card-img")
        tarjeta = (
            f'<div class="inv-card-b">{img_html}'
            f'<div class="inv-nombre">Colegio Elizardo Pérez B</div>'
            f'<div style="color:#6b7c5a;font-size:0.88rem;">Zona B — Verduras y Papa</div>'
            f'</div>'
        )
        st.markdown(tarjeta, unsafe_allow_html=True)
        st.write("")
        if st.button("Ingresar", key="inv_b", use_container_width=True):
            st.session_state.sensor_invernadero = INVERNADEROS[1]
            st.session_state.invernadero        = INVERNADEROS[1]
            st.rerun()


# ════════════════════════════════════════════════════════
#  HELPER — fila de sensor (igual que _crear_fila en laptop)
# ════════════════════════════════════════════════════════
def _fila_sensor(nombre, valor, unidad):
    """Dibuja una fila blanca con nombre a la izquierda y valor a la derecha."""
    if unidad == "%" and valor < 30:
        clase_valor = "sensor-valor-rojo"
    elif unidad == "%" and valor < 50:
        clase_valor = "sensor-valor-naranja"
    elif unidad == "°C":
        clase_valor = "sensor-valor-naranja"
    else:
        clase_valor = "sensor-valor-verde"

    st.markdown(f"""
    <div class="sensor-fila">
        <span class="sensor-nombre">{nombre}</span>
        <span class="{clase_valor}">{valor:.1f}{unidad}</span>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
#  HELPER — bloque de bomba
# ════════════════════════════════════════════════════════
def _bloque_bomba(numero, encendida, nivel_agua, color_panel,
                  crear_orden_fn, registrar_riego_fn, agregar_log_fn):
    """
    Dibuja el control de una bomba.
    Equivale a _build_bomba de la laptop.
    """
    cultivo   = "Verduras" if numero == 1 else "Papa"
    key_start = f"start_b{numero}"
    key_stop  = f"stop_b{numero}"
    key_lim   = f"lim_b{numero}"

    if encendida:
        st.markdown(f"""
        <div class="bomba-on">
            Bomba {numero} encendida
            <div class="bomba-subtexto">Nivel agua: {nivel_agua:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(min(nivel_agua / 100, 1.0))
        if st.button(f"Detener Riego de {cultivo}", key=key_stop,
                     use_container_width=True):
            crear_orden_fn(numero, "apagar",
                           invernadero=st.session_state.sensor_invernadero)
            agregar_log_fn(
                st.session_state.sensor_invernadero,
                f"Bomba {numero} detenida — {cultivo} — manual"
            )
            st.success(f"Bomba {numero} detenida")
            st.rerun()
    else:
        st.markdown(f"""
        <div class="bomba-off">
            Bomba {numero} apagada
            <div class="bomba-subtexto">Nivel agua: {nivel_agua:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(min(nivel_agua / 100, 1.0))

        limite = st.number_input(
            f"Limite minutos bomba {numero}",
            min_value=1, max_value=120, value=15, key=key_lim
        )

        if st.button(f"Iniciar Riego de {cultivo}", key=key_start,
                     use_container_width=True):
            crear_orden_fn(numero, "encender", duracion_minutos=limite,
                           invernadero=st.session_state.sensor_invernadero)
            registrar_riego_fn(
                date.today(),
                f"Manual — {cultivo}",
                st.session_state.sensor_invernadero,
                st.session_state.get("usuario", "")
            )
            agregar_log_fn(
                st.session_state.sensor_invernadero,
                f"Bomba {numero} iniciada — {cultivo} — limite {limite} min"
            )
            st.success(f"Bomba {numero} iniciada — Limite: {limite} min")
            st.rerun()


# ════════════════════════════════════════════════════════
#  VISTA 2 — PANEL PRINCIPAL DE SENSORES Y CONTROL
#  (igual que _mostrar_panel_principal en la laptop)
#
#  NOTA IMPORTANTE: los sensores son COMPARTIDOS entre las
#  dos zonas (A y B) — no se filtran por invernadero. Lo unico
#  que cambia entre paneles es que Bomba 1 controla la zona A
#  y Bomba 2 controla la zona B, cada una con su propio tanque.
# ════════════════════════════════════════════════════════
def mostrar_panel_sensores(cargar_sensores_fn, cargar_historial_fn,
                            crear_orden_fn, obtener_estado_fn,
                            registrar_riego_fn, agregar_log_fn):
    """
    Panel completo de lecturas y control de bombas.

    Parametros:
        cargar_sensores_fn  — carga ultima lectura de sensores (compartida)
        cargar_historial_fn — carga historial para graficos (compartido)
        crear_orden_fn      — crea orden de bomba real (la ejecuta el ESP32)
        obtener_estado_fn   — lee el estado real confirmado por el ESP32
        registrar_riego_fn  — registra un riego en Supabase
        agregar_log_fn      — agrega log de actividad en Supabase
    """
    st.markdown(CSS_SENSORES, unsafe_allow_html=True)

    inv       = st.session_state.sensor_invernadero
    es_zona_a = "A" in inv or "Escuela" in inv
    numero_bomba_propia = 1 if es_zona_a else 2

    # Color segun zona — igual que colores_invernadero() en la laptop
    c_hdr   = "#1A4D1D" if es_zona_a else "#03053A"
    c_borde = "#2E7D32" if es_zona_a else "#1565C0"

    # ── Header ───────────────────────────────────────────
    st.markdown(f"""
    <div class="header-sensores" style="background:{c_hdr};">
        SENSORES Y CONTROL — {inv.upper()}
    </div>
    """, unsafe_allow_html=True)

    col_v, _ = st.columns([1, 3])
    with col_v:
        if st.button("Volver", key="btn_volver_panel"):
            del st.session_state["sensor_invernadero"]
            st.rerun()

    st.markdown("---")

    # ── Cargar datos (compartidos entre zonas, sin filtrar) ──
    with st.spinner("Cargando lecturas..."):
        datos = cargar_sensores_fn()

    # Si no hay datos usar ceros — igual que la laptop
    if not datos:
        st.markdown(
            '<div style="background:#fff3cd;border:2px solid #ffb300;border-radius:12px;'
            'padding:14px 18px;color:#5c4400;font-weight:bold;margin-bottom:12px;">'
            'Sin lecturas recientes.</div>',
            unsafe_allow_html=True
        )
        datos = {
            "humedad_s1": 0, "humedad_s2": 0, "humedad_s3": 0,
            "humedad_a1": 0, "humedad_a2": 0,
            "temperatura_1": 0, "temperatura_2": 0,
            "nivel_agua_1": 0, "nivel_agua_2": 0,
            "bomba1_encendida": False, "bomba2_encendida": False,
        }
    else:
        ts = datos.get("created_at", "")
        st.markdown(
            f'<div style="color:#e0f0e0;font-size:0.85rem;margin-bottom:8px;">'
            f'Ultima lectura: {ts[11:19] if len(ts) > 10 else "—"}</div>',
            unsafe_allow_html=True
        )

    # ── Dos columnas: SENSORES | CONTROL ─────────────────
    col_sens, col_ctrl = st.columns(2)

    # ════════════════════════════
    #  COLUMNA IZQUIERDA — SENSORES (compartidos)
    #  (igual que columna izquierda de la laptop)
    # ════════════════════════════
    with col_sens:
        st.markdown(f'<div class="panel-titulo" style="background:{c_borde};">LECTURAS EN TIEMPO REAL</div>', unsafe_allow_html=True)

        st.markdown('<div class="sub-seccion">Temperatura y Agua</div>', unsafe_allow_html=True)
        _fila_sensor("Temp. Aire 1", datos.get("temperatura_1", 0), "°C")
        _fila_sensor("Temp. Aire 2", datos.get("temperatura_2", 0), "°C")
        _fila_sensor("Nivel Agua 1", datos.get("nivel_agua_1", 0), "%")
        _fila_sensor("Nivel Agua 2", datos.get("nivel_agua_2", 0), "%")

        st.markdown('<div class="sub-seccion">Humedad Suelo</div>', unsafe_allow_html=True)
        _fila_sensor("Surco 1 Verduras", datos.get("humedad_s1", 0), "%")
        _fila_sensor("Surco 2 Verduras", datos.get("humedad_s2", 0), "%")
        _fila_sensor("Surco 3 Papa",     datos.get("humedad_s3", 0), "%")

        st.markdown('<div class="sub-seccion">Humedad Aire</div>', unsafe_allow_html=True)
        _fila_sensor("Sensor Aire 1", datos.get("humedad_a1", 0), "%")
        _fila_sensor("Sensor Aire 2", datos.get("humedad_a2", 0), "%")

    # ════════════════════════════
    #  COLUMNA DERECHA — CONTROL DE RIEGO
    #  Solo se muestra la bomba propia de esta zona.
    # ════════════════════════════
    with col_ctrl:
        st.markdown(f'<div class="panel-titulo" style="background:{c_borde};">CONTROL DE RIEGO</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="sub-seccion" style="color:white;">{inv}</div>', unsafe_allow_html=True)

        etiqueta_bomba = "Bomba 1 — Verduras (tanque A)" if numero_bomba_propia == 1 else "Bomba 2 — Papa (tanque B)"
        st.markdown(f'<div class="sub-seccion">{etiqueta_bomba}</div>', unsafe_allow_html=True)

        campo_nivel  = "nivel_agua_1" if numero_bomba_propia == 1 else "nivel_agua_2"

        # Estado REAL confirmado por el ESP32 (no el que insertaria el celular)
        estado_bombas = obtener_estado_fn(inv)
        campo_estado  = "bomba1" if numero_bomba_propia == 1 else "bomba2"

        _bloque_bomba(
            numero        = numero_bomba_propia,
            encendida     = estado_bombas.get(campo_estado, False),
            nivel_agua    = datos.get(campo_nivel, 0),
            color_panel   = c_borde,
            crear_orden_fn     = crear_orden_fn,
            registrar_riego_fn = registrar_riego_fn,
            agregar_log_fn     = agregar_log_fn,
        )

    # ── Graficos historicos ──────────────────────────────
    st.markdown("---")
    st.subheader("Historial de Lecturas")
    historial = cargar_historial_fn()
    if historial:
        import pandas as pd
        df = pd.DataFrame(historial)
        df["hora"] = df["created_at"].str[11:16]

        cols_suelo = [c for c in ["humedad_s1","humedad_s2","humedad_s3"] if c in df.columns]
        if cols_suelo:
            st.line_chart(df.set_index("hora")[cols_suelo], height=200)
            st.caption("Humedad suelo — Surcos 1, 2 y 3")

        cols_temp = [c for c in ["temperatura_1", "temperatura_2"] if c in df.columns]
        if cols_temp:
            st.line_chart(df.set_index("hora")[cols_temp], height=160)
            st.caption("Temperatura ambiente — Sensores 1 y 2")
    else:
        st.info("Sin historial disponible aun.")


# ════════════════════════════════════════════════════════
#  ENRUTADOR DE LA PANTALLA SENSORES
#  (decide si mostrar seleccion o panel)
# ════════════════════════════════════════════════════════
def mostrar_sensores(cargar_sensores_fn, cargar_historial_fn,
                     crear_orden_fn, obtener_estado_fn,
                     registrar_riego_fn, agregar_log_fn):
    """
    Punto de entrada desde app.py.
    Si no hay invernadero seleccionado muestra la seleccion,
    si ya hay uno muestra el panel de sensores y control.
    """
    if "sensor_invernadero" not in st.session_state:
        mostrar_seleccion_invernadero()
    else:
        mostrar_panel_sensores(
            cargar_sensores_fn  = cargar_sensores_fn,
            cargar_historial_fn = cargar_historial_fn,
            crear_orden_fn      = crear_orden_fn,
            obtener_estado_fn   = obtener_estado_fn,
            registrar_riego_fn  = registrar_riego_fn,
            agregar_log_fn      = agregar_log_fn,
        )
