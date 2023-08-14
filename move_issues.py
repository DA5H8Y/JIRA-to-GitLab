import requests
from io import StringIO
import urllib3
import urllib.request
import gitlab
from jira import JIRA

gl = None
jira = None
jira_projects = ()

#######################################################
#        MAKE SURE THESE DETAILS ARE CORRECT          #
#######################################################
gl = gitlab.Gitlab.from_config('local', ['gitlab.cfg'])

jira = JIRA(server='http://localhost:8080',
            token_auth='??????????/')  # Self-Hosted Jira (e.g. Server): the PAT token
########################################################
#                                                      #
########################################################

urllib3.disable_warnings()

# Get all projects viewable by anonymous users.
jira_projects = jira.projects()

for jira_project in jira_projects:
    gl_project = None
    gl_project_id = None

    jira_issues = issues_in_proj = jira.search_issues(
        f'project={jira_project.name}')

    for jira_issue in jira_issues:
        issue_id = None

        reporter = jira_issue.fields.reporter
        gl_reporter = gl.users.list(username=reporter.name)[0]

        if gl_reporter is None:
            reporter_gl = gl
        else:
            reporter_it = gl_reporter.impersonationtokens.create(
                {'name': 'token1', 'scopes': ['api']})
            # use the token to create a new gitlab connection
            reporter_gl = gitlab.Gitlab(gl.url, private_token=reporter_it.token)

        gl_project = reporter_gl.projects.list(search=jira_project.name)[0]
        if gl_project:
            gl_project_id = gl_project.get_id()
        else:
            print(f'Could not find a GitLab Project that matches {jira_project.name}')
            continue

        # Create issue
        gl_issue = gl_project.issues.create({'title': jira_issue.fields.summary,
                                                'description': jira_issue.fields.description,
                                                'created_at': jira_issue.fields.created})
        issue_id = gl_issue.get_id()

        # Get attachments and upload (doesn't seem to upload to GitLab)
        for jira_attachment in jira_issue.fields.attachment:
            author = jira_attachment.author
            gl_author = gl.users.list(username=author.name)[0]

            if gl_author is None:
                author_gl = gl
            else:
                author_it = gl_author.impersonationtokens.create(
                    {'name': 'token1', 'scopes': ['api']})
                # use the token to create a new gitlab connection
                author_gl = gitlab.Gitlab(gl.url, private_token=author_it.token)
                
            gl_project2 = author_gl.projects.get(gl_project_id)
            file = jira_attachment.get()
            file2 = urllib.request.urlretrieve(jira_attachment.content, jira_attachment.filename)

            gl_issue2 = gl_project2.upload(filename=jira_attachment.filename, filedata=file)
        
        #Get comments
        for jira_comment in jira_issue.fields.comment.comments:
            author = jira_comment.author
            gl_author = gl.users.list(username=author.name)[0]

            if gl_author is None:
                author_gl = gl
            else:
                author_it = gl_author.impersonationtokens.create(
                    {'name': 'token1', 'scopes': ['api']})
                # use the token to create a new gitlab connection
                author_gl = gitlab.Gitlab(gl.url, private_token=author_it.token)
                
            gl_project2 = author_gl.projects.get(gl_project_id)
            gl_issue2 = gl_project2.issues.get(issue_id)
            gl_issue2.notes.create({'body': jira_comment.body,
                                        'created_at':jira_comment.created})
