import numpy as np
import re
import sys

sys.path.insert(0, '../pythonParsing')
from main import countEmptyLines, countWhitespaces, openFile

# import sys
# sys.path.insert(0, 'PythonParser/antlrPythonParser/')
# import main
# from main import countEmptyLines, countWhitespaces, openFile
# from main import countEmptyLines, countWhitespaces, openFile
# from main import countEmptyLines, countWhitespaces, openFile


"""Counts the number of lines of comments in a python .py file
    - includes: #,' ', " ", """ """ block comments, ''' ''' block comments, 
    - Also inline #comments which may be inaccurate """
def count_comments(filename):
    commentLinesCount = 0
    partOfBlockComment = False
    with open(filename, "r") as file:
        fileContent = file.readlines()
       
        for line in fileContent:
            # removes starting and trailing spaces 
            strippedLine = line.strip()

            # checks for # comments 
            if strippedLine.startswith("<!--") and strippedLine.endswith("-->"):
                commentLinesCount += 1
                # print("start and ended comment - one line comment")
            
            elif strippedLine.startswith("<!--") and not strippedLine.endswith("-->"):
                commentLinesCount += 1
                partOfBlockComment = True
                # print("start block comment")

            #checks for middle of block comment lines
            elif partOfBlockComment:
                commentLinesCount += 1

                if strippedLine.endswith("-->"):
                    partOfBlockComment = False
                    # print("finished block comment")
                # else:
                #     print("still in block")

            #checks for midline comments starting with # - not 100% accurate 
            elif "<!--" and "-->" in strippedLine:
                commentLinesCount += 1
                # print("midline comment")
    
    return commentLinesCount



def main():
    realData = openFile('htmlTestFile.html')
    strippedData = realData.strip()
    # print(strippedData)
    
    
    # # count white space:  use real data- where start and trailing spaces have not been stripped:
    #WHITE SPACE COUNTERS: 
    spaces, newlines = countWhitespaces(realData)
    totalLines, emptyLines = countEmptyLines('htmlTestFile.html')
    print("Spaces:", spaces)
    print("Newlines:", newlines)
    print("Empty Lines:", emptyLines)
    print("Total lines:", totalLines)

    # COMMENTS COUNTER:
    comments = count_comments('htmlTestFile.html')
    print("comments", comments)



if __name__ == '__main__':
    main()
