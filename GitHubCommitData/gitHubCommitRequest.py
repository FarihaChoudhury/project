import sys
import requests 
import json
from textParse import filterFilenames

""" Sets up GitHub API querying with access tokens and creating the URLs to query
    - returns the URL to retrieve collaborators data and commit data for a single repository """
def set_up(owner, repo, branch, accessToken):
    # Set the personal access token and HTTP headers: replace with your own

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {accessToken}"
    }

    OWNER = owner
    REPO = repo 
    BRANCH = branch
    
    collaboratorsURL = "https://api.github.com/repos/" + OWNER + "/" + REPO + "/collaborators"
    commitURL = "https://api.github.com/repos/" + OWNER + "/" + REPO + "/commits"
    filesURL =  "https://api.github.com/repos/"+ OWNER + "/" + REPO +"/git/trees/"+ BRANCH +"?recursive=1"
   
    return collaboratorsURL, commitURL, filesURL, headers


""" Creates URL to query a specific file """
def specificFileGitHubQuery(owner, repo, filename):
    OWNER = owner 
    REPO = repo 
    PATH = filename
    specificFileURL = "http://api.github.com/repos/" + OWNER + "/" + REPO + "/commits?path="+PATH
    return specificFileURL


""" Conducts the API get command with provided url and returns its response, takes headers as an optional parameter
    - Exits with error displayed to users if HTTP request is unsuccessful """
def getGitHubResponse(url, headers=None):
    try:
        if headers: 
            response = requests.get(url, headers=headers)
        else:
            response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as error:
        sys.exit("HTTP Error occurred, please check the error and try again:   " + repr(error))
    except requests.exceptions.ConnectionError as error:
        sys.exit("HTTP Error occurred, please check the error and try again:   " + repr(error))
    except requests.exceptions.RequestException as error:
        sys.exit("HTTP Error occurred, please check the error and try again:   " + repr(error))
        


""" Converts the GitHub API response into JSON format """
def convertGitHubResponseToJson(response):
    jsonResponse = response.json()
    return jsonResponse

""" Query all file names to return list of all filenames """
def getFilenamesList(files):
    allFiles = []
    for file in files["tree"]:
         allFiles.append(file["path"])
    return allFiles

""" Retrieves all collaborators of a specified file, as a list """
def getCollaboratorsOfFile(file):
    collaboratorsOfFile = []
    for i in range(len(file)):
        collaboratorsOfFile.append(file[i]["author"]["login"])
    return collaboratorsOfFile

""" Store GitHub API collaborators response in a list """
def storeCollaboratorInList(collaborators):
    collaboratorsList = []  
    for i in range(len(collaborators)):
        collaboratorsList.append(collaborators[i]["login"])
    return collaboratorsList


""" Prints all collaborators in given repository to terminal """
def printCollaborators(collaboratorsList):
    print("All collaborators:")
    print(collaboratorsList)
    print("\n")


""" Retrieves the additions and deletions source code for each individual using the GitHub API, 
    then stores necessary response in a list of dictionaries """
def retrieveCommitsSourceCodeIntoListOfDictionaries(allCommits, OWNER, REPO, headers):
    listOfDictionaryForCommits = [{} for x in range(len(allCommits))]
    # for each commit, extract the data:
    for i in range(len(allCommits)):
        commitSha = allCommits[i]['sha']
        commitAuthor = allCommits[i]['author']['login'] # must use login not name for accuracy

        # Retrieve the content of each individual commit via the GitHub API
        specificCommitUrl = "https://api.github.com/repos/" + OWNER + "/" + REPO + "/commits/" + commitSha
        specificCommitResponse = getGitHubResponse(specificCommitUrl, headers=headers)
        commit = convertGitHubResponseToJson(specificCommitResponse)

        additionsForFile = [{}]
        deletionsForFile = [{}]
        filenames = []

        for file in commit["files"]:            
            if filterFilenames(file["filename"]):
                x=0
                filenames.append(file["filename"])
        
                if "patch" in file:
                    patchCode = file["patch"]  # string contains code for whole file, includes the initial @@ -1,3 +1,6 @@ (AKA 'diff')
                    # Remove: @@ .... @@
                    newLineSymbol = "\n"
                    parts = patchCode.split(newLineSymbol, 1)
                    if len(parts) > 1:
                        patchCode = parts[1]

                    # splits patchCode into lines:
                    lines = patchCode.split("\n")  # list of each line of code from whole commit file, includes '@@ -1,3 +1,6 @@'
                    additionsPerFile = []
                    deletionsPerFile = []
                    
                    # Populate each additions line into
                    for j in range(len(lines)):
                        if lines[j].startswith("+"):
                            additionsPerFile.append(lines[j][1:])  #[1:]removes the +/ - from beginning of lines
                        if lines[j].startswith("-"):
                            deletionsPerFile.append(lines[j][1:])
                    # checks if there was any additions/deletions in current commit => if so then adds to accumulated dictionary 
                    if len(additionsPerFile) != 0:
                        additionsForFile[x][file["filename"]] = additionsPerFile

                    if len(deletionsPerFile) != 0:
                        deletionsForFile[x][file["filename"]] = deletionsPerFile
                    x+=1

        # Populating list of dictionaries: for each commit made-
        listOfDictionaryForCommits[i]["commitAuthor"] = commitAuthor
        listOfDictionaryForCommits[i]["commitSha"] = commitSha
        listOfDictionaryForCommits[i]["filesEdited"] = filenames
        listOfDictionaryForCommits[i]["additionsPerFile"] = additionsForFile
        listOfDictionaryForCommits[i]["deletionsPerFile"] = deletionsForFile

    return listOfDictionaryForCommits


"""Prints content of list of dictionary which holds commit data for each commit made in specified repository"""
def printListOfDictionaries(listOfDictionaryForCommits):
    print("List of dictionary:")
    for i in range(len(listOfDictionaryForCommits)):
        print(listOfDictionaryForCommits[i])
        print("\n")



    




