#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

ARQUIVO_FONTE = sys.argv[1]
ARQUIVO_SAIDA = sys.argv[2]
ARQUIVO_TABELA_SIMBOLOS = 'Arquivo-Tabela-Simbolos.txt'

POSSIVEIS_PROX_TOKENS = {'var':['id'],':':['integer','real'] ,'id':['+',',',':',':=','then'] ,',':['id'],'integer':[';','id','if',''],'real':[';','id','if',''],';':['id'],':=':['id'],'if':['id'],'then':['id','if'],'+':['id']}

#Verifica se identificador já foi inserido na tabela de simbolos.
def contemTabela(cadeia):
    with open(ARQUIVO_TABELA_SIMBOLOS,'r') as arquivo:
        itens_tabela = [identificador.split() for identificador in arquivo.readlines()]

    for identificador in itens_tabela:
        if(identificador[0] == cadeia):
            return True
    return False

#Insere identificadores na tabela de simbolos.
def inserirTabela(arquivo, buffer, tipo):
    # print('INSERINDO NA TABELA')
    for item in buffer:
        if(contemTabela(item[0])):
            raise RuntimeError('Nome de variável já utilizado, um nome de variável não pode ser instânciado mais de uma vez.')
        else:
            for valor in item:
                arquivo.write(valor + ' ')
            arquivo.write(tipo + '\n')
    del buffer[:]

#Lê os tokens e armazena em buffer, até identificar o tipo dos idenficadores, e mandar inseri-los.
def criarTabela(token_stream):
    buffer = []
    encerrar_declaracao = False
    with open(ARQUIVO_TABELA_SIMBOLOS,'w') as arquivo:
        for cadeia in token_stream:
            if('id' in cadeia):
                buffer.append([cadeia.split()[1],'id', 'var',])
            elif(cadeia == 'integer'):
                inserirTabela(arquivo, buffer, 'integer')
                encerrar_declaracao = True
            elif(cadeia == 'real'):
                inserirTabela(arquivo, buffer, 'real')
                encerrar_declaracao = True
            elif(cadeia == ';'):
                encerrar_declaracao = False
            elif(encerrar_declaracao):
                break

#Retorna um identificador da tabela de simbolos.
def buscarTabela(cadeia):
    with open(ARQUIVO_TABELA_SIMBOLOS,'r') as arquivo:
        itens_tabela = [identificador.split() for identificador in arquivo.readlines()]

    for identificador in itens_tabela:
        if(identificador[0] == cadeia):
            return identificador


def verificacaoTipo(token_stream):
    tipo_resultante = ''
    comecar_verificacao = False

    for cadeia in token_stream:
        if(cadeia == '*'):
            comecar_verificacao = True

        if(comecar_verificacao):
            if('id' in cadeia):
                if(tipo_resultante == ''):
                    idenficador = buscarTabela(cadeia.split()[1])
                    tipo_resultante = idenficador[3]
                else:
                    idenficador = buscarTabela(cadeia.split()[1])
                    if(tipo_resultante != idenficador[3]):
                        erro = 'Atribuição de variáveis de tipagem diferente, tipo ' + tipo_resultante + ' não pode receber tipo '+ idenficador[3]
                        raise RuntimeError(erro)

            elif(cadeia == 'if'):
                tipo_resultante = 'integer'

            elif(cadeia == 'then'):
                tipo_resultante = ''


################################################################################
######## MAIN: (Análise Sintática)
################################################################################
with open(ARQUIVO_SAIDA_LEXICO, 'r') as arquivo:
    token_stream = [token.strip() for token in arquivo.readlines()]

token_atual = ''
encontrou = False

for token_prox in token_stream:
    if(token_atual == ''):
        token_atual = token_prox
    elif(token_atual == '*'):
        continue
    elif(token_prox == '*'):
        continue
    elif(token_prox == 'fim'):
        break
    else:
        if('id' in token_atual):
            possiveis_tokens = POSSIVEIS_PROX_TOKENS['id']
        else:
            possiveis_tokens = POSSIVEIS_PROX_TOKENS[token_atual]

        for possivel_token in possiveis_tokens:
            if(possivel_token in token_prox):
                encontrou = True
        if(not encontrou):
            erro = 'Carácter ' + str(token_prox) + ' não esperado.'
            raise RuntimeError(erro)
        else:
            token_atual = token_prox
            encontrou = False



################################################################################
######## MAIN: (Análise Semântica)
################################################################################
with open(ARQUIVO_SAIDA_LEXICO, 'r') as arquivo:
    token_stream = [token.strip() for token in arquivo.readlines()]

criarTabela(token_stream)
verificacaoTipo(token_stream)
