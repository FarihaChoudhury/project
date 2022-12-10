import requests

# Set the personal access token and HTTP headers
access_token = "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"
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {access_token}"
}

OWNER = "FarihaChoudhury"
REPO = "PublicRepoTest"
REF_SHA = "a19b766" # Last commit made


# COLLABORATORS DATA:
collaboratorsURL = "https://api.github.com/repos/"+OWNER+"/"+REPO+"/collaborators"
collaboratorsResponse = requests.get(collaboratorsURL, headers=headers)

# Make a list of all collaborators in a project
collaborators = collaboratorsResponse.json()
collaboratorsList = []

for i in range(len(collaborators)):
    collaboratorsList.append(collaborators[i]["login"])

print(collaboratorsList)




# ALL COMMIT DATA FOR A PROJECT:
url = "https://api.github.com/repos/"+OWNER+"/"+REPO+"/commits"
allCommitsResponse = requests.get(url).json()

# List of dictionaries to store commit data for a repo
listOfDictionary = [{} for x in range(len(allCommitsResponse))]

for i in range(len(allCommitsResponse)):
    commitSha = allCommitsResponse[i]['sha']
    commitAuthor = allCommitsResponse[i]['commit']['author']['name']

    # EACH COMMIT DATA:
    specificCommitUrl = "https://api.github.com/repos/"+OWNER+"/"+REPO+"/commits/"+commitSha
    specificCommitResponse = requests.get(specificCommitUrl, headers=headers)
    commit = specificCommitResponse.json()

    additionsList = []
    deletionsList = []

    for file in commit["files"]:
        diff = file["patch"]
        lines = diff.split("\n")
        # for line in lines:
        for j in range(len(lines)):
            if lines[j].startswith("+"):
                additionsList.append(lines[j])
            if lines[j].startswith("-"):
                deletionsList.append(lines[j])

    # Populating list of dictionaries
    listOfDictionary[i]["commitAuthor"] = commitAuthor
    listOfDictionary[i]["commitSha"] = commitSha
    listOfDictionary[i]["additions"] = additionsList
    listOfDictionary[i]["deletions"] = deletionsList


print("List of dictionary:")
print(listOfDictionary)


# Saves content of each commit into a file
fp = open("commitDataForRepo.txt", "w")
for commit in listOfDictionary:
    fp.write(str(commit))
    fp.write("\n")
fp.close()
