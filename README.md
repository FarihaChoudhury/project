# PROJECT
3rd year project - Analysing code contributions through code classification for Python and Django projects




## TO RUN CODE:

- Navigate to GitHubCommitData directory  (project/GitHubCommitData)
    - Navigate to main.py
    - Fill the variables 'OWNER', 'REPO' and 'accessToken' with correct information
            - OWNER: GitHub login name of the owner of the repository 
            - REPO: Name of the repository 
            - accessToken: personal access token for OAuth access to GitHub REST API
    - Run main.py whilst inside the GitHubCommitData directory, from the terminal using command 'python3 main.py'
    - Wait until terminal displays: "Sorry for the wait, the classification is complete." before loading results

-  Navigate to the ResultsForCommitData directory  (project/ResultsForCommitData)
    - Run the HTTP server using the command:  'python3 -m http.server'
    - Go to a browser and type the URL 'http://localhost:8000/result.html' to view the results of the classification


## Additional details:
- All ANTLR generated code is provided in the repository

- To install antlr4's python3 runtime, run: 
    - 'pip install antlr4-python3-runtime'
    - 'java -jar antlr-4.11.1-complete.jar *.g4 -Dlanguage=Python3'


- The commands I ran to set up ANTLR (which is already done for you and not necessary) can be found in 'project/PythonParser/antlrPythonParserGenerator/parserGenerator.sh'
- These were run inside the 'project/PythonParser/antlrPythonParser/antlrParserGeneratedCode' directory 
- Follow this link if failure to set up: https://stackoverflow.com/questions/75294250/im-trying-to-generate-the-parse-tree-for-antlr4-python3-g4-grammar-file-to-par



# Author: Fariha Choudhury K20059723

