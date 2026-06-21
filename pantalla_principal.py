# ═══════════════════════════════════════════════════════
#   pantalla_principal.py — Sistema de Riego Tica-Tica
# ═══════════════════════════════════════════════════════

import streamlit as st
from datetime import date
import calendar

from utils_imagenes import tag_imagen

MESES = [
    "Enero","Febrero","Marzo","Abril","Mayo","Junio",
    "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"
]

INVERNADEROS = [
    "Escuela Elizardo Perez A",
    "Colegio Elizardo Perez B"
]

# Imagenes — mismos nombres que en tu laptop
IMG_SENSORES  = "imagenes/f1.png"
IMG_PROBLEMAS = "imagenes/b2.png"
IMG_BASEDATOS = "imagenes/b3.png"

# ── CSS ─────────────────────────────────────────────────
CSS_PRINCIPAL = """
<style>
    .stApp {
        background: linear-gradient(135deg, #1a7a2e 0%, #0d4a6b 50%, #03053A 100%) !important;
        min-height: 100vh;
    }
    [data-testid="stAppViewContainer"] { background: transparent !important; }
    [data-testid="stMain"]             { background: transparent !important; }

    .header-principal {
        background: #03053A;
        color: white;
        padding: 16px 30px;
        text-align: center;
        font-family: Arial Black, Arial, sans-serif;
        font-size: 1.3rem;
        font-weight: 900;
        letter-spacing: 2px;
        border-bottom: 3px solid #1a7a2e;
        margin-bottom: 20px;
    }
    .header-sub {
        font-size: 0.85rem;
        color: #80c880;
        font-style: italic;
        font-family: Georgia, serif;
        font-weight: normal;
        letter-spacing: 0px;
        margin-top: 4px;
    }

    .card-menu {
        background: #e8f5e8;
        border-radius: 18px;
        border: 3px solid #386D23;
        padding: 20px 16px 16px 16px;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        min-height: 300px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }
    .card-titulo {
        font-size: 1rem;
        font-weight: 900;
        color: #1a2e0a;
        font-family: Arial Black, Arial, sans-serif;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .card-img {
        width: 100%;
        max-width: 200px;
        border-radius: 10px;
        margin: 8px 0;
        object-fit: cover;
        height: 140px;
    }
    .badge-error {
        background: #fff3f3;
        border: 1px solid #f44336;
        border-radius: 10px;
        padding: 6px 14px;
        color: #c62828;
        font-weight: bold;
        font-size: 0.85rem;
        text-align: center;
    }
    .badge-ok {
        background: #f0fff4;
        border: 1px solid #4caf50;
        border-radius: 10px;
        padding: 6px 14px;
        color: #2e7d32;
        font-weight: bold;
        font-size: 0.85rem;
        text-align: center;
    }
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
    #MainMenu                 { visibility: hidden; }
    footer                    { visibility: hidden; }
    header                    { visibility: hidden; }
    [data-testid="stToolbar"] { visibility: hidden; }
</style>
"""


def mostrar_principal(cargar_riegos_fn, cargar_errores_fn):
    """
    Muestra el menu principal con las 4 tarjetas.

    Parametros:
        cargar_riegos_fn  — funcion de supabase_db.py para cargar riegos
        cargar_errores_fn — funcion de supabase_db.py para cargar errores
    """

    st.markdown(CSS_PRINCIPAL, unsafe_allow_html=True)

    # ── HEADER ──────────────────────────────────────────
    st.markdown(f"""
    <div class="header-principal">
        SISTEMA DE RIEGO DEL DISTRITO MUNICIPAL ORIGINARIO DE TICA-TICA
        <div class="header-sub">
            {st.session_state.get('rol', '')} — {st.session_state.get('usuario', '')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── SELECTOR INVERNADERO + CERRAR SESION ─────────────
    col_inv, col_cerrar = st.columns([3, 1])
    with col_inv:
        inv = st.selectbox(
            "Invernadero activo:",
            INVERNADEROS,
            index=INVERNADEROS.index(st.session_state.get("invernadero", INVERNADEROS[0]))
        )
        st.session_state.invernadero = inv
    with col_cerrar:
        st.write("")
        st.write("")
        if st.button("Cerrar sesion", key="btn_cerrar"):
            for k in ["usuario", "rol", "pagina", "invernadero"]:
                st.session_state.pop(k, None)
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── DATOS PARA LAS TARJETAS ──────────────────────────
    riegos    = cargar_riegos_fn(st.session_state.invernadero)
    errores   = cargar_errores_fn(st.session_state.invernadero)
    n_errores = len(errores)

    c1, c2, c3, c4 = st.columns(4)

    # ══════════════════════════════
    #  TARJETA 1 — SENSORES
    # ══════════════════════════════
    with c1:
        img_html = tag_imagen(IMG_SENSORES, "card-img")
        st.markdown(f"""
        <div class="card-menu">
            <div class="card-titulo">SENSORES</div>
            {img_html}
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("Ingresar", key="btn_sensores"):
            st.session_state.pagina = "sensores"
            st.rerun()

    # ══════════════════════════════
    #  TARJETA 2 — CALENDARIO
    #  (igual que la laptop: marca dias regados y hoy)
    # ══════════════════════════════
    with c2:
        hoy      = date.today()
        yr, mo   = hoy.year, hoy.month
        cal_data = calendar.monthcalendar(yr, mo)

        # Cabecera de dias de la semana
        celdas = ['<div style="display:flex;flex-wrap:wrap;justify-content:center;gap:2px;margin-top:6px;">']
        for letra in ["L", "M", "X", "J", "V", "S", "D"]:
            celdas.append(
                f'<span style="width:26px;text-align:center;font-size:9px;'
                f'font-weight:bold;color:#1565c0;">{letra}</span>'
            )

        # Dias del mes
        for week in cal_data:
            for d in week:
                if d == 0:
                    celdas.append('<span style="width:26px;height:22px;display:inline-block;"></span>')
                else:
                    d_obj     = date(yr, mo, d)
                    es_hoy    = (d_obj == hoy)
                    es_regado = d_obj in riegos

                    if es_hoy and es_regado:
                        bg, fg = "#1A7F3A", "white"
                    elif es_regado:
                        bg, fg = "#1565c0", "white"
                    elif es_hoy:
                        bg, fg = "#1A7F3A", "white"
                    else:
                        bg, fg = "#c8e6c9", "#2e7d32"

                    celdas.append(
                        f'<span style="width:26px;height:22px;background:{bg};color:{fg};'
                        f'border-radius:5px;text-align:center;font-size:10px;font-weight:bold;'
                        f'line-height:22px;display:inline-block;">{d}</span>'
                    )
        celdas.append('</div>')
        dias_html = "".join(celdas)

        leyenda_html = (
            '<div style="display:flex;justify-content:center;gap:10px;margin-top:6px;font-size:10px;">'
            '<span><span style="background:#1565c0;color:white;border-radius:3px;'
            'padding:1px 6px;font-size:9px;">&#9632;</span> Regado</span>'
            '<span><span style="background:#1A7F3A;color:white;border-radius:3px;'
            'padding:1px 6px;font-size:9px;">&#9632;</span> Hoy</span>'
            '</div>'
        )

        tarjeta_cal = (
            f'<div class="card-menu" style="min-height:300px;">'
            f'<div class="card-titulo">CALENDARIO DE RIEGO</div>'
            f'<div style="font-size:11px;font-weight:bold;color:#1565c0;margin:4px 0;">'
            f'{MESES[mo-1]}&nbsp;&nbsp;{yr}</div>'
            f'{dias_html}'
            f'{leyenda_html}'
            f'</div>'
        )
        st.markdown(tarjeta_cal, unsafe_allow_html=True)
        st.write("")
        if st.button("Ingresar", key="btn_calendario"):
            st.session_state.pagina = "calendario"
            st.rerun()

    # ══════════════════════════════
    #  TARJETA 3 — PROBLEMAS TECNICOS
    # ══════════════════════════════
    with c3:
        if n_errores > 0:
            badge = f'<div class="badge-error">Advertencia: {n_errores} error{"es" if n_errores>1 else ""} activo{"s" if n_errores>1 else ""}</div>'
        else:
            badge = '<div class="badge-ok">Todos los dispositivos OK</div>'

        img_html = tag_imagen(IMG_PROBLEMAS, "card-img")
        st.markdown(f"""
        <div class="card-menu">
            <div class="card-titulo">PROBLEMAS TECNICOS</div>
            {img_html}
            {badge}
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("Ingresar", key="btn_problemas"):
            st.session_state.pagina = "problemas"
            st.rerun()

    # ══════════════════════════════
    #  TARJETA 4 — BASE DE DATOS
    # ══════════════════════════════
    with c4:
        img_html = tag_imagen(IMG_BASEDATOS, "card-img")
        st.markdown(f"""
        <div class="card-menu">
            <div style="background:#2d6e1a;color:white;border-radius:6px;
                        padding:2px 10px;font-size:10px;font-weight:bold;
                        align-self:flex-start;">NUEVO</div>
            <div class="card-titulo">BASE DE DATOS</div>
            {img_html}
            <div style="font-size:11px;color:#1565c0;">
                Historial &middot; Registros &middot; Lecturas &middot; Logs
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("Ingresar", key="btn_basedatos"):
            st.session_state.pagina = "basedatos"
            st.rerun()