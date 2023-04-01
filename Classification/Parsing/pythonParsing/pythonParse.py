from io import StringIO
from antlr4 import *
import sys
sys.path.insert(0, '../antlrParserGeneratedCode')
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
        emptyLines = 1
    return totalLines, emptyLines


""" Calculates if a line is a comment line
    - Looks for single line comments and mid line comments by #, and single line comments by '/ "
    - Looks for start or end lines of block comments by triple "/' """
def countCommentsOnInputLine(line):
    strippedLine = line.strip()
    commentLinesCount = 0
    # single # comments 
    if strippedLine.startswith("#"):
        commentLinesCount += 1
    # triple """ or ''' - multi line
    elif strippedLine.startswith('"""') or strippedLine.endswith('"""'):
        commentLinesCount += 1
    elif strippedLine.startswith("'''") or strippedLine.endswith("'''"):
        commentLinesCount += 1
    # single " or ' - single line
    elif strippedLine.startswith('"') and strippedLine.endswith('"'):
        commentLinesCount += 1
    elif strippedLine.startswith("'") and strippedLine.endswith("'"):
        commentLinesCount += 1
    #midline comments starting with # - not 100% accurate as # can be have other uses
    elif "#" in strippedLine:
        commentLinesCount += 1

    return commentLinesCount



""" Performs classification on the python code inputted
    - takes input of single line of code 
    - performs classifications for spaces, lines, comments
    - passes code into parser 
    - performs classifications for parse tree
    - returns classification results"""
def performClassificationOnPythonInput(inputData):

    spaces = countWhitespaces(inputData)
    spacesWithoutIndent = countWhitespaces(inputData.strip())
    newLines = countNewLines(inputData)
    totalLines, emptyLines = countEmptyLinesOfInput(inputData)
    comments = countCommentsOnInputLine(inputData)

    tree, parser = parseDataSingleInput(inputData)
    result = tree.toStringTree(recog=parser)

    printStatementCount, loopCount, conditionCount, importCount, funcCount, classCount, classDefinition, viewCount, modelCount, formCount= analyseCodeTypes(result)

    return spaces, spacesWithoutIndent, newLines, emptyLines, totalLines, comments, printStatementCount, loopCount, conditionCount, importCount, funcCount, classCount, classDefinition, viewCount, modelCount, formCount


""" Given a parse tree result, searches for particular rules for classifications
    - when class definitions are found, retrieves the class name and checks calls upon Model/Form/View checker
    - returns classification results """
def analyseCodeTypes(parsedData):
    list =  parsedData.split()
    printStatementCount=0
    loopCount = 0
    conditionCount = 0
    importCount = 0
    funcCount = 0
    classCount = 0 
    funcName=""
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
                funcName = removeBracket(list[i+3])
                funcCount+= 1
            case '(classdef':
                # +3 to get the name from the antlr result 
                # e.g.,  (classdef class (name UserModelTestCase) => UserModelTestCase)
                className = removeBracket(list[i+3])
                classCount +=1
    # Checks if the class is a view, model, form or none
    viewCountFunc = viewFunctionChecker(funcName, parsedData)
    viewCount, modelCount, formCount = viewModelFormChecker(className, parsedData)
    viewCount = viewCount + viewCountFunc

    return printStatementCount, loopCount, conditionCount, importCount, funcCount, classCount, className, viewCount, modelCount, formCount

""" checks if a given function is a View function or not"""
def viewFunctionChecker(funcName, parsedDataLine):
    viewCount=0
    if (funcName):
        if not "TestCase" in parsedDataLine:
            if "request" in parsedDataLine:
                print("\n!!!!!!!!!!!!!!!!!!!!!!")
                print(parsedDataLine)
                print("\n!!!!!!!!!!!!")
                viewCount += 1
   
    return viewCount

    
""" Checks if a given class is a Model, Form, View class or none"""
def viewModelFormChecker(className, parsedDataLine):
    viewCount = 0
    modelCount = 0
    formCount = 0 
    if (className):
        if not "TestCase" in parsedDataLine:
            # if "View" in parsedDataLine:
            #     viewCount += 1
            if "Form" in parsedDataLine:
                formCount += 1
            elif "Model" in parsedDataLine:
                modelCount += 1

    return viewCount, modelCount, formCount


""" Removes bracket from parse tree result of class names"""
def removeBracket(className):
    if className.endswith(")"):
        return className[:-1]
    else:
        return className




if __name__ == '__main__':
    globals()[sys.argv[1]]()
