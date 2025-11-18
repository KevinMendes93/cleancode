import pytest

# Importaremos a classe (src) que ainda iremos criar
from src import Cliente

# --- Fixtures ---


@pytest.fixture
def cliente_fixture():
    """Fixture para um Cliente."""
    return Cliente("Fulano", "000-9090-0000", "fulano@email.com")


# --- Testes para Cliente ---


class TestCliente:
    def test_atributos_basicos(self, cliente_fixture):
        assert cliente_fixture.nome == "Fulano"
        assert cliente_fixture.telefone == "000-9090-0000"
        assert cliente_fixture.email == "fulano@email.com"

    def test_igualdade(self, cliente_fixture):
        temp_equal = Cliente("Fulano", "000-9090-0000", "fulano@email.com")
        temp_diff_nome = Cliente("Beltrano", "000-9090-0000", "fulano@email.com")
        temp_diff_phone = Cliente("Fulano", "111-1111-1111", "fulano@email.com")

        assert temp_equal == cliente_fixture
        assert temp_diff_nome != cliente_fixture
        assert temp_diff_phone != cliente_fixture

    def test_igualdade_outro_tipo(self, cliente_fixture):
        assert (
            cliente_fixture == ("Fulano", "000-9090-0000", "fulano@email.com")
        ) is False
