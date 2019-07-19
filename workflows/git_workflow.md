- create and clone a repository:<br/>
        1. create new repo on github website<br/>
        2. include gitignore<br/>
        3. copy repo link<br/>
        4. enter shell<br/>
        5. change to intended directory<br/>
        6. type:<br/>
            git clone [insert repo link]<br/>
            return<br/>

- push new commit to github:<br/>
        1. save file<br/>
        2. go to shell<br/>
            2-1. enter directory of repo/file<br/>
            2-2. type:<br/>
                2-2-1. `git status`<br/>
                (to see what has changed since last push)<br/>
                2-2-2. if all changes are to be pushed<br/>
                    type: `git add .`<br/>
                    (optionally confirm with `git status`)<br/>
                2-2-3. if commit is intended<br/>
                    type: `git commit`<br/>
                2-2-4. type:<br/>
                    `git push`<br/>

- going back to past repositories:<br/>
        0. Exploratory<br/>
            0-1. optional: make new clone in safe location<br/>
            0-2. git checkout <hash found in commits><br/>
            0-3. explore to heart's desire<br/>
            0-4. optional: fix errors<br/>
            0-5. git checkout master<br/>
        1. Reverting a repo<br/>
            1-1. git rebase/merge <branch or hash><br/>

- merging vs rebasing branch from master:<br/>
        **git merge**: preserves history but makes history more verbose<br/>
        **git rebase**: bases new branch on the most recent update of master<br/>
        source: https://www.atlassian.com/git/tutorials/merging-vs-rebasing<br/>
        give preference to the following:<br/>
            git checkout greg/dev -> git merge master<br/>
            (this process merges changes from the master branch *into* greg/dev)<br/>
        Hint at template:<br/>
            1. cd into repo<br/>
            2. checkout branch that needs changes applied to it<br/>
            3. git **merge or rebase** *branch source of changes*<br/>
