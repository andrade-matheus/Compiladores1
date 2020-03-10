#!/usr/bin/python3
# -*- coding: utf-8 -*-

#Utilizado como referência para a criação desse Tokenizador a documentação da biblioteca de regex para Python:
#https://docs.python.org/3/library/re.html#writing-a-tokenizer

import re
import sys

#ARGUMENTOS:
ARQUIVO_FONTE = sys.argv[1]
ARQUIVO_SAIDA = sys.argv[2]

#CONSTANTES:
ARQUIVO_TABELA_SIMBOLOS = 'Arquivo-Tabela-Simbolos.txt'
ARQUIVO_CODIGO_INTERMEDIARIO = 'Arquivo-Codigo-Intermediario.txt'

tokens = [
    ('Atribuição', r'\:\='),
    ('Tipos', r'integer|real'),
    ('PalavraReservada', r'var|if|then'),
    ('Identificador', r'[A-Za-z]+'),
    ('Operadores', r'\+'),
    ('Pontuações', r'[\:\;\,]'),
    ('Espaços', r'[ \t]+'),
    ('NovaLinha', r'\n'),
    ('Erro', r'.')
    ]


with open(ARQUIVO_FONTE,'r') as arquivo:
    codigo = arquivo.read()

token_regex = '|'.join('(?P<%s>%s)' % par_token for par_token in tokens)
numero_linha = 1
comeco_coluna = 0

with open(ARQUIVO_SAIDA,'w') as arquivo:
    primeira_palavra_reservada = True
    for token in re.finditer(token_regex, codigo):
        tipo_token = token.lastgroup
        valor = token.group()
        coluna = token.start() - comeco_coluna

        if(tipo_token == 'Identificador'):
            tipo_token = 'id'
        elif(tipo_token == 'PalavraReservada'):
            tipo_token = valor
        elif(tipo_token == 'Tipos'):
            tipo_token = valor
        elif(tipo_token == 'Operadores'):
            tipo_token = valor
        elif(tipo_token == 'Pontuações'):
            tipo_token = valor
        elif(tipo_token == 'Atribuição'):
            tipo_token = valor
        elif(tipo_token == 'NovaLinha'):
            comeco_coluna = token.end()
            numero_linha += 1
            continue
        elif(tipo_token == 'Espaços'):
            continue
        elif(tipo_token == 'Erro'):
            erro = '"' + valor + '" caracter inválido na linha ' + str(numero_linha) + ', coluna ' + str(coluna)
            raise SyntaxError(erro)

        arquivo.write(tipo_token + ' ' + valor + ' ' + str(numero_linha) + ' ' + str(coluna) + '\n')

    arquivo.write('fim\n')
