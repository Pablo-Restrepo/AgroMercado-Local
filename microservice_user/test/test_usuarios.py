import pytest
from unittest.mock import MagicMock

from application.services import UsuarioService


class DummyUsuario:
    def __init__(self, u_email=None):
        self.u_email = u_email
        self.p_id = None


class DummyPersona:
    def __init__(self, p_cedula=None):
        self.p_cedula = p_cedula


@pytest.fixture
def mock_usuario_repo():
    repo = MagicMock()
    # defaults
    repo.exists_email.return_value = False
    repo.save.return_value = None
    repo.find_by_email_and_password.return_value = None
    repo.find_by_id.return_value = None
    repo.delete_usuario.return_value = None
    repo.find_by_email.return_value = None
    return repo


@pytest.fixture
def mock_persona_repo():
    repo = MagicMock()
    repo.exists_cedula.return_value = False
    repo.save_persona.return_value = 123
    repo.find_by_id.return_value = None
    repo.delete_persona.return_value = None
    return repo


@pytest.fixture
def jwt_mock():
    jwt = MagicMock()
    jwt.create_access_token.return_value = "access-token"
    jwt.create_refresh_token.return_value = "refresh-token"
    jwt.verify_token.return_value = {"type": "refresh", "sub": "1", "email": "a@b.com", "username": "u"}
    return jwt


def test_registrar_usuario_raises_if_email_exists(mock_usuario_repo, mock_persona_repo):
    mock_usuario_repo.exists_email.return_value = True
    svc = UsuarioService(mock_usuario_repo, mock_persona_repo)
    persona = DummyPersona(p_cedula="111")
    usuario = DummyUsuario(u_email="a@b.com")
    with pytest.raises(ValueError):
        svc.registrar_usuario_y_persona(persona, usuario)
    mock_usuario_repo.exists_email.assert_called_once_with("a@b.com")


def test_registrar_usuario_raises_if_cedula_exists(mock_usuario_repo, mock_persona_repo):
    mock_persona_repo.exists_cedula.return_value = True
    svc = UsuarioService(mock_usuario_repo, mock_persona_repo)
    persona = DummyPersona(p_cedula="111")
    usuario = DummyUsuario(u_email="a@b.com")
    with pytest.raises(ValueError):
        svc.registrar_usuario_y_persona(persona, usuario)
    mock_persona_repo.exists_cedula.assert_called_once_with("111")


def test_registrar_usuario_success_sets_p_id_and_calls_save(mock_usuario_repo, mock_persona_repo):
    mock_persona_repo.save_persona.return_value = 555
    svc = UsuarioService(mock_usuario_repo, mock_persona_repo)
    persona = DummyPersona(p_cedula="222")
    usuario = DummyUsuario(u_email="c@d.com")
    svc.registrar_usuario_y_persona(persona, usuario)
    assert usuario.p_id == 555
    mock_persona_repo.save_persona.assert_called_once_with(persona)
    mock_usuario_repo.save.assert_called_once_with(usuario)


def test_validar_credenciales_success_returns_tokens(mock_usuario_repo, mock_persona_repo, jwt_mock):
    # repo returns tuple (u_id, u_nombre_usuario, u_email, u_rol)
    mock_usuario_repo.find_by_email_and_password.return_value = (7, "userX", "x@y.com", "productor-admin")
    svc = UsuarioService(mock_usuario_repo, mock_persona_repo)
    svc.jwt_manager = jwt_mock
    result = svc.validar_credenciales("x@y.com", "pwd")
    assert result is not None
    assert result["u_id"] == 7
    assert result["access_token"] == "access-token"
    assert result["refresh_token"] == "refresh-token"
    jwt_mock.create_access_token.assert_called_once()
    jwt_mock.create_refresh_token.assert_called_once()


def test_validar_credenciales_invalid_returns_none(mock_usuario_repo, mock_persona_repo):
    mock_usuario_repo.find_by_email_and_password.return_value = None
    svc = UsuarioService(mock_usuario_repo, mock_persona_repo)
    result = svc.validar_credenciales("no@one", "bad")
    assert result is None


def test_refresh_access_token_success(jwt_mock, mock_usuario_repo, mock_persona_repo):
    svc = UsuarioService(mock_usuario_repo, mock_persona_repo)
    svc.jwt_manager = jwt_mock
    jwt_mock.verify_token.return_value = {"type": "refresh", "sub": "1", "email": "a@b.com", "username": "u"}
    jwt_mock.create_access_token.return_value = "new-access"
    token = svc.refresh_access_token("some-refresh")
    assert token == "new-access"
    jwt_mock.verify_token.assert_called_once_with("some-refresh")
    jwt_mock.create_access_token.assert_called_once()


def test_refresh_access_token_invalid_raises(mock_usuario_repo, mock_persona_repo, jwt_mock):
    svc = UsuarioService(mock_usuario_repo, mock_persona_repo)
    svc.jwt_manager = jwt_mock
    jwt_mock.verify_token.return_value = {"type": "access"}
    with pytest.raises(ValueError):
        svc.refresh_access_token("bad-token")


def test_eliminar_usuario_y_persona_not_found_raises(mock_usuario_repo, mock_persona_repo):
    mock_usuario_repo.find_by_id.return_value = None
    svc = UsuarioService(mock_usuario_repo, mock_persona_repo)
    with pytest.raises(ValueError):
        svc.eliminar_usuario_y_persona(999)
    mock_usuario_repo.find_by_id.assert_called_once_with(999)


def test_eliminar_usuario_y_persona_deletes_related(mock_usuario_repo, mock_persona_repo):
    # simulate found usuario with attribute p_id
    usuario_obj = MagicMock()
    usuario_obj.p_id = 77
    mock_usuario_repo.find_by_id.return_value = usuario_obj
    svc = UsuarioService(mock_usuario_repo, mock_persona_repo)
    svc.eliminar_usuario_y_persona(7)
    mock_usuario_repo.delete_usuario.assert_called_once_with(7)
    mock_persona_repo.delete_persona.assert_called_once_with(77)