from collections import deque
from typing import List, Iterator, Optional, Tuple
from src.cliente import Cliente
from src.cardapio import Cardapio
from src.pedido import Pedido, StatusPedido


class System:
    
    def __init__(self):
        self.clientes: List[Cliente] = []
        self.cardapio: List[Cardapio] = []
        self.pedidos_abertos = deque()
        self.pedidos_fechados: List[Pedido] = []
    
    def add_cliente(self, cliente: Cliente):
        self.clientes.append(cliente)
    
    def add_item_cardapio(self, item: Cardapio):
        self.cardapio.append(item)
    
    def add_pedido(self, pedido: Pedido):
        self.pedidos_abertos.append(pedido)
    
    def remove_cliente_por_telefone(self, telefone: str):
        self.clientes = [cliente for cliente in self.clientes if cliente.telefone != telefone]
    
    def search_cliente_por_nome(self, nome: str) -> Iterator[Cliente]:
        nome_lower = nome.lower()
        return (cliente for cliente in self.clientes if nome_lower in cliente.nome.lower())
    
    def search_cliente_por_telefone(self, telefone: str) -> Iterator[Cliente]:
        return (cliente for cliente in self.clientes if telefone in cliente.telefone)
    
    def processar_proximo_pedido(self) -> Optional[Pedido]:

        if not self.pedidos_abertos:
            return None
        
        pedido = self.pedidos_abertos.popleft()
        pedido.fechar_pedido()
        self.pedidos_fechados.append(pedido)
        return pedido
    
    def mostrar_cardapio(self) -> str:
        if not self.cardapio:
            return ""
        return "\n".join(item.descricao for item in self.cardapio)
    
    def avancar_status_primeiro_pedido(self) -> Optional[StatusPedido]:

        if not self.pedidos_abertos:
            return None
        
        pedido = self.pedidos_abertos[0]
        pedido.avancar_status()
        
        if pedido.status == StatusPedido.ENTREGUE:
            self.pedidos_abertos.popleft()
            self.pedidos_fechados.append(pedido)
        
        return pedido.status
    
    def cancelar_primeiro_pedido(self, motivo: str) -> bool:

        if not self.pedidos_abertos:
            return False
        
        pedido = self.pedidos_abertos.popleft()
        pedido.cancelar(motivo)
        self.pedidos_fechados.append(pedido)
        return True
    
    def definir_forma_pagamento_primeiro_pedido(self, forma: str) -> Optional[str]:

        if not self.pedidos_abertos:
            return None
        
        pedido = self.pedidos_abertos[0]
        return pedido.definir_forma_pagamento(forma)
    
    def listar_pedidos_abertos(self) -> List[Tuple[Pedido, StatusPedido]]:

        return [(pedido, pedido.status) for pedido in self.pedidos_abertos]
