import sqlite3
import hashlib
import os
from microservice_user.infrastructure.db_config import DATABASE_URL


def get_db_connection():
    """Obtiene la conexión a la base de datos SQLite"""
    db_path = DATABASE_URL.replace("sqlite:///", "")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Para acceder a las columnas por nombre
    return conn


def init_db():
    """Inicializa la base de datos y crea las tablas"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Crear tabla de personas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS persona (
            p_id INTEGER PRIMARY KEY AUTOINCREMENT,
            p_cedula TEXT NOT NULL UNIQUE,
            p_nombre TEXT NOT NULL,
            p_apellido TEXT NOT NULL,
            p_telefono TEXT,
            p_direccion TEXT,
            p_fecha_nacimiento TEXT
        )
    ''')

    # Crear tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
            u_id INTEGER PRIMARY KEY AUTOINCREMENT,
            u_nombre_usuario TEXT NOT NULL,
            u_contrasenia TEXT NOT NULL,
            u_email TEXT NOT NULL,
            u_fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            u_es_activo INTEGER DEFAULT 1,
            p_id INTEGER,
            FOREIGN KEY (p_id) REFERENCES persona(p_id)
        )
    ''')

    conn.commit()
    conn.close()


class UsuarioRepository:
    def save(self, usuario):
        conn = get_db_connection()
        cursor = conn.cursor()
        # Hash de la contraseña antes de guardar
        hashed_password = self._hash_password(usuario.u_contrasenia)
        query = "INSERT INTO usuario (u_nombre_usuario, u_contrasenia, u_email, p_id) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (usuario.u_nombre_usuario,
                       hashed_password, usuario.u_email, usuario.p_id))
        conn.commit()
        conn.close()

    def exists_email(self, email):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM usuario WHERE u_email = ?"
        cursor.execute(query, (email,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    def find_by_email_and_password(self, email, password):
        conn = get_db_connection()
        cursor = conn.cursor()
        hashed_password = self._hash_password(password)
        query = """
        SELECT u.u_id, u.u_nombre_usuario, u.u_email, u.u_es_activo 
        FROM usuario u 
        WHERE u.u_email = ? AND u.u_contrasenia = ? AND u.u_es_activo = 1
        """
        cursor.execute(query, (email, hashed_password))
        result = cursor.fetchone()
        conn.close()

        if result:
            return tuple(result)
        return None

    def _hash_password(self, password):
        """Hash simple de la contraseña usando SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()


class PersonaRepository:
    def save_persona(self, persona):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO persona (p_cedula, p_apellido, p_nombre, p_fecha_nacimiento, p_direccion, p_telefono) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(query, (
            persona.p_cedula,
            persona.p_apellido,
            persona.p_nombre,
            persona.p_fecha_nacimiento,
            persona.p_direccion,
            persona.p_telefono
        ))
        conn.commit()
        p_id = cursor.lastrowid
        conn.close()
        return p_id
