from html.parser import HTMLParser

class HTMLParserClass(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tagTypesDictionary = {}

    """Override the methods and implement own implementations:"""
    def handle_starttag(self, tag, attrs):
        if tag in self.tagTypesDictionary:
            self.tagTypesDictionary[tag] += 1
        else:
            self.tagTypesDictionary[tag] = 1

    def handle_endtag(self, tag):
        pass

