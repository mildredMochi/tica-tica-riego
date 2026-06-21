# ═══════════════════════════════════════════════════════
#   pantalla_basedatos.py — Sistema de Riego Tica-Tica
# ═══════════════════════════════════════════════════════

import streamlit as st
from datetime import datetime, timezone, timedelta

SUPABASE_URL_DASHBOARD = "https://supabase.com/dashboard/project/hutmqgemeemqcwyuzrvx/editor"

# ── Zona horaria Bolivia (UTC-4) ────────────────────────
TZ_BOLIVIA = timezone(timedelta(hours=-4))

def _utc_a_bolivia(fecha_str: str) -> str:
    """Convierte fecha UTC a hora Bolivia — igual que la laptop."""
    if not fecha_str:
        return ""
    try:
        fecha_str = fecha_str.replace("Z", "+00:00")
        if "+" not in fecha_str and fecha_str.count("-") < 3:
            dt = datetime.fromisoformat(fecha_str).replace(tzinfo=timezone.utc)
        else:
            dt = datetime.fromisoformat(fecha_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(TZ_BOLIVIA).strftime("%Y-%m-%d  %H:%M:%S")
    except Exception:
        return fecha_str[:19].replace("T", "  ")


# ── CSS ─────────────────────────────────────────────────
CSS_BASEDATOS = """
<style>
    .stApp {
        background: linear-gradient(135deg, #1a7a2e 0%, #0d4a6b 50%, #03053A 100%) !important;
        min-height: 100vh;
    }
    [data-testid="stAppViewContainer"] { background: transparent !important; }
    [data-testid="stMain"]             { background: transparent !important; }

    /* Header — azul marino oscuro igual que la laptop */
    .header-bd {
        background: #0d1b2a;
        color: #f5c842;
        padding: 18px 30px;
        text-align: center;
        font-family: Arial Black, Arial, sans-serif;
        font-size: 1.3rem;
        font-weight: 900;
        letter-spacing: 2px;
        border-bottom: 3px solid #1565c0;
        margin-bottom: 0;
    }

    /* Tabla de datos */
    .tabla-bd {
        width: 100%;
        border-collapse: collapse;
        border-radius: 12px;
        overflow: hidden;
        background: white;
        box-shadow: 0 2px 12px rgba(0,0,0,0.1);
        font-size: 0.82rem;
    }
    .tabla-bd th {
        background: #1565c0;
        color: white;
        padding: 10px 12px;
        text-align: left;
        font-weight: bold;
        font-size: 0.8rem;
        white-space: nowrap;
    }
    .tabla-bd td {
        padding: 8px 12px;
        color: #1a1a2e;
        border-bottom: 1px solid #e8f0fe;
        white-space: nowrap;
        max-width: 180px;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .tabla-bd tr:nth-child(even) td { background: #f5f8ff; }
    .tabla-bd tr:hover td           { background: #e8f0fe; }

    /* Botones */
    .stButton > button {
        background-color: #1565c0 !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: bold !important;
        font-size: 0.95rem !important;
        padding: 10px 24px !important;
        width: 100% !important;
        letter-spacing: 0.5px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
    }
    .stButton > button:hover {
        background-color: #0d47a1 !important;
        color: white !important;
    }

    /* Tabs igual que la laptop */
    .stTabs [data-baseweb="tab-list"] {
        background: #1a2a3a;
        border-radius: 0;
        gap: 4px;
        padding: 4px 8px;
    }
    .stTabs [data-baseweb="tab"] {
        color: white !important;
        font-weight: bold;
        font-size: 0.95rem;
        border-radius: 0 !important;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background: #1565c0 !important;
        color: white !important;
    }

    /* Subtitulo tabla */
    .tabla-subtitulo {
        font-size: 0.85rem;
        color: #666;
        margin-bottom: 8px;
    }

    /* Textos nativos de Streamlit (subheader, labels) en blanco */\n    h1, h2, h3, .stMarkdown p, label, .stSelectbox label,\n    .stDateInput label, .stTextInput label, .stNumberInput label {\n        color: white !important;\n    }\n    .stSelectbox div[data-baseweb="select"] *,\n    .stDateInput input,\n    .stTextInput input,\n    .stNumberInput input {\n        color: #1a2e0a !important;\n    }\n\n    #MainMenu                 { visibility: hidden; }
    footer                    { visibility: hidden; }
    header                    { visibility: hidden; }
    [data-testid="stToolbar"] { visibility: hidden; }
</style>
"""


# ════════════════════════════════════════════════════════
#  PANTALLA BASE DE DATOS
# ════════════════════════════════════════════════════════
def mostrar_basedatos(get_supabase_fn):
    """
    Muestra el visor de base de datos con dos tabs:
    Lecturas Sensores y Riegos.

    Parametros:
        get_supabase_fn — funcion que devuelve el cliente de Supabase
    """
    st.markdown(CSS_BASEDATOS, unsafe_allow_html=True)

    inv = st.session_state.get("invernadero", "")

    # ── Header — fondo azul marino con texto dorado ───────
    st.markdown("""
    <div class="header-bd">
        BASE DE DATOS DEL SISTEMA DE TICA-TICA
    </div>
    """, unsafe_allow_html=True)

    # ── Botones: volver | abrir en Supabase ──────────────
    col_v, col_sup, col_esp = st.columns([1, 1, 2])
    with col_v:
        if st.button("Volver al menu", key="btn_volver_bd"):
            st.session_state.pagina = "principal"
            st.rerun()
    with col_sup:
        st.link_button("Abrir en Supabase", SUPABASE_URL_DASHBOARD)

    st.markdown("---")

    db = get_supabase_fn()

    # ── Tabs — igual que la laptop (Lecturas Sensores | Riegos) ──
    tab1, tab2 = st.tabs(["Lecturas Sensores", "Riegos"])

    # ══════════════════════════════════════════════════════
    #  TAB 1 — LECTURAS DE SENSORES
    #  (igual que _tab_sensores en la laptop)
    # ══════════════════════════════════════════════════════
    with tab1:
        st.markdown(
            "**Lecturas de sensores — lecturas_sensores**",
            help="Se registra automaticamente cada 60 segundos"
        )
        st.markdown(
            '<div class="tabla-subtitulo">Se registra automaticamente cada 60 segundos</div>',
            unsafe_allow_html=True
        )

        try:
            resp = db.table("lecturas_sensores")\
                .select("*")\
                .order("created_at", desc=True)\
                .limit(50)\
                .execute()

            if not resp.data:
                st.markdown("""
                <div style="background:white;border-radius:10px;padding:20px;
                            text-align:center;color:#888;">Sin registros.</div>
                """, unsafe_allow_html=True)
            else:
                # Construir tabla HTML igual que la laptop
                tabla = """
                <div style="overflow-x:auto;">
                <table class="tabla-bd">
                <thead><tr>
                    <th>ID</th>
                    <th>Fecha/Hora (Bolivia)</th>
                    <th>Invernadero</th>
                    <th>Hum. Suelo 1</th>
                    <th>Hum. Suelo 2</th>
                    <th>Hum. Suelo 3</th>
                    <th>Hum. Aire 1</th>
                    <th>Hum. Aire 2</th>
                    <th>Nivel Agua 1</th>
                    <th>Nivel Agua 2</th>
                    <th>Bomba 1</th>
                    <th>Bomba 2</th>
                </tr></thead>
                <tbody>
                """
                for r in resp.data:
                    b1 = "ON"  if r.get("bomba1_encendida") else "OFF"
                    b2 = "ON"  if r.get("bomba2_encendida") else "OFF"
                    c1 = "#2e7d32" if r.get("bomba1_encendida") else "#c62828"
                    c2 = "#2e7d32" if r.get("bomba2_encendida") else "#c62828"
                    tabla += f"""
                    <tr>
                        <td>{r.get('id','')}</td>
                        <td>{_utc_a_bolivia(str(r.get('created_at','')))} </td>
                        <td>{r.get('invernadero','')}</td>
                        <td>{r.get('humedad_s1') or 0:.1f}%</td>
                        <td>{r.get('humedad_s2') or 0:.1f}%</td>
                        <td>{r.get('humedad_s3') or 0:.1f}%</td>
                        <td>{r.get('humedad_a1') or 0:.1f}%</td>
                        <td>{r.get('humedad_a2') or 0:.1f}%</td>
                        <td>{r.get('nivel_agua_1') or 0:.1f}%</td>
                        <td>{r.get('nivel_agua_2') or 0:.1f}%</td>
                        <td style="color:{c1};font-weight:bold;">{b1}</td>
                        <td style="color:{c2};font-weight:bold;">{b2}</td>
                    </tr>
                    """
                tabla += "</tbody></table></div>"
                st.markdown(tabla, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error al cargar lecturas: {e}")

        st.markdown("<br>", unsafe_allow_html=True)

        # Botones — igual que la laptop
        col_act, col_lim, col_esp = st.columns([1, 1, 2])
        with col_act:
            if st.button("Actualizar tabla", key="act_sensores"):
                st.rerun()
        with col_lim:
            if st.button("Limpiar todos los datos", key="lim_sensores"):
                st.session_state["confirmar_limpiar"] = "lecturas_sensores"
                st.rerun()

        # Confirmacion de limpieza
        if st.session_state.get("confirmar_limpiar") == "lecturas_sensores":
            st.warning("Estas seguro que quieres eliminar TODAS las lecturas? Esta accion NO se puede deshacer.")
            col_si, col_no, _ = st.columns([1, 1, 3])
            with col_si:
                if st.button("Si, eliminar todo", key="confirm_lim_sens"):
                    try:
                        db.table("lecturas_sensores").delete().gt("id", 0).execute()
                        st.success("Todos los datos de lecturas fueron eliminados.")
                        st.session_state.pop("confirmar_limpiar", None)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al limpiar: {e}")
            with col_no:
                if st.button("Cancelar", key="cancel_lim_sens"):
                    st.session_state.pop("confirmar_limpiar", None)
                    st.rerun()

    # ══════════════════════════════════════════════════════
    #  TAB 2 — RIEGOS
    #  (igual que _tab_riegos en la laptop)
    # ══════════════════════════════════════════════════════
    with tab2:
        st.markdown("**Calendario de riegos registrados — riegos**")
        st.markdown(
            '<div class="tabla-subtitulo">Cada fecha marcada como dia de riego en el calendario</div>',
            unsafe_allow_html=True
        )

        try:
            resp = db.table("riegos")\
                .select("*")\
                .order("fecha", desc=True)\
                .execute()

            if not resp.data:
                st.markdown("""
                <div style="background:white;border-radius:10px;padding:20px;
                            text-align:center;color:#888;">Sin registros.</div>
                """, unsafe_allow_html=True)
            else:
                tabla = """
                <div style="overflow-x:auto;">
                <table class="tabla-bd">
                <thead><tr>
                    <th>ID</th>
                    <th>Fecha</th>
                    <th>Motivo</th>
                    <th>Invernadero</th>
                    <th>Registrado por</th>
                    <th>Creado en</th>
                </tr></thead>
                <tbody>
                """
                for r in resp.data:
                    tabla += f"""
                    <tr>
                        <td>{r.get('id','')}</td>
                        <td>{r.get('fecha','')}</td>
                        <td>{r.get('motivo','')}</td>
                        <td>{r.get('invernadero','')}</td>
                        <td>{r.get('registrado_por','') or '—'}</td>
                        <td>{_utc_a_bolivia(str(r.get('created_at','')))} </td>
                    </tr>
                    """
                tabla += "</tbody></table></div>"
                st.markdown(tabla, unsafe_allow_html=True)

                # Metrica total — igual que la laptop
                st.markdown("<br>", unsafe_allow_html=True)
                st.metric("Total de riegos registrados", len(resp.data))

        except Exception as e:
            st.error(f"Error al cargar riegos: {e}")

        st.markdown("<br>", unsafe_allow_html=True)

        col_act, col_lim, col_esp = st.columns([1, 1, 2])
        with col_act:
            if st.button("Actualizar tabla", key="act_riegos"):
                st.rerun()
        with col_lim:
            if st.button("Limpiar todos los datos", key="lim_riegos"):
                st.session_state["confirmar_limpiar"] = "riegos"
                st.rerun()

        if st.session_state.get("confirmar_limpiar") == "riegos":
            st.warning("Estas seguro que quieres eliminar TODOS los riegos registrados? Esta accion NO se puede deshacer.")
            col_si, col_no, _ = st.columns([1, 1, 3])
            with col_si:
                if st.button("Si, eliminar todo", key="confirm_lim_riegos"):
                    try:
                        db.table("riegos").delete().gt("id", 0).execute()
                        st.success("Todos los riegos fueron eliminados.")
                        st.session_state.pop("confirmar_limpiar", None)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al limpiar: {e}")
            with col_no:
                if st.button("Cancelar", key="cancel_lim_riegos"):
                    st.session_state.pop("confirmar_limpiar", None)
                    st.rerun()