# ═══════════════════════════════════════════════════════
#   pantalla_calendario.py — Sistema de Riego Tica-Tica
# ═══════════════════════════════════════════════════════

import streamlit as st
import calendar
from datetime import date, timedelta

from utils_imagenes import tag_imagen

MESES = [
    "Enero","Febrero","Marzo","Abril","Mayo","Junio",
    "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"
]

DIAS_ES = ["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo"]

INVERNADEROS = [
    "Escuela Elizardo Perez A",
    "Colegio Elizardo Perez B"
]

IMG_ESCUELA = "imagenes/E1.jpg"
IMG_COLEGIO = "imagenes/E2.jpg"

# Colores igual que la laptop
CAL_DAY_VERDURAS_BG = "#18692F"  # verde oscuro — verduras regadas
CAL_DAY_PAPA_BG     = "#7B3F00"  # marron      — papa regada
CAL_DAY_HOY_BG      = "#1A7F3A"  # verde hoy

# ── CSS ─────────────────────────────────────────────────
CSS_CALENDARIO = """
<style>
    .stApp {
        background: linear-gradient(135deg, #1a7a2e 0%, #0d4a6b 50%, #03053A 100%) !important;
        min-height: 100vh;
    }
    [data-testid="stAppViewContainer"] { background: transparent !important; }
    [data-testid="stMain"]             { background: transparent !important; }

    .header-cal {
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
    }

    /* Tabla calendario */
    .cal-tabla {
        width: 100%;
        border-collapse: separate;
        border-spacing: 4px;
        background: white;
        border-radius: 16px;
        padding: 12px;
    }
    .cal-cabecera {
        background: #2E7D32;
        color: white;
        border-radius: 8px;
        padding: 8px 4px;
        text-align: center;
        font-weight: bold;
        font-size: 0.85rem;
    }
    .cal-dia-normal   { background:#e8f5e9; color:#2e7d32; border-radius:10px; padding:10px 4px; text-align:center; font-weight:bold; font-size:0.95rem; }
    .cal-dia-hoy      { background:#1A7F3A; color:white;   border-radius:10px; padding:10px 4px; text-align:center; font-weight:bold; font-size:0.95rem; }
    .cal-dia-verduras { background:#18692F; color:white;   border-radius:10px; padding:10px 4px; text-align:center; font-weight:bold; font-size:0.95rem; }
    .cal-dia-papa     { background:#7B3F00; color:white;   border-radius:10px; padding:10px 4px; text-align:center; font-weight:bold; font-size:0.95rem; }

    /* Panel info */
    .panel-info {
        background: white;
        border-radius: 16px;
        border: 2px solid #a5d6a7;
        padding: 18px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    .card-prox-v {
        background: #e8f5e9;
        border: 2px solid #18692F;
        border-radius: 12px;
        padding: 12px 14px;
        margin-bottom: 10px;
    }
    .card-prox-p {
        background: #fdf6f0;
        border: 2px solid #7B3F00;
        border-radius: 12px;
        padding: 12px 14px;
        margin-bottom: 10px;
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

    /* Textos nativos de Streamlit (subheader, labels) en blanco
       para que se vean sobre el fondo oscuro */
    h1, h2, h3, .stMarkdown p, label, .stSelectbox label,
    .stDateInput label, .stTextInput label, .stNumberInput label {
        color: white !important;
    }
    /* El contenido DENTRO de los inputs (texto que escribe el usuario)
       se mantiene oscuro para que se lea sobre fondo claro */
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
#  CALCULOS PROXIMOS RIEGOS
#  (igual que _calcular_proximo_verduras/papa en la laptop)
# ════════════════════════════════════════════════════════
def _calcular_proximo_verduras(riegos: dict) -> date:
    hoy = date.today()
    riegos_v = sorted(
        [f for f, m in riegos.items() if "Papa" not in (m or "") and f <= hoy],
        reverse=True
    )
    if riegos_v:
        proximo = riegos_v[0] + timedelta(days=2)
        while proximo <= hoy:
            proximo += timedelta(days=2)
        return proximo
    return hoy + timedelta(days=2)


def _calcular_proximo_papa(riegos: dict) -> date:
    hoy = date.today()
    riegos_p = sorted(
        [f for f, m in riegos.items() if "Papa" in (m or "") and f <= hoy],
        reverse=True
    )
    if riegos_p:
        proximo = riegos_p[0] + timedelta(days=14)
        while proximo <= hoy:
            proximo += timedelta(days=14)
        return proximo
    return hoy + timedelta(days=14)


def _dias_restantes_texto(fecha: date) -> str:
    delta = (fecha - date.today()).days
    if delta == 0:   return "Hoy!"
    elif delta == 1: return "Manana"
    else:            return f"En {delta} dias"


# ════════════════════════════════════════════════════════
#  VISTA 1 — SELECCION DE INVERNADERO
# ════════════════════════════════════════════════════════
def _mostrar_seleccion_calendario():
    st.markdown("""
    <div class="header-cal">CALENDARIO DE RIEGO</div>
    """, unsafe_allow_html=True)

    if st.button("Volver al menu", key="btn_volver_cal_sel"):
        st.session_state.pagina = "principal"
        st.rerun()

    st.markdown("---")
    st.markdown('<div style="text-align:center;font-size:1.4rem;font-weight:bold;color:white;margin-bottom:6px;">Selecciona el invernadero</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;color:#c8e6c9;margin-bottom:28px;">De cual invernadero deseas ver y gestionar el calendario de riego?</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        img_html = tag_imagen(IMG_ESCUELA, "inv-card-img")
        tarjeta = (
            f'<div class="inv-card-a">{img_html}'
            f'<div class="inv-nombre">Escuela Elizardo Perez A</div></div>'
        )
        st.markdown(tarjeta, unsafe_allow_html=True)
        st.write("")
        if st.button("Ver Calendario", key="cal_inv_a", use_container_width=True):
            st.session_state.cal_invernadero = INVERNADEROS[0]
            st.session_state.invernadero     = INVERNADEROS[0]
            st.session_state.cal_yr = date.today().year
            st.session_state.cal_mo = date.today().month
            st.rerun()

    with c2:
        img_html = tag_imagen(IMG_COLEGIO, "inv-card-img")
        tarjeta = (
            f'<div class="inv-card-b">{img_html}'
            f'<div class="inv-nombre">Colegio Elizardo Perez B</div></div>'
        )
        st.markdown(tarjeta, unsafe_allow_html=True)
        st.write("")
        if st.button("Ver Calendario", key="cal_inv_b", use_container_width=True):
            st.session_state.cal_invernadero = INVERNADEROS[1]
            st.session_state.invernadero     = INVERNADEROS[1]
            st.session_state.cal_yr = date.today().year
            st.session_state.cal_mo = date.today().month
            st.rerun()


# ════════════════════════════════════════════════════════
#  VISTA 2 — CALENDARIO COMPLETO
# ════════════════════════════════════════════════════════
def _mostrar_calendario_completo(cargar_riegos_fn, registrar_riego_fn,
                                  eliminar_riego_fn, agregar_log_fn):
    inv  = st.session_state.cal_invernadero
    es_a = "A" in inv or "Escuela" in inv
    c_hdr   = "#1A4D1D" if es_a else "#03053A"
    c_borde = "#2E7D32" if es_a else "#1565C0"
    c_nav   = "#18692F" if es_a else "#1565C0"

    # ── Header ───────────────────────────────────────────
    st.markdown(f"""
    <div class="header-cal" style="background:{c_hdr};">
        CALENDARIO DE RIEGO — {inv.upper()}
    </div>
    """, unsafe_allow_html=True)

    col_v, _ = st.columns([1, 3])
    with col_v:
        if st.button("Volver", key="btn_volver_cal"):
            del st.session_state["cal_invernadero"]
            st.rerun()

    st.markdown("---")

    # ── Cargar riegos ────────────────────────────────────
    riegos = cargar_riegos_fn(inv)
    hoy    = date.today()

    # ── Navegacion mes ───────────────────────────────────
    c1, c2, c3 = st.columns([1, 3, 1])
    with c1:
        if st.button("Anterior", key="cal_ant"):
            if st.session_state.cal_mo == 1:
                st.session_state.cal_mo = 12
                st.session_state.cal_yr -= 1
            else:
                st.session_state.cal_mo -= 1
            st.rerun()
    with c2:
        st.markdown(
            f'<div style="text-align:center;font-size:1.3rem;font-weight:bold;color:white;">'
            f'{MESES[st.session_state.cal_mo-1]}   {st.session_state.cal_yr}</div>',
            unsafe_allow_html=True
        )
    with c3:
        if st.button("Siguiente", key="cal_sig"):
            if st.session_state.cal_mo == 12:
                st.session_state.cal_mo = 1
                st.session_state.cal_yr += 1
            else:
                st.session_state.cal_mo += 1
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    yr, mo   = st.session_state.cal_yr, st.session_state.cal_mo
    cal_data = calendar.monthcalendar(yr, mo)

    # ── Dos columnas: CALENDARIO | PANEL INFO ────────────
    col_cal, col_info = st.columns([3, 1])

    # ════════════════════════
    #  COLUMNA IZQUIERDA — TABLA CALENDARIO
    #  (igual que _dibujar_calendario en la laptop)
    # ════════════════════════
    with col_cal:
        tabla = f"""
        <table class="cal-tabla">
        <tr>
        """
        for d in ["Lunes","Martes","Mierc","Jueves","Viernes","Sabado","Domingo"]:
            tabla += f'<th class="cal-cabecera" style="background:{c_nav};">{d}</th>'
        tabla += "</tr>"

        for week in cal_data:
            tabla += "<tr>"
            for day in week:
                if day == 0:
                    tabla += '<td style="padding:4px;"></td>'
                else:
                    d_obj      = date(yr, mo, day)
                    es_hoy     = (d_obj == hoy)
                    motivo     = riegos.get(d_obj, "")
                    es_regado  = d_obj in riegos
                    es_papa    = "Papa" in (motivo or "")
                    es_verduras= es_regado and not es_papa

                    if es_papa:
                        clase = "cal-dia-papa"
                    elif es_verduras:
                        clase = "cal-dia-verduras"
                    elif es_hoy:
                        clase = "cal-dia-hoy"
                    else:
                        clase = "cal-dia-normal"

                    tooltip = f'title="{motivo}"' if motivo else ""
                    tabla += f'<td {tooltip} class="{clase}">{day}</td>'
            tabla += "</tr>"
        tabla += "</table>"

        st.markdown(tabla, unsafe_allow_html=True)

        # ── Leyenda igual que la laptop ───────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        lc1, lc2, lc3, lc4 = st.columns(4)
        with lc1:
            st.markdown(f'<span style="background:{CAL_DAY_VERDURAS_BG};color:white;border-radius:6px;padding:4px 10px;">&#9632;</span> Verduras regadas', unsafe_allow_html=True)
        with lc2:
            st.markdown(f'<span style="background:{CAL_DAY_PAPA_BG};color:white;border-radius:6px;padding:4px 10px;">&#9632;</span> Papa regada', unsafe_allow_html=True)
        with lc3:
            st.markdown(f'<span style="background:{CAL_DAY_HOY_BG};color:white;border-radius:6px;padding:4px 10px;">&#9632;</span> Hoy', unsafe_allow_html=True)
        with lc4:
            st.markdown(f'<span style="background:#e8f5e9;color:#2e7d32;border-radius:6px;padding:4px 10px;">&#9632;</span> Normal', unsafe_allow_html=True)

    # ════════════════════════
    #  COLUMNA DERECHA — PANEL INFO
    #  (igual que _build_panel_info en la laptop)
    # ════════════════════════
    with col_info:
        # Proximo riego general
        futuras = sorted([f for f in riegos if f > hoy])
        if futuras:
            prox_txt = f"Proximo riego:<br>{futuras[0].strftime('%d / %m / %Y')}"
        elif riegos:
            ultimo = max(riegos.keys())
            prox_txt = f"Ultimo riego:<br>{ultimo.strftime('%d / %m / %Y')}"
        else:
            prox_txt = "Sin riegos registrados"

        prox_v = _calcular_proximo_verduras(riegos)
        prox_p = _calcular_proximo_papa(riegos)

        panel_html = (
            f'<div class="panel-info">'
            f'<div style="font-size:1rem;font-weight:bold;color:#1a2e0a;margin-bottom:8px;">Informacion</div>'
            f'<div style="font-size:0.85rem;color:{c_nav};font-weight:bold;margin-bottom:12px;">{prox_txt}</div>'
            f'<hr style="border:1px solid {c_borde};margin:8px 0;">'
            f'<div class="card-prox-v">'
            f'<div style="font-size:0.9rem;font-weight:bold;color:{CAL_DAY_VERDURAS_BG};">Proximo Riego</div>'
            f'<div style="font-size:0.75rem;color:#6b7c5a;">Verduras - cada 2 dias</div>'
            f'<div style="font-size:0.95rem;font-weight:bold;color:#1a2e0a;margin-top:4px;">'
            f'{DIAS_ES[prox_v.weekday()]} {prox_v.day} {MESES[prox_v.month-1]}</div>'
            f'<div style="font-size:0.85rem;font-weight:bold;color:{CAL_DAY_VERDURAS_BG};">'
            f'{_dias_restantes_texto(prox_v)}</div>'
            f'</div>'
            f'<div class="card-prox-p">'
            f'<div style="font-size:0.9rem;font-weight:bold;color:{CAL_DAY_PAPA_BG};">Proximo Riego</div>'
            f'<div style="font-size:0.75rem;color:#6b7c5a;">Papa - cada 2 semanas</div>'
            f'<div style="font-size:0.95rem;font-weight:bold;color:#1a2e0a;margin-top:4px;">'
            f'{DIAS_ES[prox_p.weekday()]} {prox_p.day} {MESES[prox_p.month-1]}</div>'
            f'<div style="font-size:0.85rem;font-weight:bold;color:{CAL_DAY_PAPA_BG};">'
            f'{_dias_restantes_texto(prox_p)}</div>'
            f'</div>'
            f'</div>'
        )
        st.markdown(panel_html, unsafe_allow_html=True)

    # ── Registrar riego ──────────────────────────────────
    st.markdown("---")
    st.subheader("Registrar Riego")
    with st.form("form_riego"):
        fecha_sel  = st.date_input("Fecha de riego", value=hoy)
        motivo_sel = st.selectbox("Motivo", [
            "Manual — Verduras",
            "Manual — Papa",
            "Automatico — Verduras",
            "Automatico — Papa",
            "Programado",
            "Emergencia"
        ])
        if st.form_submit_button("Registrar Riego"):
            ok = registrar_riego_fn(
                fecha_sel, motivo_sel,
                st.session_state.invernadero,
                st.session_state.get("usuario", "")
            )
            if ok:
                agregar_log_fn(
                    st.session_state.invernadero,
                    f"Riego registrado: {fecha_sel} — {motivo_sel}"
                )
                st.success(f"Riego registrado: {fecha_sel} — {motivo_sel}")
                st.rerun()

    # ── Lista de riegos del mes ──────────────────────────
    riegos_mes = {f: m for f, m in riegos.items() if f.year == yr and f.month == mo}
    if riegos_mes:
        st.subheader(f"Riegos en {MESES[mo-1]} {yr}")
        for fecha, motivo in sorted(riegos_mes.items()):
            c1, c2 = st.columns([3, 1])
            with c1:
                es_papa = "Papa" in (motivo or "")
                color   = CAL_DAY_PAPA_BG if es_papa else CAL_DAY_VERDURAS_BG
                st.markdown(
                    f'<span style="background:{color};color:white;border-radius:6px;'
                    f'padding:2px 8px;font-size:0.8rem;">'
                    f'{"Papa" if es_papa else "Verduras"}</span> '
                    f'**{fecha.strftime("%d/%m/%Y")}** — {motivo}',
                    unsafe_allow_html=True
                )
            with c2:
                if st.button("Eliminar", key=f"del_{fecha}"):
                    eliminar_riego_fn(fecha, st.session_state.invernadero)
                    agregar_log_fn(
                        st.session_state.invernadero,
                        f"Riego eliminado: {fecha.strftime('%d/%m/%Y')}"
                    )
                    st.rerun()


# ════════════════════════════════════════════════════════
#  ENRUTADOR DE CALENDARIO
# ════════════════════════════════════════════════════════
def mostrar_calendario(cargar_riegos_fn, registrar_riego_fn,
                        eliminar_riego_fn, agregar_log_fn):
    """
    Punto de entrada desde app.py.
    Si no hay invernadero elegido muestra la seleccion,
    si ya hay uno muestra el calendario completo.
    """
    st.markdown(CSS_CALENDARIO, unsafe_allow_html=True)

    if "cal_invernadero" not in st.session_state:
        _mostrar_seleccion_calendario()
    else:
        _mostrar_calendario_completo(
            cargar_riegos_fn   = cargar_riegos_fn,
            registrar_riego_fn = registrar_riego_fn,
            eliminar_riego_fn  = eliminar_riego_fn,
            agregar_log_fn     = agregar_log_fn,
        )