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
    #PARSE TREE GENERATOR:
    tree, parser = parseDataSingleInput(inputData)
    result = tree.toStringTree(recog=parser)
    print(result)

    #WHITE SPACE COUNTERS: 
    spaces = countWhitespaces(inputData)
    spacesWithoutIndent = countWhitespaces(inputData.strip())
    newLines = countNewLines(inputData)
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

    printStatementCount, loopCount, conditionCount, importCount, funcCount, classCount, classDefinition, viewCount, modelCount, formCount= analyseCodeTypes(result)
    print("Prints:", printStatementCount)
    print("Loops:", loopCount)
    print("Conditions:", conditionCount)
    print("Imports:", importCount)
    print("Functions:", funcCount)
    print("ClassDefs:", classCount)   
    print("classDef list:", classDefinition)


    return spaces, spacesWithoutIndent, newLines, emptyLines, totalLines, comments, printStatementCount, loopCount, conditionCount, importCount, funcCount, classCount, classDefinition, viewCount, modelCount, formCount



def analyseCodeTypes(parsedData):
    list =  parsedData.split()
    printStatementCount=0
    loopCount = 0
    conditionCount = 0
    importCount = 0
    funcCount = 0
    classCount = 0 
    className=""
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
                # +3 to get the name from the antlr result of ..(classdef class (name UserModelTestCase) => UserModelTestCase)
                className = removeBracket(list[i+3])
                classCount +=1

    # Checks if the class is a view, model, form or none
    viewCount, modelCount, formCount = viewModelFormChecker(className, parsedData)
    print("", viewCount, modelCount, formCount)

    return printStatementCount, loopCount, conditionCount, importCount, funcCount, classCount, className, viewCount, modelCount, formCount

def viewModelFormChecker(className, parsedData):
    viewCount = 0
    modelCount = 0
    formCount = 0 
    if (className):
        if not "TestCase" in parsedData:
            if "View" in parsedData:
                print("VIEW FOUND")
                viewCount += 1
            elif "Form" in parsedData:
                print("FORM FOUND")
                formCount += 1
            elif "Model" in parsedData:
                print("MODEL FOUND")
                modelCount += 1

    return viewCount, modelCount, formCount
        # # define variables here to avoid repetition
        # viewCount, modelCount, formCount = checkViews(parsedData, viewCount, modelCount, formCount)
        # print("", viewCount, modelCount, formCount)



def removeBracket(className):
    if className.endswith(")"):
        return className[:-1]
    else:
        return className



def testing():
    CODE = "class Post(models.Model):"
    # CODE = "class dataClass:"
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
    globals()[sys.argv[1]]()
