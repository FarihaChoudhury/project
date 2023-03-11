import json
import sys
from CommitData import DataClass
from gitHubCommitRequest import getCollaboratorsOfFile
from textParse import filterFilenames
from gitHubCommitRequest import set_up, specificFileGitHubQuery, getGitHubResponse, convertGitHubResponseToJson, storeCollaboratorInList, storeCommitsInListOfDictionaries, getFilenamesList
# sys.path.insert(0, '../pythonParsing')
"""RUN FROM THIS FILE TO GET CODE CONTRIBUTION DATA"""


def getCodeContributionOf(OWNER, REPO, accessToken):
    dataClassObject = DataClass()

    collaboratorsURL, commitURL, filesURL, headers = set_up(OWNER, REPO, accessToken)

    # DO GET ON GITHUB API:
    collaboratorsResponse = getGitHubResponse(collaboratorsURL, headers)
    allCommitsResponse = getGitHubResponse(commitURL, headers)
    allFilesResponse = getGitHubResponse(filesURL, headers)

    if (collaboratorsResponse and allCommitsResponse and allFilesResponse):
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
        # listOfDictionaryForCommits, size = storeCommitsInListOfDictionaries(commits, OWNER, REPO, headers)
        listOfDictionaryForCommits = storeCommitsInListOfDictionaries(commits, OWNER, REPO, headers)

        # dataClassObject.createListOfDictionary(size)
        dataClassObject.setListOfDictionary(listOfDictionaryForCommits)

        """FILE NAMES DATA"""
        allFiles = getFilenamesList(files)
        dataClassObject.setFilenamesDictionaryKeys()
        contributorsOfEachFile(OWNER, REPO, allFiles, headers, dataClassObject)   

        listOfDictionaryForCommits.append(REPO)
        # STORE TO FILES: 'allCommitsInRepo.json 
        jsonFile = storeDataInFile(listOfDictionaryForCommits, 'allCommitsInRepo.json')

        listOfDictionaryForCommits.pop()
        # jsomFile = storeDataInFile(REPO, 'repositoryInfo.json')
        # openJsonFile(jsonFile)

        return dataClassObject
    else:
        print("Please try again as an error has occurred")
        sys.exit()


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
                    dataClassObject.setFilenamesDictionaryValues(collaborator, filename)
            else:
                print("Please try again as an error has occurred")
                sys.exit()

"""Saves content of the list of dictionaries onto a .JSON file"""     
def storeDataInFile(listOfDictionaryForCommits, filename):
    # Saves content of all commits (list of dictionaries) into a JSON
    with open(filename, 'w') as file:
        json.dump(listOfDictionaryForCommits, file)
    
    return 'allCommitsInRepo.json'


# """Opens JSON file and prints its content for the last commit made [0]"""
# def openJsonFile(jsonFile):
#     print("JSON FILE: ")
#     with open(jsonFile, 'r') as file:
#         d = json.load(file)
#         # print(d)

#     print("\n")
#     print(d[0]['commitAuthor'])
#     print(d[0]['filesEdited'])
#     # print(d[0]['pythonCode'])
#     print(d[0]['additions'])
#     print(d[0]["additionsPerFile"])
#     print(d[0]['deletions'])
#     print(d[0]["deletionsPerFile"])



if __name__ == '__main__':
    # allows you to call codeContributionOf from terminal 
    globals()[sys.argv[1]]()
    # RUN: python3 usingRequests.py codeContributionOf

