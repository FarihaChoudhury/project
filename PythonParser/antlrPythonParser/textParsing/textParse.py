from parserHelper import countCommentsOnInputLine, countEmptyLinesOfInput, countWhitespaces

"""Helper functions for text parsing"""

"""Performs classification on a text code input
    - returns the number of spaces, new lines, empty lines and total lines """
def performClassificationOnTextInput(inputData):
    #WHITE SPACE COUNTERS: 
    spaces = countWhitespaces(inputData)
    spacesWithoutIndent = countWhitespaces(inputData.strip())
    totalLines, emptyLines = countEmptyLinesOfInput(inputData)


    return spaces, spacesWithoutIndent, emptyLines, totalLines