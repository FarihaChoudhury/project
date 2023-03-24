import json
import sys
from commitData import DataClass
from gitHubCommitRequest import getCollaboratorsOfFile
from textParse import filterFilenames
from gitHubCommitRequest import set_up, specificFileGitHubQuery, getGitHubResponse, convertGitHubResponseToJson, storeCollaboratorInList, retrieveCommitsSourceCodeIntoListOfDictionaries, getFilenamesList
# sys.path.insert(0, '../pythonParsing')
"""RUN FROM THIS FILE TO GET CODE CONTRIBUTION DATA"""


"""Gets the GitHub API response and stores relevant data into the DataClass and allCommitsInRepo.json file"""
def getCodeContributionOf(OWNER, REPO, BRANCH, accessToken):
    dataClassObject = DataClass()

    collaboratorsURL, commitURL, filesURL, headers = set_up(OWNER, REPO, BRANCH, accessToken)
    collaboratorsResponse = getGitHubResponse(collaboratorsURL, headers)
    allCommitsResponse = getGitHubResponse(commitURL, headers)
    allFilesResponse = getGitHubResponse(filesURL, headers)

    if (collaboratorsResponse and allCommitsResponse and allFilesResponse):
        collaborators = convertGitHubResponseToJson(collaboratorsResponse)
        commits = convertGitHubResponseToJson(allCommitsResponse)
        files = convertGitHubResponseToJson(allFilesResponse)

        """STORE IN DATA CLASS: """
        # Collaborators data: 
        dataClassObject.setCollaborators(collaborators = storeCollaboratorInList(collaborators))
        # All commits data:
        listOfDictionaryForCommits = retrieveCommitsSourceCodeIntoListOfDictionaries(commits, OWNER, REPO, headers)
        dataClassObject.setListOfDictionary(listOfDictionaryForCommits)
        # Filenames data:
        allFiles = getFilenamesList(files)
        dataClassObject.setFilenamesDictionaryKeys()
        contributorsOfEachFile(OWNER, REPO, allFiles, headers, dataClassObject)   
        
        """STORE IN JSON FILE: """
        storeDataInFile(listOfDictionaryForCommits)
        return dataClassObject
    else:
        sys.exit("Please try again as an error has occurred")


"""Calls on json query method to retrieve collaborators of each file in git repository
    - populates dictionary of collaborators for each file """
def contributorsOfEachFile(owner, repo, allFiles, headers, dataClassObject):
    for filename in allFiles:
        if filterFilenames(filename):
            specificFileURL = specificFileGitHubQuery(owner, repo, filename)
            specificFileResponse = getGitHubResponse(specificFileURL, headers)
            if specificFileResponse:
                file = convertGitHubResponseToJson(specificFileResponse)
                collaboratorsOfFileList = getCollaboratorsOfFile(file)
                for collaborator in collaboratorsOfFileList:
                    # Sets the filenames to collaborator who edited it
                    dataClassObject.setFilenamesDictionaryValues(collaborator, filename)
            else:
                sys.exit("Error occurred, please try again.")


"""Saves content of the list of dictionaries onto a allCommitsInRepo.json file"""     
def storeDataInFile(listOfDictionaryForCommits):
    with open('allCommitsInRepo.json', 'w') as file:
        json.dump(listOfDictionaryForCommits, file)
    



if __name__ == '__main__':
    # allows you to call codeContributionOf from terminal 
    globals()[sys.argv[1]]()
    # RUN: python3 usingRequests.py codeContributionOf

