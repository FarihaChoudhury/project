from io import StringIO
from antlr4 import *
import sys
sys.path.insert(0, '../antlrParserGeneratedCode')
# from Python3ParserListener import Python3ParserListener
from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser
import numpy as np
import re
"""Helper functions for python code parsing"""


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
    tree = parser.single_input()  #May print error message to terminal - this is handled by ANTLR and can be ignored
    # print(tree.toStringTree(recog=parser))
    # print("\n")
    return tree, parser


""" Counts white space / tabs / empty strings for inputted data:
    - returns the number of spaces and newlines"""
def countWhitespaces(data):
    spaces = len(re.findall(r" ", data))
    return spaces


""" Counts new lines made by '\n' command for inputted data:
    - returns the number of newlines"""
def countNewLines(data):
    newlines = len(re.findall(r"\n", data))
    return newlines


""" Counts empty lines of code from input text and total lines of code """
def countEmptyLinesOfInput(inputData):
    totalLines = 1
    emptyLines = 0
    if not inputData.strip():
        # cannot strip if empty => increments count 
        emptyLines = 1
    return totalLines, emptyLines


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




"""Performs classification on the python code inputted
    - takes input in terms of code text, not a file
    - passes code into parser 
    - performs classifications and prints to terminal
    - returns these """
def performClassificationOnPythonInput(inputData):
    #PARSE TREE GENERATOR:
    # tree, parser = parseDataSingleInput(inputData)
    # result = tree.toStringTree(recog=parser)
    # print(result)

    spaces = countWhitespaces(inputData)
    spacesWithoutIndent = countWhitespaces(inputData.strip())
    newLines = countNewLines(inputData)
    totalLines, emptyLines = countEmptyLinesOfInput(inputData)
    comments = countCommentsOnInputLine(inputData)

    tree, parser = parseDataSingleInput(inputData)
    result = tree.toStringTree(recog=parser)

    printStatementCount, loopCount, conditionCount, importCount, funcCount, classCount, classDefinition, viewCount, modelCount, formCount= analyseCodeTypes(result)
    # print("Spaces:", spaces)
    # print("Spaces without indents:", spacesWithoutIndent)
    # print("Newlines:", newLines)
    # print("Empty Lines:", emptyLines)
    # print("Total lines:", totalLines)
    # print("Comment Lines", comments)
    # print("Prints:", printStatementCount)
    # print("Loops:", loopCount)
    # print("Conditions:", conditionCount)
    # print("Imports:", importCount)
    # print("Functions:", funcCount)
    # print("ClassDefs:", classCount)   
    # print("classDef list:", classDefinition)

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
            case 'print))':
                printStatementCount +=1
            case '(while_stmt' | '(for_stmt':
                loopCount +=1
            case '(if_stmt' | '(match_stmt':
                conditionCount += 1
            case '(import_stmt':
                importCount += 1
            case '(funcdef':
                funcCount+= 1
            case '(classdef':
                # +3 to get the name from the antlr result of ..(classdef class (name UserModelTestCase) => UserModelTestCase)
                className = removeBracket(list[i+3])
                classCount +=1
    # Checks if the class is a view, model, form or none
    viewCount, modelCount, formCount = viewModelFormChecker(className, parsedData)

    # print("", viewCount, modelCount, formCount)
    return printStatementCount, loopCount, conditionCount, importCount, funcCount, classCount, className, viewCount, modelCount, formCount


def viewModelFormChecker(className, parsedData):
    viewCount = 0
    modelCount = 0
    formCount = 0 
    if (className):
        if not "TestCase" in parsedData:
            if "View" in parsedData:
                viewCount += 1
            elif "Form" in parsedData:
                formCount += 1
            elif "Model" in parsedData:
                modelCount += 1

    return viewCount, modelCount, formCount
        # # define variables here to avoid repetition
        # viewCount, modelCount, formCount = checkViews(parsedData, viewCount, modelCount, formCount)
        # print("", viewCount, modelCount, formCount)

"""Removes bracket from parse tree result of class names"""
def removeBracket(className):
    if className.endswith(")"):
        return className[:-1]
    else:
        return className



# def testing():
#     CODE = "class Post(models.Model):"
#     # CODE = "class dataClass:"
#     # strippedData = data.strip()
#     # Add \n for end of file - antlr requires 
#     input_stream = InputStream(f'{CODE}\n')
#     lexer = Python3Lexer(input_stream)
#     stream = CommonTokenStream(lexer)
#     parser = Python3Parser(stream)
#     # tree = parser.single_input()
#     tree = parser.single_input()
#     result = tree.toStringTree(recog=parser)

#     print(result)
#     analyseCodeTypes(result)
    
#     return tree, parser



# if __name__ == '__main__':
#     main()

if __name__ == '__main__':
    globals()[sys.argv[1]]()
