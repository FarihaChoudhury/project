import requests
import json

# Set the personal access token and HTTP headers
access_token = "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"
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {access_token}"
}

OWNER = "FarihaChoudhury"
REPO = "PublicRepoTest"
# REF_SHA = "a19b766" # Last commit made


""" COLLABORATORS DATA: name (and id) """
collaboratorsURL = "https://api.github.com/repos/" + OWNER + "/" + REPO + "/collaborators"
collaboratorsResponse = requests.get(collaboratorsURL, headers=headers)

# Make a list of all collaborators in a project
collaborators = collaboratorsResponse.json()
collaboratorsList = []

for i in range(len(collaborators)):
    collaboratorsList.append(collaborators[i]["login"])
    # collaboratorsList.append(collaborators[i]["id"])    to include collaborator unique id

print("Collaborators:")
print(collaboratorsList)
print("\n")



""" ALL COMMIT DATA FOR A PROJECT:
    For each commit made, stores:  
        - whole commit file's content separated by lines,
        - whole commit file not separated,
        - additions contributor made,
        - deletions contributor made 
    Removed the '', +, - from beginning of commit lines """

# FOR ALL COMMITS MADE IN A REPOSITORY: stored in a list of dictionaries
commitURL = "https://api.github.com/repos/" + OWNER + "/" + REPO + "/commits"
allCommitsResponse = requests.get(commitURL).json()

listOfDictionary = [{} for x in range(len(allCommitsResponse))]


# EACH COMMIT DATA:
for i in range(len(allCommitsResponse)):
    commitSha = allCommitsResponse[i]['sha']
    commitAuthor = allCommitsResponse[i]['commit']['author']['name']

    specificCommitUrl = "https://api.github.com/repos/" + OWNER + "/" + REPO + "/commits/" + commitSha
    specificCommitResponse = requests.get(specificCommitUrl, headers=headers)
    commit = specificCommitResponse.json()

    additionsList = []
    deletionsList = []
    allCommitLinesList = []
    allCommitCodeListAsOneString = []

    for file in commit["files"]:
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
    listOfDictionary[i]["commitFileLinesAsList"] = allCommitLinesList  # separates lines into items of list
    listOfDictionary[i]["PYTHONCODE"] = allCommitCodeListAsOneString
    listOfDictionary[i]["additions"] = additionsList
    listOfDictionary[i]["deletions"] = deletionsList



print("List of dictionary:")
# print each index with space between:
for i in range(len(listOfDictionary)):
    print(listOfDictionary[i])
    print("\n")


# Saves content of each commit into a text file
# fp = open("commitDataForRepo.txt", "w")
# for commit in listOfDictionary:
#     fp.write(str(commit))
#     fp.write("\n")
# fp.close()


with open("commitDataForRepo.txt", 'w') as file:
    for commit in listOfDictionary:
        file.write(str(commit))
        file.write("\n")


# Saves content of all commits (list of dictionaries) into a JSON
with open('allCommitsInRepo.json', 'w') as file:
    # for i in range(len(listOfDictionary)):
    json.dump(listOfDictionary, file)

# HOW TO OPEN AGAIN AS PYTHON:
# print("hello")
# with open('allCommitsInRepo.json', 'r') as file:
#     d = json.load(file)
#     print(d)


