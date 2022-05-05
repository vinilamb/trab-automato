from typing import List
from classes.simbolo import Simbolo

class Palavra:
    simbolos: List[Simbolo]

    def __init__(self, str: str):
        if not str:
            simbolos = [Simbolo.Vazio]
        else:
            simbolos = [Simbolo(w) for w in str]