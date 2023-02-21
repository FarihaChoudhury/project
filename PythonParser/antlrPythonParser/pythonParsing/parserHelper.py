from io import StringIO
from antlr4 import *
import sys
sys.path.insert(0, '../antlrParserGeneratedCode')
from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser
# sys.path.insert(0, '../antlrParserGeneratedCode')
# from Python3Lexer import Python3Lexer
# from Python3Parser import Python3Parser

import numpy as np
import re


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
def parseDataSingleInput(data):
    # Add \n for end of file - antlr requires 
    input_stream = InputStream(f'{data}\n')
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

    # for generic white space: 
    # def count_whitespaces(text):
    #     return len(re.findall(r"\s", text))


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


""" Counts empty lines of code from input text and total lines of code """
def countEmptyLinesOfInput(inputData):
    print("need to fix")
    totalLines = 1
    emptyLines = 0
    if not inputData.strip():
        # cannot strip if empty => increments count 
        emptyLines = 1
    return totalLines, emptyLines


    # with open(inputData, 'r') as file:
    #     totalLines = 0
    #     emptyLines = 0
    #     for line in file:
    #         totalLines += 1
    #         if not line.strip():
    #             emptyLines += 1
    # # countTotalLines(filename)  
    # return totalLines, emptyLines

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



"""inaccurate as it considers line by line - mid block comment lines not accounted for..."""
def countCommentsOnInputLine(line):
    strippedLine = line.strip()
    commentLinesCount = 0
    # single # comments 
    if strippedLine.startswith("#"):
        commentLinesCount += 1
        print("startswith hash: ")
        print(strippedLine)
        print("\n")

    # triple """ or '''
    elif strippedLine.startswith('"""') or strippedLine.endswith('"""'):
        commentLinesCount += 1
        print("startswith triple '' or ends with it: ")
        print(strippedLine)
        print("\n")
    elif strippedLine.startswith("'''") or strippedLine.endswith("'''"):
        commentLinesCount += 1
        print("startswith triple ' or ends with it: ")
        print(strippedLine)
        print("\n")
  
    # single " or ' 
    elif strippedLine.startswith('"') or strippedLine.endswith('"'):
        commentLinesCount += 1
        print("startswith single '' or ends with it: ")
        print(strippedLine)
        print("\n")
    elif strippedLine.startswith("'") or strippedLine.endswith("'"):
        commentLinesCount += 1
        print("startswith single ' or ends with it: ")
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
    - performs classifications and prints to terminal
    - returns these """
def performClassificationOnInput(inputData):
    strippedData = inputData.strip()
    # to be in antlr form:
    # data = f'{strippedData}\n'

    #PARSE TREE GENERATOR:
    tree, parser = parseDataSingleInput(strippedData)
    print(tree.toStringTree(recog=parser))
    print("\n")

     #WHITE SPACE COUNTERS: 
    spaces, newLines = countWhitespaces(inputData)
    # totalLines, emptyLines = countEmptyLines('testFile.py')
    totalLines, emptyLines = countEmptyLinesOfInput(inputData)   # NEED TO FIX!!!
    print("Spaces:", spaces)
    print("Newlines:", newLines)
    print("Empty Lines:", emptyLines)
    print("Total lines:", totalLines)

    #COMMENTS COUNTER:
    comments = countCommentsOnInputLine(inputData)
    # comments = count_comments('testFile.py')
    print("Comment Lines", comments)

    return spaces, newLines, emptyLines, totalLines, comments



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



# if __name__ == '__main__':
#     main()

if __name__ == '__main__':
    # allows you to call openJsonFile() from terminal 
    globals()[sys.argv[1]]()
    # RUN: python3 parserHelper.py openJsonFile 



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