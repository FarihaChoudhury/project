import json
import os

""" Data class holds all data needed to store for calculating the final results of the classification 
    - holds collaborators list, filenames each collaborator edited, and final results of commit data """
class DataClass:
    listOfDictionaryForCommits=[{}]
    collaboratorsList = []
    filenames = [{}]
    results= [{}]

    """ deals with data types to create foundation of template """
    def setCollaborators(self, collaborators):
        self.collaboratorsList = collaborators


    """ Sets the list of dictionaries with the commit data """
    def setListOfDictionary(self, commitData):
        self.listOfDictionaryForCommits = commitData


    """ Sets the keys of filenamesDictionary being each collaborator """
    def setFilenamesDictionaryKeys(self):
        self.filenamesDictionary = {}
        for i in range (len(self.collaboratorsList)):
            self.filenamesDictionary[self.collaboratorsList[i]] = set()


    """ Sets the values being the filenames for the collaborator keys, in filenamesDictionary """
    def setFilenamesDictionaryValues(self, collaborator, file):
        for key, val in self.filenamesDictionary.items():
            if key == (collaborator):
                self.filenamesDictionary[collaborator].add(file)

    """ Prints the results information per repository, for all commits """
    def accessResultsList(self):
        print("Results so far:")
        for i in range(len(self.resultsListSeparate)):
            print(self.collaboratorsList[i])
            element = self.resultsListSeparate[i][(self.collaboratorsList[i])]
            print(element)


    """ Separates additions deletions and overall """
    def createResultsTemplateSeparate(self):
        self.resultsListSeparate = []
        for collaborator in self.collaboratorsList:
            resultsPerContributor = {(collaborator):{}}
            
            filesEdited={("files edited"):[]}
            additions={("additions"):{}}
            deletions={("deletions"):{}}
            overall={("overall"):{}}

            contributorData = {}
            contributorData["spaces"]= 0
            contributorData["spaces without indents"]= 0
            contributorData["new lines"]= 0
            contributorData["empty lines"]= 0
            contributorData["comment lines"]= 0
            contributorData["code lines"]= 0
            contributorData["total lines"]= 0
            contributorData["print statements"]= 0
            contributorData["conditionals"]= 0
            contributorData["loops"]= 0
            contributorData["imports"]= 0
            contributorData["functions"]= 0
            contributorData["class definitions"]= 0
            contributorData["class definitions list"]= []
            contributorData["views"]= 0
            contributorData["models"]= 0
            contributorData["forms"]= 0
            contributorData["HTML comments"] = 0
            contributorData["HTML tags"]= {}
            contributorData["HTML template tags"]= {}
            contributorData["HTML evaluation vars"] = 0

            additions["additions"].update(contributorData)
            deletions["deletions"].update(contributorData)
            overall["overall"].update(contributorData)
            
            resultsPerContributor[collaborator].update(filesEdited)
            resultsPerContributor[collaborator].update(additions)
            resultsPerContributor[collaborator].update(deletions)
            resultsPerContributor[collaborator].update(overall)
            self.resultsListSeparate.append(resultsPerContributor)

        # Saves content of all commits (list of dictionaries) into a JSON
        with open(os.path.join('../ResultsForCommitData','resultsTemplate.json'), 'w') as file:
            json.dump(self.resultsListSeparate, file)
    
        self.fillFilenames()


    """ Populates results by all files edited by each collaborator """
    def fillFilenames(self):
        # - iterates through results list
        for i in range(len(self.resultsListSeparate)):
            # - iterates through keys and values of filename dictionary and results list
            for key1, val1 in self.filenamesDictionary.items():
                for key2, val2 in self.resultsListSeparate[i].items():
                    # - links the correct collaborator and updates the filenames 
                    if key1 == key2:
                        self.resultsListSeparate[i][key1]["files edited"] = val1


    """ Increment data in a specific category for a collaborator, by a specific input value """
    def incrementResultsDataByValue(self, collaborator, classificationOption, incrementValue, category):
        # iterates through all collaborator's results and retrieves items; key + value for dictionary 
        for i in range(len(self.resultsListSeparate)):
            if self.resultsListSeparate[i].items(): 
                for key, val in self.resultsListSeparate[i].items():
                    # finds entry for specific collaborator, increments the specific category and overall by value
                    if key == collaborator:
                        self.resultsListSeparate[i][collaborator][category][classificationOption] = (self.resultsListSeparate[i][collaborator][category][classificationOption] + incrementValue)
                        self.resultsListSeparate[i][collaborator]["overall"][classificationOption] = (self.resultsListSeparate[i][collaborator]["overall"][classificationOption] + incrementValue)


    """ Decrements data in a specific category for a collaborator, by a specific input value """
    def decrementResultsDataByValue(self, collaborator, classificationOption, decrementValue, category):
        # iterates through all collaborator's results and retrieves items; key + value for dictionary 
        for i in range(len(self.resultsListSeparate)):
            if self.resultsListSeparate[i].items(): 
                for key, val in self.resultsListSeparate[i].items():
                    # finds entry for specific collaborator, increments the specific category by value, decrements overall
                    if key == collaborator:
                        self.resultsListSeparate[i][collaborator][category][classificationOption] = (self.resultsListSeparate[i][collaborator][category][classificationOption] + decrementValue)
                        self.resultsListSeparate[i][collaborator]["overall"][classificationOption] = (self.resultsListSeparate[i][collaborator]["overall"][classificationOption] - decrementValue)


    """ Appends result item to list of specified option """
    def updateListInResults(self, collaborator, classificationOption, resultItem, category, condition):
        # iterates through all collaborator's results and retrieves items; key + value for dictionary 
        for i in range(len(self.resultsListSeparate)):
            if self.resultsListSeparate[i].items(): 
                for key, val in self.resultsListSeparate[i].items():
                    # finds entry for specific collaborator and retrieves copy of dictionary cell so that changes can be made
                    if key == collaborator: 
                        classListResults = self.resultsListSeparate[i][collaborator][category][classificationOption].copy()
                        classListOverall = self.resultsListSeparate[i][collaborator]["overall"][classificationOption].copy()
        if (condition == "+"):
            classListResults.append(resultItem)
            classListOverall.append(resultItem)
        elif (condition == "-"):
            classListResults.append(resultItem)
            if resultItem in classListOverall:
                classListOverall.remove(resultItem)
        self.setValuesInResultsDictionary(collaborator, classificationOption, category, classListResults, classListOverall)


    """ Sets the result values in the result dictionary for a given collaborator, addition/deletion and under which category
        - takes a value or item for the addition/deletion 
        - takes a second value or item for the overall category """
    def setValuesInResultsDictionary(self, collaborator, classificationOption, category, valueToSet1, valueToSetOverall):
        for i in range(len(self.resultsListSeparate)):
            # retrieves the items: key and values of the dictionary
            if self.resultsListSeparate[i].items(): 
                for key, val in self.resultsListSeparate[i].items():
                    # finds entry for specific collaborator and sets new list values 
                    if key == collaborator:
                        self.resultsListSeparate[i][collaborator][category][classificationOption] = valueToSet1.copy()
                        self.resultsListSeparate[i][collaborator]["overall"][classificationOption] = valueToSetOverall.copy()


    """ Updates list which holds dictionary items  e.g., for tags and template tags """
    def updateHTMLtagsInResults(self, collaborator, classificationOption, resultItem, category, condition):
        for i in range(len(self.resultsListSeparate)):
            # retrieves the items: key and values of the dictionary 
            if self.resultsListSeparate[i].items(): 
                for key, val in self.resultsListSeparate[i].items():
                    # finds entry for specific collaborator and make copy of dictionary cell 
                    if key == collaborator:
                        currentList = self.resultsListSeparate[i][collaborator][category][classificationOption].copy()
                        currentOverall = self.resultsListSeparate[i][collaborator]["overall"][classificationOption].copy()
        # append to current list, regardless of addition or deletions
        if currentList:
            for key, val in currentList.copy().items():
                for key2, val2 in resultItem.items():
                    if key==key2:
                        currentList[key] = val + val2
                    else:
                        currentList.update(resultItem)
        else:
            currentList.update(resultItem)
        # overall:  If + item, add to list, if - item then only remove from list if it exists in list
        if currentOverall: 
            for key, val in currentOverall.copy().items():
                for key2, val2 in resultItem.items():
                    if key==key2:
                        if (condition == "+"):
                            currentOverall[key] = val + val2
                        else:
                            currentOverall[key] = val - val2
                    elif (key!=key2 and condition == "+"):
                        currentOverall.update(resultItem)
        elif (condition == "+"):
            currentOverall.update(resultItem)

        self.setValuesInResultsDictionary(collaborator, classificationOption, category, currentList, currentOverall)

    
    
 