#!/usr/bin/python3
# -*- coding: utf-8 -*-

#CONSTANTES:
ARQUIVO_FONTE = 'Arquivo-Fonte.txt'
ARQUIVO_FONTE_COM_ERROS = 'Arquivo-Fonte-Erros.txt'
ARQUIVO_SAIDA_LEXICO = 'Arquivo-Saida-lexico.txt'


# def possiveisTokens(token):
#     if(token == 'var'):                     #1 var
#         return ['id']
#     elif(token == ':'):                     #2 :
#         return ['integer','real']
#     elif('id' in token):                    #3 id
#         return ['+',',',':',':=','then']
#     elif(token == ','):                     #4 ,
#         return ['id']
#     elif(token == 'integer'):               #5 integer
#         return [';','id','if','']
#     elif(token == 'real'):                  #6 real
#         return [';','id','if','']
#     elif(token == ';'):                     #7 ;
#         return ['id']
#     elif(token == ':='):                    #8 :=
#         return ['id']
#     elif(token == 'if'):                    #9 if
#         return ['id']
#     elif(token == 'then'):                  #10 then
#         return ['id','if']
#     elif(token == '+'):                     #11 +
#         return ['id']
#
#     raise RuntimeError('Erro: token não encontrado.')

tokens_seguintes = {'var'   :['id'],
                    ':'     :['integer','real'] ,
                    'id'    :['+',',',':',':=','then'] ,
                    ','     :['id'],
                    'integer':[';','id','if',''],
                    'real'  :[';','id','if',''],
                    ';'     :['id'],
                    ':='    :['id'],
                    'if'    :['id'],
                    'then'  :['id','if'],
                    '+'     :['id']}

#MAIN:
with open(ARQUIVO_SAIDA_LEXICO, 'r') as arquivo:
    token_stream = [token.strip() for token in arquivo.readlines()]

token_atual = ''
encontrou = False

for token_prox in token_stream:
    if(token_atual == ''):
        token_atual = token_prox
    elif(token_prox == 'fim'):
        break
    else:
        for possivel_token in possiveisTokens(token_atual):
            if(possivel_token in token_prox):
                encontrou = True
        if(not encontrou):
            erro = 'Carácter ' + str(token_prox) + ' não esperado.'
            raise RuntimeError(erro)
        else:
            token_atual = token_prox
            encontrou = False

print('Análise sintática foi conclída.')
