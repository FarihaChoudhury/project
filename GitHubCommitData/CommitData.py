class dataClass:
    collaboratorsList = []
    filenames = [{}]


    def setCollaborators(self, collaborators):
        self.collaboratorsList = collaborators


    def createListOfDictionary(self, size):
        self.listOfDictionary = [{} for x in range(size)]
    
    def setListOfDictionary(self, commitData):
        self.listOfDictionary = commitData
    



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
  
    



