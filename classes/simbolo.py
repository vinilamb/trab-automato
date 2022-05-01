class Simbolo:
    def __init__(self, valor: str):
        if valor == 'ε':
            valor = ''
        if (len(valor) == 1 and valor.isalpha() and valor.islower()) or valor == '':
            self.char = valor
        else:
            raise ValueError("'{valor}' inválido como símbolo.")
    
    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Simbolo):
            return False
        return outro.char == self.char

    def __hash__(self) -> int:
        return hash(self.char)

    def __str__(self) -> str:
        return self.char if self.char != '' else 'ε'

    def __repr__(self) -> str:
        return f"Simbolo('{self.char}')" if not self.isnull() else 'Simbolo.Vazio'

    def isnull(self) -> bool:
        return self.char == ''

Simbolo.Vazio = Simbolo('')