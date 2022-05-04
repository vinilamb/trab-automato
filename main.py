from typing import List

from pkg_resources import require
from classes import arquivo_definicao_glud, Estado, Transicao, Simbolo, AFN, AFNFunc

class GLUDError(Exception):
    """Exceção para lançar quando tem erro com a GLUD."""
    pass
    
def glud_para_automato(arquivo_glud):
    """Lê o arquivo GLUD e gera um autômato para reconhecê-la."""
    
    print(f"Lendo definição da gludo do arquivo '{arquivo_glud}'")
    parse_result = arquivo_definicao_glud.parse_file(arquivo_glud).as_dict()

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
        # lados esquerdo e direito da produção
        esq: str = prod['lhs']
        dir: str = prod['rhs']

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
            raise GLUDError('Falha ao interpretar produção.')

        transicoes.append(tran)
    
    # valida produções
    for e1, s, e2 in transicoes:
        if s.char != '' and s.char not in Terminais:
            raise GLUDError(f"Símbolo '{s}' não faz parte do alfabeto")
        if e1.valor not in Variaveis:
            raise GLUDError(f"Estado '{e1}' não declarado")
        if e2 != estado_final and e2.valor not in Variaveis:
            raise GLUDError(f"Estado '{e2}' não declarado")

    funcaoPrograma = AFNFunc(transicoes)

    return AFN(
        Alfabeto=set([Simbolo(t) for t in Terminais]),
        Estados=set([Estado(v) for v in Variaveis] + [estado_final]),
        EstadoInicial=Estado(VariavelInicial),
        EstadosFinais=set([estado_final]),
        FuncaoPrograma=funcaoPrograma
    )

def encerrar():
    print("Cancelando execução...")
    exit(1)        

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Reconhece palavras a partir de uma GLUD')

    parser.add_argument('glud', metavar='glud.txt', help='Arquivo de texto com definição da gramática')

    parser.add_argument('-p', metavar='palavras', nargs='*', help='Palavras para reconhecer')
    
    parser.add_argument('-f', metavar='nome_arquivo', help="Arquivo com palavras")

    args = parser.parse_args()

    try:
        afn = glud_para_automato(args.glud)
    except GLUDError as e:
        print(f"ERRO: {e}")
        print("Cancelando execução...")
        exit(1)        

    if not afn.FuncaoPrograma.tabela.tem_ciclos(afn.EstadoInicial):
        print('A linguagem é infinita')
    else:
        print('A linguagem NÃO é infinita')

    palavrasParaRodar = []
    if args.p: 
        palavrasParaRodar += args.p

    if args.f:
        try:
            with open(args.f) as f:
                palavrasParaRodar += [linha.strip() for linha in f.readlines()]
        except:
            print(f"Não foi possível abrir arquivo '{args.f}'")
            encerrar()

    if not palavrasParaRodar:
        print('Sem palavras para testar aceitação.')
        encerrar()

    for p in palavrasParaRodar:
        aceita = 'Pertence' if afn.aceita(p) else 'NÃO pertence'
        if p == '':
            p = 'ε'
        print(f"{p} : {aceita}")