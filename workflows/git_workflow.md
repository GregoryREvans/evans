- create and clone a repository:
        1. create new repo on github website
        2. include gitignore
        3. copy repo link
        4. enter shell
        5. change to intended directory
        6. type:
            git clone [insert repo link]
            return

- push new commit to github:
        1. save file
        2. go to shell
            2-1. enter directory of repo/file
            2-2. type:
                2-2-1. `git status`
                (to see what has changed since last push)
                2-2-2. if all changes are to be pushed
                    type: `git add .`
                    (optionally confirm with `git status`)
                2-2-3. if commit is intended
                    type: `git commit`
                2-2-4. type:
                    `git push`

- going back to past repositories:
        0. Exploratory
            0-1. optional: make new clone in safe location
            0-2. git checkout <hash found in commits>
            0-3. explore to heart's desire
            0-4. optional: fix errors
            0-5. git checkout master
        1. Reverting a repo
            1-1. git rebase/merge <branch or hash>

- merging vs rebasing branch from master:
        **git merge**: preserves history but makes history more verbose
        **git rebase**: bases new branch on the most recent update of master
        source: https://www.atlassian.com/git/tutorials/merging-vs-rebasing
        give preference to the following:
            git checkout greg/dev -> git merge master
            (this process merges changes from the master branch *into* greg/dev)
        Hint at template:
            1. cd into repo
            2. checkout branch that needs changes applied to it
            3. git **merge or rebase** *branch source of changes*
