from antlr4 import *
import sys
sys.path.insert(0, '../antlrParser')
from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser

# import testFile
import numpy as np
import re

# for generic white space: 
# def count_whitespaces(text):
#     return len(re.findall(r"\s", text))

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
    - generates parse tree for file inputted data 
    - returns parse tree and parser """
def parseDataFileInput(data):
    input_stream = InputStream(data)
    lexer = Python3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    # tree = parser.single_input()
    tree = parser.file_input()
    return tree, parser
    # print(tree.toStringTree(recog=parser))
    # print("\n")

""" Parsing: using the ANTLR parser 
    - generates parse tree for single inputted data 
    - returns parse tree and parser """
def parseDataFileInput(data):
    input_stream = InputStream(data)
    lexer = Python3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    # tree = parser.single_input()
    tree = parser.single_input()
    return tree, parser
    # print(tree.toStringTree(recog=parser))
    # print("\n")

""" Counts white space of a file:
    - counts the number of spaces/ empty strings - this includes tab and empty lines
    - counts the number of new lines 
    - returns the number of spaces and newlines"""
def countWhitespaces(data):
    spaces = len(re.findall(r" ", data))
    # tabs = len(re.findall(r"\t", text))
    newlines = len(re.findall(r"\n", data))
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


"""Counts the number of lines of comments in a python .py file
    - includes: #,' ', " ", """ """ block comments, ''' ''' block comments, 
    - Also inline #comments which may be inaccurate """
def count_comments(filename):
    commentLinesCount = 0
    partOfBlockComment = False
    with open(filename, "r") as file:
        fileContent = file.readlines()
       
        for line in fileContent:
            # removes starting and trailing spaces 
            strippedLine = line.strip()

            # checks for # comments 
            if strippedLine.startswith("#"):
                commentLinesCount += 1
                # print(strippedLine)

            #checks for middle of block comment lines
            elif partOfBlockComment:
                commentLinesCount += 1

                if strippedLine.endswith("'''"):
                    partOfBlockComment = False
                elif strippedLine.endswith('"""'):
                    partOfBlockComment = False      # checks if comment blocks have ended 
            
             # checks for """" beginning comment line
            elif strippedLine.startswith('"""'):
                partOfBlockComment = True
                commentLinesCount += 1

            # checks for ''' beginning comment line
            elif strippedLine.startswith("'''"):
                partOfBlockComment = True
                print(partOfBlockComment)
                commentLinesCount += 1

            # checks for " beginning comment line 
            elif strippedLine.startswith('"'):
                commentLinesCount += 1

            # checks for ' beginning comment line 
            elif strippedLine.startswith("'"):
                commentLinesCount += 1

            #checks for midline comments starting with # - not 100% accurate 
            elif "#" in strippedLine:
                commentLinesCount += 1
    
    return commentLinesCount
    

def main():
    #PARSE TREE GENERATOR:
    # with open('testingText.txt') as file:
    with open("testFile.py") as file:
        realData = file.read()
        # print(realData)
        # need to strip: remove start and trailing "" for parser to work:
        strippedData = realData.strip()
        # print(strippedData)
        data = f'{strippedData}\n'

    # using the stripped data - to parse: 
    input_stream = InputStream(data)
    lexer = Python3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    # tree = parser.single_input()
    tree = parser.file_input()
    print(tree.toStringTree(recog=parser))
    print("\n")

    # count white space:  use real data- where start and trailing spaces have not been stripped:
    #WHITE SPACE COUNTERS: 
    spaces, newlines = countWhitespaces(realData)
    totalLines, emptyLines = countEmptyLines('testFile.py')
    print("Spaces:", spaces)
    print("Newlines:", newlines)
    print("Empty Lines:", emptyLines)
    print("Total lines:", totalLines)

    #COMMENTS COUNTER:
    comments = count_comments('testFile.py')
    print("comments", comments)



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