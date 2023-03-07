import json
import sys
from CommitData import dataClass
from gitHubCommitRequest import getCollaboratorsOfFile
"""RUN FROM THIS FILE TO GET CODE CONTRIBUTION DATA"""

# sys.path.insert(0, '../pythonParsing')
from gitHubCommitRequest import set_up, specifcFileGitHubQuery, getGitHubResponse, convertGitHubResponseToJson, storeCollaboratorInList, storeCommitsInListOfDictionaries, getFilenamesList


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
    collaboratorsResponse = getGitHubResponse(collaboratorsURL, headers)
    # allCommitsResponse = getGitHubResponse(commitURL)
    allCommitsResponse = getGitHubResponse(commitURL, headers)
    allFilesResponse = getGitHubResponse(filesURL, headers)
    # collaboratorsResponse, allCommitsResponse, allFilesResponse = getGitHubCommitData(collaboratorsURL, commitURL, filesURL, specificFileURL, headers)

    # CONVERT TO JSON!
    collaborators = convertGitHubResponseToJson(collaboratorsResponse)
    commits = convertGitHubResponseToJson(allCommitsResponse)
    files = convertGitHubResponseToJson(allFilesResponse)
    # collaborators, commits = convertGitHubResponseToJson(collaboratorsResponse, allCommitsResponse)


    """STORE IN DATA CLASS: """
    # COLLABORATORS: 
    dataClassObject.setCollaborators(collaborators = storeCollaboratorInList(collaborators))

    # LIST OF DICTIONARY
    # listOfDictionary, size = storeCommitsInListOfDictionaries(commits, OWNER, REPO, headers)
    listOfDictionary = storeCommitsInListOfDictionaries(commits, OWNER, REPO, headers)

    # dataClassObject.createListOfDictionary(size)
    dataClassObject.setListOfDictionary(listOfDictionary)

    """FILE NAMES DATA"""
    allFiles = getFilenamesList(files)
    dataClassObject.setFilenamesDictionaryKeys()
    contributorsOfEachFile(OWNER, REPO, allFiles, headers, dataClassObject)   

    listOfDictionary.append(REPO)
    # STORE TO FILES: 'allCommitsInRepo.json 
    jsonFile = storeDataInFile(listOfDictionary, 'allCommitsInRepo.json')

    listOfDictionary.pop()
    # jsomFile = storeDataInFile(REPO, 'repositoryInfo.json')
    # openJsonFile(jsonFile)

    return dataClassObject



"""Calls on json query method to retrieve collaborators of each file in git repository
    - populates dictionary of collaborators for each file """
def contributorsOfEachFile(owner, repo, allFiles, headers, dataClassObject):
    for filename in allFiles:
        # print(filename)
        specificFileURL = specifcFileGitHubQuery(owner, repo, filename)
        specificFileResponse = getGitHubResponse(specificFileURL, headers)
        file = convertGitHubResponseToJson(specificFileResponse)
        collaboratorsOfFileList = getCollaboratorsOfFile(file)
        # print(collaboratorsOfFileList)

        for collaborator in collaboratorsOfFileList:
            dataClassObject.setFilenamesDictionaryValues(collaborator, filename)


"""Saves content of the list of dictionaries onto a .JSON file"""     
def storeDataInFile(listOfDictionary, filename):
    # Saves content of all commits (list of dictionaries) into a JSON
    with open(filename, 'w') as file:
        json.dump(listOfDictionary, file)
    
    return 'allCommitsInRepo.json'


"""Opens JSON file and prints its content for the last commit made [0]"""
def openJsonFile(jsonFile):
    print("JSON FILE: ")
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



if __name__ == '__main__':
    # allows you to call codeContributionOf from terminal 
    globals()[sys.argv[1]]()
    # RUN: python3 usingRequests.py codeContributionOf

