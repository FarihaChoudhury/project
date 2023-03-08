import sys
import re
sys.path.insert(0, '../pythonParsing')
from pythonParse import countEmptyLinesOfInput, countWhitespaces, countNewLines
from pythonHTMLparser import HTMLParserClass

"""Helper functions for HTML code parsing"""

"""identifies <..> tags"""
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
    - stores this word in dict with its count """
def identifyDjangoTemplateTags(inputData):
    templateTag = {}
    # to identify and store {%...%}
    matches = re.findall(r'{\s*%\s*(\S+)\b', inputData)
    if matches:
        for match in matches:
            first_word = re.search(r'\w+', match).group()
            templateTag[first_word]=1
    return templateTag


"""Identifies HTML Evaluation variables
    - finds {{, keeps count of occurrence """
def identifyHTMLEvaluationVars(inputData):
    matches = re.findall(r'{\s*{\s*(\S+)\b', inputData)
    count = len(matches)
    return count
    """EXPLANATION:
        r'{\s*{\s*(\S+)\b'
        Find { with any amount of spaces (\s*), followed by { again, then matches any non white space \S, 
        \b ensures that the match stops at the end of the first word after the {% delimiter}}"""


"""Counts the number comments in a html line of code 
    - includes: <!-- and --> comments
    - Also inline comments """
def countHTMLComments(line):
    strippedLine = line.strip()
    commentLinesCount = 0
    # checks for <!-- starting lines comments 
    if strippedLine.startswith("<!--"):
        commentLinesCount += 1
    # checks for end of comment lines (if comment is in 2 lines)
    elif strippedLine.endswith("-->"):
        commentLinesCount += 1
    #checks for midline comments starting with <!-- ... -->
    elif "<!--" and "-->" in strippedLine:
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
    # retrieves tags, template tags, and evaluation variables
    tagCountDict = identifyHTMLtags(inputData)
    templateTagCountDict = identifyDjangoTemplateTags(inputData)
    evalVars = identifyHTMLEvaluationVars(inputData)

    return spaces, spacesWithoutIndent, newLines, emptyLines, totalLines, htmlComments, tagCountDict, templateTagCountDict, evalVars



if __name__ == '__main__':
    globals()[sys.argv[1]]()