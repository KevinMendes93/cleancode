from src.cardapio import Cardapio

class QuantidadeInvalidaError(Exception):
    pass

class ItemPedido:
    def __init__(self, opcao_menu: Cardapio, quantidade: int, observacao: str):

        self.verificar_quantidade_invalida(quantidade)
        
        self.opcao_menu = opcao_menu
        self._quantidade = quantidade
        self.observacao = observacao
    
    @property
    def quantidade(self) -> int:
        return self._quantidade
    
    @quantidade.setter
    def quantidade(self, valor: int):
        self.verificar_quantidade_invalida(valor)
        self._quantidade = valor
    
    @property
    def valor_total(self) -> float:
        return self.opcao_menu.valor * self._quantidade


    def verificar_quantidade_invalida(self, quantidade: int):
        if quantidade < 0:
            raise QuantidadeInvalidaError("Quantidade não pode ser negativa")
        if not isinstance(quantidade, int):
            raise QuantidadeInvalidaError("Quantidade deve ser um número inteiro")