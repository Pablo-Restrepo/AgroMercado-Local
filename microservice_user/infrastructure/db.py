import mysql.connector

class UsuarioRepository:
    def __init__(self, db_config):
        self.db_config = db_config

    def save(self, usuario):
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()
        query = "INSERT INTO usuario (u_nombre_usuario, u_contrasenia, u_email, p_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (usuario.u_nombre_usuario, usuario.u_contrasenia, usuario.u_email, usuario.p_id))
        conn.commit()
        cursor.close()
        conn.close()

    def exists_email(self, email):
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM usuario WHERE u_email = %s"
        cursor.execute(query, (email,))
        (count,) = cursor.fetchone()
        cursor.close()
        conn.close()
        return count > 0
    
    
class PersonaRepository:
    def __init__(self, db_config):
        self.db_config = db_config
        
    def save_persona(self, persona):
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()
        query = "INSERT INTO persona (p_cedula, p_apellido, p_nombre, p_fecha_nacimiento, p_direccion, p_telefono) VALUES (%s, %s, %s, %s, %s, %s)"
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
        cursor.close()
        conn.close()
        return p_id