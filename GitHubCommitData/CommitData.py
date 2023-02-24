"""Data class holds all data needed to store for calculating the final results of the classification 
- holds collaborators list, filenames each collaborator edited, and final results of commit data"""
import json


class dataClass:
    collaboratorsList = []
    filenames = [{}]
    results= [{}]

    addedTags={}
    deletedTags={}
    tags={}

    addedTemplateTags={}
    deletedTemplateTags={}
    templateTags={}


    """deals with data types to create foundation of template"""
    def setCollaborators(self, collaborators):
        self.collaboratorsList = collaborators


    def createListOfDictionary(self, size):
        self.listOfDictionary = [{} for x in range(size)]
    
    def setListOfDictionary(self, commitData):
        self.listOfDictionary = commitData
        # print(self.listOfDictionary)
    

    """Deals with filenames"""
    def setFilenamesDictionaryKeys(self):
        self.filenamesDictionary = {}
        for i in range (len(self.collaboratorsList)):
            self.filenamesDictionary[self.collaboratorsList[i]] = set()


    def setFilenamesDictionaryValues(self, collaborator, file):
        self.filenamesDictionary[collaborator].add(file)



    """RESULTS INFORMATION PER REPOSITORY - FOR ALL COMMITS"""
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
            # contributorData["files edited"]= []
            contributorData["spaces"]= 0
            contributorData["spaces without indents"]= 0
            contributorData["new lines"]= 0
            contributorData["empty lines"]= 0
            contributorData["comment lines"]= 0
            contributorData["code lines"]= 0
            contributorData["total lines"]= 0
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
        with open('resultsTemplate.json', 'w') as file:
            json.dump(self.resultsListSeparate, file)
        
        self.fillFilenamesSeparate()



    """ populates results by all files edited by each collaborator"""
    def fillFilenamesSeparate(self):
        # - iterates through results list
        for i in range(len(self.resultsListSeparate)):
            # - iterates through keys and values of filename dictionary and results list
            for key1, val1 in self.filenamesDictionary.items():
                for key2, val2 in self.resultsListSeparate[i].items():
                    # - links the correct collaborator and updates the filenames 
                    if key1 == key2:
                        self.resultsListSeparate[i][key1]["files edited"] = val1
                        # print(self.resultsListSeparate[i][key1])
        # print("\n filenames set:")
        # print(self.resultsListSeparate[0])
        # print(self.resultsListSeparate[1])


    """increment data in a specific category for a collaborator, by a specific input value """
    def incrementDataByValueForSeparate(self, collaborator, option, incrementValue, category):
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
                        # print(self.resultsListSeparate[i][collaborator][category])


    """decrements data in a specific category for a collaborator, by a specific input value """
    def decrementDataByValueForSeparate(self, collaborator, option, decrementValue, category):
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




    """updates local dictionaries for added tags (tags and template tags) and overall dictionary"""
    def incrementHTMLtags(self, collaborator, option, incrementItem, category, addedTagsDict, tagsDict):
        print(category)
        # separate dictionaries for addedTags and deleted tags as well as overall
        if addedTagsDict: 
            for key, val in addedTagsDict.copy().items():
                for key2, val2 in incrementItem.items():
                    if key==key2:
                        addedTagsDict[key] = val + val2
                        print(addedTagsDict[key])
                    else:
                        addedTagsDict.update(incrementItem)
        else:
            addedTagsDict.update(incrementItem)
        
        if tagsDict: 
            for key, val in tagsDict.copy().items():
                for key2, val2 in incrementItem.items():
                    if key==key2:
                        tagsDict[key] = val + val2
                        print(tagsDict[key])
                    else:
                        tagsDict.update(incrementItem)
        else:
            tagsDict.update(incrementItem)
        
        # print("added to tags dict:", addedTagsDict)
        # print("next added to overall dict:", tagsDict)
        self.updateHTMLDataByValueForSeparate(collaborator, option, category, addedTagsDict, tagsDict)


    """updates local dictionaries for deleted tags (tags and template tags) and overall dictionary"""
    def decrementHTMLtags(self, collaborator, option, decrementItem, category, deletedTagsDict, tagsDict):
        # updates global tags dictionary: first checks if it is empty, if not then checks keys and vals
        # checks keys and vals of inputted dictionary so self.tags dictionary can be updated with the new values for existing and new keys
        # if self.tags does not exist, adds inputted dictionary into it. (for provided deleted and overall tags)
    
        if deletedTagsDict: 
            for key, val in deletedTagsDict.copy().items():
                for key2, val2 in decrementItem.items():
                    if key==key2:
                        # UPDATE BY INCREMENTING WHAT WAS DELETED!
                        deletedTagsDict[key] = val + val2
                        print(deletedTagsDict[key])
                    else:
                        deletedTagsDict.update(decrementItem)
        else:
            deletedTagsDict.update(decrementItem)
       
        # now remove from overall list:
        if tagsDict:
            for key, val in tagsDict.items():
                for key2, val2 in decrementItem.items():
                    if key==key2:
                        tagsDict[key] = val - val2
                        print(tagsDict[key])

        # print("removed - so increment:", deletedTagsDict)
        # print("removed - overall", tagsDict)
        self.updateHTMLDataByValueForSeparate(collaborator, option, category, deletedTagsDict, tagsDict)


    """Updates results for the HTML sections"""
    def updateHTMLDataByValueForSeparate(self, collaborator, option, category, toIncrementTagsDict, tagsDict):
        # - iterates through all collaborator's results
        for i in range(len(self.resultsListSeparate)):
            # - retrieves the items: key and values of the dictionary 
            if self.resultsListSeparate[i].items(): 
                for key, val in self.resultsListSeparate[i].items():
                    # # - finds entry for specific collaborator
                    if key == collaborator:
                        # sets the dictionary as the tags dictionary that we updated - using .update() updates ALL HTML tag dicts in the results dict!
                        # this is why i did self.tags!
                        self.resultsListSeparate[i][collaborator][category][option] = toIncrementTagsDict
                        self.resultsListSeparate[i][collaborator]["overall"][option] = tagsDict
                        # print(self.resultsListSeparate[i][collaborator]["additions"])
                        # print(self.resultsListSeparate[i][collaborator]["overall"])




