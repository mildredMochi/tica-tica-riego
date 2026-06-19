# ═══════════════════════════════════════════════════════
#   app.py — Sistema de Riego Tica-Tica (Streamlit)
#   Enrutador principal — solo llama a los demas archivos
# ═══════════════════════════════════════════════════════

import streamlit as st

from pantalla_login import mostrar_login
from pantalla_principal import mostrar_principal
from pantalla_sensores import mostrar_sensores
from pantalla_calendario import mostrar_calendario
from pantalla_problemas import mostrar_problemas
from pantalla_basedatos import mostrar_basedatos

from supabase_db import (
    get_supabase,
    cargar_sensores_recientes,
    cargar_historial_sensores,
    guardar_estado_bomba,
    cargar_riegos,
    registrar_riego,
    eliminar_riego,
    agregar_log,
    cargar_logs,
    cargar_errores,
    resolver_error,
)

# ── CONFIGURACION DE PAGINA ──────────────────────────────
st.set_page_config(
    page_title="Sistema de Riego — Tica-Tica",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ════════════════════════════════════════════════════════
#  ENRUTADOR PRINCIPAL
# ════════════════════════════════════════════════════════
def main():
    if "pagina" not in st.session_state:
        st.session_state.pagina = "login"

    pagina = st.session_state.pagina

    if pagina == "login":
        mostrar_login()

    elif pagina == "principal":
        mostrar_principal(
            cargar_riegos_fn  = cargar_riegos,
            cargar_errores_fn = cargar_errores,
        )

    elif pagina == "sensores":
        mostrar_sensores(
            cargar_sensores_fn   = cargar_sensores_recientes,
            cargar_historial_fn  = cargar_historial_sensores,
            guardar_bomba_fn     = guardar_estado_bomba,
            registrar_riego_fn   = registrar_riego,
            agregar_log_fn       = agregar_log,
        )

    elif pagina == "calendario":
        mostrar_calendario(
            cargar_riegos_fn   = cargar_riegos,
            registrar_riego_fn = registrar_riego,
            eliminar_riego_fn  = eliminar_riego,
            agregar_log_fn     = agregar_log,
        )

    elif pagina == "problemas":
        mostrar_problemas(
            cargar_errores_fn  = cargar_errores,
            resolver_error_fn  = resolver_error,
        )

    elif pagina == "basedatos":
        mostrar_basedatos(
            get_supabase_fn = get_supabase,
        )


if __name__ == "__main__":
    main()