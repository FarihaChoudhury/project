import sys
import re
sys.path.insert(0, '../pythonParsing')
from pythonParse import countEmptyLinesOfInput, countWhitespaces, countNewLines
from pythonHTMLparser import HTMLParserClass

"""Helper functions for HTML code parsing"""


""" Identifies HTML tags
    - finds <...> tags using the Python HTML parser library
    - return the tag and the number of occurrences in a dictionary"""
def identifyHTMLtags(committedLine):
    # Create a new parser object and feed it the HTML code
    htmlParser = HTMLParserClass()
    htmlParser.feed(committedLine.strip())
    tagCountDict={}
    for tag, count in htmlParser.tagTypesDictionary.items():
        temp = {tag: count}
        tagCountDict.update(temp)
    
    return tagCountDict   # returns a dictionary for each line of code


""" Identifies Django template tags
    - finds {%, retrieves first word after it 
    - stores this word in dict with its count 
    - returns the template tags found """
def identifyDjangoTemplateTags(committedLine):
    templateTag = {}
    matches = re.findall(r'{\s*%\s*(\S+)\b', committedLine)
    if matches:
        for match in matches:
            firstWord = re.search(r'\w+', match).group()
            templateTag[firstWord]=1
    return templateTag


""" Identifies HTML evaluation variables
    - finds {{, keeps count of occurrence 
    - returns the number of evaluation variables found """
def identifyHTMLEvaluationVars(committedLine):
    matches = re.findall(r'{\s*{\s*(\S+)\b', committedLine)
    count = len(matches)
    return count


""" Counts the number comments in a html line of code 
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


""" Performs classification on the HTML code inputted
    - takes input in terms of code text, not a file
    - performs classifications and prints to terminal
    - returns these """
def performClassificationOnHTMLInput(committedLine):
    spaces = countWhitespaces(committedLine)
    spacesWithoutIndent = countWhitespaces(committedLine.strip())
    newLines = countNewLines(committedLine)
    totalLines, emptyLines = countEmptyLinesOfInput(committedLine)
    htmlComments = countHTMLComments(committedLine)

    tagCountDict = identifyHTMLtags(committedLine)
    templateTagCountDict = identifyDjangoTemplateTags(committedLine)
    evalVars = identifyHTMLEvaluationVars(committedLine)

    return spaces, spacesWithoutIndent, newLines, emptyLines, totalLines, htmlComments, tagCountDict, templateTagCountDict, evalVars