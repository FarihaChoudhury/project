
import sys
# from PythonParser.antlrPythonParser.htmlParsing.pythonHTMLparser import HTMLParserClass
sys.path.insert(0, '../pythonParsing')
from parserHelper import countEmptyLinesOfFile, countEmptyLinesOfInput, countWhitespaces, countNewLines, openFile
from pythonHTMLparser import HTMLParserClass


def useHTMLParser():
    # Sample HTML code
    # html_code = """
    # <head>
    # </body>
    # """
    html_code = '<html><head><title>Test</title></head>'
    # Create a new parser object and feed it the HTML code
    htmlParser = HTMLParserClass()
    htmlParser.feed(html_code)

    # Print out the tag types and their counts
    for tag, count in htmlParser.tagTypesDictionary.items():
        print(f"Tag {tag}: {count}")






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
    newLines = countNewLines(inputData)
    # totalLines, emptyLines = countEmptyLines('testFile.py')
    totalLines, emptyLines = countEmptyLinesOfInput(inputData)
    print("Spaces:", spaces)
    print("Newlines:", newLines)
    print("Empty Lines:", emptyLines)
    print("Total lines:", totalLines)

    #COMMENTS COUNTER:
    comments = countHTMLComments(inputData)
    # comments = count_comments('testFile.py')
    print("Comment Lines", comments)
    print("i came to here")
    return spaces, newLines, emptyLines, totalLines, comments




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
