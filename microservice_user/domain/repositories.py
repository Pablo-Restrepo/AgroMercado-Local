from abc import ABC, abstractmethod
from domain.persona import Persona
from domain.usuario import Usuario


class IPersonaRepository(ABC):
    """
    Interfaz para el repositorio de Persona.
    Define los contratos que debe cumplir cualquier implementación
    del repositorio de personas.
    """
    @abstractmethod
    def delete_persona(self, persona_id: int) -> None:
        """
        Elimina la persona por ID.

        Args:
            persona_id (int): ID de la persona a eliminar

        Raises:
            ValueError: Si la persona no existe o no puede eliminarse
        """

    @abstractmethod
    def save_persona(self, persona: Persona) -> int:
        """
        Guarda una persona en el repositorio.

        Args:
            persona (Persona): La entidad persona del dominio a guardar

        Returns:
            int: El ID de la persona guardada

        Raises:
            ValueError: Si la persona no cumple las validaciones
            Exception: Si ocurre un error al guardar
        """

    @abstractmethod
    def find_by_id(self, persona_id: int) -> Persona | None:
        """
        Busca una persona por su ID.

        Args:
            persona_id (int): El ID de la persona a buscar

        Returns:
            Persona | None: La persona encontrada o None si no existe
        """

    @abstractmethod
    def find_by_cedula(self, cedula: str) -> Persona | None:
        """
        Busca una persona por su número de cédula.

        Args:
            cedula (str): El número de cédula a buscar

        Returns:
            Persona | None: La persona encontrada o None si no existe
        """


class IUsuarioRepository(ABC):
    """
    Interfaz para el repositorio de Usuario.
    Define los contratos que debe cumplir cualquier implementación
    del repositorio de usuarios.
    """
    @abstractmethod
    def delete_usuario(self, usuario_id: int) -> None:
        """
        Elimina el usuario por ID.

        Args:
            usuario_id (int): ID del usuario a eliminar

        Raises:
            ValueError: Si el usuario no existe o no puede eliminarse
        """

    @abstractmethod
    def save(self, usuario: Usuario) -> int:
        """
        Guarda un usuario en el repositorio.

        Args:
            usuario (Usuario): La entidad usuario del dominio a guardar

        Returns:
            int: El ID del usuario guardado

        Raises:
            ValueError: Si el usuario no cumple las validaciones
            Exception: Si ocurre un error al guardar
        """

    @abstractmethod
    def exists_email(self, email: str) -> bool:
        """
        Verifica si existe un usuario con el email proporcionado.

        Args:
            email (str): El email a verificar

        Returns:
            bool: True si existe un usuario con ese email, False en caso contrario
        """

    @abstractmethod
    def find_by_id(self, usuario_id: int) -> Usuario | None:
        """
        Busca un usuario por su ID.

        Args:
            usuario_id (int): El ID del usuario a buscar

        Returns:
            Usuario | None: El usuario encontrado o None si no existe
        """

    @abstractmethod
    def find_by_email(self, email: str) -> Usuario | None:
        """
        Busca un usuario por su email.

        Args:
            email (str): El email del usuario a buscar

        Returns:
            Usuario | None: El usuario encontrado o None si no existe
        """
