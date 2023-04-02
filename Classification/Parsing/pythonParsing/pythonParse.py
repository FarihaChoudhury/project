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
def parseDataSingleInput(committedLine):
    strippedData = committedLine.strip()
    # Add \n for end of file - antlr requires this
    input_stream = InputStream(f'{strippedData}\n')
    lexer = Python3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    tree = parser.single_input()  # prints error messages to terminal - this is handled by ANTLR and can be ignored
    return tree, parser


""" Counts white space / tabs / empty strings for inputted data:
    - returns the number of spaces and newlines"""
def countWhitespaces(committedLine):
    spaces = len(re.findall(r" ", committedLine))
    return spaces


""" Counts new lines made by '\n' command for inputted data:
    - returns the number of newlines"""
def countNewLines(committedLine):
    newlines = len(re.findall(r"\n", committedLine))
    return newlines


""" Counts empty lines of code from input text and total lines of code """
def countEmptyLinesOfInput(committedLine):
    totalLines = 1
    emptyLines = 0
    if not committedLine.strip():
        emptyLines = 1
    return totalLines, emptyLines


""" Calculates if a line is a comment line
    - Looks for single line comments and mid line comments by #, and single line comments by '/ "
    - Looks for start or end lines of block comments by triple "/' """
def countCommentsOnInputLine(committedLine):
    strippedLine = committedLine.strip()
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
def performClassificationOnPythonInput(committedLine):

    spaces = countWhitespaces(committedLine)
    spacesWithoutIndent = countWhitespaces(committedLine.strip())
    newLines = countNewLines(committedLine)
    totalLines, emptyLines = countEmptyLinesOfInput(committedLine)
    comments = countCommentsOnInputLine(committedLine)

    tree, parser = parseDataSingleInput(committedLine)
    result = tree.toStringTree(recog=parser)

    printStatementCount, loopCount, conditionCount, importCount, funcCount, classCount, classDefinition, viewCount, modelCount, formCount= analyseCodeTypes(result)

    return spaces, spacesWithoutIndent, newLines, emptyLines, totalLines, comments, printStatementCount, loopCount, conditionCount, importCount, funcCount, classCount, classDefinition, viewCount, modelCount, formCount


""" Given a parse tree result, searches for particular rules for classifications
    - when class definitions are found, retrieves the class name and checks calls upon Model/Form/View checker
    - returns classification results """
def analyseCodeTypes(parsedLine):
    list =  parsedLine.split()
    printStatementCount=0
    loopCount = 0
    conditionCount = 0
    importCount = 0
    funcCount = 0
    classCount = 0 
    className= None
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
                # +3 to get the name from the antlr result 
                # e.g.,  (classdef class (name UserModelTestCase) => UserModelTestCase)
                className = removeBracket(list[i+3])
                classCount +=1
    # Checks if the function is view or class is a, model, form or none
    viewCount = viewFunctionChecker(funcCount, parsedLine)
    modelCount, formCount = modelFormClassChecker(classCount, parsedLine)

    return printStatementCount, loopCount, conditionCount, importCount, funcCount, classCount, className, viewCount, modelCount, formCount


""" Checks if a given function is a View function or not """
def viewFunctionChecker(funcCount, parsedLine):
    viewCount=0
    if (funcCount!=0):
        if "request" in parsedLine:
             viewCount += 1
   
    return viewCount

    
""" Checks if a given class is a Model or Form class or none """
def modelFormClassChecker(classCount, parsedLine):
    modelCount = 0
    formCount = 0 
    if (classCount!=0):
        if not "TestCase" in parsedLine:
            if "Form" in parsedLine:
                formCount += 1
            elif "Model" in parsedLine:
                modelCount += 1

    return modelCount, formCount


""" Removes bracket from parse tree result of class names """
def removeBracket(className):
    if className.endswith(")"):
        return className[:-1]
    else:
        return className
