# ═══════════════════════════════════════════════════════════════
#   supabase_db.py — Conexion con Supabase para el Sistema de Riego
#   Tica-Tica 
# ═══════════════════════════════════════════════════════════════

import streamlit as st
from supabase import create_client, Client
from datetime import date, datetime


def _obtener_credenciales():
    """
    Lee las credenciales desde secrets.toml de Streamlit.
    Si no estan configuradas usa los valores directos como respaldo.
    """
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return url, key
    except Exception:
        # Respaldo directo (igual que la laptop)
        url = "https://hutmqgemeemqcwyuzrvx.supabase.co"
        key = "sb_publishable_qfABKFGQ57jAPBAfje1OYA_Teqtc9ix"
        return url, key


@st.cache_resource
def get_supabase() -> Client:
    """
    Devuelve el cliente de Supabase.
    Usa cache para no reconectar en cada recarga.
    """
    url, key = _obtener_credenciales()
    try:
        client = create_client(url, key)
        return client
    except Exception as e:
        print(f"[Supabase] Error al conectar: {e}")
        return None


# ════════════════════════════════════════════════════════════════
#  SENSORES
# ════════════════════════════════════════════════════════════════
def cargar_sensores_recientes(invernadero: str) -> dict:
    """Carga la ultima lectura de sensores — igual que la laptop."""
    db = get_supabase()
    if not db:
        return {}
    try:
        resp = db.table("lecturas_sensores")\
            .select("*")\
            .eq("invernadero", invernadero)\
            .order("created_at", desc=True)\
            .limit(1)\
            .execute()
        return resp.data[0] if resp.data else {}
    except Exception as e:
        print(f"[Supabase] Error al cargar sensores: {e}")
        return {}


def cargar_historial_sensores(invernadero: str, limite: int = 50) -> list:
    """Carga historial de lecturas para graficos."""
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
    except Exception as e:
        print(f"[Supabase] Error al cargar historial: {e}")
        return []


def guardar_estado_bomba(invernadero: str, bomba: int, encendida: bool) -> bool:
    """Guarda el estado de la bomba — igual que la laptop."""
    db = get_supabase()
    if not db:
        return False
    try:
        db.table("lecturas_sensores").insert({
            "invernadero":      invernadero,
            "humedad_s1":       0,
            "humedad_s2":       0,
            "humedad_s3":       0,
            "humedad_a1":       0,
            "humedad_a2":       0,
            "temperatura":      0,
            "nivel_agua_1":     0,
            "nivel_agua_2":     0,
            "bomba1_encendida": encendida if bomba == 1 else False,
            "bomba2_encendida": encendida if bomba == 2 else False,
            "modo_automatico":  False,
        }).execute()
        return True
    except Exception as e:
        print(f"[Supabase] Error al guardar bomba: {e}")
        return False


# ════════════════════════════════════════════════════════════════
#  RIEGOS
# ════════════════════════════════════════════════════════════════
def cargar_riegos(invernadero: str) -> dict:
    """Carga el calendario de riegos — igual que la laptop."""
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
    except Exception as e:
        print(f"[Supabase] Error al cargar riegos: {e}")
        return {}


def registrar_riego(fecha: date, motivo: str,
                    invernadero: str, usuario: str) -> bool:
    """Registra un riego — igual que la laptop."""
    db = get_supabase()
    if not db:
        return False
    try:
        db.table("riegos").upsert({
            "fecha":          fecha.isoformat(),
            "motivo":         motivo,
            "invernadero":    invernadero,
            "registrado_por": usuario,
        }, on_conflict="fecha,invernadero").execute()
        return True
    except Exception as e:
        print(f"[Supabase] Error al registrar riego: {e}")
        return False


def eliminar_riego(fecha: date, invernadero: str) -> bool:
    """Elimina un riego del calendario — igual que la laptop."""
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
    except Exception as e:
        print(f"[Supabase] Error al eliminar riego: {e}")
        return False


# ════════════════════════════════════════════════════════════════
#  LOGS DE ACTIVIDAD
# ════════════════════════════════════════════════════════════════
def agregar_log(invernadero: str, mensaje: str) -> bool:
    """Guarda un log de actividad — igual que agregar_log de la laptop."""
    db = get_supabase()
    if not db:
        return False
    try:
        db.table("registro_actividad").insert({
            "mensaje":     mensaje,
            "invernadero": invernadero,
            "usuario":     st.session_state.get("usuario", ""),
        }).execute()
        return True
    except Exception as e:
        print(f"[Supabase] Error al guardar log: {e}")
        return False


def cargar_logs(invernadero: str, limite: int = 30) -> list:
    """Carga el registro de actividad — igual que la laptop."""
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
        return [
            f"[{r['fecha_hora'][11:19]}] {r['mensaje']}"
            for r in reversed(resp.data)
        ]
    except Exception as e:
        print(f"[Supabase] Error al cargar logs: {e}")
        return []


# ════════════════════════════════════════════════════════════════
#  ERRORES DE DISPOSITIVOS
# ════════════════════════════════════════════════════════════════
def cargar_errores(invernadero: str) -> list:
    """Carga errores activos de dispositivos — igual que la laptop."""
    db = get_supabase()
    if not db:
        return []
    try:
        resp = db.table("errores_dispositivos")\
            .select("*")\
            .eq("invernadero", invernadero)\
            .order("created_at", desc=True)\
            .execute()
        return resp.data
    except Exception as e:
        print(f"[Supabase] Error al cargar errores: {e}")
        return []


def resolver_error(error_id: int) -> bool:
    """Marca un error como resuelto — igual que marcar_error_resuelto de la laptop."""
    db = get_supabase()
    if not db:
        return False
    try:
        db.table("errores_dispositivos")\
            .update({
                "resuelto":    True,
                "resuelto_en": datetime.now().isoformat(),
            })\
            .eq("id", error_id)\
            .execute()
        return True
    except Exception as e:
        print(f"[Supabase] Error al resolver error: {e}")
        return False