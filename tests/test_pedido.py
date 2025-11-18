import datetime

import pytest

# Importaremos as classes (src) que ainda iremos criar
from src import Cardapio, Cliente, ItemPedido, Pedido
from src.item_pedido import QuantidadeInvalidaError
from src.pedido import (
    FormaPagamento,
    FormaPagamentoInvalidaError,
    MotivoCancelamentoObrigatorioError,
    PagamentoNaoPermitidoError,
    PedidoJaEntregueError,
    StatusPedido,
)

# --- Fixtures ---


@pytest.fixture
def cliente_fixture():
    """Fixture para um Cliente."""
    return Cliente("Fulano", "000-9090-0000", "fulano@email.com")


@pytest.fixture
def cardapio_itens_variados_fixture():
    """Fixture para múltiplos itens de cardápio."""
    prato_principal = Cardapio("Prato1", 10.00)
    acompanhamento = Cardapio("Prato2", 8.50)
    bebida = Cardapio("Bebida1", 3.49)
    return prato_principal, acompanhamento, bebida


@pytest.fixture
def pedido_fixture(cliente_fixture):
    """Fixture para um Pedido básico."""
    data_pedido = datetime.datetime(2019, 3, 22, 14, 24, 6)
    return Pedido(cliente_fixture, data_pedido, "Rua X", situacao_aberto=True)


# --- Testes para Pedido ---


class TestPedido:
    def test_attributes_and_item_management(
        self, pedido_fixture, cardapio_itens_variados_fixture, cliente_fixture
    ):
        prato, acompanhamento, bebida = cardapio_itens_variados_fixture
        data_pedido = datetime.datetime(2019, 3, 22, 14, 24, 6)

        assert pedido_fixture.data_hora == data_pedido
        assert pedido_fixture.cliente == cliente_fixture
        assert pedido_fixture.endereco == "Rua X"
        assert pedido_fixture.situacao_aberto is True
        assert pedido_fixture.valor_total == 0
        assert len(pedido_fixture.itens) == 0

        item1 = ItemPedido(prato, 2, "sem ingrediente1")
        pedido_fixture.add_item(item1)

        assert len(pedido_fixture.itens) == 1
        assert pedido_fixture.itens[0] == item1
        assert pedido_fixture.valor_total == 20.00

        item2 = ItemPedido(acompanhamento, 1, "preparação2")
        pedido_fixture.add_item(item2)

        assert len(pedido_fixture.itens) == 2
        assert pedido_fixture.itens[1] == item2
        assert pedido_fixture.valor_total == 28.50

        item3 = ItemPedido(bebida, 3, "saborX")
        pedido_fixture.add_item(item3)

        assert len(pedido_fixture.itens) == 3
        assert pedido_fixture.itens[2] == item3
        assert pedido_fixture.valor_total == pytest.approx(38.97)

    def test_modify_item_in_pedido(
        self, pedido_fixture, cardapio_itens_variados_fixture
    ):
        prato, acompanhamento, bebida = cardapio_itens_variados_fixture
        pedido_fixture.add_item(ItemPedido(prato, 2, ""))
        pedido_fixture.add_item(ItemPedido(acompanhamento, 1, ""))
        pedido_fixture.add_item(ItemPedido(bebida, 3, ""))

        pedido_fixture.itens[2].quantidade = 1

        assert pedido_fixture.valor_total == pytest.approx(31.99)

    def test_modify_pedido_state(self, pedido_fixture):
        pedido_fixture.endereco = "Rua 7"
        pedido_fixture.fechar_pedido()

        assert pedido_fixture.endereco == "Rua 7"
        assert pedido_fixture.situacao_aberto is False

    def test_valor_total_sem_itens(self, cliente_fixture):
        pedido = Pedido(cliente_fixture, datetime.datetime(2023, 1, 1, 0, 0), "Rua A")
        assert pedido.valor_total == 0

    def test_fechar_pedido_sem_itens(self, cliente_fixture):
        pedido = Pedido(cliente_fixture, datetime.datetime(2023, 1, 1, 0, 0), "Rua A")
        pedido.fechar_pedido()
        assert pedido.situacao_aberto is False

    def test_preserva_ordem_itens(
        self, cliente_fixture, cardapio_itens_variados_fixture
    ):
        prato, acompanhamento, bebida = cardapio_itens_variados_fixture
        pedido = Pedido(cliente_fixture, datetime.datetime(2023, 1, 1, 0, 0), "Rua A")
        item1 = ItemPedido(prato, 1, "")
        item2 = ItemPedido(acompanhamento, 1, "")
        item3 = ItemPedido(bebida, 1, "")
        pedido.add_item(item1)
        pedido.add_item(item2)
        pedido.add_item(item3)
        assert pedido.itens == [item1, item2, item3]

    def test_status_inicial_e_fluxo_avanco(self, pedido_fixture):
        assert pedido_fixture.status == StatusPedido.RECEBIDO
        assert pedido_fixture.situacao_aberto is True

        pedido_fixture.avancar_status()
        assert pedido_fixture.status == StatusPedido.EM_PREPARO

        pedido_fixture.avancar_status()
        assert pedido_fixture.status == StatusPedido.PRONTO

        pedido_fixture.avancar_status()
        assert pedido_fixture.status == StatusPedido.A_CAMINHO

        pedido_fixture.avancar_status()
        assert pedido_fixture.status == StatusPedido.ENTREGUE
        assert pedido_fixture.situacao_aberto is False

        pedido_fixture.avancar_status()
        assert pedido_fixture.status == StatusPedido.ENTREGUE

    def test_cancelar_pedido_define_motivo_e_fecha(self, pedido_fixture):
        pedido_fixture.cancelar("Cliente desistiu")
        assert pedido_fixture.status == StatusPedido.CANCELADO
        assert pedido_fixture.cancelamento_motivo == "Cliente desistiu"
        assert pedido_fixture.situacao_aberto is False

        pedido_fixture.avancar_status()
        assert pedido_fixture.status == StatusPedido.CANCELADO

    def test_definir_forma_pagamento_dinheiro(self, pedido_fixture):
        assert pedido_fixture.definir_forma_pagamento("dinheiro") == "dinheiro"
        assert pedido_fixture.forma_pagamento == "dinheiro"

    def test_definir_forma_pagamento_pix(self, pedido_fixture):
        assert pedido_fixture.definir_forma_pagamento("PIX") == "pix"
        assert pedido_fixture.forma_pagamento == "pix"

    def test_definir_forma_pagamento_cartao(self, pedido_fixture):
        assert pedido_fixture.definir_forma_pagamento("cartao") == "cartao"
        assert pedido_fixture.forma_pagamento == "cartao"

    def test_definir_forma_pagamento_invalida_gera_erro(self, pedido_fixture):
        with pytest.raises(FormaPagamentoInvalidaError):
            pedido_fixture.definir_forma_pagamento("boleto")

    def test_item_quantidade_nao_pode_ser_negativa(
        self, cardapio_itens_variados_fixture
    ):
        prato, *_ = cardapio_itens_variados_fixture
        with pytest.raises(QuantidadeInvalidaError):
            ItemPedido(prato, -1, "")

    def test_item_quantidade_deve_ser_inteira(self, cardapio_itens_variados_fixture):
        prato, *_ = cardapio_itens_variados_fixture
        item = ItemPedido(prato, 1, "")
        with pytest.raises(QuantidadeInvalidaError):
            item.quantidade = 1.5

    def test_cancelar_pedido_entregue_dispara_erro(self, pedido_fixture):
        pedido_fixture.avancar_status()
        pedido_fixture.avancar_status()
        pedido_fixture.avancar_status()
        pedido_fixture.avancar_status()
        with pytest.raises(PedidoJaEntregueError):
            pedido_fixture.cancelar("tarde demais")

    def test_definir_pagamento_apos_conclusao_dispara_erro(self, pedido_fixture):
        pedido_fixture.cancelar("falha no contato")
        with pytest.raises(PagamentoNaoPermitidoError):
            pedido_fixture.definir_forma_pagamento(FormaPagamento.PIX)

    def test_cancelar_sem_motivo_dispara_erro(self, pedido_fixture):
        with pytest.raises(MotivoCancelamentoObrigatorioError):
            pedido_fixture.cancelar("")
