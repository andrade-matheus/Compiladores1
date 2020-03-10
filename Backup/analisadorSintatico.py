#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

#ARGUMENTOS:
ARQUIVO_FONTE = sys.argv[1]
ARQUIVO_SAIDA = sys.argv[2]

#CONSTANTES:
ARQUIVO_TABELA_SIMBOLOS = 'Arquivo-Tabela-Simbolos.txt'
ARQUIVO_CODIGO_INTERMEDIARIO = 'Arquivo-Codigo-Intermediario.txt'

def contemTabela(cadeia):
    with open(ARQUIVO_TABELA_SIMBOLOS,'r') as arquivo:
        itens_tabela = [item.split() for item in arquivo.readlines()]

    for identificador in itens_tabela:
        if(identificador[0] == cadeia):
            return True
    return False

def inserirTabela(buffer, tipo):
    with open(ARQUIVO_TABELA_SIMBOLOS,'a') as arquivo:
        for item in buffer_tabela:
            if(contemTabela(item[0])):
                raise RuntimeError('Nome de variável já utilizado, um nome de variável não pode ser instânciado mais de uma vez.')
            else:
                with open(ARQUIVO_TABELA_SIMBOLOS,'a') as arquivo:
                    for valor in item:
                        arquivo.write(valor + ' ')
                    arquivo.write(tipo + '\n')

    del buffer_tabela[:]

def buscarTabela(cadeia):
    with open(ARQUIVO_TABELA_SIMBOLOS,'r') as arquivo:
        itens_tabela = [identificador.split() for identificador in arquivo.readlines()]

    for identificador in itens_tabela:
        if(identificador[0] == cadeia):
            return identificador

    error = 'Variável "' + cadeia + '" não declarada'
    raise NameError(error)

def verificarTipo():
    empilhaId(getTokenAtualInfo().split()[1])
    if(getTipoResultante() == ''):
        id = getTokenAtualInfo().split()[1]
        tipo = buscarTabela(id)[3]
        setTipoResultante(tipo)
    else:
        id = getTokenAtualInfo().split()[1]
        tipo = buscarTabela(id)[3]
        if(tipo != tipo_resultante):
            erro = 'Tipo da variável ' + str(getTokenAtualInfo().split()[1]) + ' incompatível na' +' linha ' + str(getTokenAtualInfo().split()[2]) + ', coluna ' + str(getTokenAtualInfo().split()[3])
            raise TypeError(erro)


def getTokenAtual():
    global pos
    # print(token_stream[pos])
    return token_stream[pos].split()[0]

def getTokenAtualInfo():
    global pos
    return token_stream[pos]

def setTipoResultante(tipo):
    global tipo_resultante
    tipo_resultante = tipo

def getTipoResultante():
    global tipo_resultante
    return tipo_resultante

def empilhaId(id):
    global pilha_id
    pilha_id.append(id)

def desempilhaId():
    global pilha_id
    del pilha_id[len(pilha_id)-1]

def Z():
    # print('ENTROU Z')
    global pos
    if(I()):
        if(S()):
            return True
        else:
            return False
    else:
        return False

def I():
    # print('ENTROU I')
    global pos
    if(getTokenAtual() == 'var'):
        pos += 1
        if(D()):

            return True
        else:
            return False
    else:
        return False

def D():
    # print('ENTROU D')
    global pos
    if(L()):
        if(getTokenAtual() == ':'):
            pos += 1
            if(K()):
                if(O()):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

def L():
    # print('ENTROU L')
    global pos
    if(getTokenAtual() == 'id'):
        buffer_tabela.append([getTokenAtualInfo().split()[1], 'id', 'var'])
        pos += 1
        if(X()):
            return True
        else:
            return False
    else:
        return False

def X():
    # print('ENTROU X')
    global pos
    if(getTokenAtual() == ','):
        pos += 1
        if(L()):
            return True
        else:
            return False
    elif(getTokenAtual() == ':'):
        return True
    else:
        return False

def K():
    # print('ENTROU K')
    global pos
    if(getTokenAtual() == 'integer'):
        # print('BUFFER:')
        # print(buffer_tabela)
        pos += 1
        inserirTabela(buffer_tabela, 'integer')
        return True

    elif(getTokenAtual() == 'real'):
        # print('BUFFER:')
        # print(buffer_tabela)
        inserirTabela(buffer_tabela, 'real')
        pos += 1
        return True

    else:
        return False

def O():
    # print('ENTROU O')
    global pos
    if(getTokenAtual() == ';'):
        pos += 1
        if(D()):
            return True
        else:
            return False
    elif(getTokenAtual() == 'id'):
        verificarTipo()
        return True

    elif(getTokenAtual() == 'if'):
        setTipoResultante('integer')
        return True
    else:
        return False

def S():
    # print('ENTROU S')
    global pos
    if(getTokenAtual() == 'id'):

        verificarTipo()
        pos += 1
        if(getTokenAtual() == ':='):
            pos += 1
            if(E()):
                return True
            else:
                return False
        else:
            return False
    elif(getTokenAtual() == 'if'):
        pos += 1
        setTipoResultante('integer')
        if(E()):
            if(getTokenAtual() == 'then'):
                setTipoResultante('')
                pos += 1
                if(S()):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

def E():
    # print('ENTROU E')
    global pos
    if(T()):
        if(R()):
            return True
        else:
            return False
    else:
        return False

def R():
    # print('ENTROU R')
    global pos
    if(getTokenAtual() == '+'):
        pos += 1
        if(T()):
            if(R()):
                return True
            else:
                return False
        else:
            return False
    elif(getTokenAtual() == 'then'):
        return True
    elif(getTokenAtual() == 'fim'):
        return True
    else:
        return False

def T():
    # print('ENTROU T')
    global pos
    if(getTokenAtual() == 'id'):
        verificarTipo()
        pos += 1
        return True
    else:
        return False



pilha_id = []
tipo_resultante = ''

token_stream = []
pos = 0
buffer_tabela = []


with open(ARQUIVO_TABELA_SIMBOLOS,'w') as arquivo:
    with open(ARQUIVO_SAIDA, 'r') as arquivo:
        token_stream = [token.strip() for token in arquivo.readlines()]

if(Z()):
    # print('Análise sintática e verificação de tipos concluída sem erros.')
    pass
else:
    erro = '"' + getTokenAtual() + '" caracter inválido na linha ' + str(getTokenAtualInfo().split()[2]) + ', coluna ' + str(getTokenAtualInfo().split()[3])
    # print(erro)
    raise SyntaxError(erro)
