from io import StringIO
from antlr4 import *
import sys

from pythonParse import countWhitespaces
sys.path.insert(0, '../antlrParserGeneratedCode')
from Python3ParserListener import Python3ParserListener
from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser
import numpy as np
import re

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

""" Counts empty lines of code of a file and total lines of code """
def countEmptyLinesOfFile(filename):
    with open(filename, 'r') as file:
        totalLines = 0
        emptyLines = 0
        for line in file:
            totalLines += 1
            if not line.strip():
                emptyLines += 1
    # countTotalLines(filename)  
    return totalLines, emptyLines

# """Counts the number of lines of comments in a python .py file
#     - includes: #,' ', " ", """ """ block comments, ''' ''' block comments, 
#     - Also inline #comments which may be inaccurate """
def count_comments(filename):
    commentLinesCount = 0
    inBlockComment = False
    blockCommentStart = None
    with open(filename, "r") as file:
        lines = file.readlines()

        for line in lines:
            strippedLine = line.strip() # removes starting and trailing spaces 
            # checks for # comments 
            if strippedLine.startswith("#"):
                commentLinesCount += 1
            #checks for middle and end of block comment lines
            elif inBlockComment:
                commentLinesCount += 1
                if blockCommentStart == "'''" or strippedLine.endswith("'''"):
                    inBlockComment = False
                elif blockCommentStart == '"""' or strippedLine.endswith('"""'):
                    inBlockComment = False
            # """
            elif strippedLine.startswith('"""'):
                if strippedLine!='"""':
                  if strippedLine.endswith('"""'):
                    inBlockComment = False
                    # block_comment_start = ' """ '
                    commentLinesCount += 1
                  else: 
                      inBlockComment = True
                      # needs to look for end in next lines
                      blockCommentStart = ' """ '
                      commentLinesCount += 1
                elif strippedLine=='"""':
                    inBlockComment = True
                    # needs to look for end in next lines
                    blockCommentStart = ' """ '
                    commentLinesCount += 1
            # '''
            elif strippedLine.startswith("'''"):
                if strippedLine!="'''":
                  if strippedLine.endswith("'''"):
                    inBlockComment = False
                    commentLinesCount += 1
                  else: 
                      inBlockComment = True
                      # needs to look for end in next lines
                      blockCommentStart = "'''"
                      commentLinesCount += 1
                elif strippedLine=="'''":
                    inBlockComment = True
                    # needs to look for end in next lines
                    blockCommentStart = "'''"
                    commentLinesCount += 1
            # " comment line 
            elif strippedLine.startswith('"'):
                commentLinesCount += 1
            # ' beginning comment line 
            elif strippedLine.startswith("'") and strippedLine !="'":
                commentLinesCount += 1
            #midline comments starting with # - not 100% accurate 
            elif "#" in strippedLine:
                commentLinesCount += 1
        return commentLinesCount


# def main():
# def performClassificationOnFile(filename):
def performClassificationOnFile():
    # realData = openFile(filename)
    realData = openFile('testFile.py')
    strippedData = realData.strip()
    data = f'{strippedData}\n'

    #PARSE TREE GENERATOR:
    tree, parser = parseDataFileInput(data)
    print(tree.toStringTree(recog=parser))
    print("\n")

   
    #WHITE SPACE COUNTERS: 
    spaces, newlines = countWhitespaces(realData)
    totalLines, emptyLines = countEmptyLinesOfFile('testFile.py')   # TAKES FILE!!!
    # totalLines, emptyLines = countEmptyLinesOfFile(filename) 
    print("Spaces:", spaces)
    print("Newlines:", newlines)
    print("Empty Lines:", emptyLines)
    print("Total lines:", totalLines)

    #COMMENTS COUNTER:
    comments = count_comments('testFile.py')
    print("Comment Lines", comments)



def testFarse(data):
    strippedData = data.strip()
    # Add \n for end of file - antlr requires 
    input_stream = InputStream(f'{strippedData}')
    lexer = Python3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    tree = parser.single_input()  #May print error message to terminal - this is handled by ANTLR and can be ignored
    # print(tree.toStringTree(recog=parser))
    # print("\n")
    # ree, parser = parseDataFileInput(data)
    print(tree.toStringTree(recog=parser))
    print("\n")
    return tree, parser

def test():
    list = ["def printHelloWorld():",'x = "Hello world"', "print(x)"]
    print(list)
    for i in range(len(list)):
        print(list[i])
        testFarse(list[i])

    #  def printHelloWorld():
    #                 x = "Hello world"
    #                 print(x)}     

if __name__ == '__main__':
    globals()[sys.argv[1]]()