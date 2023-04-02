import json
import sys
from commitData import DataClass
from gitHubCommitRequest import getCollaboratorsOfFile
from textParse import filterFilenames
from gitHubCommitRequest import set_up, specificFileGitHubQuery, getGitHubResponse, convertGitHubResponseToJson, storeCollaboratorInList, retrieveCommitsSourceCodeIntoListOfDictionaries, getFilenamesList
""" Retrieves code contribution data by interacting with gitHubCommitRequests.py, and stores into DataClass in commitData.py """


""" Gets the GitHub API response and stores relevant data into the DataClass and allCommitsInRepo.json file """
def getCodeContributionOf(OWNER, REPO, BRANCH, accessToken):
    dataClass = DataClass()

    collaboratorsURL, commitURL, filesURL, headers = set_up(OWNER, REPO, BRANCH, accessToken)
    collaboratorsResponse = getGitHubResponse(collaboratorsURL, headers)
    allCommitsResponse = getGitHubResponse(commitURL, headers)
    allFilesResponse = getGitHubResponse(filesURL, headers)

    if (collaboratorsResponse and allCommitsResponse and allFilesResponse):
        collaborators = convertGitHubResponseToJson(collaboratorsResponse)
        commits = convertGitHubResponseToJson(allCommitsResponse)
        files = convertGitHubResponseToJson(allFilesResponse)

        """ Store in DataClass: collaborators data, all commits, filenames """
        dataClass.setCollaborators(collaborators = storeCollaboratorInList(collaborators))
        listOfDictionaryForCommits = retrieveCommitsSourceCodeIntoListOfDictionaries(commits, OWNER, REPO, headers)
        dataClass.setListOfDictionary(listOfDictionaryForCommits)
        allFiles = getFilenamesList(files)
        dataClass.setFilenamesDictionaryKeys()
        contributorsOfEachFile(OWNER, REPO, allFiles, headers, dataClass)   
        
        """ Store in JSON file: """
        storeDataInFile(listOfDictionaryForCommits)
        return dataClass
    else:
        sys.exit("Please try again as an error has occurred")


""" Calls on json query method to retrieve collaborators of each file in GitHub repository
    - populates dictionary of collaborators for each file """
def contributorsOfEachFile(owner, repo, allFiles, headers, dataClass):
    for filename in allFiles:
        if filterFilenames(filename):
            specificFileURL = specificFileGitHubQuery(owner, repo, filename)
            specificFileResponse = getGitHubResponse(specificFileURL, headers)
            if specificFileResponse:
                file = convertGitHubResponseToJson(specificFileResponse)
                collaboratorsOfFileList = getCollaboratorsOfFile(file)
                for collaborator in collaboratorsOfFileList:
                    # Sets the filenames to collaborator who edited it
                    dataClass.setFilenamesDictionaryValues(collaborator, filename)
            else:
                sys.exit("Error occurred, please try again.")


""" Saves content of the list of dictionaries onto a allCommitsInRepo.json file """     
def storeDataInFile(listOfDictionaryForCommits):
    with open('allCommitsInRepo.json', 'w') as file:
        json.dump(listOfDictionaryForCommits, file)

