import sys
import re
sys.path.insert(0, '../pythonParsing')
from pythonParse import countEmptyLinesOfInput, countWhitespaces, countNewLines
from pythonHTMLparser import HTMLParserClass

"""Helper functions for HTML code parsing"""


""" Identifies HTML tags
    - finds <...> tags using the Python HTML parser library
    - return the tag and the number of occurrences in a dictionary"""
def identifyHTMLtags(inputData):
    # Create a new parser object and feed it the HTML code
    htmlParser = HTMLParserClass()
    htmlParser.feed(inputData.strip())
    tagCountDict={}

    for tag, count in htmlParser.tagTypesDictionary.items():
        temp = {tag: count}
        tagCountDict.update(temp)
    
    return tagCountDict
    # gives a dictionary for each line of code --- 


""" Identifies Django template tags
    - finds {%, retrieves first word after it 
    - stores this word in dict with its count 
    - returns the template tags found """
def identifyDjangoTemplateTags(inputData):
    templateTag = {}
    # to identify and store {%...%}
    matches = re.findall(r'{\s*%\s*(\S+)\b', inputData)
    if matches:
        for match in matches:
            first_word = re.search(r'\w+', match).group()
            templateTag[first_word]=1
    return templateTag


"""Identifies HTML evaluation variables
    - finds {{, keeps count of occurrence 
    - returns the number of evaluation variables found"""
def identifyHTMLEvaluationVars(inputData):
    matches = re.findall(r'{\s*{\s*(\S+)\b', inputData)
    count = len(matches)
    return count


"""Counts the number comments in a html line of code 
    - includes: <!-- and --> comments
    - returns the comments found """
def countHTMLComments(line):
    strippedLine = line.strip()
    commentLinesCount = 0
    
    if "<!--" in strippedLine:
        commentLinesCount += 1
    elif "-->" in strippedLine:
            commentLinesCount += 1  

    return commentLinesCount


"""Performs classification on the HTML code inputted
    - takes input in terms of code text, not a file
    - performs classifications and prints to terminal
    - returns these """
def performClassificationOnHTMLInput(inputData):
    spaces = countWhitespaces(inputData)
    spacesWithoutIndent = countWhitespaces(inputData.strip())
    newLines = countNewLines(inputData)
    totalLines, emptyLines = countEmptyLinesOfInput(inputData)
    htmlComments = countHTMLComments(inputData)

    tagCountDict = identifyHTMLtags(inputData)
    templateTagCountDict = identifyDjangoTemplateTags(inputData)
    evalVars = identifyHTMLEvaluationVars(inputData)

    return spaces, spacesWithoutIndent, newLines, emptyLines, totalLines, htmlComments, tagCountDict, templateTagCountDict, evalVars


if __name__ == '__main__':
    globals()[sys.argv[1]]()