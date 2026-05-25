# ═══════════════════════════════════════════════════════
#   app.py — Sistema de Riego Tica-Tica (Streamlit)
# ═══════════════════════════════════════════════════════

import streamlit as st
from datetime import date, datetime
import calendar

# ── CONFIGURACIÓN DE PÁGINA ──────────────────────────────
st.set_page_config(
    page_title="Sistema de Riego — Tica-Tica",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── USUARIOS (igual que tu pantalla_login.py) ────────────
USUARIOS = {
    "admin":      {"password": "123", "rol": "Administrador",   "icono": "⚙️"},
    "asesores":   {"password": "123", "rol": "Asesor Técnico",  "icono": "🌿"},
    "presidente": {"password": "123", "rol": "Presidente",      "icono": "🌾"},
    "junta":      {"password": "123", "rol": "Junta Directiva", "icono": "🏛️"},
}

INVERNADEROS = [
    "Escuela Elizardo Pérez A",
    "Colegio Elizardo Pérez B"
]

MESES = [
    "Enero","Febrero","Marzo","Abril","Mayo","Junio",
    "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"
]

# ── ESTILOS CSS ──────────────────────────────────────────
st.markdown("""
<style>
    /* Fondo general */
    .stApp { background-color: #f0f7f0; }

    /* Header principal */
    .header-principal {
        background: linear-gradient(135deg, #03053A, #1a4a1a);
        color: #F9FDFA;
        padding: 22px 30px;
        border-radius: 0 0 18px 18px;
        text-align: center;
        font-family: 'Times New Roman', serif;
        font-size: 1.6rem;
        font-weight: bold;
        margin-bottom: 24px;
        letter-spacing: 1px;
    }
    .header-sub {
        font-size: 0.95rem;
        color: #80c880;
        font-style: italic;
        font-family: Georgia, serif;
        margin-top: 4px;
    }

    /* Tarjetas del menú principal */
    .card-menu {
        background: #e8f5e8;
        border-radius: 20px;
        border: 3px solid #386D23;
        padding: 28px 20px;
        text-align: center;
        height: 320px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        transition: transform 0.2s;
        cursor: pointer;
    }
    .card-menu:hover { transform: translateY(-4px); }
    .card-titulo {
        font-size: 1.15rem;
        font-weight: bold;
        color: #2d3a1e;
        font-family: Arial, sans-serif;
    }
    .card-icono { font-size: 4.5rem; margin: 10px 0; }

    /* Login */
    .login-card {
        background: white;
        border-radius: 20px;
        border: 1px solid #c8e6c9;
        padding: 36px 40px;
        max-width: 460px;
        margin: 0 auto;
        box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    }
    .login-titulo {
        text-align: center;
        font-size: 1.4rem;
        font-weight: bold;
        color: #1a3a1a;
        margin-bottom: 6px;
    }
    .login-sub {
        text-align: center;
        color: #88aa88;
        font-size: 0.9rem;
        margin-bottom: 20px;
    }

    /* Sensores */
    .sensor-card {
        background: white;
        border-radius: 16px;
        border: 2px solid #a5d6a7;
        padding: 20px;
        text-align: center;
        margin-bottom: 12px;
    }
    .sensor-valor {
        font-size: 2.2rem;
        font-weight: bold;
        color: #2e7d32;
    }
    .sensor-label {
        font-size: 0.85rem;
        color: #6b7c5a;
        margin-top: 4px;
    }

    /* Bomba */
    .bomba-on {
        background: #f0fff4;
        border: 3px solid #1c2aa2;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
    }
    .bomba-off {
        background: #fff0f0;
        border: 3px solid #ed7f7f;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
    }

    /* Calendario */
    .cal-dia-regado {
        background: #1565c0;
        color: white;
        border-radius: 8px;
        padding: 4px 8px;
        font-weight: bold;
    }
    .cal-dia-hoy {
        background: #1A7F3A;
        color: white;
        border-radius: 8px;
        padding: 4px 8px;
        font-weight: bold;
    }
    .cal-dia-normal {
        background: #e8f5e9;
        color: #2e7d32;
        border-radius: 8px;
        padding: 4px 8px;
    }

    /* Ocultar menú de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Botones personalizados */
    .stButton > button {
        background-color: #386D23;
        color: white;
        border-radius: 12px;
        border: none;
        font-weight: bold;
        padding: 10px 24px;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #2d5a1b;
        color: white;
    }

    /* Badge error */
    .badge-error {
        background: #fff3f3;
        border: 1px solid #f44336;
        border-radius: 10px;
        padding: 8px 16px;
        color: #c62828;
        font-weight: bold;
        text-align: center;
    }
    .badge-ok {
        background: #f0fff4;
        border: 1px solid #4caf50;
        border-radius: 10px;
        padding: 8px 16px;
        color: #2e7d32;
        font-weight: bold;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
#  CONEXIÓN SUPABASE
# ════════════════════════════════════════════════════════
@st.cache_resource
def get_supabase():
    try:
        from supabase import create_client
        SUPABASE_URL = "https://hutmqgemeemqcwyuzrvx.supabase.co"
        SUPABASE_KEY = "sb_publishable_qfABKFGQ57jAPBAfje1OYA_Teqtc9ix"
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        pass  # Error silencioso, se maneja en cada función
        return None


def cargar_sensores_recientes(invernadero):
    """Carga la última lectura de sensores desde Supabase."""
    db = get_supabase()
    if not db:
        return None
    try:
        resp = db.table("lecturas_sensores")\
            .select("*")\
            .eq("invernadero", invernadero)\
            .order("created_at", desc=True)\
            .limit(1)\
            .execute()
        return resp.data[0] if resp.data else None
    except Exception as e:
        st.warning(f"Error cargando sensores: {e}")
        return None


def cargar_historial_sensores(invernadero, limite=50):
    """Carga historial de lecturas para gráficos."""
    db = get_supabase()
    if not db:
        return []
    try:
        resp = db.table("lecturas_sensores")\
            .select("*")\
            .eq("invernadero", invernadero)\
            .order("created_at", desc=True)\
            .limit(limite)\
            .execute()
        return list(reversed(resp.data))
    except Exception:
        return []


def cargar_riegos(invernadero):
    """Carga calendario de riegos."""
    db = get_supabase()
    if not db:
        return {}
    try:
        resp = db.table("riegos")\
            .select("fecha, motivo")\
            .eq("invernadero", invernadero)\
            .execute()
        return {
            date.fromisoformat(r["fecha"]): r["motivo"]
            for r in resp.data
        }
    except Exception:
        return {}


def registrar_riego(fecha, motivo, invernadero, usuario):
    """Registra un riego en Supabase."""
    db = get_supabase()
    if not db:
        return False
    try:
        db.table("riegos").upsert({
            "fecha": fecha.isoformat(),
            "motivo": motivo,
            "invernadero": invernadero,
            "registrado_por": usuario,
        }, on_conflict="fecha,invernadero").execute()
        return True
    except Exception as e:
        st.error(f"Error al registrar riego: {e}")
        return False


def eliminar_riego(fecha, invernadero):
    """Elimina un riego del calendario."""
    db = get_supabase()
    if not db:
        return False
    try:
        db.table("riegos")\
            .delete()\
            .eq("fecha", fecha.isoformat())\
            .eq("invernadero", invernadero)\
            .execute()
        return True
    except Exception:
        return False


def cargar_logs(invernadero, limite=30):
    """Carga registro de actividad."""
    db = get_supabase()
    if not db:
        return []
    try:
        resp = db.table("registro_actividad")\
            .select("fecha_hora, mensaje")\
            .eq("invernadero", invernadero)\
            .order("fecha_hora", desc=True)\
            .limit(limite)\
            .execute()
        return [f"[{r['fecha_hora'][11:19]}] {r['mensaje']}" for r in resp.data]
    except Exception:
        return []


def cargar_errores(invernadero):
    """Carga errores de dispositivos."""
    db = get_supabase()
    if not db:
        return []
    try:
        resp = db.table("errores_dispositivos")\
            .select("*")\
            .eq("invernadero", invernadero)\
            .eq("resuelto", False)\
            .order("created_at", desc=True)\
            .execute()
        return resp.data
    except Exception:
        return []


# ════════════════════════════════════════════════════════
#  PANTALLA LOGIN
# ════════════════════════════════════════════════════════
def pantalla_login():
    st.markdown("""
    <div class="header-principal">
        SISTEMA DE RIEGO<br>
        <div class="header-sub">Distrito Municipal Originario de Tica-Tica</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div style="text-align:center; font-size:5rem;">🌱💧</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-titulo">Iniciar Sesión</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-sub">Ingrese sus credenciales de acceso</div>', unsafe_allow_html=True)

        with st.form("login_form"):
            usuario = st.text_input("👤 Usuario", placeholder="Ingrese su usuario...")
            password = st.text_input("🔒 Contraseña", type="password", placeholder="••••••••")
            ingresar = st.form_submit_button("🌿  INGRESAR AL SISTEMA", use_container_width=True)

            if ingresar:
                u = usuario.strip().lower()
                p = password.strip()
                if not u or not p:
                    st.error("⚠️ Complete todos los campos")
                elif u in USUARIOS and USUARIOS[u]["password"] == p:
                    st.session_state.usuario = u
                    st.session_state.rol = USUARIOS[u]["rol"]
                    st.session_state.icono = USUARIOS[u]["icono"]
                    st.session_state.pagina = "principal"
                    st.session_state.invernadero = INVERNADEROS[0]
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas")

        # Acceso rápido
        st.markdown("---")
        st.markdown('<div style="text-align:center; color:#88aa88; font-size:0.85rem;">— Acceso rápido —</div>', unsafe_allow_html=True)
        cols = st.columns(4)
        for i, (usr, info) in enumerate(USUARIOS.items()):
            with cols[i]:
                if st.button(f"{info['icono']} {usr}", key=f"quick_{usr}"):
                    st.session_state.usuario = usr
                    st.session_state.rol = info["rol"]
                    st.session_state.icono = info["icono"]
                    st.session_state.pagina = "principal"
                    st.session_state.invernadero = INVERNADEROS[0]
                    st.rerun()

        st.markdown('<div style="text-align:center; color:#88aa88; font-size:0.8rem; margin-top:20px;">🌱 Invernadero Tica-Tica v1.0</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
#  PANTALLA PRINCIPAL (menú 4 tarjetas)
# ════════════════════════════════════════════════════════
def pantalla_principal():
    # Header
    st.markdown(f"""
    <div class="header-principal">
        SISTEMA DE RIEGO DEL DISTRITO MUNICIPAL ORIGINARIO DE TICA-TICA
        <div class="header-sub">{st.session_state.icono} {st.session_state.rol} — {st.session_state.usuario}</div>
    </div>
    """, unsafe_allow_html=True)

    # Selector de invernadero
    col_inv, col_cerrar = st.columns([3, 1])
    with col_inv:
        inv = st.selectbox(
            "🏠 Invernadero activo:",
            INVERNADEROS,
            index=INVERNADEROS.index(st.session_state.invernadero)
        )
        st.session_state.invernadero = inv
    with col_cerrar:
        st.write("")
        st.write("")
        if st.button("🚪 Cerrar sesión"):
            for key in ["usuario", "rol", "icono", "pagina", "invernadero"]:
                st.session_state.pop(key, None)
            st.rerun()

    st.markdown("---")

    # Cargar datos para el mini calendario
    riegos = cargar_riegos(st.session_state.invernadero)
    errores = cargar_errores(st.session_state.invernadero)
    n_errores = len(errores)

    # ── 4 TARJETAS ──────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="card-menu">
            <div class="card-titulo">🌡️ SENSORES</div>
            <div class="card-icono">💧🌡️</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("➤ Ingresar", key="btn_sensores"):
            st.session_state.pagina = "sensores"
            st.rerun()

    with c2:
        # Mini calendario
        hoy = date.today()
        yr, mo = hoy.year, hoy.month
        cal_data = calendar.monthcalendar(yr, mo)
        dias_html = ""
        for week in cal_data:
            for d in week:
                if d == 0:
                    dias_html += '<span style="display:inline-block;width:28px;height:24px;"></span>'
                else:
                    d_obj = date(yr, mo, d)
                    es_hoy = (d_obj == hoy)
                    es_regado = d_obj in riegos
                    if es_hoy or es_regado:
                        bg = "#1A7F3A" if es_hoy else "#1565c0"
                        dias_html += f'<span style="display:inline-block;width:28px;height:24px;background:{bg};color:white;border-radius:5px;text-align:center;font-size:11px;font-weight:bold;line-height:24px;">{d}</span>'
                    else:
                        dias_html += f'<span style="display:inline-block;width:28px;height:24px;background:#e8f5e9;color:#2e7d32;border-radius:5px;text-align:center;font-size:11px;line-height:24px;">{d}</span>'
            dias_html += "<br>"

        st.markdown(f"""
        <div class="card-menu" style="height:auto; padding:18px;">
            <div class="card-titulo">📅 CALENDARIO DE RIEGO</div>
            <div style="font-size:12px;font-weight:bold;color:#1565c0;margin:8px 0;">{MESES[mo-1]} {yr}</div>
            <div style="font-size:10px;line-height:1.8;">{dias_html}</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("➤ Ingresar", key="btn_calendario"):
            st.session_state.pagina = "calendario"
            st.rerun()

    with c3:
        badge_html = f'<div class="badge-error">⚠️ {n_errores} error{"es" if n_errores>1 else ""} activo{"s" if n_errores>1 else ""}</div>' \
                     if n_errores > 0 else \
                     '<div class="badge-ok">✅ Todos los dispositivos OK</div>'
        st.markdown(f"""
        <div class="card-menu">
            <div class="card-titulo">⚙️ PROBLEMAS TÉCNICOS</div>
            <div class="card-icono">⚠️🔧</div>
            {badge_html}
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("➤ Ingresar", key="btn_problemas"):
            st.session_state.pagina = "problemas"
            st.rerun()

    with c4:
        st.markdown("""
        <div class="card-menu">
            <div style="background:#386D23;color:white;border-radius:8px;padding:2px 10px;font-size:11px;font-weight:bold;">NUEVO</div>
            <div class="card-titulo">🗄️ BASE DE DATOS</div>
            <div class="card-icono">📊📋</div>
            <div style="font-size:11px;color:#1565c0;">Historial · Registros · Lecturas · Logs</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("➤ Ingresar", key="btn_basedatos"):
            st.session_state.pagina = "basedatos"
            st.rerun()


# ════════════════════════════════════════════════════════
#  FUNCIONES SUPABASE — CONTROL BOMBAS
# ════════════════════════════════════════════════════════
def guardar_estado_bomba(invernadero, bomba, encendida):
    """Guarda el estado de la bomba en Supabase."""
    db = get_supabase()
    if not db:
        return False
    try:
        campo = "bomba1_encendida" if bomba == 1 else "bomba2_encendida"
        # Buscar última lectura y actualizar estado
        db.table("lecturas_sensores").insert({
            "invernadero": invernadero,
            campo: encendida,
            "humedad_s1": 0, "humedad_s2": 0, "humedad_s3": 0,
            "humedad_a1": 0, "humedad_a2": 0,
            "temperatura": 0, "nivel_agua_1": 0, "nivel_agua_2": 0,
            "bomba1_encendida": encendida if bomba == 1 else False,
            "bomba2_encendida": encendida if bomba == 2 else False,
            "modo_automatico": False,
        }).execute()
        return True
    except Exception:
        return False


# ════════════════════════════════════════════════════════
#  PANTALLA SENSORES — SELECCIÓN INVERNADERO
# ════════════════════════════════════════════════════════
def pantalla_sensores():
    # Si no ha seleccionado invernadero para sensores, mostrar selección
    if "sensor_invernadero" not in st.session_state:
        _pantalla_seleccion_invernadero()
    else:
        _pantalla_panel_sensores()


def _pantalla_seleccion_invernadero():
    """Vista 1 — Selección de invernadero A o B."""
    st.markdown("""
    <div class="header-principal">
        🌡️ SENSORES Y CONTROL DE RIEGO
    </div>
    """, unsafe_allow_html=True)

    if st.button("← Volver al menú"):
        st.session_state.pagina = "principal"
        st.rerun()

    st.markdown("---")
    st.markdown('<div style="text-align:center;font-size:1.4rem;font-weight:bold;color:#2d3a1e;margin-bottom:8px;">Selecciona el invernadero</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;color:#6b7c5a;margin-bottom:28px;">¿En cuál invernadero deseas ver los sensores y controlar el riego?</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div style="background:#e8f5e8;border:3px solid #2E7D32;border-radius:20px;padding:30px;text-align:center;">
            <div style="font-size:3.5rem;">🌿</div>
            <div style="font-weight:bold;font-size:1.1rem;color:#2d3a1e;margin:12px 0;">Escuela Elizardo Pérez A</div>
            <div style="color:#6b7c5a;font-size:0.9rem;">Invernadero A — Verduras y Papa</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("➤ Ingresar al Invernadero A", key="inv_a", use_container_width=True):
            st.session_state.sensor_invernadero = INVERNADEROS[0]
            st.session_state.invernadero = INVERNADEROS[0]
            st.rerun()

    with c2:
        st.markdown("""
        <div style="background:#e3f2fd;border:3px solid #1565C0;border-radius:20px;padding:30px;text-align:center;">
            <div style="font-size:3.5rem;">🌱</div>
            <div style="font-weight:bold;font-size:1.1rem;color:#2d3a1e;margin:12px 0;">Colegio Elizardo Pérez B</div>
            <div style="color:#6b7c5a;font-size:0.9rem;">Invernadero B — Verduras y Papa</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("➤ Ingresar al Invernadero B", key="inv_b", use_container_width=True):
            st.session_state.sensor_invernadero = INVERNADEROS[1]
            st.session_state.invernadero = INVERNADEROS[1]
            st.rerun()


def _pantalla_panel_sensores():
    """Vista 2 — Panel completo de sensores y control de bombas."""
    inv = st.session_state.sensor_invernadero
    es_a = "A" in inv or "Escuela" in inv
    color_hdr = "#1A4D1D" if es_a else "#03053A"
    color_btn = "#2E7D32"
    color_borde = "#2E7D32" if es_a else "#1565C0"

    st.markdown(f"""
    <div style="background:{color_hdr};color:white;padding:18px 24px;border-radius:0 0 16px 16px;
        text-align:center;font-family:Arial;font-weight:bold;font-size:1.1rem;margin-bottom:16px;">
        🌡️ SENSORES Y CONTROL — {inv.upper()}
    </div>
    """, unsafe_allow_html=True)

    c_volver, c_inv = st.columns([1, 3])
    with c_volver:
        if st.button("← Volver"):
            del st.session_state["sensor_invernadero"]
            st.rerun()
    with c_inv:
        st.markdown(f'<div style="color:{color_borde};font-weight:bold;padding-top:8px;">🏠 {inv}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Cargar datos
    with st.spinner("Cargando lecturas..."):
        datos = cargar_sensores_recientes(inv)

    # ── COLUMNAS: SENSORES | CONTROL ─────────────────────
    col_sens, col_ctrl = st.columns([1, 1])

    # ════════════════════
    #  COLUMNA IZQUIERDA: SENSORES
    # ════════════════════
    with col_sens:
        st.markdown(f'<div style="background:{color_borde};color:white;border-radius:10px;padding:8px;text-align:center;font-weight:bold;margin-bottom:12px;">📡 LECTURAS EN TIEMPO REAL</div>', unsafe_allow_html=True)

        if not datos:
            st.warning("⚠️ Sin lecturas recientes")
            st.info("💡 Datos a las: 8am · 12pm · 6pm · 10pm")
            # Mostrar valores en 0
            datos = {
                "humedad_s1": 0, "humedad_s2": 0, "humedad_s3": 0,
                "humedad_a1": 0, "humedad_a2": 0, "temperatura": 0,
                "nivel_agua_1": 0, "nivel_agua_2": 0,
                "bomba1_encendida": False, "bomba2_encendida": False,
            }
        else:
            ts = datos.get("created_at", "")
            hora = ts[11:19] if len(ts) > 10 else "—"
            st.caption(f"🕐 Última lectura: {hora}")

        def tarjeta_sensor(icono, nombre, valor, unidad, color):
            color_val = "#d32f2f" if (unidad == "%" and valor < 30) else \
                        "#e65100" if (unidad == "%" and valor < 50) else \
                        "#e65100" if unidad == "°C" else "#2e7d32"
            st.markdown(f"""
            <div style="background:white;border:1.5px solid #a5d6a7;border-radius:12px;
                padding:10px 14px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                <span style="color:#2d3a1e;font-size:0.9rem;">{icono} {nombre}</span>
                <span style="font-weight:bold;font-size:1.1rem;color:{color_val};">{valor:.1f}{unidad}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("**💧 Humedad Suelo**")
        tarjeta_sensor("🌱", "Surco 1 — Verduras", datos.get("humedad_s1", 0), "%", color_btn)
        tarjeta_sensor("🌱", "Surco 2 — Verduras", datos.get("humedad_s2", 0), "%", color_btn)
        tarjeta_sensor("🥔", "Surco 3 — Papa",     datos.get("humedad_s3", 0), "%", color_btn)

        st.markdown("**💨 Humedad Aire**")
        tarjeta_sensor("💨", "Sensor Aire 1", datos.get("humedad_a1", 0), "%", color_btn)
        tarjeta_sensor("💨", "Sensor Aire 2", datos.get("humedad_a2", 0), "%", color_btn)

        st.markdown("**🌡️ Temperatura & Agua**")
        tarjeta_sensor("🌡️", "Temperatura",   datos.get("temperatura",  0), "°C", color_btn)
        tarjeta_sensor("🚰", "Nivel Agua 1",  datos.get("nivel_agua_1", 0), "%",  color_btn)
        tarjeta_sensor("🚰", "Nivel Agua 2",  datos.get("nivel_agua_2", 0), "%",  color_btn)

    # ════════════════════
    #  COLUMNA DERECHA: CONTROL DE BOMBAS
    # ════════════════════
    with col_ctrl:
        st.markdown(f'<div style="background:{color_borde};color:white;border-radius:10px;padding:8px;text-align:center;font-weight:bold;margin-bottom:12px;">⚙️ CONTROL DE RIEGO</div>', unsafe_allow_html=True)

        b1_on = datos.get("bomba1_encendida", False)
        b2_on = datos.get("bomba2_encendida", False)
        niv1  = datos.get("nivel_agua_1", 0)
        niv2  = datos.get("nivel_agua_2", 0)

        # ── BOMBA 1 ──────────────────────────────────────
        st.markdown("**⚙️ Bomba 1 — Verduras**")
        if b1_on:
            st.markdown(f"""
            <div class="bomba-on">
                <div style="font-size:1.5rem;font-weight:bold;">🟢 ENCENDIDA</div>
                <div style="color:#6b7c5a;font-size:0.85rem;">Nivel agua: {niv1:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(min(niv1 / 100, 1.0))
            if st.button("🔴 Detener Riego Verduras", key="stop_b1", use_container_width=True):
                guardar_estado_bomba(inv, 1, False)
                db = get_supabase()
                if db:
                    from datetime import date as d_
                    db.table("riegos").upsert({
                        "fecha": d_.today().isoformat(),
                        "motivo": "Manual — Verduras",
                        "invernadero": inv,
                        "registrado_por": st.session_state.get("usuario", "")
                    }, on_conflict="fecha,invernadero").execute()
                st.success("✅ Bomba 1 detenida")
                st.rerun()
        else:
            st.markdown(f"""
            <div class="bomba-off">
                <div style="font-size:1.5rem;font-weight:bold;">🔴 APAGADA</div>
                <div style="color:#6b7c5a;font-size:0.85rem;">Nivel agua: {niv1:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(min(niv1 / 100, 1.0))
            limite1 = st.number_input("⏱️ Límite (minutos)", min_value=1, max_value=120,
                                       value=15, key="lim_b1")
            if niv1 < 20 and niv1 > 0:
                st.error("⚠️ Nivel de agua muy bajo. No se puede iniciar.")
            else:
                if st.button("🟢 Iniciar Riego Verduras", key="start_b1", use_container_width=True):
                    guardar_estado_bomba(inv, 1, True)
                    st.success(f"✅ Bomba 1 iniciada — Límite: {limite1} min")
                    st.rerun()

        st.markdown("---")

        # ── BOMBA 2 ──────────────────────────────────────
        st.markdown("**⚙️ Bomba 2 — Papa**")
        if b2_on:
            st.markdown(f"""
            <div class="bomba-on">
                <div style="font-size:1.5rem;font-weight:bold;">🟢 ENCENDIDA</div>
                <div style="color:#6b7c5a;font-size:0.85rem;">Nivel agua: {niv2:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(min(niv2 / 100, 1.0))
            if st.button("🔴 Detener Riego Papa", key="stop_b2", use_container_width=True):
                guardar_estado_bomba(inv, 2, False)
                st.success("✅ Bomba 2 detenida")
                st.rerun()
        else:
            st.markdown(f"""
            <div class="bomba-off">
                <div style="font-size:1.5rem;font-weight:bold;">🔴 APAGADA</div>
                <div style="color:#6b7c5a;font-size:0.85rem;">Nivel agua: {niv2:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(min(niv2 / 100, 1.0))
            limite2 = st.number_input("⏱️ Límite (minutos)", min_value=1, max_value=120,
                                       value=15, key="lim_b2")
            if niv2 < 20 and niv2 > 0:
                st.error("⚠️ Nivel de agua muy bajo. No se puede iniciar.")
            else:
                if st.button("🟢 Iniciar Riego Papa", key="start_b2", use_container_width=True):
                    guardar_estado_bomba(inv, 2, True)
                    st.success(f"✅ Bomba 2 iniciada — Límite: {limite2} min")
                    st.rerun()

    # ── GRÁFICOS HISTÓRICOS ──────────────────────────────
    st.markdown("---")
    st.subheader("📈 Historial de Lecturas")
    historial = cargar_historial_sensores(inv)
    if historial:
        import pandas as pd
        df = pd.DataFrame(historial)
        df["hora"] = df["created_at"].str[11:16]
        cols_suelo = [c for c in ["humedad_s1","humedad_s2","humedad_s3"] if c in df.columns]
        if cols_suelo:
            st.line_chart(df.set_index("hora")[cols_suelo], height=200)
            st.caption("💧 Humedad suelo — Sensores 1, 2 y 3")
        if "temperatura" in df.columns:
            st.line_chart(df.set_index("hora")[["temperatura"]], height=160)
            st.caption("🌡️ Temperatura ambiente")
    else:
        st.info("Sin historial disponible aún.")


# ════════════════════════════════════════════════════════
#  PANTALLA CALENDARIO
# ════════════════════════════════════════════════════════
def pantalla_calendario():
    st.markdown(f"""
    <div class="header-principal" style="font-size:1.2rem;">
        📅 CALENDARIO DE RIEGO — {st.session_state.invernadero}
    </div>
    """, unsafe_allow_html=True)

    if st.button("← Volver al menú"):
        st.session_state.pagina = "principal"
        st.rerun()

    st.markdown("---")

    riegos = cargar_riegos(st.session_state.invernadero)
    hoy = date.today()

    # Navegación de mes
    if "cal_yr" not in st.session_state:
        st.session_state.cal_yr = hoy.year
    if "cal_mo" not in st.session_state:
        st.session_state.cal_mo = hoy.month

    c1, c2, c3 = st.columns([1, 3, 1])
    with c1:
        if st.button("◀ Anterior"):
            if st.session_state.cal_mo == 1:
                st.session_state.cal_mo = 12
                st.session_state.cal_yr -= 1
            else:
                st.session_state.cal_mo -= 1
            st.rerun()
    with c2:
        st.markdown(f'<div style="text-align:center;font-size:1.3rem;font-weight:bold;color:#1565c0;">{MESES[st.session_state.cal_mo-1]} {st.session_state.cal_yr}</div>', unsafe_allow_html=True)
    with c3:
        if st.button("Siguiente ▶"):
            if st.session_state.cal_mo == 12:
                st.session_state.cal_mo = 1
                st.session_state.cal_yr += 1
            else:
                st.session_state.cal_mo += 1
            st.rerun()

    # Calendario — tabla HTML pura (evita el bug removeChild de Streamlit)
    yr, mo = st.session_state.cal_yr, st.session_state.cal_mo
    cal_data = calendar.monthcalendar(yr, mo)

    tabla = """
    <table style="width:100%;border-collapse:separate;border-spacing:4px;">
    <tr>
    """
    for dia in ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"]:
        tabla += f'<th style="text-align:center;background:#c8e6c9;color:#2e7d32;border-radius:6px;padding:6px;font-size:0.9rem;">{dia}</th>'
    tabla += "</tr>"

    for week in cal_data:
        tabla += "<tr>"
        for day in week:
            if day == 0:
                tabla += '<td style="padding:4px;"></td>'
            else:
                d_obj = date(yr, mo, day)
                es_hoy    = (d_obj == hoy)
                es_regado = d_obj in riegos
                if es_hoy and es_regado:
                    bg, fg = "#1A7F3A", "white"
                elif es_regado:
                    bg, fg = "#1565c0", "white"
                elif es_hoy:
                    bg, fg = "#1A7F3A", "white"
                else:
                    bg, fg = "#e8f5e9", "#2e7d32"
                motivo = riegos.get(d_obj, "")
                tooltip = f'title="{motivo}"' if motivo else ""
                tabla += f'<td {tooltip} style="text-align:center;background:{bg};color:{fg};border-radius:8px;padding:10px 4px;font-weight:bold;font-size:0.95rem;">{day}</td>'
        tabla += "</tr>"
    tabla += "</table>"
    st.markdown(tabla, unsafe_allow_html=True)

    # Leyenda
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<span style="background:#1565c0;color:white;border-radius:6px;padding:4px 12px;">■</span> Día regado', unsafe_allow_html=True)
    with c2:
        st.markdown('<span style="background:#1A7F3A;color:white;border-radius:6px;padding:4px 12px;">■</span> Hoy', unsafe_allow_html=True)
    with c3:
        st.markdown('<span style="background:#e8f5e9;color:#2e7d32;border-radius:6px;padding:4px 12px;">■</span> Normal', unsafe_allow_html=True)

    # Registrar riego
    st.markdown("---")
    st.subheader("➕ Registrar Riego")
    with st.form("form_riego"):
        fecha_sel = st.date_input("Fecha de riego", value=hoy)
        motivo_sel = st.selectbox("Motivo", ["Manual", "Automático", "Programado", "Emergencia"])
        registrar = st.form_submit_button("💧 Registrar Riego")
        if registrar:
            ok = registrar_riego(fecha_sel, motivo_sel,
                                  st.session_state.invernadero,
                                  st.session_state.usuario)
            if ok:
                st.success(f"✅ Riego registrado: {fecha_sel} — {motivo_sel}")
                st.rerun()

    # Lista de riegos del mes
    riegos_mes = {f: m for f, m in riegos.items() if f.year == yr and f.month == mo}
    if riegos_mes:
        st.subheader(f"📋 Riegos en {MESES[mo-1]} {yr}")
        for fecha, motivo in sorted(riegos_mes.items()):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"💧 **{fecha.strftime('%d/%m/%Y')}** — {motivo}")
            with c2:
                if st.button("🗑️ Eliminar", key=f"del_{fecha}"):
                    eliminar_riego(fecha, st.session_state.invernadero)
                    st.rerun()


# ════════════════════════════════════════════════════════
#  PANTALLA PROBLEMAS TÉCNICOS
# ════════════════════════════════════════════════════════
def pantalla_problemas():
    st.markdown(f"""
    <div class="header-principal" style="font-size:1.2rem;">
        ⚙️ PROBLEMAS TÉCNICOS — {st.session_state.invernadero}
    </div>
    """, unsafe_allow_html=True)

    if st.button("← Volver al menú"):
        st.session_state.pagina = "principal"
        st.rerun()

    st.markdown("---")

    errores = cargar_errores(st.session_state.invernadero)

    if not errores:
        st.markdown('<div class="badge-ok" style="font-size:1.1rem;padding:16px;">✅ Todos los dispositivos funcionan correctamente</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="badge-error" style="font-size:1.1rem;padding:16px;">⚠️ {len(errores)} error{"es" if len(errores)>1 else ""} activo{"s" if len(errores)>1 else ""}</div>', unsafe_allow_html=True)
        st.markdown("---")
        for err in errores:
            icono = err.get("icono", "⚠️")
            nombre = err.get("nombre", "Dispositivo")
            tipo = err.get("tipo_error", "Error")
            mensaje = err.get("mensaje", "")
            ts = err.get("created_at", "")[:16].replace("T", " ")
            st.markdown(f"""
            <div style="background:#fff3f3;border:1px solid #f44336;border-radius:12px;padding:16px;margin-bottom:10px;">
                <div style="font-weight:bold;font-size:1rem;">{icono} {nombre}</div>
                <div style="color:#c62828;margin:4px 0;">🔴 {tipo}: {mensaje}</div>
                <div style="color:#999;font-size:0.8rem;">🕐 {ts}</div>
            </div>
            """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
#  PANTALLA BASE DE DATOS
# ════════════════════════════════════════════════════════
def pantalla_basedatos():
    st.markdown(f"""
    <div class="header-principal" style="font-size:1.2rem;">
        🗄️ BASE DE DATOS — {st.session_state.invernadero}
    </div>
    """, unsafe_allow_html=True)

    if st.button("← Volver al menú"):
        st.session_state.pagina = "principal"
        st.rerun()

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["📊 Lecturas de Sensores", "💧 Historial de Riegos", "📋 Registro de Actividad"])

    with tab1:
        st.subheader("Últimas lecturas de sensores")
        historial = cargar_historial_sensores(st.session_state.invernadero, limite=100)
        if historial:
            import pandas as pd
            df = pd.DataFrame(historial)
            columnas = ["created_at", "humedad_s1", "humedad_s2", "humedad_s3",
                        "humedad_a1", "humedad_a2", "temperatura",
                        "nivel_agua_1", "nivel_agua_2",
                        "bomba1_encendida", "bomba2_encendida"]
            columnas_existentes = [c for c in columnas if c in df.columns]
            st.dataframe(df[columnas_existentes], use_container_width=True)
        else:
            st.info("Sin lecturas disponibles.")

    with tab2:
        st.subheader("Historial completo de riegos")
        riegos = cargar_riegos(st.session_state.invernadero)
        if riegos:
            import pandas as pd
            df_riegos = pd.DataFrame([
                {"Fecha": f.strftime("%d/%m/%Y"), "Motivo": m}
                for f, m in sorted(riegos.items(), reverse=True)
            ])
            st.dataframe(df_riegos, use_container_width=True)
            st.metric("Total de riegos registrados", len(riegos))
        else:
            st.info("Sin riegos registrados.")

    with tab3:
        st.subheader("Registro de actividad reciente")
        logs = cargar_logs(st.session_state.invernadero)
        if logs:
            for log in logs:
                st.text(log)
        else:
            st.info("Sin actividad registrada.")


# ════════════════════════════════════════════════════════
#  ENRUTADOR PRINCIPAL
# ════════════════════════════════════════════════════════
def main():
    if "pagina" not in st.session_state:
        st.session_state.pagina = "login"

    pagina = st.session_state.pagina

    if pagina == "login":
        pantalla_login()
    elif pagina == "principal":
        pantalla_principal()
    elif pagina == "sensores":
        pantalla_sensores()
    elif pagina == "calendario":
        pantalla_calendario()
    elif pagina == "problemas":
        pantalla_problemas()
    elif pagina == "basedatos":
        pantalla_basedatos()


if __name__ == "__main__":
    main()