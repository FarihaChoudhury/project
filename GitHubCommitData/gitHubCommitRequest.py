import requests 
import json

"""Sets up GitHub API querying with access tokens and creating the URLs to query
    - returns the URL to retrieve collaborators data and commit data for a single repository
"""
def set_up(owner, repo, accessToken):
    # Set the personal access token and HTTP headers: replace with your own

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {accessToken}"
    }

    # replace owner and repository name by repository you wish to query
    OWNER = owner     # OWNER = "FarihaChoudhury"
    REPO = repo       # REPO = "PublicRepoTest"
    # REF_SHA = "a19b766" # Last commit made

    # COLLABORATORS DATA: name and repository ID
    collaboratorsURL = "https://api.github.com/repos/" + OWNER + "/" + REPO + "/collaborators"
    commitURL = "https://api.github.com/repos/" + OWNER + "/" + REPO + "/commits"
   
    return collaboratorsURL, commitURL, headers



"""Retrieves the collaborators and commit details of a single repository"""
def getGitHubCommitData(collaboratorsURL, commitURL, headers):
    collaboratorsResponse = requests.get(collaboratorsURL, headers=headers)
    allCommitsResponse = requests.get(commitURL)
    
    return collaboratorsResponse, allCommitsResponse


"""Converts the GitHub API response into JSON format"""
def convertGitHubResponseToJson(collaboratorsResponse, allCommitsResponse):
    collaborators = collaboratorsResponse.json()
    commits = allCommitsResponse.json()

    return collaborators, commits


"""Store GitHub API collaborators response in a list"""
def storeCollaboratorInList(collaborators):
    collaboratorsList = []

    for i in range(len(collaborators)):
        collaboratorsList.append(collaborators[i]["login"])
        # collaboratorsList.append(collaborators[i]["id"])    to include collaborator unique id

    print("All collaborators:")
    print(collaboratorsList)
    print("\n")

    return collaboratorsList


"""Store GitHub API commit response in a list of dictionaries"""
def storeCommitsInListOfDictionaries(allCommits, OWNER, REPO, headers):
    listOfDictionary = [{} for x in range(len(allCommits))]
    # EACH COMMIT DATA:
    for i in range(len(allCommits)):
        commitSha = allCommits[i]['sha']
        commitAuthor = allCommits[i]['commit']['author']['name']

        specificCommitUrl = "https://api.github.com/repos/" + OWNER + "/" + REPO + "/commits/" + commitSha
        specificCommitResponse = requests.get(specificCommitUrl, headers=headers)
        commit = specificCommitResponse.json()

        additionsList = []
        deletionsList = []
        allCommitLinesList = []
        allCommitCodeListAsOneString = []
        filenames = []

        for file in commit["files"]:
            filenames = file['filename']
            patchCode = file["patch"]  # string contains code for whole file, includes the initial @@ -1,3 +1,6 @@ (AKA 'diff')

            # Remove: @@ .... @@
            newLineSymbol = "\n"
            parts = patchCode.split(newLineSymbol, 1)
            if len(parts) > 1:
                patchCode = parts[1]
            # print(patchCode)

            # splits patchCode into lines:
            lines = patchCode.split("\n")  # list of each line of code from whole commit file, includes '@@ -1,3 +1,6 @@'

            # Populate each additions line into
            for j in range(len(lines)):
                if lines[j].startswith("+"):
                    additionsList.append(lines[j][1:])    # [1:]removes the +/ - from beginning of lines
                if lines[j].startswith("-"):
                    deletionsList.append(lines[j][1:])
                else:
                    allCommitLinesList.append(lines[j][1:])   #  add all lines from commit file

        allCommitCodeListAsOneString = "\n".join(allCommitLinesList)

        # Populating list of dictionaries: for each commit made-
        listOfDictionary[i]["commitAuthor"] = commitAuthor
        listOfDictionary[i]["commitSha"] = commitSha
        listOfDictionary[i]["filesEdited"] = filenames
        listOfDictionary[i]["commitFileLinesAsList"] = allCommitLinesList  # separates lines into items of list
        listOfDictionary[i]["pythonCode"] = allCommitCodeListAsOneString
        listOfDictionary[i]["additions"] = additionsList
        listOfDictionary[i]["deletions"] = deletionsList

    print("List of dictionary:")
    # print each index with space between:
    for i in range(len(listOfDictionary)):
        print(listOfDictionary[i])
        print("\n")

    return listOfDictionary


def storeDataInFile(listOfDictionary):
    # Saves content of each commit into a text file
    with open("commitDataForRepo.txt", 'w') as file:
        for commit in listOfDictionary:
            file.write(str(commit))
            file.write("\n")


    # Saves content of all commits (list of dictionaries) into a JSON
    with open('allCommitsInRepo.json', 'w') as file:
        json.dump(listOfDictionary, file)


    




