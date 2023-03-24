from pythonParse import countEmptyLinesOfInput, countWhitespaces

"""Helper functions for text parsing"""

"""Performs classification on a input
    - returns the number of spaces, new lines, empty lines and total lines """
def performClassificationOnTextInput(inputData):
    spaces = countWhitespaces(inputData)
    spacesWithoutIndent = countWhitespaces(inputData.strip())
    totalLines, emptyLines = countEmptyLinesOfInput(inputData)

    return spaces, spacesWithoutIndent, emptyLines, totalLines


"""Filters filenames by specific file extensions and returns false if invalid filename found"""
def filterFilenames(filename):
    invalidFilenames = (".eot",".svg","ttf","woff",".yml",".xml",".iml",".gitignore",".coveragerc", ".idea", ".vscode", "__pycache__", 
                        "django.yml", "__init__.py", "requirements.txt", "manage.py", "wsgi.py", "asgi.py", "Procfile", )

    if (filename.endswith(invalidFilenames)):
        return False
    else:
        return True 
