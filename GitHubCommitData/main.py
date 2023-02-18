from usingJSONResponse import openJsonFile
from usingRequests import codeContributionOf


"""To run the whole code contribution classifier"""
def main():
    codeContributionOf()
    openJsonFile()



if __name__ == '__main__':
    main()
    # TO RUN: python3 main.py