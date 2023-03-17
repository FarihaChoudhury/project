"""Data class holds all data needed to store for calculating the final results of the classification 
- holds collaborators list, filenames each collaborator edited, and final results of commit data"""
import json
import os


class DataClass:
    listOfDictionaryForCommits=[{}]
    collaboratorsList = []
    filenames = [{}]
    results= [{}]

    """Class variables were used as editing a list/ dictionary within dictionary causes effects on other collections in the datatype"""
    # addedTags={}
    # deletedTags={}
    # tags={} 

    # addedTemplateTags={}
    # deletedTemplateTags={}
    # templateTags={}

    # addedClasses=[]
    # classesList = []
    # deletedClasses=[]


    """deals with data types to create foundation of template"""
    def setCollaborators(self, collaborators):
        self.collaboratorsList = collaborators


    """Sets the list of dictionaries with the commit data"""
    def setListOfDictionary(self, commitData):
        self.listOfDictionaryForCommits = commitData


    """Sets the keys of filenamesDictionary being each collaborator"""
    def setFilenamesDictionaryKeys(self):
        self.filenamesDictionary = {}
        for i in range (len(self.collaboratorsList)):
            # print(self.collaboratorsList)
            self.filenamesDictionary[self.collaboratorsList[i]] = set()


    """Sets the values being the filenames for the collaborator keys, in filenamesDictionary"""
    # def setFilenamesDictionaryValues(self, collaborator, file):
    #     self.filenamesDictionary[collaborator].add(file)

    #     """Sets the values being the filenames for the collaborator keys, in filenamesDictionary"""
    def setFilenamesDictionaryValues(self, collaborator, file):
        # self.filenamesDictionary[collaborator].add(file)
        for key, val in self.filenamesDictionary.items():
            if key == (collaborator):
                self.filenamesDictionary[collaborator].add(file)

    """prints the results information per repository, for all commits """
    def accessResultsList(self):
        print("RESULTS SO FAR")
        for i in range(len(self.resultsListSeparate)):
            print(self.collaboratorsList[i])
            element = self.resultsListSeparate[i][(self.collaboratorsList[i])]
            print(element)


    """Separates additions deletions and overall"""
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
            # resultsPerContributor[collaborator].append(contributorData)
            self.resultsListSeparate.append(resultsPerContributor)
        
        for i in range(len(self.resultsListSeparate)):
            print(self.resultsListSeparate[i])
            print("\n")

        # Saves content of all commits (list of dictionaries) into a JSON
        with open(os.path.join('../ResultsForCommitData','resultsTemplate.json'), 'w') as file:
            json.dump(self.resultsListSeparate, file)
    
        self.fillFilenames()


    """ populates results by all files edited by each collaborator"""
    def fillFilenames(self):
        # - iterates through results list
        for i in range(len(self.resultsListSeparate)):
            # - iterates through keys and values of filename dictionary and results list
            for key1, val1 in self.filenamesDictionary.items():
                for key2, val2 in self.resultsListSeparate[i].items():
                    # - links the correct collaborator and updates the filenames 
                    if key1 == key2:
                        self.resultsListSeparate[i][key1]["files edited"] = val1


    """increment data in a specific category for a collaborator, by a specific input value """
    def incrementResultsDataByValue(self, collaborator, option, incrementValue, category):
        # - iterates through all collaborator's results
        for i in range(len(self.resultsListSeparate)):
            # - retrieves the items: key and values of the dictionary 
            if self.resultsListSeparate[i].items(): 
                for key, val in self.resultsListSeparate[i].items():
                    # # - finds entry for specific collaborator
                    if key == collaborator:
                        # print(self.resultsListSeparate[i][collaborator][category][option])
                        # - increments the specific category by 1 
                        self.resultsListSeparate[i][collaborator][category][option] = (self.resultsListSeparate[i][collaborator][category][option] + incrementValue)
                        self.resultsListSeparate[i][collaborator]["overall"][option] = (self.resultsListSeparate[i][collaborator]["overall"][option] + incrementValue)
        """CANNOT REFACTOR TO USE setValuesInResultsDictionary AS THE CURRENT VALUE IS NEEDED FOR THE INCREMENT"""


    """decrements data in a specific category for a collaborator, by a specific input value """
    def decrementResultsDataByValue(self, collaborator, option, decrementValue, category):
        # - iterates through all collaborator's results
        for i in range(len(self.resultsListSeparate)):
            # - retrieves the items: key and values of the dictionary 
            if self.resultsListSeparate[i].items(): 
                for key, val in self.resultsListSeparate[i].items():
                    # - finds entry for specific collaborator
                    if key == collaborator:
                        # - decrements the specific category by 1 in overall, but +1 in deletes sectionx 
                        self.resultsListSeparate[i][collaborator][category][option] = (self.resultsListSeparate[i][collaborator][category][option] + decrementValue)
                        self.resultsListSeparate[i][collaborator]["overall"][option] = (self.resultsListSeparate[i][collaborator]["overall"][option] - decrementValue)
                """CANNOT REFACTOR TO USE setValuesInResultsDictionary AS THE CURRENT VALUE IS NEEDED FOR THE IN/DECREMENT"""





    def updateDefinitionsListInResults(self, collaborator, option, resultItem, category, condition):
        for i in range(len(self.resultsListSeparate)):
            # - retrieves the items: key and values of the dictionary 
            if self.resultsListSeparate[i].items(): 
                for key, val in self.resultsListSeparate[i].items():
                    # # - finds entry for specific collaborator
                    if key == collaborator:
                        # sets the dictionary as the tags dictionary that we updated - using .update() updates ALL HTML tag dicts in the results dict!
                        # this is why i did self.tags!
                        classListResults = self.resultsListSeparate[i][collaborator][category][option].copy()
                        # print(self.resultsListSeparate[i][collaborator][category][option])
                        classListOverall = self.resultsListSeparate[i][collaborator]["overall"][option].copy()
        
        if (condition == "+"):
            classListResults.append(resultItem)
            # FOR OVERALL:
            classListOverall.append(resultItem)
        elif (condition == "-"):
            classListResults.append(resultItem)
            # FOR OVERALL:
            if resultItem in classListOverall:
                classListOverall.remove(resultItem)
        self.setValuesInResultsDictionary(collaborator, option, category, classListResults, classListOverall)


    """Sets the result values in the result dictionary for a given collaborator, addition/deletion and under which category
        - takes a value or item for the addition/deletion 
        - takes a second value or item for the overall category"""
    def setValuesInResultsDictionary(self, collaborator, option, category, valueToSet1, valueToSetOverall):
        for i in range(len(self.resultsListSeparate)):
            # - retrieves the items: key and values of the dictionary 
            if self.resultsListSeparate[i].items(): 
                for key, val in self.resultsListSeparate[i].items():
                    # # - finds entry for specific collaborator
                    if key == collaborator:
                        # sets the dictionary as the tags dictionary that we updated - using .update() updates ALL HTML tag dicts in the results dict!
                        # this is why i did self.tags!
                        self.resultsListSeparate[i][collaborator][category][option] = valueToSet1.copy()
                        # print(self.resultsListSeparate[i][collaborator][category][option])
                        self.resultsListSeparate[i][collaborator]["overall"][option] = valueToSetOverall.copy()
                        # print(self.resultsListSeparate[i][collaborator]["overall"][option])



    """updates local dictionaries for REMOVED  tags (tags and template tags) and overall dictionary"""
    def updateHTMLtagsInResults(self, collaborator, option, resultItem, category, condition):
        for i in range(len(self.resultsListSeparate)):
            # - retrieves the items: key and values of the dictionary 
            if self.resultsListSeparate[i].items(): 
                for key, val in self.resultsListSeparate[i].items():
                    # # - finds entry for specific collaborator
                    if key == collaborator:
                        currentList = self.resultsListSeparate[i][collaborator][category][option].copy()
                        currentOverall = self.resultsListSeparate[i][collaborator]["overall"][option].copy()
        # append to current list, regardless of addition or deletions
        # resultUpdated = []
        if currentList:
            print(resultItem) 
            print("before:", currentList)
            for key, val in currentList.copy().items():
                for key2, val2 in resultItem.items():
                    if key==key2:
                        # print("matched:", key)
                        # print("need to be", val + val2)
                        currentList[key] = val + val2
                    else:
                        currentList.update(resultItem)
                        # resultUpdated = currentList.copy()
        else:
            currentList.update(resultItem)
            # resultUpdated = currentList.copy()

        print("after:", currentList)
        # if resultUpdated:
        #     print("after TRY:", resultUpdated)
        # if its +, then adds to list even if it doesn't exist for overall, if - then dont add if it doesn't exist because then they deleted something they didn't add!
        # this is because if they added it, it would be in overall already 
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
        
        print("after:", currentOverall)

        self.setValuesInResultsDictionary(collaborator, option, category, currentList, currentOverall)

    
    
 