# ═══════════════════════════════════════════════════════
#   utils_imagenes.py — Convierte imagenes a base64
#   Esto es necesario porque Streamlit Cloud no permite
#   cargar imagenes locales directamente con <img src="ruta">
#   dentro de HTML. Hay que convertirlas a base64 primero.
# ═══════════════════════════════════════════════════════

import streamlit as st
import base64
import os


@st.cache_data
def imagen_a_base64(ruta: str) -> str:
    """
    Convierte una imagen local a una cadena base64 que se puede
    usar directamente en <img src="data:image/...;base64,...">

    Si la imagen no existe, devuelve cadena vacia para que el
    contenedor de la imagen se oculte sin romper la pagina.
    """
    if not os.path.exists(ruta):
        return ""
    try:
        with open(ruta, "rb") as f:
            data = f.read()
        ext = ruta.split(".")[-1].lower()
        mime = "jpeg" if ext in ("jpg", "jpeg") else ext
        b64 = base64.b64encode(data).decode()
        return f"data:image/{mime};base64,{b64}"
    except Exception:
        return ""


def tag_imagen(ruta: str, css_class: str = "") -> str:
    """
    Devuelve un tag <img> completo y listo para insertar en HTML,
    usando base64. Si la imagen no existe, devuelve un div vacio
    en su lugar (no rompe el diseño).
    """
    src = imagen_a_base64(ruta)
    if not src:
        return f'<div class="{css_class}" style="display:flex;align-items:center;justify-content:center;color:#999;font-size:0.8rem;">Sin imagen</div>'
    return f'<img src="{src}" class="{css_class}">'