from datetime import datetime
from enum import Enum
from typing import List
from src.cliente import Cliente
from src.item_pedido import ItemPedido


class StatusPedido(Enum):
    RECEBIDO = "recebido"
    EM_PREPARO = "em_preparo"
    PRONTO = "pronto"
    A_CAMINHO = "a_caminho"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"


class FormaPagamento:
    DINHEIRO = "dinheiro"
    PIX = "pix"
    CARTAO = "cartao"


class FormaPagamentoInvalidaError(Exception):
    pass


class PedidoJaEntregueError(Exception):
    pass


class PagamentoNaoPermitidoError(Exception):
    pass


class MotivoCancelamentoObrigatorioError(Exception):
    pass


class Pedido:
    def __init__(self, cliente: Cliente, data_hora: datetime, endereco: str, 
                 situacao_aberto: bool = True):

        self.cliente = cliente
        self.data_hora = data_hora
        self.endereco = endereco
        self.situacao_aberto = situacao_aberto
        self.itens: List[ItemPedido] = []
        self.status = StatusPedido.RECEBIDO
        self.forma_pagamento = None
        self.cancelamento_motivo = None
    
    def add_item(self, item: ItemPedido):
        self.itens.append(item)
    
    @property
    def valor_total(self) -> float:
        return sum(item.valor_total for item in self.itens)
    
    def fechar_pedido(self):
        self.situacao_aberto = False
    
    def avancar_status(self):
        if self.status == StatusPedido.CANCELADO or self.status == StatusPedido.ENTREGUE:
            return
        
        ordem_status = [
            StatusPedido.RECEBIDO,
            StatusPedido.EM_PREPARO,
            StatusPedido.PRONTO,
            StatusPedido.A_CAMINHO,
            StatusPedido.ENTREGUE
        ]
        
        indice_atual = ordem_status.index(self.status)
        if indice_atual < len(ordem_status) - 1:
            self.status = ordem_status[indice_atual + 1]
            
            if self.status == StatusPedido.ENTREGUE:
                self.situacao_aberto = False
    
    def cancelar(self, motivo: str):

        if not motivo or motivo.strip() == "":
            raise MotivoCancelamentoObrigatorioError("Motivo de cancelamento é obrigatório")
        
        if self.status == StatusPedido.ENTREGUE:
            raise PedidoJaEntregueError("Não é possível cancelar um pedido já entregue")
        
        self.status = StatusPedido.CANCELADO
        self.cancelamento_motivo = motivo
        self.situacao_aberto = False
    
    def definir_forma_pagamento(self, forma: str) -> str:

        if self.status in [StatusPedido.CANCELADO, StatusPedido.ENTREGUE]:
            raise PagamentoNaoPermitidoError("Não é possível definir pagamento após conclusão do pedido")
        
        forma_normalizada = forma.lower().strip()
        
        formas_validas = [FormaPagamento.DINHEIRO, FormaPagamento.PIX, FormaPagamento.CARTAO]
        
        if forma_normalizada not in formas_validas:
            raise FormaPagamentoInvalidaError(f"Forma de pagamento '{forma}' inválida")
        
        self.forma_pagamento = forma_normalizada
        return forma_normalizada