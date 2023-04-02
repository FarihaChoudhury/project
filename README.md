# PROJECT
## Analysing code contributions through code classification for Python and Django projects
3rd year project

All ANTLR-generated files are not my intellectual property. These have been taken from the ANTLR documentation: 
    - https://www.antlr.org
    - https://github.com/antlr/antlr4/blob/master/doc/index.md
    - https://github.com/antlr/grammars-v4/tree/master/python/python3
    - https://github.com/antlr/grammars-v4/tree/master/python/python3/Python3
    - https://stackoverflow.com/questions/75294250/im-trying-to-generate-the-parse-tree-for-antlr4-python3-g4-grammar-file-to-par

## Requirements:
- Python3 
- ANTLR for Python3 (see steps below)
- A repository with access/ownership and a GitHub access token.
- This project was coded in VScode - system paths remain in settings.json, use VScode if unable to work on other IDEs
## TO INSTALL ANTLR: 
- All ANTLR generated code is provided in the repository, within the directory at 'project/Classification/Parsing/antlrParserGeneratedCode'
- To test for this:
    - Navigate to the 'project/Classification/Parsing/antlrParserGeneratedCode' directory
    - run: python3 transformGrammar.py
- Regardless, the Python3 runtime for ANTLR must be installed, run: 
    - pip install antlr4-python3-runtime
    - java -jar antlr-4.11.1-complete.jar *.g4 -Dlanguage=Python3

- If these steps do not work, navigate to file parserGenerator.sh in directory 'project/Classification/antlrPythonParserGenerator'
    - These were run inside the 'project/PythonParser/antlrPythonParser/antlrParserGeneratedCode' directory 
- Follow this link if failure to set up: https://stackoverflow.com/questions/75294250/im-trying-to-generate-the-parse-tree-for-antlr4-python3-g4-grammar-file-to-par


## TO RUN PROJECT CODE:

To perform classification:
- Navigate to GitHubCommitData directory  'project/GitHubCommitData'
    - Navigate to main.py
    - The 'OWNER', 'REPO', 'BRANCH' and 'accessToken' are filled with correct information for testing a provided repository
            - OWNER: GitHub login name of the owner of the repository 
            - REPO: Name of the repository (must have ownership of repository tested)
            - BRANCH: Default branch of repository, "main" or "master" depending on repository set up.
            - accessToken: personal access token for OAuth access to GitHub REST API
    - Run main.py whilst inside the GitHubCommitData directory, from the terminal using command 'python3 main.py'
            - If there was an error with the previous step, the system will exit with an error message
    - Wait until terminal displays: "Sorry for the wait, the classification is complete." before loading results

To view results: 
-  Once the classification is complete, navigate to the ResultsForCommitData directory  - 'project/ResultsForCommitData'
    - Run the HTTP server using the command:  'python3 -m http.server'
    - Go to a browser and type the URL 'http://localhost:8000/result.html' to view the results of the classification



 GitHub link to TestProject repository: https://github.com/FarihaChoudhury/TestProject
    - This is the repository that was developed for testing this software
    - Details of this repository can be found in project/GitHubCommitData/main.py



### Author: Fariha Choudhury K20059723
### GitHub link for this project: https://github.com/FarihaChoudhury/project

