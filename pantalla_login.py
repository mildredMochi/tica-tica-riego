# ═══════════════════════════════════════════════════════
#   pantalla_login.py — Sistema de Riego Tica-Tica
# ═══════════════════════════════════════════════════════

import streamlit as st

# ── USUARIOS ─────────────────────────────────────────────
USUARIOS = {
    "presidente":      {"password": "123", "rol": "Presidente"},
    "vicepresidente":  {"password": "123", "rol": "Vicepresidente"},
    "profesores":      {"password": "123", "rol": "Profesores"},
}

INVERNADEROS = [
    "Escuela Elizardo Pérez A",
    "Colegio Elizardo Pérez B"
]

# ── CSS ESTILOS LOGIN ────────────────────────────────────
CSS_LOGIN = """
<style>
    .stApp {
        background: linear-gradient(135deg, #1a7a2e 0%, #0d4a6b 50%, #03053A 100%) !important;
        min-height: 100vh;
    }
    [data-testid="stAppViewContainer"] { background: transparent !important; }
    [data-testid="stMain"]             { background: transparent !important; }

    .header-login {
        background: #03053A;
        color: white;
        padding: 18px 30px;
        text-align: center;
        font-family: Arial Black, Arial, sans-serif;
        font-size: 1.5rem;
        font-weight: 900;
        letter-spacing: 2px;
        border-bottom: 3px solid #1a7a2e;
        margin-bottom: 32px;
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

    .login-card {
        background: rgba(255, 255, 255, 0.97);
        border-radius: 24px;
        border: 2px solid #a5d6a7;
        padding: 40px 44px;
        max-width: 460px;
        margin: 0 auto 24px auto;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
    }
    .login-gota {
        text-align: center;
        font-size: 5rem;
        margin-bottom: 8px;
    }
    .login-titulo {
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        color: #1a3a1a;
        margin-bottom: 4px;
        font-family: Arial, sans-serif;
    }
    .login-sub {
        text-align: center;
        color: #88aa88;
        font-size: 0.9rem;
        margin-bottom: 20px;
    }

    .stButton > button {
        background-color: #2d6e1a !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: bold !important;
        font-size: 1rem !important;
        padding: 12px 24px !important;
        width: 100% !important;
        letter-spacing: 1px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
    }
    .stButton > button:hover {
        background-color: #1a5010 !important;
        color: white !important;
    }

    .version-txt {
        text-align: center;
        color: #c8e6c9;
        font-size: 0.8rem;
        margin-top: 16px;
    }

    #MainMenu                 { visibility: hidden; }
    footer                    { visibility: hidden; }
    header                    { visibility: hidden; }
    [data-testid="stToolbar"] { visibility: hidden; }
</style>
"""


def mostrar_login():
    """Muestra la pantalla de inicio de sesion. Requiere usuario y contrasena siempre."""

    st.markdown(CSS_LOGIN, unsafe_allow_html=True)

    # ── HEADER ──────────────────────────────────────────
    st.markdown("""
    <div class="header-login">
        SISTEMA DE RIEGO
        <div class="header-sub">Distrito Municipal Originario de Tica-Tica</div>
    </div>
    """, unsafe_allow_html=True)

    # ── TARJETA LOGIN ────────────────────────────────────
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:

        st.markdown("""
        <div class="login-card">
            <div class="login-gota">💧</div>
            <div class="login-titulo">Iniciar Sesion</div>
            <div class="login-sub">Ingrese sus credenciales de acceso</div>
        </div>
        """, unsafe_allow_html=True)

        # Campos de usuario y contrasena — unica forma de entrar
        usuario  = st.text_input("Usuario",    placeholder="Ingrese su usuario...")
        password = st.text_input("Contrasena", type="password", placeholder="••••••••")

        if st.button("INGRESAR AL SISTEMA", use_container_width=True):
            u = usuario.strip().lower()
            p = password.strip()
            if not u or not p:
                st.error("Complete todos los campos")
            elif u in USUARIOS and USUARIOS[u]["password"] == p:
                st.session_state.usuario     = u
                st.session_state.rol         = USUARIOS[u]["rol"]
                st.session_state.pagina      = "principal"
                st.session_state.invernadero = INVERNADEROS[0]
                st.rerun()
            else:
                st.error("Usuario o contrasena incorrectos")

        st.markdown('<div class="version-txt">Invernadero Tica-Tica v1.0</div>', unsafe_allow_html=True)