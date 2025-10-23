from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from microservice_user.domain.repositories import IPersonaRepository, IUsuarioRepository
from microservice_user.domain.persona import Persona
from microservice_user.domain.usuario import Usuario
from microservice_user.infrastructure.modelsSQL import PersonaModel, UsuarioModel
from microservice_user.infrastructure.engine import engine


class PersonaRepository(IPersonaRepository):
    """
    Implementación del repositorio de Persona usando SQLAlchemy ORM.
    Maneja la persistencia y recuperación de entidades Persona.
    """

    def __init__(self, db_config=None):
        # db_config se mantiene para compatibilidad, pero usamos SQLAlchemy
        pass

    def save_persona(self, persona: Persona) -> int:
        """
        Guarda una persona utilizando SQLAlchemy ORM.

        Convierte la entidad de dominio a modelo de infraestructura,
        la persiste en la base de datos y retorna el ID generado.
        """
        with Session(engine) as session:
            # Verificar si la cédula ya existe
            existing_persona = session.exec(
                select(PersonaModel).where(
                    PersonaModel.p_cedula == persona.p_cedula)
            ).first()

            if existing_persona:
                raise ValueError(
                    f"Ya existe una persona con la cédula {persona.p_cedula}")

            try:
                persona_model = PersonaModel(
                    p_cedula=persona.p_cedula,
                    p_apellido=persona.p_apellido,
                    p_nombre=persona.p_nombre,
                    p_fecha_nacimiento=persona.p_fecha_nacimiento,
                    p_direccion=persona.p_direccion,
                    p_telefono=persona.p_telefono
                )
                session.add(persona_model)
                session.commit()
                session.refresh(persona_model)
                return persona_model.p_id
            except IntegrityError as e:
                session.rollback()
                if "Duplicate entry" in str(e) and "P_cedula" in str(e):
                    raise ValueError(
                        f"Ya existe una persona con la cédula {persona.p_cedula}")
                raise ValueError("Error al guardar la persona")

    def find_by_id(self, persona_id: int) -> Persona | None:
        """
        Busca una persona por ID y la convierte a entidad de dominio.
        """
        with Session(engine) as session:
            stmt = select(PersonaModel).where(PersonaModel.p_id == persona_id)
            persona_model = session.exec(stmt).first()

            if not persona_model:
                return None

            return self._model_to_domain(persona_model)

    def find_by_cedula(self, cedula: str) -> Persona | None:
        """
        Busca una persona por cédula y la convierte a entidad de dominio.
        """
        with Session(engine) as session:
            stmt = select(PersonaModel).where(PersonaModel.p_cedula == cedula)
            persona_model = session.exec(stmt).first()

            if not persona_model:
                return None

            return self._model_to_domain(persona_model)

    def exists_cedula(self, cedula: str) -> bool:
        """
        Verifica si existe una persona con la cédula especificada.
        """
        with Session(engine) as session:
            stmt = select(PersonaModel).where(PersonaModel.p_cedula == cedula)
            persona_model = session.exec(stmt).first()
            return persona_model is not None

    def _model_to_domain(self, persona_model: PersonaModel) -> Persona:
        """
        Convierte un modelo de infraestructura a entidad de dominio.
        """
        return Persona(
            p_id=persona_model.p_id,
            p_cedula=persona_model.p_cedula,
            p_apellido=persona_model.p_apellido,
            p_nombre=persona_model.p_nombre,
            p_fecha_nacimiento=persona_model.p_fecha_nacimiento,
            p_direccion=persona_model.p_direccion,
            p_telefono=persona_model.p_telefono
        )

    def delete_persona(self, persona_id: int) -> None:
        """
        Elimina una persona por su ID.
        Lanza ValueError si no existe.
        """
        with Session(engine) as session:
            stmt = select(PersonaModel).where(PersonaModel.p_id == persona_id)
            persona_model = session.exec(stmt).first()
            if not persona_model:
                raise ValueError(f"La persona con id {persona_id} no existe")
            session.delete(persona_model)
            session.commit()


class UsuarioRepository(IUsuarioRepository):
    """
    Implementación del repositorio de Usuario usando SQLAlchemy ORM.
    Maneja la persistencia y recuperación de entidades Usuario.
    """

    def __init__(self, db_config=None):
        # db_config se mantiene para compatibilidad, pero usamos SQLAlchemy
        pass

    def save(self, usuario: Usuario) -> int:
        """
        Guarda un usuario utilizando SQLAlchemy ORM.

        Convierte la entidad de dominio a modelo de infraestructura,
        la persiste en la base de datos y retorna el ID generado.
        """
        with Session(engine) as session:
            try:
                usuario_model = UsuarioModel(
                    u_nombre_usuario=usuario.u_nombre_usuario,
                    u_contrasenia=usuario.u_contrasenia,
                    u_email=usuario.u_email,
                    p_id=usuario.p_id
                )
                session.add(usuario_model)
                session.commit()
                session.refresh(usuario_model)
                usuario.u_id = usuario_model.u_id  # Actualizar el ID en la entidad
                return usuario_model.u_id
            except IntegrityError as e:
                session.rollback()
                if "Duplicate entry" in str(e) and "u_email" in str(e):
                    raise ValueError(
                        f"Ya existe un usuario con el email {usuario.u_email}")
                raise ValueError("Error al guardar el usuario")

    def exists_email(self, email: str) -> bool:
        """
        Verifica si existe un usuario con el email especificado.
        """
        with Session(engine) as session:
            stmt = select(UsuarioModel).where(UsuarioModel.u_email == email)
            usuario_model = session.exec(stmt).first()
            return usuario_model is not None

    def find_by_id(self, usuario_id: int) -> Usuario | None:
        """
        Busca un usuario por ID y lo convierte a entidad de dominio.
        """
        with Session(engine) as session:
            stmt = select(UsuarioModel).where(UsuarioModel.u_id == usuario_id)
            usuario_model = session.exec(stmt).first()

            if not usuario_model:
                return None

            return self._model_to_domain(usuario_model)

    def find_by_email(self, email: str) -> Usuario | None:
        """
        Busca un usuario por email y lo convierte a entidad de dominio.
        """
        with Session(engine) as session:
            stmt = select(UsuarioModel).where(UsuarioModel.u_email == email)
            usuario_model = session.exec(stmt).first()

            if not usuario_model:
                return None

            return self._model_to_domain(usuario_model)

    def find_by_email_and_password(self, email: str, password: str):
        with Session(engine) as session:
            stmt = select(
                UsuarioModel.u_id,
                UsuarioModel.u_nombre_usuario,
                UsuarioModel.u_email
            ).where(
                UsuarioModel.u_email == email,
                UsuarioModel.u_contrasenia == password,
            )
            row = session.exec(stmt).first()
            return tuple(row) if row else None

    def delete_usuario(self, usuario_id: int) -> None:
        """
        Elimina un usuario por su ID.
        Lanza ValueError si no existe.
        """
        with Session(engine) as session:
            stmt = select(UsuarioModel).where(UsuarioModel.u_id == usuario_id)
            usuario_model = session.exec(stmt).first()
            if not usuario_model:
                raise ValueError(f"El usuario con id {usuario_id} no existe")
            session.delete(usuario_model)
            session.commit()

    def _model_to_domain(self, usuario_model: UsuarioModel) -> Usuario:
        """
        Convierte un modelo de infraestructura a entidad de dominio.
        """
        return Usuario(
            u_id=usuario_model.u_id,
            u_nombre_usuario=usuario_model.u_nombre_usuario,
            u_contrasenia=usuario_model.u_contrasenia,
            u_email=usuario_model.u_email,
            p_id=usuario_model.p_id
        )
