from antlr4 import *
from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser
import sys
import testFile
import numpy as np


def main():
    with open('testingText.txt') as file:
        # data = file.read()
        data = f'{file.read()}\n'

    input_stream = InputStream(data)
    lexer = Python3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    tree = parser.single_input()
    print(tree.toStringTree(recog=parser))

if __name__ == '__main__':
    main()

# HOW TO RUN:
# Go to project folder (outside antlr folder) 
# run: python3 main.py  :))) be happy im proud of you 


# def main():

#     # input_stream = InputStream('print("hello world")\n')
#     # print(testFile)

#     # filename = 'testingText.txt'
#     # data = np.loadtxt(filename, delimiter=',', dtype=str)
#     # print(data)

#     with open('testingText.txt') as file:
#         data = file.read()

#     # print(data)