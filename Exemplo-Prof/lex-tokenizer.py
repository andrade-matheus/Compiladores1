#!/usr/bin/python3      # indica ao script onde está o interpretador Python no ambiente Linux
# -*- coding: utf-8 -*-    # permite colocar caracteres acentuados nestes programas/scripts

#tokenizando um arquivo contendo o código fonte da linguagem a ser compilada


import nltk

fd = open('arqFonte','r')
stream = fd.read()

# utilizando tokenizador já pronto da biblioteca nltk
tokenizer = nltk.WordPunctTokenizer()
termList = tokenizer.tokenize(stream)
print (" ============== \n Lista de Tokens com WordPunctTokenizer \n =================")
for w in termList:
		print(w.lower())


# utilizando tokenizador Regexp customizado

ident = '\w+'
pont = '\(|\)|\{|\;|\}'

reg = ident + '|' + pont

tokenizer = nltk.RegexpTokenizer(reg)
termList = tokenizer.tokenize(stream)
print (" ============== \n Lista de Tokens com RegexpTokenizer \n =================")
for w in termList:
		print(w.lower())


fd.close
