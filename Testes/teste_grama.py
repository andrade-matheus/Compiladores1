from __future__ import print_function
from AnalisadorLexico import Lexico
from AnalisadorSintatico import Sintatico


for file in ['atr.g', 'doip.g', 'exp.g', 'nome.g', 'pthen.g', 'soma.g', 'then.g', 'tipo.g', 'var.g']:
    with open('teste_gramatica\\' + file, 'r') as f:
        print(file)
        print()
        analisador_lexico = Lexico()
        analisador_lexico.tokenizar(f.read())
        analisador_sintatico = Sintatico(analisador_lexico.tokens, analisador_lexico.tokens_linhas)
        analisador_sintatico.run(analisador_lexico.tokens_id)
        f.close()
