from io import StringIO
from antlr4 import *
import sys
sys.path.insert(0, '../antlrParserGeneratedCode')
from Python3ParserListener import Python3ParserListener
from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser
import numpy as np
import re
"""Helper functions for python code parsing"""

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
    strippedData = data.strip()
    # Add \n for end of file - antlr requires 
    input_stream = InputStream(f'{strippedData}\n')
    lexer = Python3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    # tree = parser.single_input()
    tree = parser.single_input()
    # pythonListener = Python3ParserListener()
    # walker = ParseTreeWalker()
    # walker.walk(pythonListener, walker)
    # ParseTreeWalker.DEFAULT.walk()
    return tree, parser
    # print(tree.toStringTree(recog=parser))
    # print("\n")


""" Counts white space of a file:
    - counts the number of spaces/ empty strings - this includes tab and empty lines
    - counts the number of new lines 
    - returns the number of spaces and newlines"""
def countWhitespaces(data):
    spaces = len(re.findall(r" ", data))
    return spaces

def countNewLines(data):
    # tabs = len(re.findall(r"\t", text))
    newlines = len(re.findall(r"\n", data))
    return newlines

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
    # print("need to fix")
    totalLines = 1
    emptyLines = 0
    if not inputData.strip():
        # cannot strip if empty => increments count 
        emptyLines = 1
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

    # triple """ or '''
    elif strippedLine.startswith('"""') or strippedLine.endswith('"""'):
        commentLinesCount += 1
    elif strippedLine.startswith("'''") or strippedLine.endswith("'''"):
        commentLinesCount += 1

    # single " or ' 
    elif strippedLine.startswith('"') or strippedLine.endswith('"'):
        commentLinesCount += 1
    elif strippedLine.startswith("'") or strippedLine.endswith("'"):
        commentLinesCount += 1

     #midline comments starting with # - not 100% accurate 
    elif "#" in strippedLine:
        commentLinesCount += 1

    return commentLinesCount


# def countCommentsOnLineRegex(line):
#     strippedLine = line.strip()
#     commentLinesCount = 0



"""Performs classification on the python code inputted
    - takes input in terms of code text, not a file
    - passes code into parser 
    - performs classifications and prints to terminal
    - returns these """
def performClassificationOnPythonInput(inputData):
    # to be in antlr form: need to strip -- and include new line-- but done in parseDataSingleInput
        # strippedData = inputData.strip()
        # data = f'{strippedData}\n'

    #PARSE TREE GENERATOR:
    tree, parser = parseDataSingleInput(inputData)
    result = tree.toStringTree(recog=parser)
    print(result)
    # print("\n")

    #WHITE SPACE COUNTERS: 
    spaces = countWhitespaces(inputData)
    spacesWithoutIndent = countWhitespaces(inputData.strip())
    newLines = countNewLines(inputData)
    # totalLines, emptyLines = countEmptyLines('testFile.py')
    totalLines, emptyLines = countEmptyLinesOfInput(inputData)

    print("Spaces:", spaces)
    print("Spaces without indents:", spacesWithoutIndent)
    print("Newlines:", newLines)
    print("Empty Lines:", emptyLines)
    print("Total lines:", totalLines)

    #COMMENTS COUNTER:
    comments = countCommentsOnInputLine(inputData)
    # comments = count_comments('testFile.py')
    print("Comment Lines", comments)

    printStatementCount, loopCount, conditionCount, importCount, funcCount, classCount = analyseCodeTypes(result)
    print("Prints:", printStatementCount)
    print("Loops:", loopCount)
    print("Conditions:", conditionCount)
    print("Imports:", importCount)
    print("Functions:", funcCount)
    print("ClassDefs:", classCount)   


    return spaces, spacesWithoutIndent, newLines, emptyLines, totalLines, comments



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




# def findPrint(parsedItem):
#     printStatementcount = 0
#     loopCount = 0 
#     conditionsCount = 0
#     importCount = 0
#     funcCount = 0 
#     classCount = 0
#     match parsedItem:
#         # PRINT 
#         case 'print))':
#             print(" print") 
#             printStatementcount +=1
#         # LOOPS
#         case '(while_stmt' | '(for_stmt':
#             print(" WHILE")
#             loopCount +=1
#         # CONDITIONS
#         case '(if_stmt' | '(match_stmt' :
#             print(" CONDITION")
#             conditionsCount += 1
#         # IMPORTS
#         case '(import_stmt':
#             print(" IMPORT")
#             importCount += 1
#         # FUNCTIONS
#         case '(funcdef':
#             print(" FUNCTION")
#             funcCount+= 1
#         # CLASSES
#         case '(classdef':
#             print(" CLASS")
#             classCount +=1
        
#     return printStatementcount, loopCount, conditionsCount, importCount, funcCount, classCount
                # try_stmt
            # case _:
            #     print('Command not recognized')
                # print(parsedData.split())

# def analyseCodeTypes(parsedData):
#     list =  parsedData.split()
#     printStatementCount=0
#     loopsCount = 0
#     conditionCount = 0
#     importCount = 0
#     funcCount = 0
#     classCount = 0
#     for i in range(len(list)):
#         # z = findMore(list[i])
#         # if z != "":
#         #     print(z)
#         prints, loops, conditions, imports, functions, classDefs = findPrint(list[i])
#         printStatementCount += prints
#         loopsCount += loops
#         conditionCount += conditions
#         importCount+= imports
#         funcCount += functions
#         classCount += classDefs

#         # loopsCount += findLoops(list[i])

# # def findLoops(parsedItem):

#     print(printStatementCount)
#     print(loopsCount)
#     print(conditionCount)
#     print(importCount)
#     print(funcCount)
#     print(classCount)
#     return printStatementCount, loopsCount, conditionCount, importCount, funcCount, classCount


def analyseCodeTypes(parsedData):
    list =  parsedData.split()
    printStatementCount=0
    loopCount = 0
    conditionCount = 0
    importCount = 0
    funcCount = 0
    classCount = 0
    for i in range(len(list)):
        match list[i]:
            # PRINT 
            case 'print))':
                printStatementCount +=1
            # LOOPS
            case '(while_stmt' | '(for_stmt':
                loopCount +=1
            # CONDITIONS
            case '(if_stmt' | '(match_stmt':
                conditionCount += 1
            # IMPORTS
            case '(import_stmt':
                importCount += 1
            # FUNCTIONS
            case '(funcdef':
                funcCount+= 1
            # CLASSES
            case '(classdef':
                classCount +=1
    return printStatementCount, loopCount, conditionCount, importCount, funcCount, classCount


def testing():
    CODE = "if a: print(a)"
    # strippedData = data.strip()
    # Add \n for end of file - antlr requires 
    input_stream = InputStream(f'{CODE}\n')
    lexer = Python3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    # tree = parser.single_input()
    tree = parser.single_input()
    result = tree.toStringTree(recog=parser)

    print(result)
    analyseCodeTypes(result)
    
    return tree, parser



# if __name__ == '__main__':
#     main()

if __name__ == '__main__':
    globals()[sys.argv[1]]()



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