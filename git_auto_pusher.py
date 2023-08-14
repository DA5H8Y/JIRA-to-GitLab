import sys
import os
import subprocess
import json

def list_folders(dir: str):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in dirs:
            r.append(os.path.join(root, name))
    
    for i in range(len(r)):
        r[i] = str(r[i]).replace(f'{dir}/', "")
        
    return r

def chdir(dir: str):
    try:
        os.chdir(dir)

    except NotADirectoryError:
        print("You have not chosen a directory.")

    except FileNotFoundError:
        print("The folder was not found. The path is incorrect.")

    except PermissionError:
        print("You do not have access to this folder/file.")

def get_project_list():
    p = []
    
    with open('project_list.json', 'r') as f:
        data = json.load(f)

    for project in data['Projects']:
        if 'options' in project:
            if not('nolocal' in project['options']):
                p.append(project)
        else:
            p.append(project)

    return p

def get_project_parts(dir, repo):
    path = '/'
    name = None
    version = None

    parts = dir.split('/')
    if len(parts) == 1:
        name = parts            # Set like this for now
        parts = dir.split('\\') # Lets see if its a windows problem

    if len(parts) == 2:
        path = '/' + parts[0] + '/'
        name = parts[1]
    elif len(parts) >= 3:
        path = '/'.join(parts[:-2])
        path = path.replace(repo,'') + '/'
        name = parts[-2]
        version = parts[-1].replace(f'{name}_','')
    
    return path, name, version

def git_init(branch: str):
    PIPE = subprocess.PIPE
    
    cmd = ['git', 'init', f'--initial-branch={branch}']
    print(' '.join(cmd))
    process = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdoutput, stderroutput = process.communicate()

def git_rename_remote(old: str='origin',new: str='old-origin'):
    PIPE = subprocess.PIPE
    cmd = ['git', 'remote', 'rename', old, new]
    print(' '.join(cmd))
    process = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdoutput, stderroutput = process.communicate()

def git_add_remote(remote: str):
    PIPE = subprocess.PIPE
    cmd = ['git', 'remote', 'add', 'origin', remote]
    print(' '.join(cmd))
    process = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdoutput, stderroutput = process.communicate()

def git_add_files(file: str='.'):
    PIPE = subprocess.PIPE
    cmd = ['git', 'add', file]
    print(' '.join(cmd))
    process = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdoutput, stderroutput = process.communicate()

def git_commit(msg: str=''):
    PIPE = subprocess.PIPE
    cmd = ['git', 'commit', '-m', f'"{msg}"']
    print(' '.join(cmd))
    process = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdoutput, stderroutput = process.communicate()

def git_push(remote: str='', branch: str=''):
    PIPE = subprocess.PIPE
    
    if (remote != '') and (branch !=''):
        cmd = ['git', 'push', '-u', remote, branch]
        print(' '.join(cmd))
        process = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
    else:
        cmd = ['git', 'push']
        print(' '.join(cmd))
        process = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
    
    stdoutput, stderroutput = process.communicate()

def git_tag(name: str, desc: str='', remote: str='origin'):
    PIPE = subprocess.PIPE
    cmd = ['git', 'tag', '-a', name, '-m',  f'"{desc}"']
    print(' '.join(cmd))
    process = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdoutput, stderroutput = process.communicate()

    cmd = ['git', 'push', remote, '--tags']
    print(' '.join(cmd))
    process = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdoutput, stderroutput = process.communicate()

def git_checkout_tag(name: str):
    PIPE = subprocess.PIPE
    cmd = ['git', 'checkout', name]
    print(' '.join(cmd))
    process = subprocess.Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdoutput, stderroutput = process.communicate()

def push_existing_folder(path: str, project: str, version: str, url: str, branch: str):
    if (path is not None) and (project is not None):
        #git init --initial-branch=main
        git_init(branch)

        project= project.lower().replace(' ','-')

        #git remote add origin git@gitlab.localhost.com:path/name.git
        giturl = f'git@{url}{path}{project}.git'
        git_add_remote(giturl)

        #git add .
        git_add_files()

        #git commit -m "Initial commit"
        git_commit("Commit by Auto Uploader")

        #git push -u origin main
        git_push('origin', branch)

        if version is not None:
            git_tag(version, 'Autotagged from old repo')
            git_checkout_tag(version)

def push_existing_repo(path: str, name: str, version: str, url: str, branch: str):
    if (path is not None) and (name is not None):
        #git remote rename origin old-origin
        git_rename_remote('origin','old-origin')

        #git remote add origin http://gitlab.localhost.com/path/name.git
        giturl = f'git@{url}{path}{name}.git'
        git_add_remote(giturl)

        #git push -u origin --all        
        git_push('origin', '--all') # a bit cheeky but works

        #git push -u origin --tags        
        git_push('origin', '--tags') # a bit cheeky but works

def main(argv=()):
    repo = None
    url = None
    branch = 'main'

    if len(argv) < 5:
        print('Command syntax: python|py git_pull -d <root directory> -u <url> -h')
        return
    
    for i in range(len(argv)):
        #if i == 1:
        #    continue
        if argv[i] == '-d':
            repo = argv[i + 1]
            print(f'Using folder: {repo}')
        elif argv[i] == '-u':
            url = f'{argv[i + 1]}:'
        elif argv[i] == '-b':
            branch = f'{argv[i + 1]}:'
            print(f'Using url: {url}')
        elif argv[i] == '-h':
            print(f'''Command syntax: python|py git_pull -d [root directory] -u [url] -b [branch] -h
                options:

                -d [root directory] The absolute path to the directory that mimics the GitLab repository structure
                -u [url]            The url of the GitLab instance
                -b [branch]         The branch to push too, defaults to main
                -h                  Prints this help, and stops''')
            return

    projects = get_project_list()
    project_list = []
    for p in projects:
        project_list.append(p['path'] + p['name'])

    chdir(repo)
    dirs = list_folders(os.getcwd())

    for dir in dirs:
        [path, name, version] = get_project_parts(dir, repo)
        if f'{path}{name}' in project_list:
            print(f'Process repo: {dir}')
            #cd existing_folder
            chdir(os.path.join(repo, dir))
            ldirs = list_folders(os.getcwd())
            if os.path.join(os.getcwd(), '.git') in ldirs:
                push_existing_repo(path, name, version, url, branch)
                print(f'Repo handled as an existing repository.')
            else:
                push_existing_folder(path, name, version, url, branch)
                print(f'Repo handled as an existing directory.') 
            

if __name__ == "__main__":
    main(sys.argv)