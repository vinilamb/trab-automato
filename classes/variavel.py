class Variavel:
    def __init__(self, valor: str):
        if len(valor) == 1 and valor.isalpha() and valor.isupper():
            self.char = valor
        else:
            raise ValueError("'{valor}' inválido como variável.")
    
    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Variavel):
            return False
        return outro.char == self.char

    def __hash__(self) -> int:
        return hash(self.char)

    def __repr__(self) -> str:
        return f"Variavel('{self.char}')"