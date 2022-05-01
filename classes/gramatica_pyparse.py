from pyparsing import *

# Interpreta o arquivo de definição da GLUD.

ident = Word(alphas+'_')

var = Char(srange('[A-Z]'))
var_set = '{' + delimited_list(var('vars*')) + '}' 

term = Char(srange('[a-z]'))
term_set = '{' + delimited_list(term('terms*')) + '}'

machine_content = '(' + var_set + ',' + term_set + ',' + ident('content_prod') + ',' + var('start') + ')'
machine_line = ident('name') + '=' + machine_content
prod_name_line = ident('line_prod')

prod = Group(var('lhs') + '->' + Combine((term + Opt(var)) | Empty())('rhs'))

arquivo_definicao_glud: ParserElement = machine_line + prod_name_line + ZeroOrMore(prod)('productions')
