import pytest

# Importaremos a classe (src) que ainda iremos criar
from src import Cardapio

# --- Fixtures ---


@pytest.fixture
def cardapio_fixture():
    """Fixture para um item do Cardapio."""
    return Cardapio("Prato1", 10.00)


# --- Testes para Cardapio ---


class TestCardapio:
    def test_atributos_basicos(self, cardapio_fixture):
        assert cardapio_fixture.descricao == "Prato1"
        assert cardapio_fixture.valor == 10.00

        cardapio_fixture.descricao = "Lanche1"
        cardapio_fixture.valor = 5.55

        assert cardapio_fixture.descricao == "Lanche1"
        assert cardapio_fixture.valor == 5.55

    def test_igualdade(self, cardapio_fixture):
        temp_diff_valor = Cardapio("Prato1", 9.00)
        temp_equal = Cardapio("Prato1", 10.00)
        temp_diff_desc = Cardapio("Lanche1", 10.00)

        # (Use o __eq__ do Python)
        assert temp_diff_valor != cardapio_fixture
        assert temp_equal == cardapio_fixture
        assert temp_diff_desc != cardapio_fixture

    def test_igualdade_outro_tipo(self, cardapio_fixture):
        assert (cardapio_fixture == ("Prato1", 10.00)) is False
