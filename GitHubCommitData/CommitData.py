"""Data class holds all data needed to store for calculating the final results of the classification 
- holds collaborators list, filenames each collaborator edited, and final results of commit data"""
class dataClass:
    collaboratorsList = []
    filenames = [{}]

    results= [{}]


    def setCollaborators(self, collaborators):
        self.collaboratorsList = collaborators


    def createListOfDictionary(self, size):
        self.listOfDictionary = [{} for x in range(size)]
    
    def setListOfDictionary(self, commitData):
        self.listOfDictionary = commitData
        # print(self.listOfDictionary)
    



    def setFilenamesDictionaryKeys(self):
        self.filenamesDictionary = {}
        for i in range (len(self.collaboratorsList)):
            self.filenamesDictionary[self.collaboratorsList[i]] = set()


    def setFilenamesDictionaryValues(self, collaborator, file):
        self.filenamesDictionary[collaborator].add(file)

        # for i in range(len(fileslist)):
        #         print("")


        # """USING PREV METHOD - USES ALL FILES - EVEN DELETED ONES I THINK..."""
        # # self.filenamesDictionary

        # for i in range(len(self.listOfDictionary)):
        #     self.filenamesDictionary[self.listOfDictionary[i]['commitAuthor']].add(self.listOfDictionary[i]['filesEdited'])
  
    
    """RESULTS INFORMATION PER REPOSITORY - FOR ALL COMMITS"""

    def accessResultsList(self):
        print("RESULTS SO FAR")
        for i in range(len(self.resultsList)):
            print(self.collaboratorsList[i])
            element = self.resultsList[i][(self.collaboratorsList[i])]
            print(element)


    def createResultsTemplate(self):
        self.resultsList = []
        for collaborator in self.collaboratorsList:
            test = collaborator
            resultsPerContributor = {(collaborator):[]}

            contributorData = {}
            contributorData["files edited"]= []
            contributorData["empty lines"]= 0
            contributorData["comment lines"]= 0
            contributorData["code lines"]= 0
            contributorData["HTML divs"]= 0
            resultsPerContributor[collaborator].append(contributorData)
            self.resultsList.append(resultsPerContributor)
    
        print("\n POPULATING DATA: files names + increment fariha comment lines: \n")
        self.fillFilenames()
        # passes in Fariha --- REPLACE BY REAL !
        self.incrementData(test, "comment lines")
        self.accessResultsList()




    """increment data in a specific category for a collaborator, by 1 """
    def incrementData(self, collaborator, option):
        # - iterates through all collaborator's results
        for i in range(len(self.resultsList)):
            # - retrieves the items: key and values of the dictionary 
            if self.resultsList[i].items(): 
                for key, val in self.resultsList[i].items():
                    # - finds entry for specific collaborator
                    if key == collaborator:
                        self.resultsList[i][collaborator][0][option] += 1
                  
        # print("\n increment by 1:")
        # self.accessResultsList()
    

    """increment data in a specific category for a collaborator, by a specific input value """
    def incrementDataByValue(self, collaborator, option, incrementValue):
        # - iterates through all collaborator's results
        for i in range(len(self.resultsList)):
            # - retrieves the items: key and values of the dictionary 
            if self.resultsList[i].items(): 
                for key, val in self.resultsList[i].items():
                    # - finds entry for specific collaborator
                    if key == collaborator:
                        # - increments the specific category by 1 
                        self.resultsList[i][collaborator][0][option] = (self.resultsList[i][collaborator][0][option] + incrementValue)
              
        # print("\n increment by value:")
        # self.accessResultsList()


    """ populates results by all files edited by each collaborator"""
    def fillFilenames(self):
        # - iterates through results list
        for i in range(len(self.resultsList)):
            # - iterates through keys and values of filename dictionary and results list
            for key1, val1 in self.filenamesDictionary.items():
                for key2, val2 in self.resultsList[i].items():
                    # - links the correct collaborator and updates the filenames 
                    if key1 == key2:
                        self.resultsList[i][key1][0]["files edited"] = val1
        
        # print("\n filenames set:")
        # self.accessResultsList()


    




            # x=0
            # print(resultsList[x])
            # resultsList[x][collaborator] = [1, 2]
            # x+=1
        # for i in range (len(resultsList)):
        #     resultsList[x][]
            # listOfDictionary[i]["commitAuthor"] = commitAuthor
            # listOfDictionary[i]["commitSha"] = commitSha
            # listOfDictionary[i]["filesEdited"] = filenames
            # listOfDictionary[i]["commitFileLinesAsList"] = allCommitLinesList  # separates lines into items of list
            # listOfDictionary[i]["pythonCode"] = allCommitCodeListAsOneString
            # listOfDictionary[i]["additions"] = additionsList
            # listOfDictionary[i]["additionsPerFile"] = additionsForFile
            # listOfDictionary[i]["deletions"] = deletionsList
            # listOfDictionary[i]["deletionsPerFile"] = deletionsForFile


        # print(resultsList)


        






