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
#  NOTA: Hay un solo set de sensores compartido por las dos zonas
#  de riego (A y B). Ya NO se filtra por invernadero — se toma
#  siempre la ultima lectura que exista, sin importar el nombre
#  que traiga el campo "invernadero".
# ════════════════════════════════════════════════════════════════
def cargar_sensores_recientes(invernadero: str = None) -> dict:
    """
    Carga la ultima lectura de sensores (compartida entre zonas).
    El parametro invernadero se deja opcional por compatibilidad,
    pero ya NO se usa para filtrar.
    """
    db = get_supabase()
    if not db:
        return {}
    try:
        resp = db.table("lecturas_sensores")\
            .select("*")\
            .order("created_at", desc=True)\
            .limit(1)\
            .execute()
        return resp.data[0] if resp.data else {}
    except Exception as e:
        print(f"[Supabase] Error al cargar sensores: {e}")
        return {}


def cargar_historial_sensores(invernadero: str = None, limite: int = 50) -> list:
    """
    Carga historial de lecturas para graficos (compartido entre zonas).
    El parametro invernadero se deja opcional por compatibilidad,
    pero ya NO se usa para filtrar.
    """
    db = get_supabase()
    if not db:
        return []
    try:
        resp = db.table("lecturas_sensores")\
            .select("*")\
            .order("created_at", desc=True)\
            .limit(limite)\
            .execute()
        return list(reversed(resp.data))
    except Exception as e:
        print(f"[Supabase] Error al cargar historial: {e}")
        return []


def guardar_estado_bomba(invernadero: str, bomba: int, encendida: bool) -> bool:
    """
    Actualiza el estado de la bomba en la ULTIMA fila existente,
    en vez de insertar una fila nueva llena de ceros.
    Asi no se pierden los datos de sensores mas recientes.
    """
    db = get_supabase()
    if not db:
        return False
    try:
        # 1. Buscar la ultima fila existente
        resp = db.table("lecturas_sensores")\
            .select("id")\
            .order("created_at", desc=True)\
            .limit(1)\
            .execute()

        campo = "bomba1_encendida" if bomba == 1 else "bomba2_encendida"

        if resp.data:
            # 2a. Ya existe una fila — actualizar solo el campo de la bomba
            fila_id = resp.data[0]["id"]
            db.table("lecturas_sensores")\
                .update({campo: encendida})\
                .eq("id", fila_id)\
                .execute()
        else:
            # 2b. No existe ninguna fila todavia — crear una minima
            db.table("lecturas_sensores").insert({
                "invernadero":      invernadero,
                "bomba1_encendida": encendida if bomba == 1 else False,
                "bomba2_encendida": encendida if bomba == 2 else False,
            }).execute()

        return True
    except Exception as e:
        print(f"[Supabase] Error al guardar bomba: {e}")
        return False


# ════════════════════════════════════════════════════════════════
#  BOMBAS — ORDENES REALES AL ESP32 (igual que la laptop)
#  NOTA: esta es la forma CORRECTA de encender/apagar la bomba.
#  Nunca se debe escribir bomba1_encendida/bomba2_encendida a mano
#  desde la app (eso es lo que hacia guardar_estado_bomba arriba y
#  no mueve el rele fisico) — el ESP32 es el unico que ejecuta
#  ordenes de 'ordenes_bomba' y luego reporta el estado real.
# ════════════════════════════════════════════════════════════════
def crear_orden_bomba(bomba: int, accion: str, duracion_minutos: int = 0,
                       invernadero: str = "Escuela Elizardo Pérez A") -> bool:
    """Inserta una orden en 'ordenes_bomba' para que el ESP32 la ejecute."""
    db = get_supabase()
    if not db:
        return False
    try:
        db.table("ordenes_bomba").insert({
            "invernadero":      invernadero,
            "bomba":            bomba,
            "accion":           accion,
            "duracion_minutos": duracion_minutos,
            "ejecutada":        False,
        }).execute()
        return True
    except Exception as e:
        print(f"[Supabase] Error al crear orden de bomba: {e}")
        return False


def obtener_estado_bombas(invernadero: str = "Escuela Elizardo Pérez A") -> dict:
    """Lee el estado REAL confirmado por el ESP32 (ultima fila de lecturas_sensores)."""
    db = get_supabase()
    if not db:
        return {}
    try:
        resp = db.table("lecturas_sensores")\
            .select("bomba1_encendida, bomba2_encendida")\
            .eq("invernadero", invernadero)\
            .order("created_at", desc=True)\
            .limit(1)\
            .execute()
        if resp.data:
            d = resp.data[0]
            return {
                "bomba1": bool(d.get("bomba1_encendida", False)),
                "bomba2": bool(d.get("bomba2_encendida", False)),
            }
        return {}
    except Exception as e:
        print(f"[Supabase] Error al leer estado de bombas: {e}")
        return {}


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