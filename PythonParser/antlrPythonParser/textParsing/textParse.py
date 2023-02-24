

from parserHelper import countCommentsOnInputLine, countEmptyLinesOfInput, countWhitespaces


"""Performs classification on a text code input
    - returns the number of spaces, new lines, empty lines and total lines """
def performClassificationOnTextInput(inputData):
    # strippedData = inputData.strip()

    #WHITE SPACE COUNTERS: 
    spaces = countWhitespaces(inputData)
    spacesWithoutIndent = countWhitespaces(inputData.strip())
    # totalLines, emptyLines = countEmptyLines('testFile.py')
    totalLines, emptyLines = countEmptyLinesOfInput(inputData)
    # print("Spaces:", spaces)
    # print("Spaces without indents:", spacesWithoutIndent)
    # print("Newlines:", newLines)
    # print("Empty Lines:", emptyLines)
    # print("Total lines:", totalLines)

    # #COMMENTS COUNTER:
    # comments = countCommentsOnInputLine(inputData)
    # # comments = count_comments('testFile.py')
    # print("Comment Lines", comments)

    return spaces, spacesWithoutIndent, emptyLines, totalLines