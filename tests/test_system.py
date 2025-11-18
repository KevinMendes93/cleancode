import datetime

import pytest

# Importaremos as classes (src) que ainda iremos criar
from src import Cardapio, Cliente, Pedido, System
from src.pedido import StatusPedido

# Instruções de implementação:
# - Use `collections.deque` para `pedidos_abertos` (FIFO). Exemplo: from collections import deque
#   - operações úteis: append(item), popleft(), len(dq), dq[0] para 'peek'.
# Essas escolhas mantêm a implementação eficiente e compatível com os testes.

# --- Fixtures ---


@pytest.fixture
def sys_fixture():
    """Fixture para uma nova instância do System."""
    return System()


@pytest.fixture
def clientes_fixture():
    """Fixture para múltiplos Clientes."""
    fulano = Cliente("Fulano", "000-9090-0000", "fulano@email.com")
    beltrano = Cliente("Beltrano", "000-9080-0000", "beltrano@email.com")
    cicrano = Cliente("Cicrano", "000-9080-0000", "cicrano@email.com")
    return fulano, beltrano, cicrano


@pytest.fixture
def cardapio_itens_fixture():
    """Fixture para múltiplos itens de Cardapio."""
    prato = Cardapio("Prato1", 10.00)
    acompanhamento = Cardapio("Prato2", 8.50)
    bebida = Cardapio("Bebida1", 3.49)
    return prato, acompanhamento, bebida


@pytest.fixture
def pedidos_fixture(clientes_fixture):
    """Fixture para múltiplos Pedidos."""
    fulano, beltrano, _ = clientes_fixture
    pedido_fulano = Pedido(fulano, datetime.datetime(2023, 1, 1, 12, 0), "Rua X", True)
    pedido_beltrano_1 = Pedido(
        beltrano, datetime.datetime(2023, 1, 1, 12, 1), "Rua Y", True
    )
    pedido_beltrano_2 = Pedido(
        beltrano, datetime.datetime(2023, 1, 1, 12, 2), "Rua Z", True
    )
    return pedido_fulano, pedido_beltrano_1, pedido_beltrano_2


# --- Testes para System ---


class TestSystem:
    def test_adicionar_cliente(self, sys_fixture, clientes_fixture):
        fulano, beltrano, cicrano = clientes_fixture

        sys_fixture.add_cliente(fulano)
        sys_fixture.add_cliente(beltrano)
        sys_fixture.add_cliente(cicrano)

        assert len(sys_fixture.clientes) == 3
        assert sys_fixture.clientes[0] == fulano
        assert sys_fixture.clientes[1] == beltrano

    def test_adicionar_item_cardapio(self, sys_fixture, cardapio_itens_fixture):
        prato, acompanhamento, bebida = cardapio_itens_fixture

        sys_fixture.add_item_cardapio(prato)
        sys_fixture.add_item_cardapio(acompanhamento)
        sys_fixture.add_item_cardapio(bebida)

        assert len(sys_fixture.cardapio) == 3
        assert sys_fixture.cardapio[0] == prato
        assert sys_fixture.cardapio[2] == bebida

    def test_adicionar_pedido(self, sys_fixture, pedidos_fixture):
        pedido_fulano, pedido_beltrano_1, pedido_beltrano_2 = pedidos_fixture

        sys_fixture.add_pedido(pedido_fulano)
        sys_fixture.add_pedido(pedido_beltrano_1)
        sys_fixture.add_pedido(pedido_beltrano_2)

        assert len(sys_fixture.pedidos_abertos) == 3
        assert sys_fixture.pedidos_abertos.popleft() == pedido_fulano
        assert sys_fixture.pedidos_abertos.popleft() == pedido_beltrano_1
        assert sys_fixture.pedidos_abertos.popleft() == pedido_beltrano_2

    def test_remove_cliente_por_telefone(self, sys_fixture, clientes_fixture):
        sys_fixture.add_cliente(clientes_fixture[0])
        sys_fixture.add_cliente(clientes_fixture[1])
        sys_fixture.add_cliente(clientes_fixture[2])

        sys_fixture.remove_cliente_por_telefone("000-9999-0000")

        assert len(sys_fixture.clientes) == 3

        sys_fixture.remove_cliente_por_telefone("000-9080-0000")

        assert len(sys_fixture.clientes) == 1
        assert sys_fixture.clientes[0] == clientes_fixture[0]

    def test_buscar_clientes(self, sys_fixture, clientes_fixture):
        fulano, beltrano, cicrano = clientes_fixture
        sys_fixture.add_cliente(fulano)
        sys_fixture.add_cliente(beltrano)
        sys_fixture.add_cliente(cicrano)

        resultados = sys_fixture.search_cliente_por_nome("Fulano")

        assert list(resultados) == [fulano]

        resultados = sys_fixture.search_cliente_por_telefone("000-9090-0000")

        assert list(resultados) == [fulano]

        resultados = sys_fixture.search_cliente_por_nome("l")

        assert list(resultados) == [fulano, beltrano]

        resultados = sys_fixture.search_cliente_por_telefone("000-9080-0000")

        assert list(resultados) == [beltrano, cicrano]

    def test_fluxo_processamento_pedidos(self, sys_fixture, pedidos_fixture):
        pedido_fulano, pedido_beltrano_1, pedido_beltrano_2 = pedidos_fixture

        sys_fixture.add_pedido(pedido_fulano)
        assert sys_fixture.pedidos_abertos[0] == pedido_fulano
        assert len(sys_fixture.pedidos_abertos) == 1
        assert len(sys_fixture.pedidos_fechados) == 0

        sys_fixture.processar_proximo_pedido()

        assert not sys_fixture.pedidos_abertos
        assert len(sys_fixture.pedidos_fechados) == 1
        assert sys_fixture.pedidos_fechados[0] == pedido_fulano

        sys_fixture.add_pedido(pedido_beltrano_1)
        sys_fixture.add_pedido(pedido_beltrano_2)

        assert len(sys_fixture.pedidos_abertos) == 2
        assert sys_fixture.pedidos_abertos[0] == pedido_beltrano_1

        sys_fixture.processar_proximo_pedido()

        assert len(sys_fixture.pedidos_fechados) == 2
        assert sys_fixture.pedidos_fechados[1] == pedido_beltrano_1
        assert len(sys_fixture.pedidos_abertos) == 1
        assert sys_fixture.pedidos_abertos[0] == pedido_beltrano_2

        sys_fixture.processar_proximo_pedido()

        assert len(sys_fixture.pedidos_fechados) == 3
        assert sys_fixture.pedidos_fechados[2] == pedido_beltrano_2
        assert not sys_fixture.pedidos_abertos

    def test_processar_proximo_pedido_fila_vazia(self, sys_fixture):
        assert sys_fixture.processar_proximo_pedido() is None
        assert not sys_fixture.pedidos_fechados

    def test_mostrar_cardapio_vazio(self, sys_fixture):
        assert sys_fixture.mostrar_cardapio() == ""

    def test_mostrar_cardapio_com_itens(self, sys_fixture, cardapio_itens_fixture):
        prato, acompanhamento, bebida = cardapio_itens_fixture
        sys_fixture.add_item_cardapio(prato)
        sys_fixture.add_item_cardapio(acompanhamento)
        sys_fixture.add_item_cardapio(bebida)
        assert sys_fixture.mostrar_cardapio() == "Prato1\nPrato2\nBebida1"

    def test_busca_sem_resultados(self, sys_fixture):
        assert list(sys_fixture.search_cliente_por_nome("x")) == []
        assert list(sys_fixture.search_cliente_por_telefone("000")) == []

    def test_avancar_status_primeiro_pedido(self, sys_fixture, clientes_fixture):
        fulano, *_ = clientes_fixture
        pedido = Pedido(fulano, datetime.datetime(2023, 1, 1, 12, 0), "Rua A")
        sys_fixture.add_pedido(pedido)
        assert sys_fixture.avancar_status_primeiro_pedido() == StatusPedido.EM_PREPARO
        assert sys_fixture.avancar_status_primeiro_pedido() == StatusPedido.PRONTO
        assert sys_fixture.avancar_status_primeiro_pedido() == StatusPedido.A_CAMINHO
        assert sys_fixture.avancar_status_primeiro_pedido() == StatusPedido.ENTREGUE
        assert sys_fixture.pedidos_fechados[-1] == pedido

    def test_cancelar_primeiro_pedido(self, sys_fixture, clientes_fixture):
        fulano, *_ = clientes_fixture
        pedido = Pedido(fulano, datetime.datetime(2023, 1, 1, 12, 0), "Rua A")
        sys_fixture.add_pedido(pedido)
        assert sys_fixture.cancelar_primeiro_pedido("Fora da rota") is True
        assert sys_fixture.pedidos_fechados[-1] == pedido
        assert pedido.status.name == "CANCELADO"

    def test_definir_forma_pagamento_primeiro_pedido(
        self, sys_fixture, clientes_fixture
    ):
        fulano, *_ = clientes_fixture
        pedido = Pedido(fulano, datetime.datetime(2023, 1, 1, 12, 0), "Rua A")
        sys_fixture.add_pedido(pedido)
        assert sys_fixture.definir_forma_pagamento_primeiro_pedido("pix") == "pix"
        assert pedido.forma_pagamento == "pix"

    def test_listar_pedidos_abertos_mostra_status(self, sys_fixture, clientes_fixture):
        fulano, beltrano, *_ = clientes_fixture
        p1 = Pedido(fulano, datetime.datetime(2023, 1, 1, 12, 0), "Rua A")
        p2 = Pedido(beltrano, datetime.datetime(2023, 1, 1, 12, 1), "Rua B")
        sys_fixture.add_pedido(p1)
        sys_fixture.add_pedido(p2)
        lista = sys_fixture.listar_pedidos_abertos()
        assert [(p.cliente.nome, s) for p, s in lista] == [
            ("Fulano", StatusPedido.RECEBIDO),
            ("Beltrano", StatusPedido.RECEBIDO),
        ]
        sys_fixture.avancar_status_primeiro_pedido()
        lista = sys_fixture.listar_pedidos_abertos()
        assert [(p.cliente.nome, s) for p, s in lista] == [
            ("Fulano", StatusPedido.EM_PREPARO),
            ("Beltrano", StatusPedido.RECEBIDO),
        ]
