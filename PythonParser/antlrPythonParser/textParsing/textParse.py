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


"""Filters filenames by speciifc file extensions and returns false for these"""
def filterFilenames(filename):
    invalidFilenames = (".eot",".svg","ttf","woff",".yml",".xml",".iml",".gitignore",".coveragerc", ".idea", ".vscode", "__pycache__")

    match filename:
        case "djangi.yml":
              return False
        case "__init__.py":
            return False
        case "requirements.txt":
            return False
        case "manage.py":
            return False
        case "wsgi.py":
            return False
        case "asgi.py":
            return False
    # if (filename.endswith(".eot") | filename.endswith(".svg") | filename.endswith("ttf") | filename.endswith("woff")):
    if (filename.endswith(invalidFilenames)):
        return False
    return True 
