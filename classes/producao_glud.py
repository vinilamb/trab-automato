from typing import NamedTuple, Tuple

from .variavel import Variavel
from .simbolo import Simbolo

class ProducaoGLUD(NamedTuple):
    Esq: Variavel
    Dir: Tuple[Simbolo, Variavel | None]

