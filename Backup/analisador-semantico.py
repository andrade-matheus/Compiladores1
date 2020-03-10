#!/usr/bin/python3
# -*- coding: utf-8 -*-

#CONSTANTES:
ARQUIVO_FONTE = 'Arquivo-Fonte.txt'
ARQUIVO_FONTE_COM_ERROS = 'Arquivo-Fonte-Erros.txt'
ARQUIVO_SAIDA_LEXICO = 'Arquivo-Saida-lexico.txt'
ARQUIVO_TABELA_SIMBOLOS = 'Arquivo-Tabela-Simbolos.txt'

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
            raise RuntimeError(Nome de variável já utilizado, um nome de variável não pode ser instânciado mais de uma vez.)
        else:
            for valor in item:
                arquivo.write(valor + ' ')
            arquivo.write(tipo + '\n')
    del buffer[:]

#Lê os tokens e armazena em buffer, até identificar o tipo dos idenficadores, e mandar inseri-los.
def criarTabela(token_stream):
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

#MAIN:
with open(ARQUIVO_SAIDA_LEXICO, 'r') as arquivo:
    token_stream = [token.strip() for token in arquivo.readlines()]

buffer = []
criarTabela(token_stream)
buscarTabela()
