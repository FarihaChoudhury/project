from io import StringIO
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



# """Counts total number of lines of code """
# def countTotalLines(filename):
#     with open(filename, 'r') as file:
#         count = 0
#         for line in file:
#             count += 1
#     print(count)
#     return count 




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
                print("startswith hash: ")
                print(strippedLine)
                print("\n")

            #checks for middle and end of block comment lines
            elif inBlockComment:
                commentLinesCount += 1
                print('part of block/end:')
                print(strippedLine)

                if blockCommentStart == "'''" or strippedLine.endswith("'''"):
                    inBlockComment = False

                elif blockCommentStart == '"""' or strippedLine.endswith('"""'):
                    inBlockComment = False
                print("\n")

            # """
            elif strippedLine.startswith('"""'):
                if strippedLine!='"""':
                  if strippedLine.endswith('"""'):
                    inBlockComment = False
                    # block_comment_start = ' """ '
                    commentLinesCount += 1
                    print("startswith triple'': ")
                    print(strippedLine)
                    print("\n")
                  else: 
                      inBlockComment = True
                      # needs to look for end in next lines
                      blockCommentStart = ' """ '
                      commentLinesCount += 1
                      print("startswith triple'': ")
                      print(strippedLine)
                      print("\n")
                elif strippedLine=='"""':
                    inBlockComment = True
                    # needs to look for end in next lines
                    blockCommentStart = ' """ '
                    commentLinesCount += 1
                    print("startswith triple'': ")
                    print(strippedLine)
                    print("\n")
            
            # '''
            elif strippedLine.startswith("'''"):
                if strippedLine!="'''":
                  if strippedLine.endswith("'''"):
                    inBlockComment = False
                    commentLinesCount += 1
                    print("startswith triple' ' ' : ")
                    print(strippedLine)
                    print("\n")
                  else: 
                      inBlockComment = True
                      # needs to look for end in next lines
                      blockCommentStart = "'''"
                      commentLinesCount += 1
                      print("startswith triple' ' ': ")
                      print(strippedLine)
                      print("\n")
                elif strippedLine=="'''":
                    inBlockComment = True
                    # needs to look for end in next lines
                    blockCommentStart = "'''"
                    commentLinesCount += 1
                    print("startswith triple' ' ' : ")
                    print(strippedLine)
                    print("\n")         

            # " comment line 
            elif strippedLine.startswith('"'):
                commentLinesCount += 1
                print("startswith double'': ")
                print(strippedLine)
                print("\n")

            # ' beginning comment line 
            elif strippedLine.startswith("'") and strippedLine !="'":
                commentLinesCount += 1
                print("startswith single': ")
                print(strippedLine)
                print("\n")

            #midline comments starting with # - not 100% accurate 
            elif "#" in strippedLine:
                commentLinesCount += 1
                print("mid hash:")
                print(strippedLine)
                print("\n")
        
        return commentLinesCount


"""Performs classification on the python code inputted
    - takes input in terms of code text, not a file
    - passes code into parser 
    - performs classifications and prints to terminal"""
def performClassification(inputData):
    strippedData = inputData.strip()
    data = f'{strippedData}\n'

    #PARSE TREE GENERATOR:
    tree, parser = parseDataFileInput(data)
    print(tree.toStringTree(recog=parser))
    print("\n")

     #WHITE SPACE COUNTERS: 
    spaces, newlines = countWhitespaces(inputData)
    totalLines, emptyLines = countEmptyLines('testFile.py')
    print("Spaces:", spaces)
    print("Newlines:", newlines)
    print("Empty Lines:", emptyLines)
    print("Total lines:", totalLines)

    #COMMENTS COUNTER:
    comments = count_comments('testFile.py')
    print("Comment Lines", comments)



def main():
    realData = openFile('testFile.py')
    strippedData = realData.strip()
    data = f'{strippedData}\n'

    #PARSE TREE GENERATOR:
    tree, parser = parseDataFileInput(data)
    print(tree.toStringTree(recog=parser))
    print("\n")

   
    #WHITE SPACE COUNTERS: 
    spaces, newlines = countWhitespaces(realData)
    totalLines, emptyLines = countEmptyLines('testFile.py')
    print("Spaces:", spaces)
    print("Newlines:", newlines)
    print("Empty Lines:", emptyLines)
    print("Total lines:", totalLines)

    #COMMENTS COUNTER:
    comments = count_comments('testFile.py')
    print("Comment Lines", comments)



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