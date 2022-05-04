class Simbolo:
    """Representa o símbolo do alfateto de um autômato ou a lista de terminais de uma GLUD.
    Os únicos valores válidos são letras minúsculas (a-z) e '' para representar o símbolo nulo.
    
    Passar ε no construtor gera Simbolo com valor == ''.
    Passar qualquer outra str no argumento causa uma exceção.

    Implementa semântica de comparação: Simbolo só pode ser igual a outro Simbolo com mesmo atributo valor.
    """
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
        """O Simbolo é vazio i.e. tem valor == ''."""
        return self.char == ''

Simbolo.Vazio = Simbolo('')