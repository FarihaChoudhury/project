import json
import sys


"""calls on additions for files in all commits and deletions for files in all commits"""
def readAdditionsAndDeletions():
    readAdditionsForFilesInAllCommits()
    readDeletionsForFilesInAllCommits()

"""Opens JSON file and prints its content for the last commit made"""
# allCommitsInRepo.json 
# def openJsonFile(jsonFile):
def openJsonFile():
    jsonFile = "allCommitsInRepo.json"
    print("JSON FILE: ")
    # with open('allCommitsInRepo.json', 'r') as file:
    with open(jsonFile, 'r') as file:
        commitData = json.load(file)

    # for i in range(len(commitData)):
    #     print("\n")
    #     print(commitData[i]['commitAuthor'])
    #     print(commitData[i]['filesEdited'])
    #     # print(d[0]['pythonCode'])
    #     # print(d[0]['additions'])
    #     print(commitData[i]["additionsPerFile"])
    #     # print(d[0]['deletions'])
    #     print(commitData[i]["deletionsPerFile"])
    print("\n")
    print("look:")
    readAdditionsForFilesInAllCommits()
    # print("\n")
    # print(d[0]['commitAuthor'])
    # print(d[0]['filesEdited'])
    # # print(d[0]['pythonCode'])
    # # print(d[0]['additions'])
    # print(d[0]["additionsPerFile"])
    # # print(d[0]['deletions'])
    # print(d[0]["deletionsPerFile"])


"""Reads the additionsPerFile item in the list of dictionaries of all commits made in a repository"""
def readAdditionsForFilesInAllCommits():
    jsonFile = "allCommitsInRepo.json"
    with open(jsonFile, 'r') as file:
        commitData = json.load(file)

    additions = []
    for i in range(len(commitData)):
        # add all additions for all commits into one list
        additions.append(commitData[i]["additionsPerFile"][0])
    # call function to differentiate code types: python, html, text 
    differentiateCodeTypes(additions)
    return additions



"""Takes a list which contains dictionary items and checks the keys of these items
    - if the key holds a Python file, text file or HTML file, the necessary classifications will be called on the values """
def differentiateCodeTypes(listOfDictionariesForCommits): 
    for i in range(len(listOfDictionariesForCommits)):    
        # iterates each item of the list of dictionaries by the key and value 
        for key, val in listOfDictionariesForCommits[i][0].items():
            # print(key)
            if key.endswith(".py"):
                print("PYTHON FILE: ")
                print(key)
                retrievePythonCodeToParse(val)
            elif key.endswith(".md") or key.endswith(".txt"):
                print("TEXT FILE:")
                print(key)
                retrieveTextCodeToParse(val)
            elif key.endswith(".html"):
                print("HTML FILES:")
                print(key)
                retrieveHTMLCodeToParse(val)


"""Accesses the value of the dictionaries which store the Python code"""
def retrievePythonCodeToParse(valueList):
    for val in valueList:
        print(val)
        # CALL PYTHON PARSER!!!

"""Accesses the value of the dictionaries which store the text"""
def retrieveTextCodeToParse(valueList):
    for val in valueList:
        print(val)
        # CALL TEXT PARSER!!!

"""Accesses the value of the dictionaries which store the HTML code"""
def retrieveHTMLCodeToParse(valueList):
    for val in valueList:
        print(val)
        # CALL HTML PARSER!!!



"""Reads the deletionsPerFile item in the list of dictionaries of all commits made in a repository"""
def readDeletionsForFilesInAllCommits():
    jsonFile = "allCommitsInRepo.json"
    with open(jsonFile, 'r') as file:
        commitData = json.load(file)

    deletions = []
    for i in range(len(commitData)):
        # add all deletions for all commits into one list
        deletions.append(commitData[i]["deletionsPerFile"][0])
    # call function to differentiate code types: python, html, text 
    differentiateCodeTypes(deletions)
    return deletions


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
