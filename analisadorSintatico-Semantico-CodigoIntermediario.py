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
    global pos
    with open(ARQUIVO_TABELA_SIMBOLOS,'a') as arquivo:
        for item in buffer_tabela:
            if(contemTabela(item[0])):
                pos -= 2
                error = 'Nome de variável "' + getValorAtual() + '" já utilizado, um nome de variável não pode ser instânciado mais de uma vez.'
                raise NameError(error)
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

    #print(cadeia)
    error = 'Variável "' + cadeia + '" não declarada'
    raise NameError(error)

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
    buffer_tabela.append([cadeia, 'id', 'var', tipo])
    inserirTabela(buffer_tabela, tipo)
    return cadeia

def verificarTipo():
    if(getTipoResultante() == ''):
        valor = getValorAtual()
        tipo = buscarTabela(valor)[3]
        setTipoResultante(tipo)
    else:
        valor = getValorAtual()
        # print( 'VALOR: ' + valor)
        tipo = buscarTabela(valor)[3]
        # print('TIPO: ' + tipo)
        if(tipo != tipo_resultante):
            erro = 'Tipo da variável ' + str(getTokenAtualInfo().split()[1]) + ' incompatível na' +' linha ' + str(getTokenAtualInfo().split()[2]) + ', coluna ' + str(getTokenAtualInfo().split()[3])
            raise TypeError(erro)


def getTokenAtual():
    global pos
    # print(token_stream[pos])
    return token_stream[pos].split()[0]

def getValorAtual():
    global pos
    return token_stream[pos].split()[1]

def getTokenAtualInfo():
    global pos
    return token_stream[pos]

def setTipoResultante(tipo):
    global tipo_resultante
    tipo_resultante = tipo

def getTipoResultante():
    global tipo_resultante
    return tipo_resultante

def empilha(pilha, id):
    pilha.append(id)

def pop(pilha):
    if(pilha):
        valor_top = pilha[len(pilha)-1]
        del pilha[len(pilha)-1]
        return valor_top
    else:
        return ''

def peek(pilha):
    if(pilha):
        return pilha[len(pilha)-1]
    else:
        return ''

def gerarCodigo():
    while(pilha_id):
        if(peek(pilha_op) == '+'):
            id_dir = pop(pilha_id)
            id_esq = pop(pilha_id)
            operador = pop(pilha_op)

            id = buscarTabela(id_dir)   #Buscar id na tabela para pegar tipo
            temp = geraTemp(id[3])      #Pega tipo da variavel
            buffer_quad.append([operador, id_esq, id_dir, temp])
            empilha(pilha_id, temp)

            if(getTokenAtual() == 'then'):
                aux_id = pop(pilha_id)
                buffer_quad.append(['JF', aux_id, '','-'])
        elif(getTokenAtual() == 'then'):
            aux_id = pop(pilha_id)
            buffer_quad.append(['JF', aux_id, '','-'])
        else:
            id_dir = pop(pilha_id)
            id_esq = pop(pilha_id)
            operador = pop(pilha_op)
            buffer_quad.append([operador, id_esq, id_dir, '-'])

def lancarErro(caracterEsperado):
    global pos
    if(getTokenAtual() != 'var'):
        pos -= 1

    erro = '"' + getValorAtual() + '" caracter inválido na linha ' + str(getTokenAtualInfo().split()[2]) + ', era esperado "' + caracterEsperado + '" , coluna ' + str(getTokenAtualInfo().split()[3])
    raise SyntaxError(erro)

def Z():
    #print('ENTROU Z')
    global pos
    if(I()):
        if(S()):
            return True
        else:
            return False
    else:
        return False

def I():
    #print('ENTROU I')
    global pos
    if(getTokenAtual() == 'var'):
        pos += 1
        if(D()):

            return True
        else:
            return False
    else:
        lancarErro('var')

def D():
    #print('ENTROU D')
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
            lancarErro(':')
    else:
        return False

def L():
    #print('ENTROU L')
    global pos
    if(getTokenAtual() == 'id'):
        buffer_tabela.append([getTokenAtualInfo().split()[1], 'id', 'var'])
        pos += 1
        if(X()):
            return True
        else:
            return False
    else:
        lancarErro('id')

def X():
    #print('ENTROU X')
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
        lancarErro(', | :')

def K():
    #print('ENTROU K')
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
        lancarErro('integer | real')

def O():
    #print('ENTROU O')
    global pos
    if(getTokenAtual() == ';'):
        pos += 1
        if(D()):
            return True
        else:
            return False
    elif(getTokenAtual() == 'id'):
        return True

    elif(getTokenAtual() == 'if'):
        return True
    else:
        lancarErro('; | id | if')

def S():
    #print('ENTROU S')
    global pos
    if(getTokenAtual() == 'id'):
        empilha(pilha_id, getValorAtual())
        verificarTipo()
        pos += 1
        if(getTokenAtual() == ':='):
            empilha(pilha_op, getValorAtual())
            pos += 1
            if(E()):
                return True
            else:
                return False
        else:
            lancarErro(':=')
    elif(getTokenAtual() == 'if'):
        pos += 1
        setTipoResultante('integer')
        if(E()):
            if(getTokenAtual() == 'then'):
                gerarCodigo()
                setTipoResultante('')
                pos += 1
                if(S()):
                    return True
                else:
                    return False
            else:
                lancarErro('then')
        else:
            return False
    else:
        lancarErro('id | if')

def E():
    #print('ENTROU E')
    global pos
    if(T()):
        if(R()):
            return True
        else:
            return False
    else:
        return False

def R():
    #print('ENTROU R')
    global pos
    if(getTokenAtual() == '+'):
        empilha(pilha_op, getValorAtual())
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
        lancarErro('+ | then')

def T():
    #print('ENTROU T')
    global pos
    if(getTokenAtual() == 'id'):
        empilha(pilha_id, getValorAtual())
        verificarTipo()
        pos += 1
        return True
    else:
        lancarErro('id')


token_stream = []
pos = 0
buffer_tabela = []
buffer_quad = []
pilha_id = []
pilha_op = []
tipo_resultante = ''

with open(ARQUIVO_TABELA_SIMBOLOS,'w') as arquivo:
    with open(ARQUIVO_SAIDA, 'r') as arquivo:
        token_stream = [token.strip() for token in arquivo.readlines()]

if(Z()):
    gerarCodigo()
    ultima_linha = len(buffer_quad) + 1
    cont_linha = 1
    with open(ARQUIVO_CODIGO_INTERMEDIARIO, 'w') as arquivo:
        for item in buffer_quad:
            if(item[0] == 'JF'):
                item[2] = str(ultima_linha)

            arquivo.write(str(cont_linha) + ': [' + item[0] + ' ' + item[1] + ' ' + item[2] + ' ' + item[3] + ']\n')
            cont_linha += 1

        arquivo.write(str(cont_linha) + ': [...]\n')
