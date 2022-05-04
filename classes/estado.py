class Estado:
    """Representa o estado de um autômato. Este deve ser válido como um identifier no Python, ou será lançada exceção."""
    valor: str

    def __init__(self, valor: str):
        if valor.isidentifier():
            self.valor = valor
        else:
            raise ValueError('String inválida como Estado para autômato.')
    
    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Estado):
            return False
        return outro.valor == self.valor

    def __hash__(self) -> int:
        return hash(self.valor)

    def __str__(self) -> str:
        return self.valor

    def __repr__(self) -> str:
        return f"Estado('{self.valor}')"