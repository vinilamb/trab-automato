from typing import List, Set, Tuple
from classes import arquivo_definicao_glud, Estado, Transicao, Simbolo, AFN, AFNFunc

def glud_para_automato(arquivo_glud):
    print(f"Lendo definição da gludo do arquivo '{arquivo_glud}'")
    parse_result = arquivo_definicao_glud.parse_file('glud.txt').as_dict()

    nome_glud = parse_result['name']
    nome_prod = parse_result['content_prod']
    line_prod = parse_result['line_prod']
    
    print(f"Convertendo GLUD '{nome_glud}' para autômato.")
    
    if nome_prod != line_prod:
        print(f"Não encontrado o conjunto de produções '{nome_prod}'")

    Variaveis = parse_result['vars']
    Terminais = parse_result['terms']
    VariavelInicial = parse_result['start']

    estado_final = Estado('Qf')
    transicoes: List[Transicao] = []
    for prod in parse_result['productions']:
        esq: str = prod['lhs']
        dir: str = prod['rhs']
        
        tran = None
        if dir == '':
            tran = Transicao(Estado(esq), Simbolo.Vazio, estado_final)
        elif len(dir) == 1:
            if dir.islower():
                tran = Transicao(Estado(esq), Simbolo(dir), estado_final)
            else:
                tran = (Transicao, Simbolo.Vazio, Estado(dir))
        elif len(dir) == 2:
            t, v = dir
            tran = Transicao(Estado(esq), Simbolo(t), Estado(v))

        if tran == None:
            print('ERROR: Falha ao interpretar produção.')
        
        transicoes.append(tran)
        
    funcaoPrograma = AFNFunc(transicoes)

    return AFN(
        Alfabeto=set([Simbolo(t) for t in Terminais]),
        Estados=set([Estado(v) for v in Variaveis] + [estado_final]),
        EstadoInicial=VariavelInicial,
        EstadosFinais=set([estado_final]),
        FuncaoPrograma=funcaoPrograma
    )

afn = glud_para_automato('glud.txt')

print(afn.FuncaoPrograma)