class Cliente:
    def __init__(self, nome: str, telefone: str, email: str):
        self.nome = nome
        self.telefone = telefone
        self.email = email
    
    def __eq__(self, other):
        if not isinstance(other, Cliente):
            return False

        return (self.nome == other.nome and 
                self.telefone == other.telefone and 
                self.email == other.email)
    
    def __ne__(self, other):
        return not self.__eq__(other)
