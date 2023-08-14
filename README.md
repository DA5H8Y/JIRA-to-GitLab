# GitLab Management

## Tools
To use the two avaliable tools in this repository follow these instructions

### Prerequisites
1. Python
2. Python-venv
3. GitLab API token
4. JIRA API token

### Installation
This step requires an internet connection, as it downloads the required Python modules from the internet.

Run ```install.bat``` or ```install.sh```

### Setup the scripts

There is some parameters to check to setup the scripts;

1. [activate](/env/Scripts/activate) line 41 Make sure that the Virtual Environment path is correct

    ```bash
    VIRTUAL_ENV=".\env"
    export VIRTUAL_ENV
    ```

2. [gitlab.cfg](gitlab.cfg) make sure that a configuration is set correctly and that you API token value is correct for that instance

    ```config
    [example]
    url = http://gitlab.localhost.com
    private_token = 
    api_version = 4
    ```

3. [create_from_file.py](create_from_file.py) line 8 ensure that the GitLab configuration id is set to the right value in (gitlab.cfg)[gitlab.cfg]

    ```Python
    #######################################################
    #        MAKE SURE THESE DETAILS ARE CORRECT          #
    #######################################################
    gl = gitlab.Gitlab.from_config('default', ['gitlab.cfg'])  
    #######################################################
    #                                                     #
    #######################################################
    ```

4. [move_issues_from_jira_to_gitlab.py](move_issues_from_jira_to_gitlab.py) line 15-18 ensure that;

    1. The GitLab configuration id is set to the right value in [gitlab.cfg](gitlab.cfg)
    2. The JIRA server URL is correct, and
    3. The JIRA token is correct for that instance (preferably an Administrator level user.)

    ```Python
    #######################################################
    #        MAKE SURE THESE DETAILS ARE CORRECT          #
    #######################################################
    gl = gitlab.Gitlab.from_config('local', ['gitlab.cfg'])

    jira = JIRA(server='http://localhost:8080',
            token_auth='MzUyMjM3NTQ0NjY2OiWGkKiOjfTCahuGnfPcCdfZOJB8')  # Self-Hosted Jira (e.g. Server): the PAT token
    ########################################################
    #                                                      #
    ########################################################
    ```

5. [project_list.json](project_list.json) make sure that this is a list of projects with full namespaces that you wish to create or to auto push to GitLab.
There exists an options field for specifying special treatments during the auto push process, at the moment only one option exists "tag", this will expect that
there are multiple folders within the final project folder of the format project_"tagname" for example, Project3_v1.0 and Project3_v2.0.
The following JSON example is reflected in the sample "Repository" folder structure provided.

    ```json
    {
        "Groups":[
            {
                "name":"RandD",
                "path":"/"
            },
            {
                "name":"Tasks",
                "path":"/RandD/"
            },
            {
                "name":"Tools",
                "path":"/"
            },
            {
                "name":"Toolboxes",
                "path":"/"
            }
        ],
        "Projects":[
            {        
                "name":"RandD",
                "path":"/RandD/",
                "options":["nolocal"]
            },
            {        
                "name":"Documents",
                "path":"/RandD/"
            },
            {        
                "name":"RandD 001 - Simple Git",
                "path":"/RandD/Tasks/"
            },
            {        
                "name":"Tools",
                "path":"/Tools/",
                "options":["nolocal"]
            },
            {        
                "name":"Simulink",
                "path":"/Tools/",
                "options":[]
            },
            {        
                "name":"Toolboxes",
                "path":"/Toolboxes/",
                "options":["nolocal"]
            },
            {        
                "name":"RandD Blockset",
                "path":"/Toolboxes/",
                "options":["version"]
            }
        ]
    }
    ```

### Run The Scripts

You should now be ready to run the scripts;

1. [create_from_file.py](create_from_file.py) This Python script takes the list of projects in [project_list.txt](project_list.txt) and creates any missing groups and projects.

    ```bash
    py create_from_file.py
    ```

2. [git_auto_pusher.py](git_auto_pusher.py) This Python script iterates through a provided folder structure and setup and pushes directories that match the list of projects in [project_list.txt](project_list.txt) to GitLab.

    ```bash
    py git_auto_pusher.py -d R:\ -u gitlab.localhost.com
    ```

3. [move_issues_from_jira_to_gitlab.py](move_issues_from_jira_to_gitlab.py) This Python script cycles through all the projects in the JIRA repository and then recreates the projects issues in GitLab projects that match names.

    ```bash
    py move_issues_from_jira_to_gitlab.py
    ```

## Guides

The following two guides are available in this repository;

### Server Management

Server Management is captured in another file [GitLabServerManagement](GitLabServerManagement.md).

### Git

A guide to git is captured in another file [Git-Guide](Git-Guide.md).
