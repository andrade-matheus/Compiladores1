#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import os

#CONSTANTES:
ARQUIVO_FONTE = 'Arquivo-Fonte.txt'
ARQUIVO_SAIDA_LEXICO = 'Arquivo-Saida-lexico.txt'
ARQUIVO_TABELA_SIMBOLOS = 'Arquivo-Tabela-Simbolos.txt'
ARQUIVO_CODIGO_INTERMEDIARIO = 'Arquivo-Codigo-Intermediario.txt'

ARQUIVO_FONTE_EM_TESTE = ARQUIVO_FONTE

try:
    print('Iniciando análise Léxica\n...')
    subprocess.check_call(['python', 'analisadorLexico.py', ARQUIVO_FONTE_EM_TESTE,  ARQUIVO_SAIDA_LEXICO])
    print('Análise léxica foi conclída.\n')

    print('Iniciando análise Sintática e Verificação de tipos\n...')
    subprocess.check_call(['python', 'analisadorSintatico-Semantico-CodigoIntermediario.py' , ARQUIVO_FONTE_EM_TESTE,  ARQUIVO_SAIDA_LEXICO])
    print('Análise sintática foi conclída.')
    print('Análise de tipagem foi conclída.\n')
    print('Código intermediário gerado.\n')

    print('\n')
    print('Código Fonte: (' + ARQUIVO_FONTE_EM_TESTE +')')
    subprocess.call(['cat', ARQUIVO_FONTE_EM_TESTE])

    print('\n')
    print('Lista de Tokens: (' + ARQUIVO_SAIDA_LEXICO +')')
    subprocess.call(['cat', ARQUIVO_SAIDA_LEXICO])

    print('\n')
    print('Tabela de Símbolos: (' + ARQUIVO_TABELA_SIMBOLOS +')')
    subprocess.call(['cat', ARQUIVO_TABELA_SIMBOLOS])

    print('\n')
    print('Código intermediário: (' + ARQUIVO_CODIGO_INTERMEDIARIO +')')
    subprocess.call(['cat', ARQUIVO_CODIGO_INTERMEDIARIO])

except subprocess.CalledProcessError as error:
    print(error)
    exit()
