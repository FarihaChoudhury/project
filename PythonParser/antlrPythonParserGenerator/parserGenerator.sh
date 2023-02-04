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

cat << EOF > main.py
from antlr4 import *
from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser

def main():
    input_stream = InputStream('print("hello world")\n')
    lexer = Python3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    tree = parser.single_input()
    print(tree.toStringTree(recog=parser))

if __name__ == '__main__':
    main()
EOF

python3 --version

python3 main.py


