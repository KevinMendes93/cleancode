from collections import deque
from typing import List, Iterator, Optional, Tuple
from src.cliente import Cliente
from src.cardapio import Cardapio
from src.pedido import Pedido, StatusPedido


class System:
    """Classe que representa o sistema de gerenciamento de pedidos."""
    
    def __init__(self):
        """Inicializa o sistema."""
        self.clientes: List[Cliente] = []
        self.cardapio: List[Cardapio] = []
        self.pedidos_abertos = deque()
        self.pedidos_fechados: List[Pedido] = []
    
    def add_cliente(self, cliente: Cliente):
        """Adiciona um cliente ao sistema."""
        self.clientes.append(cliente)
    
    def add_item_cardapio(self, item: Cardapio):
        """Adiciona um item ao cardápio."""
        self.cardapio.append(item)
    
    def add_pedido(self, pedido: Pedido):
        """Adiciona um pedido à fila de pedidos abertos."""
        self.pedidos_abertos.append(pedido)
    
    def remove_cliente_por_telefone(self, telefone: str):
        """Remove clientes pelo telefone."""
        self.clientes = [c for c in self.clientes if c.telefone != telefone]
    
    def search_cliente_por_nome(self, nome: str) -> Iterator[Cliente]:
        """
        Busca clientes por nome (busca parcial, case-insensitive).
        
        Args:
            nome: Nome ou parte do nome a buscar
            
        Returns:
            Iterator com os clientes encontrados
        """
        nome_lower = nome.lower()
        return (c for c in self.clientes if nome_lower in c.nome.lower())
    
    def search_cliente_por_telefone(self, telefone: str) -> Iterator[Cliente]:
        """
        Busca clientes por telefone (busca parcial).
        
        Args:
            telefone: Telefone ou parte do telefone a buscar
            
        Returns:
            Iterator com os clientes encontrados
        """
        return (c for c in self.clientes if telefone in c.telefone)
    
    def processar_proximo_pedido(self) -> Optional[Pedido]:
        """
        Processa o próximo pedido da fila (FIFO).
        Remove da fila de abertos e adiciona aos fechados.
        
        Returns:
            O pedido processado ou None se a fila estiver vazia
        """
        if not self.pedidos_abertos:
            return None
        
        pedido = self.pedidos_abertos.popleft()
        pedido.fechar_pedido()
        self.pedidos_fechados.append(pedido)
        return pedido
    
    def mostrar_cardapio(self) -> str:
        """
        Retorna uma string com todos os itens do cardápio.
        
        Returns:
            String com descrições dos itens separadas por quebra de linha
        """
        if not self.cardapio:
            return ""
        return "\n".join(item.descricao for item in self.cardapio)
    
    def avancar_status_primeiro_pedido(self) -> Optional[StatusPedido]:
        """
        Avança o status do primeiro pedido da fila.
        Se o pedido for entregue, remove da fila e adiciona aos fechados.
        
        Returns:
            O novo status do pedido ou None se a fila estiver vazia
        """
        if not self.pedidos_abertos:
            return None
        
        pedido = self.pedidos_abertos[0]
        pedido.avancar_status()
        
        if pedido.status == StatusPedido.ENTREGUE:
            self.pedidos_abertos.popleft()
            self.pedidos_fechados.append(pedido)
        
        return pedido.status
    
    def cancelar_primeiro_pedido(self, motivo: str) -> bool:
        """
        Cancela o primeiro pedido da fila.
        
        Args:
            motivo: Motivo do cancelamento
            
        Returns:
            True se cancelou com sucesso, False se a fila estiver vazia
        """
        if not self.pedidos_abertos:
            return False
        
        pedido = self.pedidos_abertos.popleft()
        pedido.cancelar(motivo)
        self.pedidos_fechados.append(pedido)
        return True
    
    def definir_forma_pagamento_primeiro_pedido(self, forma: str) -> Optional[str]:
        """
        Define a forma de pagamento do primeiro pedido da fila.
        
        Args:
            forma: Forma de pagamento
            
        Returns:
            A forma de pagamento normalizada ou None se a fila estiver vazia
        """
        if not self.pedidos_abertos:
            return None
        
        pedido = self.pedidos_abertos[0]
        return pedido.definir_forma_pagamento(forma)
    
    def listar_pedidos_abertos(self) -> List[Tuple[Pedido, StatusPedido]]:
        """
        Lista todos os pedidos abertos com seus status.
        
        Returns:
            Lista de tuplas (pedido, status)
        """
        return [(pedido, pedido.status) for pedido in self.pedidos_abertos]
