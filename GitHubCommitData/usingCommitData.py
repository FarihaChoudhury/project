import json
import os
import sys
# from CommitData import dataClass
# from antlrPythonParser.htmlParsing.htmlParse import performClassificationOnHTMLInput
# from PythonParser.antlrPythonParser.textParsing.textParse import performClassificationOnTextInput
sys.path.insert(0, '../Classification/Parsing/pythonParsing')
sys.path.insert(0, '../Classification/Parsing/htmlParsing')
sys.path.insert(0, '../Classification/Parsing/textParsing')
sys.path.insert(0, '../Classification/Parsing/antlrParserGeneratedCode')
from pythonParse import performClassificationOnPythonInput
from textParse import performClassificationOnTextInput
from htmlParse import performClassificationOnHTMLInput

# from htmlParse import performClassificationOnHTMLInput
# from pythonParsing import 


"""Converts a set into a list object for JSON serialize purposes"""
def jsonSetSerializer(setObject):
    if isinstance(setObject, set):
        return list(setObject)
    return setObject


def getClassificationsResults(dataClass):
    setUpClassificationsResults(dataClass)
    print("\n addition ------------: \n")
    readAdditionsFromClass(dataClass)
    print("\n deletions------------: \n")
    readDeletionsFromClass(dataClass)

    print("\n results ---------: \n")
    for i in range(len(dataClass.resultsListSeparate)):
            print(dataClass.resultsListSeparate[i])
            print("\n")
    
    storeJSONresults(dataClass)


"""calls on additions for files in all commits and deletions for files in all commits"""
def setUpClassificationsResults(dataClass):
# def readAdditionsAndDeletions(dataClass):
    # 1- create template for results
    # dataClass.createResultsTemplate()
    dataClass.createResultsTemplateSeparate()
    print("\n template made --- \n")
    # 2 - read additions and deletions
    # print("\n addition ------------: \n")
    # readAdditionsFromClass(dataClass)
    # print("\n deletions------------: \n")
    # readDeletionsFromClass(dataClass)

    # print("\n results ---------: \n")
    # for i in range(len(dataClass.resultsListSeparate)):
    #         print(dataClass.resultsListSeparate[i])
    #         print("\n")
    
    # storeJSONresults(dataClass)


"""Stores results on a JSON file"""
def storeJSONresults(dataClass):
    # Change set of filenames to list so that it can be dumped into JSON
    for i in range(len(dataClass.resultsListSeparate)):
        if dataClass.resultsListSeparate[i].items(): 
            for key, val in dataClass.resultsListSeparate[i].items():
                # set the filenames set as list:
                dataClass.resultsListSeparate[i][key]["files edited"] = jsonSetSerializer(dataClass.resultsListSeparate[i][key]["files edited"])
    # store results to json file
    with open(os.path.join('../ResultsForCommitData', 'results.json'), "w") as file:
        json.dump(dataClass.resultsListSeparate, file)
    

# def readAdditionsFromClass(dataClass):
#     commitData = dataClass.listOfDictionaryForCommits
#     additions = []
#     # for i in range(len(commitData)):
#     print(0)
#     if (commitData[0]["additionsPerFile"][0]):
#         # print(commitData[i])
#         # sets all additions for specific commits into one list
#         contributor = commitData[0]["commitAuthor"]
#         print(contributor)
#         additions = commitData[0]["additionsPerFile"][0]
#         print("add", additions)
#         differentiateCodeTypes(dataClass, contributor, additions, True)
#         # else:
#         #     print("no addition here")
#     return additions

# """Reads the deletionsPerFile item in the list of dictionaries of all commits made in a repository"""
# def readDeletionsFromClass(dataClass):
#     commitData = dataClass.listOfDictionaryForCommits
#     deletions = []
#     # for i in range(len(commitData)):
#     print(0)
#     if (commitData[0]["deletionsPerFile"][0]):
#         contributor = commitData[0]["commitAuthor"]
#         # print(contributor)
#         deletions = commitData[0]["deletionsPerFile"][0]
#         # print(deletions)
#         # call function to differentiate the code types of each line and perform classification
#         differentiateCodeTypes(dataClass, contributor, deletions, False)
#     return deletions

# "''THIS IS REAL VERSIONS - USES ALLLLL COMMITS: "
"""Reads the additionsPerFile item in the list of dictionaries of all commits made in a repository"""
def readAdditionsFromClass(dataClass):
    commitData = dataClass.listOfDictionaryForCommits
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
    return additions

# """Reads the deletionsPerFile item in the list of dictionaries of all commits made in a repository"""
def readDeletionsFromClass(dataClass):
    commitData = dataClass.listOfDictionaryForCommits
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
    return deletions


"""Takes a list which contains dictionary items and checks the keys of these items
    - if the key holds a Python file, text file or HTML file, the necessary classifications will be called on the values """
def differentiateCodeTypes(dataClass, contributor, listOfDictionariesForCommits, increment): 
    if listOfDictionariesForCommits.items(): 
        for key, val in listOfDictionariesForCommits.items():
            if key.endswith(".py"):
                # print(" PYTHON FILE: ")
                retrievePythonCodeToParse(dataClass, contributor, key, val, increment)
            elif key.endswith(".md") or key.endswith(".txt") or key.endswith(".JSON"):
                # print(" TEXT OR JSON FILE:")
                retrieveTextCodeToParse(dataClass, contributor, key, val, increment)
            elif key.endswith(".html"):
                # print(" HTML FILES:")
                retrieveHTMLCodeToParse(dataClass, contributor, key, val, increment)



"""Accesses the value of the dictionaries which store the Python code, calls function to perform the classification and passes the results to be updated"""
def retrievePythonCodeToParse(dataClass, contributor, filename, valueList, increment):
    print(increment)
    for valItem in valueList:
        spaces, spacesWithoutIndent, newLines, emptyLines, totalLines, comments,  printStatementCount, loopCount, conditionCount, importCount, funcCount, classCount, classDefinition, viewCount, modelCount, formCount = performClassificationOnPythonInput(valItem)
        codeLines = (totalLines - comments) - emptyLines
        updateDataInResults(
            dataClass, 
            contributor, 
            increment, 
            spaces=spaces, 
            strippedSpaces=spacesWithoutIndent, 
            newLines=newLines, 
            emptyLines=emptyLines, 
            comments=comments, 
            codeLines=codeLines, 
            totalLines=totalLines,
            printStatementCount=printStatementCount,
            loopCount=loopCount,
            conditionCount=conditionCount,
            importCount=importCount,
            funcCount=funcCount,
            classCount=classCount,
            classDefinitionList = classDefinition, 
            viewCount = viewCount, 
            modelCount = modelCount, 
            formCount= formCount)
        # print(dataClass.resultsListSeparate)
        # print("\n")


"""Accesses the value of the dictionaries which store the text/JSON data, calls function to perform the classification and passes the results to be updated"""
def retrieveTextCodeToParse(dataClass, contributor, filename, valueList, increment):
    for valItem in valueList:
        spaces, spacesWithoutIndent, emptyLines, totalLines = performClassificationOnTextInput(valItem)
        updateDataInResults(
            dataClass, 
            contributor, 
            increment, 
            spaces=spaces, 
            strippedSpaces=spacesWithoutIndent, 
            emptyLines = emptyLines, 
            totalLines = totalLines)
        # print(dataClass.resultsListSeparate)
        # print("\n")


"""Accesses the value of the dictionaries which store the HTML code, calls function to perform the classification and passes the results to be updated"""
def retrieveHTMLCodeToParse(dataClass, contributor, filename, valueList, increment):
    for valItem in valueList:
        spaces, spacesWithoutIndent, newLines, emptyLines, totalLines, htmlComments, tagCountDict, templateTagCountDict, evalVars = performClassificationOnHTMLInput(valItem)
        codeLines = (totalLines - htmlComments) - emptyLines
        updateDataInResults(
            dataClass, 
            contributor, 
            increment, 
            spaces=spaces,
            strippedSpaces=spacesWithoutIndent, 
            newLines=newLines, 
            emptyLines=emptyLines, 
            HTMLcomments=htmlComments, 
            codeLines=codeLines, 
            totalLines=totalLines,
            HTMLtags = tagCountDict,
            HTMLtemplateTags = templateTagCountDict,
            HTMLevalVars = evalVars)
        # print(dataClass.resultsListSeparate)
        # print("\n")
        

def updateDataInResults(dataClass, contributor, increment, spaces = None, strippedSpaces =None, newLines = None, emptyLines = None, comments = None, 
                        codeLines = None, totalLines = None, printStatementCount = None, loopCount = None, conditionCount = None, importCount = None, 
                        funcCount = None, classCount = None, classDefinitionList = None, viewCount = None, modelCount = None, formCount= None,
                        HTMLcomments = None, HTMLtags=None, HTMLtemplateTags=None, HTMLevalVars=None):
    if increment == True: 
        additionsCategory = "additions"
        incrementResults(dataClass, contributor, "spaces", spaces, additionsCategory)
        incrementResults(dataClass, contributor, "spaces without indents", strippedSpaces, additionsCategory)
        incrementResults(dataClass, contributor, "new lines", newLines, additionsCategory)
        incrementResults(dataClass, contributor, "empty lines", emptyLines, additionsCategory)
        incrementResults(dataClass, contributor, "comment lines", comments, additionsCategory)
        incrementResults(dataClass, contributor, "code lines", codeLines, additionsCategory)
        incrementResults(dataClass, contributor, "total lines", totalLines, additionsCategory)
        incrementResults(dataClass, contributor, "print statements", printStatementCount, additionsCategory)
        incrementResults(dataClass, contributor, "conditionals", conditionCount, additionsCategory)
        incrementResults(dataClass, contributor, "loops", loopCount, additionsCategory)
        incrementResults(dataClass, contributor, "imports", importCount, additionsCategory)
        incrementResults(dataClass, contributor, "functions", funcCount, additionsCategory)
        incrementResults(dataClass, contributor, "class definitions", classCount, additionsCategory)
        incrementResults(dataClass, contributor, "class definitions list", None, additionsCategory, classDefinitionList=classDefinitionList)
        incrementResults(dataClass, contributor, "views", viewCount, additionsCategory)
        incrementResults(dataClass, contributor, "models", modelCount, additionsCategory)
        incrementResults(dataClass, contributor, "forms", formCount, additionsCategory)
        incrementResults(dataClass, contributor, "HTML comments", HTMLcomments, additionsCategory)
        incrementResults(dataClass, contributor, "HTML evaluation vars", HTMLevalVars, additionsCategory)
        incrementResults(dataClass, contributor, "HTML tags", None, additionsCategory, incrementTags= HTMLtags)
        incrementResults(dataClass, contributor, "HTML template tags", None, additionsCategory, incrementTemplateTags= HTMLtemplateTags)
        # print("INCREMENT")

    else: 
        deletionsCategory = "deletions"
        decrementResults(dataClass, contributor, "spaces", spaces, deletionsCategory)
        decrementResults(dataClass, contributor, "spaces without indents", strippedSpaces, deletionsCategory)
        decrementResults(dataClass, contributor, "new lines", newLines, deletionsCategory)
        decrementResults(dataClass, contributor, "empty lines", emptyLines, deletionsCategory)
        decrementResults(dataClass, contributor, "comment lines", comments, deletionsCategory)
        decrementResults(dataClass, contributor, "code lines", codeLines, deletionsCategory)
        decrementResults(dataClass, contributor, "total lines", totalLines, deletionsCategory)
        decrementResults(dataClass, contributor, "print statements", printStatementCount, deletionsCategory)
        decrementResults(dataClass, contributor, "conditionals", conditionCount, deletionsCategory)
        decrementResults(dataClass, contributor, "loops", loopCount, deletionsCategory)
        decrementResults(dataClass, contributor, "imports", importCount, deletionsCategory)
        decrementResults(dataClass, contributor, "functions", funcCount, deletionsCategory)
        decrementResults(dataClass, contributor, "class definitions", classCount, deletionsCategory)
        decrementResults(dataClass, contributor, "class definitions list", None, deletionsCategory, classDefinitionList=classDefinitionList)
        decrementResults(dataClass, contributor, "views", viewCount, deletionsCategory)
        decrementResults(dataClass, contributor, "models", modelCount, deletionsCategory)
        decrementResults(dataClass, contributor, "forms", formCount, deletionsCategory)
        decrementResults(dataClass, contributor, "HTML comments", HTMLcomments, deletionsCategory)
        decrementResults(dataClass, contributor, "HTML evaluation vars", HTMLevalVars, deletionsCategory)
        decrementResults(dataClass, contributor, "HTML tags", None, deletionsCategory, decrementTags= HTMLtags)
        decrementResults(dataClass, contributor, "HTML template tags", None, deletionsCategory, decrementTemplateTags= HTMLtemplateTags)
        # print("DECREMENT")


def incrementResults(dataClass, collaborator, option, incrementValue, category, incrementTags=None, incrementTemplateTags=None, classDefinitionList=None):
    if incrementValue:
        dataClass.incrementResultsDataByValue(collaborator, option, incrementValue, category)
    if incrementTags:
        dataClass.incrementHTMLtagsInResults(collaborator, option, incrementTags, category, dataClass.addedTags, dataClass.tags)
    if incrementTemplateTags:
        dataClass.incrementHTMLtagsInResults(collaborator, option, incrementTemplateTags, category, dataClass.addedTemplateTags,  dataClass.templateTags)
    if classDefinitionList:
        dataClass.appendClassDefinitionsListFromResults(collaborator, option, classDefinitionList, category, dataClass.addedClasses, dataClass.classesList)
        

def decrementResults(dataClass, collaborator, option, decrementValue, category, decrementTags=None, decrementTemplateTags=None, classDefinitionList=None):
    if decrementValue: 
    # increment the "deletions" category then decrement overall 
        dataClass.decrementResultsDataByValue(collaborator, option, decrementValue, category)
    if decrementTags:
        dataClass.decrementHTMLtagsInResults(collaborator, option, decrementTags, category, dataClass.deletedTags, dataClass.tags)
    if decrementTemplateTags:
        dataClass.decrementHTMLtagsInResults(collaborator, option, decrementTemplateTags, category, dataClass.deletedTemplateTags, dataClass.templateTags)
    if classDefinitionList:
        dataClass.removeClassDefinitionsListFromResults(collaborator, option, classDefinitionList, category, dataClass.deletedClasses, dataClass.classesList)
        


if __name__ == '__main__':
    globals()[sys.argv[1]]()
    