"""
FindOut - Autenticación y gestión de usuarios de la aplicación.

Usa una base de datos SQLite local (data/findout_users.db), independiente
del DWH de Greenmovil, para almacenar los usuarios que pueden ingresar a
FindOut. Las contraseñas se guardan siempre con hash bcrypt, nunca en texto
plano.
"""

import sqlite3
from pathlib import Path
from datetime import datetime

import bcrypt

DB_PATH = Path(__file__).parent / "data" / "findout_users.db"


def _get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _get_conn()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            nombre_completo TEXT,
            rol TEXT NOT NULL DEFAULT 'usuario',
            activo INTEGER NOT NULL DEFAULT 1,
            creado_en TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def hay_usuarios() -> bool:
    conn = _get_conn()
    n = conn.execute("SELECT COUNT(*) AS c FROM usuarios").fetchone()["c"]
    conn.close()
    return n > 0


def crear_usuario(username: str, password: str, nombre_completo: str, rol: str = "usuario"):
    username = (username or "").strip().lower()
    if not username or not password:
        return False, "Usuario y contraseña son obligatorios."
    if len(password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres."

    conn = _get_conn()
    existe = conn.execute("SELECT 1 FROM usuarios WHERE username = ?", (username,)).fetchone()
    if existe:
        conn.close()
        return False, "Ese nombre de usuario ya existe."

    pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    conn.execute(
        """INSERT INTO usuarios (username, password_hash, nombre_completo, rol, activo, creado_en)
           VALUES (?, ?, ?, ?, 1, ?)""",
        (username, pw_hash, (nombre_completo or "").strip(), rol, datetime.now().isoformat(timespec="seconds")),
    )
    conn.commit()
    conn.close()
    return True, "Usuario creado correctamente."


def verificar_usuario(username: str, password: str):
    username = (username or "").strip().lower()
    conn = _get_conn()
    row = conn.execute("SELECT * FROM usuarios WHERE username = ?", (username,)).fetchone()
    conn.close()

    if not row or not row["activo"]:
        return None
    if bcrypt.checkpw(password.encode("utf-8"), row["password_hash"].encode("utf-8")):
        return dict(row)
    return None


def listar_usuarios():
    conn = _get_conn()
    rows = conn.execute(
        "SELECT id, username, nombre_completo, rol, activo, creado_en FROM usuarios ORDER BY creado_en"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def cambiar_estado_usuario(user_id: int, activo: bool):
    conn = _get_conn()
    conn.execute("UPDATE usuarios SET activo = ? WHERE id = ?", (1 if activo else 0, user_id))
    conn.commit()
    conn.close()


def eliminar_usuario(user_id: int):
    conn = _get_conn()
    conn.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()


def cambiar_password(user_id: int, nueva_password: str):
    if len(nueva_password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres."
    pw_hash = bcrypt.hashpw(nueva_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    conn = _get_conn()
    conn.execute("UPDATE usuarios SET password_hash = ? WHERE id = ?", (pw_hash, user_id))
    conn.commit()
    conn.close()
    return True, "Contraseña actualizada."
