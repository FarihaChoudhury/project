from usingJSONResponse import readAdditionsAndDeletions
from usingRequests import codeContributionOf


"""To run the whole code contribution classifier"""
def main():
    OWNER = "FarihaChoudhury"
    REPO = "PublicRepoTest"
    # OWNER = "FarihaChoudhury"
    # REPO = "SEG-small-group-project"

    # accessToken = "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"
    accessToken =  "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"

    dataClass = codeContributionOf(OWNER, REPO, accessToken)
    # if dataClass: 
    readAdditionsAndDeletions(dataClass)
    print("Sorry for the wait, the classification is complete.")



if __name__ == '__main__':
    main()
    # TO RUN: python3 main.py