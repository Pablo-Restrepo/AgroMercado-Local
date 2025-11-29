import pytest
from application.services import UsuarioService
from application.dtos import UsuarioDTO


class TestUsuarioService:
    @pytest.fixture
    def usuario_service(self, mock_usuario_repo):
        return UsuarioService(mock_usuario_repo)

    @pytest.mark.asyncio
    async def test_crear_usuario_exitoso(
        self, usuario_service, mock_usuario_repo, usuario_dto, usuario_activo
    ):
        mock_usuario_repo.save_usuario.return_value = usuario_activo
        
        resultado = await usuario_service.crear_usuario(usuario_dto)
        
        assert resultado.id == usuario_activo.id
        mock_usuario_repo.save_usuario.assert_called_once()

