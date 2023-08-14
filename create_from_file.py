import gitlab
import json
import urllib3 # So we can disable the warnings
from create_gitlab_project import create_project

#######################################################
#        MAKE SURE THESE DETAILS ARE CORRECT          #
#######################################################
gl = gitlab.Gitlab.from_config('default', ['gitlab.cfg'])  
#######################################################
#                                                     #
#######################################################
urllib3.disable_warnings()

with open('project_list.json', 'r') as f:
    data = json.load(f)

for project in data['Projects']:
    fullname = project['path'] + project['name']
    print(f'Creating project: {fullname}')
    print("="*(len(fullname) + 18))
    if create_project(gl, fullname ) is not None:
        print('''   Successfully created project.''')

f.close()
