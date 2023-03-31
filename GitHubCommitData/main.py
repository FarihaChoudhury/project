from usingCommitData import getClassificationsResults
from usingRequests import getCodeContributionOf


""" Runs the code contribution classifier 
    - OWNER, REPO, BRANCH and accessToken must be supplied with correct information 
    - BRANCH must be the repository's default branch, i.e., main or master
    - A repository with access rights is provided"""
def main():
    # OWNER = "FarihaChoudhury"
    # REPO = "PublicRepoTest"
    # BRANCH = "main"

    # OWNER = "lisa947"
    # REPO = "SEG-small-group-project"
    # BRANCH = "main"
    
    
    # OWNER = "FarihaChoudhury"
    # REPO = "SEG-small-group-project"
    # BRANCH = "main"

    OWNER = "FarihaChoudhury"
    REPO = "TestProject"
    BRANCH = "main"

    # accessToken = "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"
    accessToken =  "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"

    dataClass = getCodeContributionOf(OWNER, REPO, BRANCH, accessToken)
    getClassificationsResults(dataClass, REPO)
    print("Sorry for the wait, the classification is complete.")




if __name__ == '__main__':
    main()
    # TO RUN: python3 main.py