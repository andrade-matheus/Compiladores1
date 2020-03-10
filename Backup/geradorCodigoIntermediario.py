#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

#ARGUMENTOS:
# ARQUIVO_FONTE = sys.argv[1]
# ARQUIVO_SAIDA = sys.argv[2]

ARQUIVO_FONTE = 'Arquivo-Fonte.txt'
ARQUIVO_SAIDA = 'Arquivo-Saida-lexico.txt'

#CONSTANTES:
ARQUIVO_TABELA_SIMBOLOS = 'Arquivo-Tabela-Simbolos.txt'
ARQUIVO_CODIGO_INTERMEDIARIO = 'Arquivo-Codigo-Intermediario.txt'

def inserirTabela(cadeia, token, categoria, tipo):
    with open(ARQUIVO_TABELA_SIMBOLOS,'a') as arquivo:
        arquivo.write(cadeia + ' ' + token + ' ' + categoria + ' ' + tipo + '\n')

def buscarTabela(cadeia):
    with open(ARQUIVO_TABELA_SIMBOLOS,'r') as arquivo:
        itens_tabela = [identificador.split() for identificador in arquivo.readlines()]

    # print(itens_tabela)
    # print('ENTROU')
    for identificador in itens_tabela:
        if(identificador[0] == cadeia):
            # print('ENTROU')
            return identificador

    return None

def buscarUltimoTemp():
    temp_num = 0
    with open(ARQUIVO_TABELA_SIMBOLOS,'r') as arquivo:
        itens_tabela = [identificador.split() for identificador in arquivo.readlines()]

    for identificador in itens_tabela:
        if('temp' in identificador[0]):
            temp_num = identificador[0][-1]

    return temp_num

def geraTemp(tipo):
    temp_num = int(buscarUltimoTemp()) + 1
    cadeia = 'temp' + str(temp_num)
    inserirTabela(cadeia, 'id', 'var', tipo)
    return cadeia

def pop(pilha):
    if(not pilha):
        return ''
    else:
        topo = pilha[len(pilha)-1]
        del pilha[len(pilha)-1]
        return topo

def peek(pilha):
    if(not pilha):
        return ''
    else:
        return pilha[len(pilha)-1]

with open(ARQUIVO_SAIDA, 'r') as arquivo:
    token_stream = [token.strip() for token in arquivo.readlines()]

comecar = False
cont_comandos = 0
buffer_quad = []
pilha_id = []
pilha_op = []
operador = ''

# print(token_stream)

token_passado = ''
for item in token_stream:
    # print('BUFFER QUAD: ', end='')
    # print(buffer_quad, end=' | ')
    # print('PILHA ID: ', end='')
    # print(pilha_id)

    token = item.split()[0]

    if(token_passado == 'integer' or token_passado == 'real'):
        if(token == 'if' or token == 'id'):
            comecar = True

    if(comecar):
        if(token == 'if'):
            cont_comandos += 1


        if(token == 'id'):
            pilha_id.append(item.split()[1])
            if(peek(pilha_op) == '+'):
                if(len(pilha_id) >= 2):
                    id_dir = pop(pilha_id)
                    id_esq = pop(pilha_id)
                    operador = pop(pilha_op)

                    # print(id_dir)

                    id = buscarTabela(id_dir)

                    # print(id)

                    temp = geraTemp(id[3])

                    buffer_quad.append([operador, id_esq, id_dir, temp])

                    pilha_id.append(temp)

        if(token != '+'):
            if(token_passado == 'id'):
                if(peek(pilha_op) == ':='):
                    if(len(pilha_id) >= 2):
                        id_dir = pop(pilha_id)
                        id_esq = pop(pilha_id)
                        operador = pop(pilha_op)

                        buffer_quad.append([operador, id_esq, id_dir, '-'])

        if(token == '+'):
            cont_comandos += 1
            pilha_op.append(token)

        if(token == ':='):
            cont_comandos += 1
            pilha_op.append(token)

        if(token == 'then'):
            aux_id = pilha_id[len(pilha_id)-1]
            buffer_quad.append(['JF', aux_id, '','-'])

    token_passado = token


ultima_linha = len(buffer_quad) + 1
cont_linha = 1
with open(ARQUIVO_CODIGO_INTERMEDIARIO, 'w') as arquivo:
    for item in buffer_quad:
        if(item[0] == 'JF'):
            item[2] = str(ultima_linha)

        arquivo.write(str(cont_linha) + ': [' + item[0] + ' ' + item[1] + ' ' + item[2] + ' ' + item[3] + ']\n')
        cont_linha += 1

    arquivo.write(str(cont_linha) + ': [...]\n')
