import requests


USER = "FarihaChoudhury"
REPO = "PublicRepoTest"
REF_SHA = "9334f70"

# All commits in a project:
# url = "https://api.github.com/repos/"+USER+"/"+REPO+"/commits"

# Specific commmit:
url = "https://api.github.com/repos/"+USER+"/"+REPO+"/commits/"+REF_SHA
response = requests.get(url).json()

# Get only code added and the random thing at the top
response = response["files"][0]["patch"]

print(response)

# Saves content of commit into a file
fp = open("stuff.txt", "w")
fp.write(response)
fp.close()