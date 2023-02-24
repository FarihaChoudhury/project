from html.parser import HTMLParser

class HTMLParserClass(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tagTypesDictionary = {}
        # self.dataTypesDictionary = {}

    """Override the methods and implement own implementations:"""
    def handle_starttag(self, tag, attrs):
        # self.tag_types[tag] = self.tag_types.get(tag, 0) + 1
        if tag in self.tagTypesDictionary:
            self.tagTypesDictionary[tag] += 1
        else:
            self.tagTypesDictionary[tag] = 1
        # print(self.tagTypesDictionary)

    def handle_endtag(self, tag):
        pass

    # def handle_data(self, data):
    #     if data.strip() == "":
    #         pass
    #     else: 
    #         # pass
    #         if data in self.tagTypesDictionary:
    #             self.dataTypesDictionary[data] += 1
    #         else:
    #             self.dataTypesDictionary[data] = 1
    
    # dont use as it wont pick up on first lines of block comments like <!--
    # def handle_comment(self, comment):
    #     if comment in self.tagTypesDictionary:
    #         self.tagTypesDictionary[comment] += 1
    #     else:
    #         self.tagTypesDictionary[comment] = 1