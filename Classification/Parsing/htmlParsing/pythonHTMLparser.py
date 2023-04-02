from html.parser import HTMLParser

"""Class for Python's HTMLParser"""
class HTMLParserClass(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tagTypesDictionary = {}

    """ Overrides handle_starttag from HTMLParser
        - stores tags found into a dictionary with a count of its occurrence 
        - for a single line of code """
    def handle_starttag(self, tag, attrs):
        if tag in self.tagTypesDictionary:
            self.tagTypesDictionary[tag] += 1
        else:
            self.tagTypesDictionary[tag] = 1

    def handle_endtag(self, tag):
        pass

