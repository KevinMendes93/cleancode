class Cardapio:    
    def __init__(self, descricao: str, valor: float):

        self.descricao = descricao
        self.valor = valor
    
    def eh_igual(self, outro_item) -> bool:
        if not isinstance(outro_item, Cardapio):
            return False
            
        return self.descricao == outro_item.descricao and self.valor == outro_item.valor
    
    def __eq__(self, other):
        return self.eh_igual(other)
    
    def __ne__(self, other):
        return not self.eh_igual(other)