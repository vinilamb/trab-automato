from collections import defaultdict
from typing import Callable, List, Set, Tuple, Union, NamedTuple, DefaultDict

from .tabela_de_transicoes import TabelaTransicoes, Transicao
from .estado import Estado
from .simbolo import Simbolo

class AFNFunc:
    tabela: TabelaTransicoes

    def __init__(self, transicoes: List[Transicao]):
        self.tabela = TabelaTransicoes(transicoes)

    def __str__(self):
        txt = 'AFNFunc:\n'
        for t in self.tabela.obter_transicoes():
            txt += str(t) + '\n'
        return txt

    def __call__(self, estados: Set[Estado], simbolo) -> Set[Estado]:
        estados = self.tabela.fecho_vazio_conjunto(estados)

        if simbolo == '':
            return estados

        resultado = set()
        for e in estados:
            resultado = self.tabela.obter_estados(e, simbolo)

        return self.tabela.fecho_vazio_conjunto(resultado)


# Autômato de estado finito não-determinístico com movimentos vazios
class AFN(NamedTuple):
    Alfabeto: Set[Simbolo]
    Estados: Set[Estado]
    EstadoInicial: Estado
    FuncaoPrograma: AFNFunc
    EstadosFinais: Set[Estado]

    def aceita(self, palavra):
        estados = set([self.EstadoInicial])

        for simbolo in palavra:
            out = f"{estados}, {simbolo} -> "
            estados = self.FuncaoPrograma(estados, simbolo)
            out += str(estados)
            print(out)

        for e in estados:
            if e in self.EstadosFinais:
                return True

        return False

