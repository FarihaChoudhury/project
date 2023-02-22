import re
import sys
import tokenize
from io import BytesIO

"""ONLY IDENTIFIES THE # COMMENTS WITH TOKENISE!"""
    # tokens = tokenize.tokenize(BytesIO(code_with_multiline_comment.encode('utf-8')).readline)
    # print(tokens)
    # for tok in tokens:
    #     if tok.type == tokenize.COMMENT:
    #         print(f"Comment: {tok.string.strip()}")


"""ALTERNTAIVES FOR BLOCK COMMENTS: ONLY WORKS FOR FILE INPUT"""
def alternative():
    file = "file.py"

    with open(file, "r") as f:
        fileContents = f.read()

    #or regexPattern: '(?:""")(.*?)(?:""")'
    regexPattern = '("""[\s\S]*?""")|(\'\'\'[\s\S]*?\'\'\')'
    pattern = re.compile(regexPattern, re.DOTALL)
    BlockComments = pattern.findall(fileContents)
    print(len(BlockComments))


# """ALTERNATIVES FOR COMMENTS - ONLY WORKS FOR FILE INPUT: """
#     file = "file.py"

#     regexPattern = 
#     with open(file, "r") as f:
#         content = f.read()

#     p = re.compile('(?:""")(.*?)(?:""")', re.DOTALL)
#     result = p.findall(content)
#     print(result)

# """Alternative 2: mix chatgpt and ^ """

#     regexPattern = '("""[\s\S]*?""")|(\'\'\'[\s\S]*?\'\'\')'
#     pattern = re.compile(regexPattern, re.DOTALL)
#     BlockComments = pattern.findall(fileInput)
#     print(len(BlockComments))

# Search for matching comments in the code string
# matches = re.findall(pattern, code)

# # Print out the matching comments
# for match in matches:
#     print(f"Comment: {match}")




def find():

    file = "file.py"

    with open(file, "r") as f:
        fileContents = f.read()

    # version 1
    p = re.compile('("""[\s\S]*?""")|(\'\'\'[\s\S]*?\'\'\')', re.DOTALL)
    result = p.findall(fileContents)
    print(result)
    print(len(result))
    print("\n")

# version 2
    regexPattern = '("""[\s\S]*?""")|(\'\'\'[\s\S]*?\'\'\')'
    pattern = re.compile(regexPattern, re.DOTALL)
    BlockComments = pattern.findall(fileContents)
    print(len(BlockComments))
    print("\n")

# version 3
    p = re.compile('(?:""")(.*?)(?:""")', re.DOTALL)
    result = p.findall(fileContents)
    print(result)
    print(len(result))




if __name__ == '__main__':
    # allows you to call openJsonFile() from terminal 
    globals()[sys.argv[1]]()
    # RUN: python3 parserHelper.py openJsonFile
