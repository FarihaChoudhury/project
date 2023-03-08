import sys
import requests 
import json
from textParse import filterFilenames

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
    BRANCH = "main"
    # REF_SHA = "a19b766" # Last commit made

    # COLLABORATORS DATA: name and repository ID
    collaboratorsURL = "https://api.github.com/repos/" + OWNER + "/" + REPO + "/collaborators"

    commitURL = "https://api.github.com/repos/" + OWNER + "/" + REPO + "/commits"
    filesURL =  "https://api.github.com/repos/"+ OWNER + "/" + REPO +"/git/trees/"+ BRANCH +"?recursive=1"
   
    return collaboratorsURL, commitURL, filesURL, headers


"""creates URL to query a specific file """
def specificFileGitHubQuery(owner, repo, filename):
    OWNER = owner 
    REPO = repo 
    PATH = filename
    specificFileURL = "http://api.github.com/repos/" + OWNER + "/" + REPO + "/commits?path="+PATH
    return specificFileURL


"""Conducts the API get command with provided url and returns its response, takes headers as an optional parameter"""
def getGitHubResponse(url, headers=None):
    try:
        if headers: 
            response = requests.get(url, headers=headers)
            # response.raise_for_status()
        else:
            response = requests.get(url)
            # response.raise_for_status()
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as error:
        print ("Http Error: ",error)
        print("Please check the error stated above and try again")
        sys.exit()
    except requests.exceptions.ConnectionError as error:
        print ("Error Connecting: ",error)
        print("Please check the error stated above and try again")
        sys.exit()
    except requests.exceptions.RequestException as error:
        print ("Error: ",error)
        print("Please check the error stated above and try again")
        sys.exit()
        


"""Converts the GitHub API response into JSON format"""
def convertGitHubResponseToJson(response):
    jsonResponse = response.json()
    return jsonResponse

"""Query all file names to return list of all filenames"""
def getFilenamesList(files):
    allFiles = []
    for file in files["tree"]:
         allFiles.append(file["path"])
    return allFiles

"""Retrieves all collaborators of a specified file, as a list """
def getCollaboratorsOfFile(file):
    collaboratorsOfFile = []
    for i in range(len(file)):
        collaboratorsOfFile.append(file[i]["author"]["login"])
    return collaboratorsOfFile

"""Store GitHub API collaborators response in a list"""
def storeCollaboratorInList(collaborators):
    collaboratorsList = []  
    for i in range(len(collaborators)):
        collaboratorsList.append(collaborators[i]["login"])
        # collaboratorsList.append(collaborators[i]["id"])    to include collaborator unique i
    return collaboratorsList


"""Prints all collaborators in given repository to terminal"""
def printCollaborators(collaboratorsList):
    print("All collaborators:")
    print(collaboratorsList)
    print("\n")


"""Store GitHub API commit response in a list of dictionaries"""
def storeCommitsInListOfDictionaries(allCommits, OWNER, REPO, headers):
    listOfDictionary = [{} for x in range(len(allCommits))]
    # EACH COMMIT DATA:
    for i in range(len(allCommits)):
        commitSha = allCommits[i]['sha']
        # USES FULL LOGIN NAME - NOT JUST NAME!!
        # commitAuthor = allCommits[i]['commit']['author']['name']
        commitAuthor = allCommits[i]['author']['login']

        specificCommitUrl = "https://api.github.com/repos/" + OWNER + "/" + REPO + "/commits/" + commitSha
        # specificCommitResponse = requests.get(specificCommitUrl, headers=headers)
        specificCommitResponse = getGitHubResponse(specificCommitUrl, headers=headers)
        commit = convertGitHubResponseToJson(specificCommitResponse)

        additionsList = []
        additionsForFile = [{}]
        deletionsForFile = [{}]
        deletionsList = []
        allCommitLinesList = []
        allCommitCodeListAsOneString = []
        filenames = []

        for file in commit["files"]:
            
            if filterFilenames(file["filename"]):
                x=0
                filenames.append(file["filename"])
            
                if (file["patch"]):
                    patchCode = file["patch"]  # string contains code for whole file, includes the initial @@ -1,3 +1,6 @@ (AKA 'diff')
                    # Remove: @@ .... @@
                    newLineSymbol = "\n"
                    parts = patchCode.split(newLineSymbol, 1)
                    if len(parts) > 1:
                        patchCode = parts[1]
                    # print(patchCode)

                    # splits patchCode into lines:
                    lines = patchCode.split("\n")  # list of each line of code from whole commit file, includes '@@ -1,3 +1,6 @@'
                    additionsPerFile = []
                    deletionsPerFile = []
                    
                    # Populate each additions line into
                    for j in range(len(lines)):
                        if lines[j].startswith("+"):
                            additionsList.append(lines[j][1:])    # [1:]removes the +/ - from beginning of lines
                            additionsPerFile.append(lines[j][1:])
                        if lines[j].startswith("-"):
                            deletionsList.append(lines[j][1:])
                            """append to per file list so it can be accumulated at the end """
                            deletionsPerFile.append(lines[j][1:])
                        else:
                            allCommitLinesList.append(lines[j][1:])   #  add all lines from commit file - DO I EVEN NEED??
                    # checks if there was any additions/deletions in current commit => if so then adds to accumulated dictionary 
                    if len(additionsPerFile) != 0:
                        additionsForFile[x][file["filename"]] = additionsPerFile

                    if len(deletionsPerFile) != 0:
                        deletionsForFile[x][file["filename"]] = deletionsPerFile
                    x+=1

        allCommitCodeListAsOneString = "\n".join(allCommitLinesList)

        # Populating list of dictionaries: for each commit made-
        listOfDictionary[i]["commitAuthor"] = commitAuthor
        listOfDictionary[i]["commitSha"] = commitSha
        listOfDictionary[i]["filesEdited"] = filenames
        listOfDictionary[i]["commitFileLinesAsList"] = allCommitLinesList  # i dont really use it
        listOfDictionary[i]["pythonCode"] = allCommitCodeListAsOneString  # i dont really ever use it 
        listOfDictionary[i]["additions"] = additionsList
        listOfDictionary[i]["additionsPerFile"] = additionsForFile
        listOfDictionary[i]["deletions"] = deletionsList
        listOfDictionary[i]["deletionsPerFile"] = deletionsForFile

    # printListOfDictionaries(listOfDictionary)
    return listOfDictionary


"""Prints content of list of dictionary which holds commit data for each commit made in specified repository"""
def printListOfDictionaries(listOfDictionary):
    print("List of dictionary:")
    for i in range(len(listOfDictionary)):
        print(listOfDictionary[i])
        print("\n")



    




