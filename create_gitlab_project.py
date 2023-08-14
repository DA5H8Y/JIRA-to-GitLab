import gitlab

def create_project(gl, PROJECT_PATH: str):
    project = None
    group = None
    group_id = None
    project_id = None

    # check to see if the namespace exists.
    namespaces = PROJECT_PATH.split("/")
    group_name = "/".join(namespaces[:-1])
    project_name = namespaces.pop()

    # Search group create if it doesn't exist
    try:
        group = gl.groups.get(group_name)
        group_id = group.get_id()
    except:
        group_id = create_group(gl, group_name)
    
    # Search group parent create if it doesn't exist
    try:
        project = gl.projects.get(PROJECT_PATH)
        project_id = project.get_id()
    except:
        project = gl.projects.create({'name': project_name, 'namespace_id': group_id})
        project_id = project.get_id()

    return project_id

def create_group(gl, GROUP_PATH: str):
    group = None
    group_id = None
    parent = None
    parent_id = None
    group_name = None
    parent_name = None

    namespaces = GROUP_PATH.split("/")
    parent_name = "/".join(namespaces[:-1])
    group_name = namespaces.pop()
    
    # Search group create if it doesn't exist
    if not parent_name:
        group = gl.groups.create({'name': group_name, 'path': group_name})
        group_id = group.get_id()
    else:
        try:
            parent = gl.groups.get(parent_name)
            parent_id = parent.get_id()
        except:
            parent_id = create_group(gl, parent_name)
            
        group = gl.groups.create({'name': group_name, 'path': group_name,'parent_id': parent_id})
        group_id = group.get_id()

    return group_id

if __name__ == "__main__":
    gl = gitlab.Gitlab.from_config('default', ['gitlab.cfg'])  
    create_project(gl, 'systems2/test/awesome_project')