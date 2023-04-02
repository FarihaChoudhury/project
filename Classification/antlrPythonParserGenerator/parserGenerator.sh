#!/usr/bin/env bash
wget https://raw.githubusercontent.com/antlr/grammars-v4/master/python/python3/Python3Lexer.g4
wget https://raw.githubusercontent.com/antlr/grammars-v4/master/python/python3/Python3Parser.g4
wget https://raw.githubusercontent.com/antlr/grammars-v4/master/python/python3/Python3/transformGrammar.py
wget https://raw.githubusercontent.com/antlr/grammars-v4/master/python/python3/Python3/Python3LexerBase.py 
wget https://raw.githubusercontent.com/antlr/grammars-v4/master/python/python3/Python3/Python3ParserBase.py
wget https://www.antlr.org/download/antlr-4.11.1-complete.jar

python3 transformGrammar.py

pip install antlr4-python3-runtime

java -jar antlr-4.11.1-complete.jar *.g4 -Dlanguage=Python3

