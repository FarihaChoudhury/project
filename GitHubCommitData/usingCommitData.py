import json
import os
import sys
sys.path.insert(0, '../Classification/Parsing/pythonParsing')
sys.path.insert(0, '../Classification/Parsing/htmlParsing')
sys.path.insert(0, '../Classification/Parsing/textParsing')
sys.path.insert(0, '../Classification/Parsing/antlrParserGeneratedCode')
from pythonParse import performClassificationOnPythonInput
from textParse import performClassificationOnTextInput
from htmlParse import performClassificationOnHTMLInput


""" Converts a set into a list object for JSON serialize purposes"""
def jsonSetSerializer(setObject):
    if isinstance(setObject, set):
        return list(setObject)
    return setObject
    
    
"""Controls the receiving of stored commit data for classifications and storing of the results into the results.json file  """
def getClassificationsResults(dataClass, REPO):
    setUpClassificationsResults(dataClass)
    
    readAdditionsFromClass(dataClass)
    readDeletionsFromClass(dataClass)
    
    storeJSONresults(dataClass, REPO)


""" Sets up base template for results in the dataClass """
def setUpClassificationsResults(dataClass):
    dataClass.createResultsTemplateSeparate()


""" Stores results on a JSON file
    - Must change sets to lists for JSON compatibility; convert set of filenames to list """
def storeJSONresults(dataClass, REPO):
    for i in range(len(dataClass.resultsListSeparate)):
        if dataClass.resultsListSeparate[i].items(): 
            for key, val in dataClass.resultsListSeparate[i].items():
                # change the filenames set to list:
                dataClass.resultsListSeparate[i][key]["files edited"] = jsonSetSerializer(dataClass.resultsListSeparate[i][key]["files edited"])
    # store results to json file
    dataClass.resultsListSeparate.append(REPO)
    with open(os.path.join('../ResultsForCommitData', 'results.json'), "w") as file:
        json.dump(dataClass.resultsListSeparate, file)


""" Reads the additionsPerFile item in the list of dictionaries of all commits made in a repository
    Then calls on classifications on retrieved additions"""
def readAdditionsFromClass(dataClass):
    commitData = dataClass.listOfDictionaryForCommits
    additions = []
    for i in range(len(commitData)):
        if (commitData[i]["additionsPerFile"][0]):
            contributor = commitData[i]["commitAuthor"]
            additions = commitData[i]["additionsPerFile"][0]
            differentiateCodeTypes(dataClass, contributor, additions, True)
    return additions


""" Reads the deletionsPerFile item in the list of dictionaries of all commits made in a repository
    Then calls on classifications on retrieved deletions"""
def readDeletionsFromClass(dataClass):
    commitData = dataClass.listOfDictionaryForCommits
    deletions = []
    for i in range(len(commitData)):
        if (commitData[i]["deletionsPerFile"][0]):
            contributor = commitData[i]["commitAuthor"]
            deletions = commitData[i]["deletionsPerFile"][0]
            differentiateCodeTypes(dataClass, contributor, deletions, False)
    return deletions


""" Takes a list which contains dictionary items and checks the keys of these items.
    Based on file type, corresponding classifications take place """
def differentiateCodeTypes(dataClass, contributor, listOfDictionariesForCommits, increment): 
    if listOfDictionariesForCommits.items(): 
        for key, val in listOfDictionariesForCommits.items():
            if key.endswith(".py"):
                retrievePythonCodeToParse(dataClass, contributor, val, increment)
            elif key.endswith(".md") or key.endswith(".txt") or key.endswith(".JSON"):
                retrieveTextCodeToParse(dataClass, contributor, val, increment)
            elif key.endswith(".html"):
                retrieveHTMLCodeToParse(dataClass, contributor, val, increment)


""" Accesses the value of the dictionaries which store the Python code, calls function to perform the classification,
    passes the results to be updated"""
def retrievePythonCodeToParse(dataClass, contributor, valueList, increment):
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


""" Accesses the value of the dictionaries which store the text/JSON data, calls function to perform the classification,
    passes the results to be updated"""
def retrieveTextCodeToParse(dataClass, contributor, valueList, increment):
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


""" Accesses the value of the dictionaries which store the HTML code, calls function to perform the classification,
    passes the results to be updated"""
def retrieveHTMLCodeToParse(dataClass, contributor, valueList, increment):
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
        

""" Given classification results obtained for each line of code parsed, updates the corresponding categories for collaborator """
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
        incrementResults(dataClass, contributor, "function definitions", funcCount, additionsCategory)
        incrementResults(dataClass, contributor, "class definitions", classCount, additionsCategory)
        incrementResults(dataClass, contributor, "class definitions list", None, additionsCategory, classDefinitionList=classDefinitionList)
        incrementResults(dataClass, contributor, "views", viewCount, additionsCategory)
        incrementResults(dataClass, contributor, "models", modelCount, additionsCategory)
        incrementResults(dataClass, contributor, "forms", formCount, additionsCategory)
        incrementResults(dataClass, contributor, "HTML comments", HTMLcomments, additionsCategory)
        incrementResults(dataClass, contributor, "HTML evaluation vars", HTMLevalVars, additionsCategory)
        incrementResults(dataClass, contributor, "HTML tags", None, additionsCategory, incrementTags= HTMLtags)
        incrementResults(dataClass, contributor, "HTML template tags", None, additionsCategory, incrementTemplateTags= HTMLtemplateTags)

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
        decrementResults(dataClass, contributor, "function definitions", funcCount, deletionsCategory)
        decrementResults(dataClass, contributor, "class definitions", classCount, deletionsCategory)
        decrementResults(dataClass, contributor, "class definitions list", None, deletionsCategory, classDefinitionList=classDefinitionList)
        decrementResults(dataClass, contributor, "views", viewCount, deletionsCategory)
        decrementResults(dataClass, contributor, "models", modelCount, deletionsCategory)
        decrementResults(dataClass, contributor, "forms", formCount, deletionsCategory)
        decrementResults(dataClass, contributor, "HTML comments", HTMLcomments, deletionsCategory)
        decrementResults(dataClass, contributor, "HTML evaluation vars", HTMLevalVars, deletionsCategory)
        decrementResults(dataClass, contributor, "HTML tags", None, deletionsCategory, decrementTags= HTMLtags)
        decrementResults(dataClass, contributor, "HTML template tags", None, deletionsCategory, decrementTemplateTags= HTMLtemplateTags)


""" Calls DataClass to increment its additions and overall with the classification results for a collaborator """
def incrementResults(dataClass, collaborator, option, incrementValue, category, incrementTags=None, incrementTemplateTags=None, classDefinitionList=None):
    if incrementValue:
        dataClass.incrementResultsDataByValue(collaborator, option, incrementValue, category)
    if incrementTags:
        dataClass.updateHTMLtagsInResults(collaborator, option, incrementTags, category, "+")
    if incrementTemplateTags:
        dataClass.updateHTMLtagsInResults(collaborator, option, incrementTemplateTags, category, "+")
    if classDefinitionList:
        dataClass.updateListInResults(collaborator, option, classDefinitionList, category, "+")
        
        
""" Calls DataClass to decrement its deletions and update its overall with the classification results for a collaborator """
def decrementResults(dataClass, collaborator, option, decrementValue, category, decrementTags=None, decrementTemplateTags=None, classDefinitionList=None):
    if decrementValue: 
        dataClass.decrementResultsDataByValue(collaborator, option, decrementValue, category)
    if decrementTags:
        dataClass.updateHTMLtagsInResults(collaborator, option, decrementTags, category, "-")
    if decrementTemplateTags:
        dataClass.updateHTMLtagsInResults(collaborator, option, decrementTemplateTags, category, "-")
    if classDefinitionList:
        dataClass.updateListInResults(collaborator, option, classDefinitionList, category, "-")
    