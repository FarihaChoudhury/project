import json
import sys
from CommitData import dataClass
# from PythonParser.antlrPythonParser.htmlParsing.htmlParse import performClassificationOnHTMLInput
# from PythonParser.antlrPythonParser.textParsing.textParse import performClassificationOnTextInput
sys.path.insert(0, '../PythonParser/antlrPythonParser/pythonParsing')
sys.path.insert(0, '../PythonParser/antlrPythonParser/htmlParsing')
sys.path.insert(0, '../PythonParser/antlrPythonParser/textParsing')
sys.path.insert(0, '../PythonParser/antlrPythonParser/antlrParserGeneratedCode')
from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser
from parserHelper import performClassificationOnPythonInput
from textParse import performClassificationOnTextInput
from htmlParse import performClassificationOnHTMLInput

# from htmlParse import performClassificationOnHTMLInput
# from pythonParsing import 


"""Converts a set into a list object for JSON serialise purposes"""
def jsonSetSerializer(setObject):
    if isinstance(setObject, set):
        return list(setObject)
    return setObject




"""calls on additions for files in all commits and deletions for files in all commits"""
def readAdditionsAndDeletions(dataClass):
    # 1- create template for results
    # dataClass.createResultsTemplate()
    dataClass.createResultsTemplateSeparate()
    print("\n template made --- \n")
    # 2 - read additions and deletions
    print("\n addition ------------: \n")
    readAdditionsFromClass(dataClass)
    print("\n deletions------------: \n")
    readDeletionsFromClass(dataClass)

    print("\n results ---------: \n")
    for i in range(len(dataClass.resultsListSeparate)):
            print(dataClass.resultsListSeparate[i])
            print("\n")
    
    storeJSONresults(dataClass)


"""Stores results on a JSON file"""
def storeJSONresults(dataClass):
    # Change set of filenames to list so that it can be dumped into JSON
    for i in range(len(dataClass.resultsListSeparate)):
        if dataClass.resultsListSeparate[i].items(): 
            for key, val in dataClass.resultsListSeparate[i].items():
                # set the filenames set as list:
                dataClass.resultsListSeparate[i][key]["files edited"] = jsonSetSerializer(dataClass.resultsListSeparate[i][key]["files edited"])
    # store results to json file
    with open('results.json', "w") as file:
        json.dump(dataClass.resultsListSeparate, file)
    


"""Reads the additionsPerFile item in the list of dictionaries of all commits made in a repository"""
def readAdditionsFromClass(dataClass):
    commitData = dataClass.listOfDictionary
    additions = []
    for i in range(len(commitData)):
        print(i)
        if (commitData[i]["additionsPerFile"][0]):
            # print(commitData[i])
            # sets all additions for specific commits into one list
            contributor = commitData[i]["commitAuthor"]
            print(contributor)
            additions = commitData[i]["additionsPerFile"][0]
            print(additions)
            differentiateCodeTypes(dataClass, contributor, additions, True)
        # else:
        #     print("no addition here")
    return additions

"""Reads the deletionsPerFile item in the list of dictionaries of all commits made in a repository"""
def readDeletionsFromClass(dataClass):
    commitData = dataClass.listOfDictionary
    deletions = []
    for i in range(len(commitData)):
        print(i)
        if (commitData[i]["deletionsPerFile"][0]):
            contributor = commitData[i]["commitAuthor"]
            print(contributor)
            deletions = commitData[i]["deletionsPerFile"][0]
            print(deletions)
            # call function to differentiate the code types of each line and perform classification
            differentiateCodeTypes(dataClass, contributor, deletions, False)
    
        # else:
        #     print("no deletion here")
    return deletions


def differentiateCodeTypes(dataClass, contributor, listOfDictionariesForCommits, increment): 

    if listOfDictionariesForCommits.items(): 
        for key, val in listOfDictionariesForCommits.items():
            if key.endswith(".py"):
                print(" PYTHON FILE: ")
                # print(key)
                # print(val)
                retrievePythonCodeToParse(dataClass, contributor, key, val, increment)
                print("\n")
            elif key.endswith(".md") or key.endswith(".txt"):
                print(" TEXT FILE:")
                # print(key)
                # print(val)
                retrieveTextCodeToParse(dataClass, contributor, key, val, increment)
                print("\n")
            elif key.endswith(".html"):
                print(" HTML FILES:")
                # print(key)
                retrieveHTMLCodeToParse(dataClass, contributor, key, val, increment)



# """Reads the additionsPerFile item in the list of dictionaries of all commits made in a repository"""
# def readAdditionsForFilesInAllCommits():
#     jsonFile = "allCommitsInRepo.json"
#     with open(jsonFile, 'r') as file:
#         commitData = json.load(file)

#     additions = []
#     for i in range(len(commitData)):
#         # add all additions for all commits into one list
#         additions.append(commitData[i]["additionsPerFile"][0])
#     # call function to differentiate code types: python, html, text 
#     differentiateCodeTypes(additions)
#     return additions

# """Takes a list which contains dictionary items and checks the keys of these items
#     - if the key holds a Python file, text file or HTML file, the necessary classifications will be called on the values """
# def differentiateCodeTypes(listOfDictionariesForCommits, dataClass, contributor): 
#     for i in range(len(listOfDictionariesForCommits)): 
#         print(listOfDictionariesForCommits)   
#         # iterates each item of the list of dictionaries by the key and value 
#         if listOfDictionariesForCommits[i].items(): 
#             for key, val in listOfDictionariesForCommits[i].items():
#                 if key.endswith(".py"):
#                     print(" PYTHON FILE: ")
#                     """NEED TO DIFFERENTIATE THE FILENAMES (KEY) AND THEN PUT INTO RELEVANT ONES"""
#                     print(key)
#                     retrievePythonCodeToParse(val, key, dataClass, contributor)
#                     print("\n FINISHED:")
#                     print(dataClass.resultsList)
#                 elif key.endswith(".md") or key.endswith(".txt"):
#                     print(" TEXT FILE:")
#                     print(key)
#                     retrieveTextCodeToParse(val)
#                 elif key.endswith(".html"):
#                     print(" HTML FILES:")
#                     print(key)
#                     retrieveHTMLCodeToParse(val)


# """Takes a list which contains dictionary items and checks the keys of these items
#     - if the key holds a Python file, text file or HTML file, the necessary classifications will be called on the values """
# def differentiateCodeTypes(listOfDictionariesForCommits): 
#     for i in range(len(listOfDictionariesForCommits)):    
#         # iterates each item of the list of dictionaries by the key and value 
#         # print(listOfDictionariesForCommits[i])
#         if listOfDictionariesForCommits[i][0].items(): 
#             for key, val in listOfDictionariesForCommits[i][0].items():
#                 # print(key)
#                 if key.endswith(".py"):
#                     print("PYTHON FILE: ")
#                     print(key)
#                     retrievePythonCodeToParse(val)
#                 elif key.endswith(".md") or key.endswith(".txt"):
#                     print("TEXT FILE:")
#                     print(key)
#                     retrieveTextCodeToParse(val)
#                 elif key.endswith(".html"):
#                     print("HTML FILES:")
#                     print(key)
#                     retrieveHTMLCodeToParse(val)


"""Accesses the value of the dictionaries which store the Python code"""
def retrievePythonCodeToParse(dataClass, contributor, filename, valueList, increment):
    """NEED TO DIFFERENTIATE THE FILENAMES (KEY) AND THEN PUT INTO RELEVANT ONES"""
    
    print(increment)
    for valItem in valueList:
        spaces, newLines, emptyLines, totalLines, comments = performClassificationOnPythonInput(valItem)
        codeLines = (totalLines - comments) - emptyLines

        updateDataInResults(dataClass, contributor, increment, spaces=spaces, newLines=newLines, emptyLines=emptyLines, comments=comments, codeLines=codeLines, totalLines=totalLines)
        print(dataClass.resultsListSeparate)
        print("\n")


"""Accesses the value of the dictionaries which store the text"""
def retrieveTextCodeToParse(dataClass, contributor, filename, valueList, increment):
    print(increment)
    for valItem in valueList:
        spaces, emptyLines, totalLines = performClassificationOnTextInput(valItem)
        # print("next")
        updateDataInResults(dataClass, contributor, increment, spaces = spaces, emptyLines = emptyLines, totalLines = totalLines )
        print(dataClass.resultsListSeparate)
        print("\n")



"""Accesses the value of the dictionaries which store the HTML code"""
def retrieveHTMLCodeToParse(dataClass, contributor, filename, valueList, increment):
    print(increment)
    for valItem in valueList:
        # print(valItem)

        spaces, newLines, emptyLines, totalLines, comments = performClassificationOnHTMLInput(valItem)
        codeLines = (totalLines - comments) - emptyLines
        updateDataInResults(dataClass, contributor, increment, spaces=spaces, newLines=newLines, emptyLines=emptyLines, comments=comments, codeLines=codeLines, totalLines=totalLines)
        print(dataClass.resultsListSeparate)
        print("\n")
        

def updateDataInResults(dataClass, contributor, increment, spaces = 0, newLines = 0, emptyLines = 0, comments = 0, codeLines = 0, totalLines = 0):
    if increment == True: 
        additionsCategory = "additions"
        incrementResults(dataClass, contributor, "spaces", spaces, additionsCategory)
        incrementResults(dataClass, contributor, "new lines", newLines, additionsCategory)
        incrementResults(dataClass, contributor, "empty lines", emptyLines, additionsCategory)
        incrementResults(dataClass, contributor, "comment lines", comments, additionsCategory)
        incrementResults(dataClass, contributor, "code lines", codeLines, additionsCategory)
        incrementResults(dataClass, contributor, "total lines", totalLines, additionsCategory)
        # dataClass.incrementDataByValueForSeparate(contributor, "spaces", spaces, additionsCategory)
        print("INCREMENT")

    else: 
        deletionsCategory = "deletions"
        decrementResults(dataClass, contributor, "spaces", spaces, deletionsCategory)
        decrementResults(dataClass, contributor, "new lines", newLines, deletionsCategory)
        decrementResults(dataClass, contributor, "empty lines", emptyLines, deletionsCategory)
        decrementResults(dataClass, contributor, "comment lines", comments, deletionsCategory)
        decrementResults(dataClass, contributor, "code lines", codeLines, deletionsCategory)
        decrementResults(dataClass, contributor, "total lines", totalLines, deletionsCategory)
        # dataClass.decrementDataByValueForSeparate(contributor, "spaces", spaces, deletionsCategory)
        print("DECREMENT")


def incrementResults(dataClass, collaborator, option, incrementValue, category):
    dataClass.incrementDataByValueForSeparate(collaborator, option, incrementValue, category)
    dataClass.incrementDataByValueForSeparate(collaborator, option, incrementValue, "overall")

def decrementResults(dataClass, collaborator, option, decrementValue, category):
    # increment the "deletions" category then decrement overall 
    dataClass.incrementDataByValueForSeparate(collaborator, option, decrementValue, category)
    dataClass.decrementDataByValueForSeparate(collaborator, option, decrementValue, "overall")




# """Saves content of the list of dictionaries onto a .txt file and a .JSON file"""     
# def storeDataInPyFile(additionsCode):
#     # Saves content of each commit into a text file
#     with open('pythonAdditions.py', 'w') as file:
#         for additionLine in additionsCode:
#             file.write(str(additionLine))
#             file.write("\n")


if __name__ == '__main__':
    # allows you to call openJsonFile() from terminal 
    globals()[sys.argv[1]]()
    # RUN: python3 usingJSONResponse.py openJsonFile 



# """Reads the deletionsPerFile item in the list of dictionaries of all commits made in a repository"""
# def readDeletionsForFilesInAllCommits():
#     jsonFile = "allCommitsInRepo.json"
#     with open(jsonFile, 'r') as file:
#         commitData = json.load(file)

#     deletions = []
#     for i in range(len(commitData)):
#         # add all deletions for all commits into one list
#         deletions.append(commitData[i]["deletionsPerFile"][0])
#     # call function to differentiate code types: python, html, text 
#     # print(deletions)
#     differentiateCodeTypes(deletions)
#     return deletions
    