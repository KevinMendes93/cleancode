class Cardapio:
    def __init__(self, descricao: str, valor: float):
        self.descricao = descricao
        self.valor = valor

    def __eq__(self, other):
        if not isinstance(other, Cardapio):
            return False

        return (
            self.descricao == other.descricao
            and self.valor == other.valor
        )
