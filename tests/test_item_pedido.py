import pytest

# Importaremos as classes (src) que ainda iremos criar
from src import Cardapio, ItemPedido

# --- Fixtures ---


@pytest.fixture
def cardapio_fixture():
    """Fixture para um item do Cardapio."""
    return Cardapio("Prato1", 10.00)


# --- Testes para ItemPedido ---


class TestItemPedido:
    def test_atributos_basicos(self, cardapio_fixture):
        item = ItemPedido(cardapio_fixture, 2, "sem ingrediente1")

        assert item.opcao_menu == cardapio_fixture
        assert item.quantidade == 2
        assert item.observacao == "sem ingrediente1"

        item.quantidade = 5
        item.observacao = "sem ingrediente2"

        assert item.quantidade == 5
        assert item.observacao == "sem ingrediente2"

    def test_valor_total(self, cardapio_fixture):
        item = ItemPedido(cardapio_fixture, 3, "")
        assert item.valor_total == 30.00

    def test_valor_total_zero(self, cardapio_fixture):
        item = ItemPedido(cardapio_fixture, 0, "")
        assert item.valor_total == 0.0