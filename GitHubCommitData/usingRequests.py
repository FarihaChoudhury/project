import sys


# sys.path.insert(0, '../pythonParsing')
from gitHubCommitRequest import set_up, getGitHubCommitData, convertGitHubResponseToJson, storeCollaboratorInList, storeCommitsInListOfDictionaries, storeDataInFile



def codeContributionOf():
    OWNER = "FarihaChoudhury"
    REPO = "PublicRepoTest"
    accessToken = "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"

    collaboratorsURL, commitURL, headers = set_up(OWNER, REPO, accessToken)

    collaboratorsResponse, allCommitsResponse = getGitHubCommitData(collaboratorsURL, commitURL, headers)

    collaborators, commits = convertGitHubResponseToJson(collaboratorsResponse, allCommitsResponse)

    collaboratorsList = storeCollaboratorInList(collaborators)

    listOfDictionary = storeCommitsInListOfDictionaries(commits, OWNER, REPO, headers)

    storeDataInFile(listOfDictionary)



if __name__ == '__main__':
    # allows you to call codeContributionOf from terminal 
    globals()[sys.argv[1]]()
    # RUN: python3 usingRequests.py codeContributionOf

