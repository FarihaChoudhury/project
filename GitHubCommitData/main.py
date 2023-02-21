from usingJSONResponse import openJsonFile, readAdditionsAndDeletions
from usingRequests import codeContributionOf


"""To run the whole code contribution classifier"""
def main():
    dataClass = codeContributionOf()
    # openJsonFile(dataClass)
    readAdditionsAndDeletions(dataClass)



if __name__ == '__main__':
    main()
    # TO RUN: python3 main.py