
import sys
import re
# from PythonParser.antlrPythonParser.htmlParsing.pythonHTMLparser import HTMLParserClass
sys.path.insert(0, '../pythonParsing')
from parserHelper import countEmptyLinesOfFile, countEmptyLinesOfInput, countWhitespaces, countNewLines, openFile
from pythonHTMLparser import HTMLParserClass




"""identifies <..> tags"""
def identifyHTMLtags(inputData):
    # 1 html, 2 heads, 1 title: 
    html_code = '<!--hello-->'
    # Create a new parser object and feed it the HTML code
    htmlParser = HTMLParserClass()
    # htmlParser.feed(html_code)
    htmlParser.feed(inputData.strip())

    tagCountDict={}

    # Print out the tag types and their counts
    for tag, count in htmlParser.tagTypesDictionary.items():
        temp = {tag: count}
        tagCountDict.update(temp)
        # print(f"Tag {tag}: {count}")
    
    return tagCountDict
    # gives a dictionary for each line of code --- 

    # need to update existing dictionary - increment/decrement 




# def call():
#     pee = identifyDjangoTemplateTags()
#     see= identifyHTMLEvaluationVars()
#     # print(pee)
#     print(see)


# to identify and store {%...%}
def identifyDjangoTemplateTags(inputData):
    templateTag = {}

    """finds {% and gets the first word after it so it can be stored in dict!}"""
    code = 'This is some code { % for i in range(5) %}{{ i }}{% endfor %} and here is {% another %} code block.'

    matches = re.findall(r'{\s*%\s*(\S+)\b', inputData)
    if matches:
        for match in matches:
            first_word = re.search(r'\w+', match).group()
            print(f"First word after : {first_word}")
            templateTag[first_word]=1
    # else:
    #     print("No code blocks found.")
    # print(templateTag)
    return templateTag


# to identify and count {{ }}
def identifyHTMLEvaluationVars(inputData):
    """finds {{ and counts occurrences}"""
    code = 'This is some code {% for i in range(5) %}{{ i }} { { hi} } '

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


# def identifyTag(line):


"""Performs classification on the HTML code inputted
    - takes input in terms of code text, not a file
    - performs classifications and prints to terminal
    - returns these 
    """
def performClassificationOnHTMLInput(inputData):
    # WHITE SPACE COUNTERS: 
    spaces = countWhitespaces(inputData)
    spacesWithoutIndent = countWhitespaces(inputData.strip())
    newLines = countNewLines(inputData)

    totalLines, emptyLines = countEmptyLinesOfInput(inputData)
    # print("Spaces:", spaces)
    # print("Spaces without indents:", spacesWithoutIndent)
    # print("Newlines:", newLines)
    # print("Empty Lines:", emptyLines)
    # print("Total lines:", totalLines)

    #COMMENTS COUNTER: inputData
    htmlComments = countHTMLComments(inputData)
    # print("Comment Lines", htmlComments)

    # retrieves tags and template tags 
    tagCountDict = identifyHTMLtags(inputData)
    templateTagCountDict = identifyDjangoTemplateTags(inputData)
    evalVars = identifyHTMLEvaluationVars(inputData)


    return spaces, spacesWithoutIndent, newLines, emptyLines, totalLines, htmlComments, tagCountDict, templateTagCountDict, evalVars




if __name__ == '__main__':
    # allows you to call openJsonFile() from terminal 
    globals()[sys.argv[1]]()
    # RUN: python3 parserHelper.py openJsonFile






# """ for file input"""

# """Counts the number comments in a html .html file
#     - includes: <!-- ... --> comments
#     - Also inline comments """
# def count_comments(filename):
#     commentLinesCount = 0
#     partOfBlockComment = False
#     with open(filename, "r") as file:
#         fileContent = file.readlines()
       
#         for line in fileContent:
#             # removes starting and trailing spaces 
#             strippedLine = line.strip()

#             # checks for # comments 
#             if strippedLine.startswith("<!--") and strippedLine.endswith("-->"):
#                 commentLinesCount += 1
            
#             elif strippedLine.startswith("<!--") and not strippedLine.endswith("-->"):
#                 commentLinesCount += 1
#                 partOfBlockComment = True

#             #checks for middle of block comment lines
#             elif partOfBlockComment:
#                 commentLinesCount += 1

#                 if strippedLine.endswith("-->"):
#                     partOfBlockComment = False

#             #checks for midline comments starting with # - not 100% accurate 
#             elif "<!--" and "-->" in strippedLine:
#                 commentLinesCount += 1
#                 # print("midline comment")
    
#     return commentLinesCount



# def parseHTMLfile():
#     realData = openFile('htmlTestFile.html')
#     strippedData = realData.strip()
#     # print(strippedData)
    
    
#     # # count white space:  use real data- where start and trailing spaces have not been stripped:
#     #WHITE SPACE COUNTERS: 
#     spaces, newlines = countWhitespaces(realData)
#     totalLines, emptyLines = countEmptyLinesOfFile('htmlTestFile.html')
#     print("Spaces:", spaces)
#     print("Newlines:", newlines)
#     print("Empty Lines:", emptyLines)
#     print("Total lines:", totalLines)

#     # COMMENTS COUNTER:
#     comments = count_comments('htmlTestFile.html')
#     print("comments", comments)



# # if __name__ == '__main__':
# #     parseHTMLfile()

# if __name__ == '__main__':
#     # allows you to call openJsonFile() from terminal 
#     globals()[sys.argv[1]]()
#     # RUN: python3 htmlParse.py openJsonFile 
