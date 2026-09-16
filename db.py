"""
FindOut - Conexión al Data Warehouse (GRMDW) de Greenmovil.

Las credenciales se leen de st.secrets["dwh"] (ver .streamlit/secrets.toml.example).
Nunca se deja la contraseña escrita en el código fuente.
"""

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text


def construir_engine(host=None, port=None, database=None, user=None, password=None):
    """
    Construye el engine de conexión. Si no se pasan parámetros, los toma
    de st.secrets["dwh"].
    """
    cfg = st.secrets.get("dwh", {}) if hasattr(st, "secrets") else {}

    host = host or cfg.get("host", "10.0.22.78")
    port = port or cfg.get("port", 5432)
    database = database or cfg.get("database", "GRMDW")
    user = user or cfg.get("user", "")
    password = password or cfg.get("password", "")

    if not user or not password:
        raise ValueError(
            "Faltan credenciales del DWH. Configúralas en .streamlit/secrets.toml "
            "(copia secrets.toml.example) o usa la conexión manual de la barra lateral."
        )

    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    return create_engine(url, pool_pre_ping=True)


def probar_conexion(engine=None) -> bool:
    eng = engine or construir_engine()
    with eng.connect() as conn:
        conn.execute(text("SELECT 1"))
    return True


def _es_procede(valor) -> bool:
    if isinstance(valor, bool):
        return valor
    if valor is None:
        return False
    texto = str(valor).strip().upper()
    return texto in {"SI", "SÍ", "S", "TRUE", "1", "T"}


def obtener_novedades(fecha_inicio, fecha_fin, solo_procede: bool = True, engine=None) -> pd.DataFrame:
    """
    Consulta op."FactNovedadesOperador" en el rango de fechas indicado y
    devuelve las columnas relevantes para el cruce de bonificación.

    El filtro de "Procede" se aplica en pandas (no en SQL) porque el tipo de
    dato de esa columna puede variar (booleano, texto, entero) y así evitamos
    errores de tipo en la consulta.
    """
    eng = engine or construir_engine()

    query = text(
        """
        SELECT
            "Fecha",
            "TipoNovedad",
            "PmGrupo",
            "DetalleNovedad",
            "Operador",
            "PuntosPmConciliados",
            "Procede"
        FROM op."FactNovedadesOperador"
        WHERE "Fecha" BETWEEN :fecha_inicio AND :fecha_fin
        """
    )

    with eng.connect() as conn:
        df = pd.read_sql(query, conn, params={"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin})

    if solo_procede and "Procede" in df.columns:
        df = df[df["Procede"].apply(_es_procede)].copy()

    df["PuntosPmConciliados"] = pd.to_numeric(df["PuntosPmConciliados"], errors="coerce").fillna(0)

    return df
