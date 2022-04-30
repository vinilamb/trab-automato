from collections import defaultdict
from multiprocessing.sharedctypes import Value
from typing import Callable, List, Set, Tuple, Union, NamedTuple, DefaultDict

Simbolo = str
S_VAZIO: Simbolo = ''

Estado = str
# Estado origem, simbolo, próximo estado
class Transicao(Tuple[Estado, Simbolo, Estado]):
    def __str__(self):
        return f"{self[0]}, {self[1]} -> {self[2]}"

class AFNFunc:
    def __init__(self, transicoes: List[Transicao]):
        transdict = defaultdict(lambda: defaultdict(set))
        for e, s, prox in transicoes:
            transdict[e][s].add(prox)
        self.dict = transdict

    def __str__(self):
        txt = 'AFNFunc:\n'
        for est, dict1 in self.dict.items():
            for s, estados in dict1.items():
                txt += f"\t{est}, {s if s != '' else 'ε'} -> {estados if len(estados) > 0 else '{}'}\n"
        return txt

    def __call__(self, estados: Set[Estado], simbolo) -> Set[Estado]:
        estados = self.fecho_vazio_conjunto(estados)

        if simbolo == '':
            return estados

        resultado = set()
        for e in estados:
            resultado = resultado.union(self.dict[e][simbolo])

        return self.fecho_vazio_conjunto(resultado)

    def fecho_vazio_conjunto(self, estados: Set[Estado]) -> Set[Estado]:
        fecho = set()
        for e in estados:
            fecho = fecho.union(self.fecho_vazio(e))
        return fecho

    def fecho_vazio(self, estadoInicial: Set[Estado]) -> Set[Estado]:
        fecho = set([estadoInicial])

        def percorre_vazias(e):
            for e2 in self.dict[e]['']:
                if e2 not in fecho:
                    fecho.add(e2)
                    percorre_vazias(e2)

        percorre_vazias(estadoInicial)

        return fecho


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

