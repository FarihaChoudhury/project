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



def find2():
    line1= " #1 "
    line1= line1.strip()

    line2= ' 2 """ '
    line2= line2.strip()

    line3= " '''3 "
    line3= line3.strip()

    line4= ' "4 "'
    line4= line4.strip()

    line5= " '5 ''' "
    line5= line5.strip()

    line6 = 'print(x =This is a comment) #hi '
    line6= line6.strip()


    # Regular expression to match either a # comment or triple-quoted comment start
    comment_regex = r'#|"""'
    # comment_regex = r'^(#|"""|''')'

    # USE:
    # cannot combine due to mismatch of " and '
    #finds # or """ or '''
    tripleBlockCommentStartRegex = r'^([#].*|("""|\'\'\').*)'

    tripleBlockCommentEndRegex = r'("""|\'\'\')$'
        # return 1, 2, 3


    # use:
    # to idenitfy single ' or " - START AND ENDS WITH IT 
    singleCommentStartAndEndRegex = r"^(['\"]).*\1$"
            # return 4, 5

    # use: 
    # to find # anywhere in the line
    midlineCommentRegex = r"\#"

    """for midline comments"""
    # comment_regex = r"^(?!print).*#.*$"
    # comment_regex = r"(?<!print.*)#.*$"
    # comment_regex =r"^(?!.*print\s*\().*#[^']*"
    # comment_regex = r"^(?!.*\bprint\s*\().*#.*"

    
    # if re.match(r"^(?!.*print\s*\().*#[^']*", line6):
    #     print(f"Found comment: {line6}")

    # # Search for comment start in the line

    # match = re.search(tripleBlockCommentEndRegex, 'boo """')
    # if match:
    #     print(match)
    #     print(("Comment found:", match.group()))
    #     print("Comment start found at position", match.start())

    # else:
    #     print("No comment start found.")

    """KEY: ---- THIS WORKS!!! """
    tripleBlockCommentAndHashStartRegex = r'^([#].*|("""|\'\'\').*)'

    tripleBlockCommentEndRegex = r'("""|\'\'\')$'
    singleCommentStartAndEndRegex = r"^(['\"]).*\1$"
    midlineCommentRegex = r"\#"

    print("\n here: \n")

    line = line5
    count = 0

    if (re.search(singleCommentStartAndEndRegex, line)):
        match = re.search(singleCommentStartAndEndRegex, line)
        print("single start and end ")
        print(match.group())
        count+=1

    elif (re.search(tripleBlockCommentAndHashStartRegex, line)):
        match = re.search(tripleBlockCommentAndHashStartRegex, line)
        print("triple block start or # start")
        print(match.group())
        count+=1

    elif (re.search(tripleBlockCommentEndRegex, line)):
        match = re.search(tripleBlockCommentEndRegex, line)
        print("triple block end")
        print(match.group())
        count+=1

    elif(re.search(midlineCommentRegex, line)):
        match = re.search(midlineCommentRegex, line)
        print("midline #")
        print(match.group())
        count+=1

    return count



if __name__ == '__main__':
    # allows you to call openJsonFile() from terminal 
    globals()[sys.argv[1]]()
    # RUN: python3 parserHelper.py openJsonFile
