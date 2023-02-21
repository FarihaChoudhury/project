import json
import sys
from CommitData import dataClass
from gitHubCommitRequest import getCollaboratorsOfFile
"""RUN FROM THIS FILE TO GET CODE CONTRIBUTION DATA"""

# sys.path.insert(0, '../pythonParsing')
from gitHubCommitRequest import set_up, specifcFileGitHubQuery, getGitHubResponseWithHeaders, getGitHubResponse, convertGitHubResponseToJson, storeCollaboratorInList, storeCommitsInListOfDictionaries, storeDataInFile, getFilenamesList


    # # FOR CONTRIBUTORS OF SPECIFIC FILE:
    # print("\n collaborators of specific file")
    # specificFileResponse = requests.get(specificFileURL)
    # specificFileContent = specificFileResponse.json()
    # for i in range(len(specificFileContent)):
    #     print(specificFileContent[i]["author"]["login"])

    # print(specificFileContent[])


def codeContributionOf():
    dataClassObject = dataClass()
    OWNER = "FarihaChoudhury"
    REPO = "PublicRepoTest"
    # accessToken = "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"
    accessToken =  "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"

    collaboratorsURL, commitURL, filesURL, headers = set_up(OWNER, REPO, accessToken)

    # DO GET ON GITHUB API:
    collaboratorsResponse = getGitHubResponseWithHeaders(collaboratorsURL, headers)
    # allCommitsResponse = getGitHubResponse(commitURL)
    allCommitsResponse = getGitHubResponseWithHeaders(commitURL, headers)
    allFilesResponse = getGitHubResponseWithHeaders(filesURL, headers)
    # collaboratorsResponse, allCommitsResponse, allFilesResponse = getGitHubCommitData(collaboratorsURL, commitURL, filesURL, specificFileURL, headers)

    # CONVERT TO JSON!
    collaborators = convertGitHubResponseToJson(collaboratorsResponse)
    commits = convertGitHubResponseToJson(allCommitsResponse)
    files = convertGitHubResponseToJson(allFilesResponse)
    # collaborators, commits = convertGitHubResponseToJson(collaboratorsResponse, allCommitsResponse)


    """STORE IN DATA CLASS: """
    # COLLABORATORS: 
    dataClass.setCollaborators(dataClass, collaborators = storeCollaboratorInList(collaborators))
    # print("FROM CLASS:")
    # print(dataClass.collaboratorsList)

    # LIST OF DICTIONARY
    listOfDictionary, size = storeCommitsInListOfDictionaries(commits, OWNER, REPO, headers)
    # print("test1 from function")
    # print(listOfDictionary)

    dataClass.createListOfDictionary(dataClass, size)
    dataClass.setListOfDictionary(dataClass, listOfDictionary)
    # print("\n test from class:")
    # print(dataClass.listOfDictionary)

    """FILE NAMES DATA"""
    allFiles = getFilenamesList(files)
    dataClass.setFilenamesDictionaryKeys(dataClass)
    contributorsOfEachFile(OWNER, REPO, allFiles, headers)
    print("All filenames:")
    print(dataClass.filenamesDictionary)    

    
    # STORE TO FILES:  'commitDataForRepo.txt', 'allCommitsInRepo.json 
    textFile, jsonFile = storeDataInFile(dataClass.listOfDictionary)
    # openJsonFile(jsonFile)

    return dataClassObject



"""Calls on json query method to retrieve collaborators of each file in git repository
    - populates dictionary of collaborators for each file """
def contributorsOfEachFile(owner, repo, allFiles, headers):
    for filename in allFiles:
        # print(filename)
        specificFileURL = specifcFileGitHubQuery(owner, repo, filename)
        specificFileResponse = getGitHubResponseWithHeaders(specificFileURL, headers)
        file = convertGitHubResponseToJson(specificFileResponse)
        collaboratorsOfFileList = getCollaboratorsOfFile(file)
        # print(collaboratorsOfFileList)

        for collaborator in collaboratorsOfFileList:
            dataClass.setFilenamesDictionaryValues(dataClass, collaborator, filename)



"""Opens JSON file and prints its content for the last commit made"""
def openJsonFile(jsonFile):
    print("JSON FILE: ")
    # with open('allCommitsInRepo.json', 'r') as file:
    with open(jsonFile, 'r') as file:
        d = json.load(file)
        # print(d)

    print("\n")
    print(d[0]['commitAuthor'])
    print(d[0]['filesEdited'])
    # print(d[0]['pythonCode'])
    print(d[0]['additions'])
    print(d[0]["additionsPerFile"])
    print(d[0]['deletions'])
    print(d[0]["deletionsPerFile"])

    # dictionary = dictionaryToHoldFilenames()
    # countFilenames(jsonFile, dictionary)
    # countFilenames(jsonFile)



# def dictionaryToHoldFilenames():
#     dictionary = {}
#     for i in range (len(dataClass.collaboratorsList)) : 
#         dictionary[dataClass.collaboratorsList[i]] = set()
    
#     print(dictionary)
#     return dictionary 

# def countFilenames(jsonFile, dictionary):
#     print("\n filenames")
#     with open(jsonFile, 'r') as file:
#         d = json.load(file)

#     for i in range(len(d)):
#         dictionary[d[i]['commitAuthor']].add(d[i]['filesEdited'])


#     print(dictionary)

            # for j in range (len(dataClass.collaboratorsList)):
            #     if d[i]['commitAuthor'] == dataClass.collaboratorsList[j]:
            #         print(d[i]['commitAuthor'])
            #         print("fin^")
            #     # else:
            #     #     print("1")
            #     #     print(d[i]['commitAuthor'])
            #     #     print("2")
            #     #     print(dataClass.collaboratorsList[j])
            # # print(d[i]['commitAuthor'])
            # # print(d[i]['filesEdited'])
        # print("\n")



if __name__ == '__main__':
    # allows you to call codeContributionOf from terminal 
    globals()[sys.argv[1]]()
    # RUN: python3 usingRequests.py codeContributionOf

