from typing import List, Set, Tuple
from automato.automato import AFNFunc, Estado, Simbolo, AFN, Transicao
from gramatica.glud import full_grammar_file

def glud_para_automato(arquivo_glud):
    print(f"Lendo definição da gludo do arquivo '{arquivo_glud}'")
    parse_result = full_grammar_file.parse_file('glud.txt').as_dict()

    nome_glud = parse_result['name']
    nome_prod = parse_result['content_prod']
    line_prod = parse_result['line_prod']
    
    print(f"Convertendo GLUD '{nome_glud}' para autômato.")
    
    if nome_prod != line_prod:
        print(f"Não encontrado o conjunto de produções '{nome_prod}'")

    Variaveis = set(parse_result['vars'])
    Terminais = set(parse_result['terms'])
    VariavelInicial = parse_result['start']

    estado_final = 'Qf'
    transicoes: List[Transicao] = []
    for prod in parse_result['productions']:
        esq: str = prod['lhs']
        dir: str = prod['rhs']

        tran = None
        if dir == '':
            tran = (esq, '', estado_final)
        elif len(dir) == 1:
            if dir.islower():
                tran = (esq, dir, estado_final)
            else:
                tran = (esq, '', dir)
        elif len(dir) == 2:
            t, v = dir
            tran = (esq, t, v)

        if tran == None:
            print('ERROR: Falha ao interpretar produção.')
        
        transicoes.append(tran)
        
    Estados = set(Variaveis)
    Estados.add(estado_final)

    funcaoPrograma = AFNFunc(transicoes)

    return AFN(
        Alfabeto=Variaveis,
        Estados=Estados,
        EstadoInicial=VariavelInicial,
        EstadosFinais=set([estado_final]),
        FuncaoPrograma=funcaoPrograma
    )

afn = glud_para_automato('glud.txt')

ok = afn.aceita('emememmeememem')
if ok:
    print('aceitou')
else:
    print('recusou')