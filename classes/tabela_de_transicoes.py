from collections import defaultdict
from typing import DefaultDict, Tuple, List, Set, Union

from .simbolo import Simbolo
from .estado import Estado

class TransicaoError(Exception):
    pass

# Classe que representa uma transição de autômato finito.
class Transicao(Tuple[Estado, Simbolo, Estado]):
    def __new__(cls, e, s, e2):
        return super().__new__(cls, tuple([e, s, e2]))
    def __str__(self):
        return f"{self[0]}, {self[1]} -> {self[2]}"
    def is_vazia(self):
        return self[1] == Simbolo.Vazio

# Estrutura de dados para lidar com transições do autômato finito.
# 
class TabelaTransicoes:
    dict: DefaultDict

    def __init__(self, transicoes: List[Transicao]) -> None:
        transdict = defaultdict(lambda: defaultdict(set))
        for e, s, e2 in transicoes:
            transdict[e][s].add(e2)
        self.dict = transdict

    # Transição de autômato determinístico
    def proximo_estado(self, estado: Estado, simbolo: Simbolo) -> Union[Estado, None]:
        conjuntoEstados = self.dict[estado][simbolo]
        if len(conjuntoEstados) == 1:
            return list(conjuntoEstados)[0]
        elif len(conjuntoEstados) == 0:
            return None

    # proximo_estado() para autômatos não determinísticos
    def obter_estados(self, estado: Estado, simbolo: Simbolo) -> Set[Estado]:
        return self.dict[estado][simbolo]

    # Retorna todos os estados atingíveis por movimentos vazios.
    def fecho_vazio(self, estadoInicial: Set[Estado]) -> Set[Estado]:
        fecho = set([estadoInicial])

        def percorre_vazias(e):
            for e2 in self.dict[e][Simbolo.Vazio]:
                if e2 not in fecho:
                    fecho.add(e2)
                    percorre_vazias(e2)

        percorre_vazias(estadoInicial)

        return fecho

    # fecho vazio para um conjunto de estados
    def fecho_vazio_conjunto(self, estados: Set[Estado]) -> Set[Estado]:
        fecho = set()
        for e in estados:
            fecho = fecho.union(self.fecho_vazio(e))
        return fecho
        
    def tem_ciclos(self, estadoInicial: Set[Simbolo]):
        import networkx as nx
        edges = [(e.valor, e2.valor) for e, _, e2 in self.obter_transicoes()]
        G = nx.DiGraph(edges)
        return nx.is_directed_acyclic_graph(G)

    def obter_transicoes(self) -> List[Transicao]:
        result = []
        for e, dict2 in self.dict.items():
            for s, e2 in dict2.items():
                for t in e2:
                    result.append(Transicao(e, s, t))
        return result