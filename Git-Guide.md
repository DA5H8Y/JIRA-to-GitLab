# GitLab Guide

Hopefully this guide provides a little help with using git/GitLab.

## GitLab

GitLab is being used as a replacement for JIRA and Bitbucket.

### Structure

The structure of the groups and projects with GitLab is as specified below:

* RandD
  * RandD (Project) - for issue tracking
  * Documents (Project)
  * Tasks
    * RandD XXX - XXX (Project)
    * ...
* Tools
  * Tools (Project) - for issue tracking
  * Simulink (Project)
  * ...
* Toolboxes
  * Toolboxes (Project) - for issue tracking
  * RandD Blockset (Project)
  * ...

### Issues

Issues should be raised as per previous JIRA templates using the projects with the same name as the groups as issue management containers.

### Server Management

Server Management is captured in another file [GitLabServerManagement](GitLabServerManagement.md)

## Git

From 2023 onwards, the team will use more of the features of git - such as tagging and branching.

### Tags

Tags can be used to track releases of a project, and are used within the Tools, Toolboxes for such a purpose.

#### List tags

To lists the tags available use the git tag command, you can also use the option -l followed by a pattern to match for example ```-l v*.0```

```bash
$ git tag
v1.0
v2.0
```

#### Create tags

To create a tag you need to specify a name using the option ```-a name``` and the option ```-m "message"``` . If you don’t specify a message for an annotated tag, Git launches your editor so you can type it in.

```bash
git tag -a v1.4 -m "my version 1.4"
```

You can also tag later, use the log command, see below, to get the commit hash then just add the has (or part of it) when making your tag

```bash
git tag -a v1.2 9fceb02
```

#### Sharing tags

Tags need to be pushed just like any other change

```bash
$ git push origin v1.5
Counting objects: 14, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (12/12), done.
Writing objects: 100% (14/14), 2.05 KiB | 0 bytes/s, done.
Total 14 (delta 3), reused 0 (delta 0)
To git@gitlab.localhost.com:randd:randd-001-simple-git.git
* [new tag]         v1.5 -> v1.5
 ```

#### Deleting tags

To delete tags locally and on the server use the following two commands

```bash
git tag -d NewTag
git push origin --delete NewTag
```

#### Checking out tags

If you want to view the versions of files a tag is pointing to, you can do a git checkout of that tag, although this puts your repository in “detached HEAD” state, which has some ill side effects, but not necessary when you're handling releases.

```bash
$ git checkout v2.0.0
Note: switching to 'v2.0.0'.
You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by performing another checkout.
If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:
git switch -c <new-branch-name>
Or undo this operation with:
git switch -
Turn off this advice by setting config variable advice.detachedHead to false
HEAD is now at 99ada87... Merge pull request #89 from randd/rand-001
```

In “detached HEAD” state, if you make changes and then create a commit, the tag will stay the same, but your new commit won’t belong to any branch and will be unreachable, except by the exact commit hash. Thus, if you need to make changes — say you’re fixing a bug on an older version, for instance — you will generally want to create a branch:

```bash
$ git checkout -b version2 v2.0.0
Switched to a new branch 'version2'
```

If you do this and make a commit, your version2 branch will be slightly different than your v2.0.0 tag since it will move forward with your new changes, so do be careful.

#### Getting tag information

To get information about the tag use the option ```show```

```bash
$ git show v1.4
tag v1.4
Tagger: Dan Ashby <dan.ashby@email.co.uk>
Date:   Sat May 3 20:19:12 2014 -0700
my version 1.4
commit ca82a6dff817ec66f44342007202690a93763949
Author: Dave Morely <dave.morley@email.co.uk>
Date:   Mon Mar 17 21:52:11 2008 -0700
Change version number
```

### Commits

Commit messages should include a reference to the appropriate issue, for example;

```bash
git commit -m "[RandD#1] Initial commit."
```

### Commit History

Using the ```--pretty=oneline``` option is so useful

```bash
$ git log --pretty=oneline
15027957951b64cf874c3557a0f3547bd83b3ff6 Merge branch 'experiment'
a6b4c97498bd301d84096da251c98a07c7723e65 Create write support
0d52aaab4479697da7686c15f77a3d64d9165190 One more thing
6d52a271eda8725415634dd79daabbc4d9b6008e Merge branch 'experiment'
0b7434d86859cc7b8c3d5e1dddfed66ff742fcbc Add commit function
4682c3261057305bdd616e23b64b0857d832627b Add todo file
166ae0c4d3f420721acbb115cc33848dfcc2121a Create write support
9fceb02d0ae598e95dc970b74767f19372d61af8 Update rakefile
964f16d36dfccde844893cac5b347e7b3d44abbc Commit the todo
8a5cbc430f1a9c3d00faaeffd07798508422908a Update readme
```