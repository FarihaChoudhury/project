from antlr4 import *
from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser
import sys
import numpy as np
import re

# for generic white space: 
# def count_whitespaces(text):
#     return len(re.findall(r"\s", text))


# """ Opens file and returns its contents"""
# def openFile(filename):
#     with open(filename, 'r') as file:
#         realData = file.read()
#     return realData


""" Opens file and returns its contents"""
def openFile(filename):
    with open(filename, 'r') as file:
        # realData = file.read()
        realData = readFile(file)
        # print(realData)
        return realData

""" Reads file and returns its contents"""
def readFile(file):
    realData = file.read()
    return realData


""" Parsing: using the ANTLR parser 
    - generates parse tree for inputted data 
    - returns parse tree and parser """
def parseData(data):
    input_stream = InputStream(data)
    lexer = Python3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    # tree = parser.single_input()
    tree = parser.file_input()
    return tree, parser
    # print(tree.toStringTree(recog=parser))
    # print("\n")


""" Counts white space of a file:
    - counts the number of spaces/ empty strings - this includes tab and empty lines
    - counts the number of new lines 
    - returns the number of spaces and newlines"""
def countWhitespaces(text):
    spaces = len(re.findall(r" ", text))
    # tabs = len(re.findall(r"\t", text))
    newlines = len(re.findall(r"\n", text))
    return spaces, newlines



""" Counts empty lines of code and total lines of code """
def countEmptyLines(filename):
    with open(filename, 'r') as file:
        totalLines = 0
        emptyLines = 0
        for line in file:
            totalLines += 1
            if not line.strip():
                emptyLines += 1
    # countTotalLines(filename)  
    return totalLines, emptyLines



# """Counts total number of lines of code """
# def countTotalLines(filename):
#     with open(filename, 'r') as file:
#         count = 0
#         for line in file:
#             count += 1
#     print(count)
#     return count 
    



def main():
    realData = openFile('testFile.py')
    strippedData = realData.strip()
    data = f'{strippedData}\n'

    #PARSE TREE GENERATOR:
    tree, parser = parseData(data)
    print(tree.toStringTree(recog=parser))
    print("\n")

   
    #WHITE SPACE COUNTERS: 
    spaces, newlines = countWhitespaces(realData)
    totalLines, emptyLines = countEmptyLines('testFile.py')
    print("Spaces:", spaces)
    print("Newlines:", newlines)
    print("Empty Lines:", emptyLines)
    print("Total lines:", totalLines)


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