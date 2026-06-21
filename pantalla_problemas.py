# ═══════════════════════════════════════════════════════
#   pantalla_problemas.py — Sistema de Riego Tica-Tica
# ═══════════════════════════════════════════════════════

import streamlit as st
from datetime import datetime, timezone, timedelta

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
        return dt.astimezone(TZ_BOLIVIA).strftime("%d/%m/%Y  %H:%M:%S")
    except Exception:
        return fecha_str[:19].replace("T", "  ")


# ── Colores de estado — igual que la laptop ─────────────
def _color_estado(estado: str):
    """Devuelve (bg, borde, color_texto, texto_estado)."""
    if estado == "ok":
        return "#f0fff4", "#66bb6a", "#1b5e20", "Funcionando"
    if estado == "error":
        return "#fff3f0", "#ef5350", "#b71c1c", "Error"
    if estado == "desconectado":
        return "#fffde7", "#ffb300", "#e65100", "Desconectado"
    if estado == "reconectando":
        return "#e3f2fd", "#1565c0", "#0d47a1", "Reconectando"
    return "#f0fff4", "#66bb6a", "#1b5e20", "Funcionando"


# ── CSS ─────────────────────────────────────────────────
CSS_PROBLEMAS = """
<style>
    .stApp {
        background: linear-gradient(135deg, #1a7a2e 0%, #0d4a6b 50%, #03053A 100%) !important;
        min-height: 100vh;
    }
    [data-testid="stAppViewContainer"] { background: transparent !important; }
    [data-testid="stMain"]             { background: transparent !important; }

    /* Header */
    .header-prob {
        background: #3a1a00;
        color: #ffd580;
        padding: 16px 30px;
        text-align: center;
        font-family: Arial Black, Arial, sans-serif;
        font-size: 1.2rem;
        font-weight: 900;
        letter-spacing: 2px;
        border-bottom: 3px solid #e07b20;
        margin-bottom: 0;
    }

    /* Barra resumen */
    .barra-resumen {
        background: #2d1a00;
        padding: 10px 24px;
        display: flex;
        gap: 24px;
        align-items: center;
        margin-bottom: 16px;
        border-radius: 0 0 12px 12px;
        flex-wrap: wrap;
    }
    .res-ok   { color: #66bb6a; font-weight: bold; font-size: 0.95rem; }
    .res-err  { color: #ef9a9a; font-weight: bold; font-size: 0.95rem; }
    .res-warn { color: #ffcc02; font-weight: bold; font-size: 0.95rem; }

    /* Tarjeta dispositivo */
    .dev-card {
        border-radius: 14px;
        border-width: 2px;
        border-style: solid;
        padding: 14px 18px;
        margin-bottom: 10px;
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    .dev-nombre  { font-weight: bold; font-size: 1rem; font-family: Arial, sans-serif; }
    .dev-info    { font-size: 0.82rem; color: #666; }
    .dev-estado  { font-weight: bold; font-size: 0.88rem; border-radius: 8px; padding: 2px 10px; display: inline-block; }
    .dev-error   { font-size: 0.82rem; margin-top: 4px; }

    /* Tarjeta de error en el log */
    .err-card {
        border-radius: 10px;
        border-width: 1px;
        border-style: solid;
        padding: 10px 14px;
        margin-bottom: 8px;
    }
    .err-titulo  { font-weight: bold; font-size: 0.95rem; }
    .err-mensaje { font-size: 0.85rem; color: #333; margin-top: 2px; }
    .err-fecha   { font-size: 0.78rem; color: #888; margin-top: 4px; }
    .err-badge-activo   { color: #b71c1c; font-weight: bold; font-size: 0.8rem; }
    .err-badge-resuelto { color: #1b5e20; font-weight: bold; font-size: 0.8rem; }

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

    /* Textos nativos de Streamlit (subheader, labels) en blanco */\n    h1, h2, h3, .stMarkdown p, label, .stSelectbox label,\n    .stDateInput label, .stTextInput label, .stNumberInput label {\n        color: white !important;\n    }\n    .stSelectbox div[data-baseweb="select"] *,\n    .stDateInput input,\n    .stTextInput input,\n    .stNumberInput input {\n        color: #1a2e0a !important;\n    }\n\n    #MainMenu                 { visibility: hidden; }
    footer                    { visibility: hidden; }
    header                    { visibility: hidden; }
    [data-testid="stToolbar"] { visibility: hidden; }
</style>
"""


# ════════════════════════════════════════════════════════
#  PANTALLA PRINCIPAL DE PROBLEMAS TECNICOS
# ════════════════════════════════════════════════════════
def mostrar_problemas(cargar_errores_fn, resolver_error_fn=None):
    """
    Muestra el diagnostico tecnico del sistema.

    Parametros:
        cargar_errores_fn — funcion de supabase_db.py para cargar errores
        resolver_error_fn — funcion opcional para marcar un error como resuelto
    """
    st.markdown(CSS_PROBLEMAS, unsafe_allow_html=True)

    inv = st.session_state.get("invernadero", "")

    # ── Header ───────────────────────────────────────────
    st.markdown("""
    <div class="header-prob">DIAGNOSTICO TECNICO DEL SISTEMA</div>
    """, unsafe_allow_html=True)

    # ── Boton volver ─────────────────────────────────────
    col_v, _ = st.columns([1, 3])
    with col_v:
        if st.button("Volver al menu", key="btn_volver_prob"):
            st.session_state.pagina = "principal"
            st.rerun()

    st.markdown("---")

    # ── Cargar errores desde Supabase ────────────────────
    with st.spinner("Cargando diagnostico..."):
        errores = cargar_errores_fn(inv)

    n_activos   = len([e for e in errores if not e.get("resuelto", False)])
    n_resueltos = len([e for e in errores if e.get("resuelto", False)])
    n_total     = len(errores)

    # ── Barra de resumen — igual que la laptop ────────────
    st.markdown(f"""
    <div class="barra-resumen">
        <span class="res-ok">Dispositivos OK: revisando</span>
        <span class="res-err">Errores criticos: {n_activos}</span>
        <span class="res-warn">Total registros: {n_total}  |  Resueltos: {n_resueltos}</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Sin errores ───────────────────────────────────────
    if n_activos == 0:
        st.markdown("""
        <div style="background:#f0fff4;border:2px solid #66bb6a;border-radius:14px;
                    padding:24px;text-align:center;margin:16px 0;">
            <div style="font-size:1.2rem;font-weight:bold;color:#1b5e20;">
                Todos los dispositivos funcionan correctamente
            </div>
            <div style="color:#4a7a4a;font-size:0.9rem;margin-top:6px;">
                No hay errores activos en este momento
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Dos columnas: DISPOSITIVOS | LOG DE ERRORES ───────
    col_devs, col_log = st.columns([1, 1])

    # ════════════════════════
    #  COLUMNA IZQUIERDA — ESTADO DE DISPOSITIVOS
    #  (igual que panel izquierdo de la laptop)
    # ════════════════════════
    with col_devs:
        st.markdown("""
        <div style="background:#3a1a00;color:#ffd580;border-radius:10px;
                    padding:8px;text-align:center;font-weight:bold;
                    margin-bottom:12px;">
            Estado de Dispositivos
        </div>
        """, unsafe_allow_html=True)

        if not errores:
            st.info("Sin registros de dispositivos.")
        else:
            # Agrupar errores por dispositivo
            dispositivos = {}
            for err in errores:
                dev_id = err.get("nombre", err.get("dev_id", "Desconocido"))
                if dev_id not in dispositivos:
                    dispositivos[dev_id] = {
                        "nombre":  dev_id,
                        "tipo":    err.get("tipo_error", "Error"),
                        "errores": [],
                        "resuelto_ultimo": True,
                    }
                dispositivos[dev_id]["errores"].append(err)
                if not err.get("resuelto", False):
                    dispositivos[dev_id]["resuelto_ultimo"] = False

            for dev_id, dev in dispositivos.items():
                tiene_error = not dev["resuelto_ultimo"]
                estado      = "error" if tiene_error else "ok"
                bg, borde, color_txt, txt_estado = _color_estado(estado)

                ultimo_err = ""
                for e in reversed(dev["errores"]):
                    if not e.get("resuelto", False):
                        ts       = _utc_a_bolivia(e.get("created_at", ""))
                        ultimo_err = f"Ultimo error ({ts}): {e.get('mensaje','')}"
                        break

                st.markdown(f"""
                <div class="dev-card" style="background:{bg};border-color:{borde};">
                    <div class="dev-nombre" style="color:{color_txt};">{dev_id}</div>
                    <div class="dev-info">[{dev['tipo']}]</div>
                    <div class="dev-estado" style="background:{borde}20;color:{color_txt};">
                        {txt_estado}
                    </div>
                    {'<div class="dev-error" style="color:#b71c1c;">'+ultimo_err+'</div>' if ultimo_err else ''}
                </div>
                """, unsafe_allow_html=True)

    # ════════════════════════
    #  COLUMNA DERECHA — LOG DE ERRORES
    #  (igual que panel derecho de la laptop)
    # ════════════════════════
    with col_log:
        st.markdown("""
        <div style="background:#3a1a00;color:#ffd580;border-radius:10px;
                    padding:8px;text-align:center;font-weight:bold;
                    margin-bottom:12px;">
            Registro de Errores
        </div>
        """, unsafe_allow_html=True)

        # Filtro — igual que los radio buttons de la laptop
        filtro = st.radio(
            "Filtrar:",
            ["Todos", "Activos", "Resueltos"],
            horizontal=True,
            key="filtro_errores"
        )

        if filtro == "Activos":
            errores_filtrados = [e for e in errores if not e.get("resuelto", False)]
        elif filtro == "Resueltos":
            errores_filtrados = [e for e in errores if e.get("resuelto", False)]
        else:
            errores_filtrados = errores

        if not errores_filtrados:
            st.markdown("""
            <div style="background:#f0fff4;border:1px solid #66bb6a;border-radius:10px;
                        padding:16px;text-align:center;color:#1b5e20;font-weight:bold;">
                Sin errores registrados
            </div>
            """, unsafe_allow_html=True)
        else:
            for err in reversed(errores_filtrados):
                resuelto  = err.get("resuelto", False)
                nombre    = err.get("nombre", err.get("dev_id", "Dispositivo"))
                tipo      = err.get("tipo_error", "Error")
                mensaje   = err.get("mensaje", "")
                ts        = _utc_a_bolivia(err.get("created_at", ""))
                err_id    = err.get("id", "")

                bg    = "#f0fff4" if resuelto else "#fff3f0"
                borde = "#66bb6a" if resuelto else "#ef5350"
                badge = '<span class="err-badge-resuelto">Resuelto</span>' \
                        if resuelto else \
                        '<span class="err-badge-activo">Activo</span>'

                st.markdown(f"""
                <div class="err-card" style="background:{bg};border-color:{borde};">
                    <div class="err-titulo" style="color:{'#1b5e20' if resuelto else '#b71c1c'};">
                        {nombre} [{tipo}]
                    </div>
                    <div class="err-mensaje">{mensaje}</div>
                    <div class="err-fecha">{ts} &nbsp; {badge}</div>
                </div>
                """, unsafe_allow_html=True)

                # Boton resolver si esta activo y hay funcion para ello
                if not resuelto and resolver_error_fn and err_id:
                    if st.button(f"Marcar como resuelto", key=f"res_{err_id}"):
                        resolver_error_fn(err_id)
                        st.success("Marcado como resuelto")
                        st.rerun()