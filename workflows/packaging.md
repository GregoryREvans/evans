- packaging:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;We want to have a `wrapper directory` and a `contents directory`, both having the same name. The wrapper directory should contain things like a `readme.md` file, `setup.py`, `.gitignore`, `.travis.yml`, and the `contents directory` among other things.<br/> <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Inside the contents directory should be all of the relevant files for the package. If you want to cleanly refer to items within the package from outside of the package, adding imports to the `__init__.py` files is the solution, but beware, you can accidentally call things before they are imported. Also, parallel importing can be tricky so don't try to truncate import paths while refering to items within the package itself.<br/> <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;any directory containing an `__init__.py` file, even if it is empty, can be seen by python as a package.<br/> <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;We can use `setup.py` to install the package, but more often than not, it should be best to add the path of the `wrapper directory` of the package to the `PYTHONPATH`. We can do this in `.bash_profile` for a bash shell or in `.zshrc` for a zsh shell. **Make sure to concatenate elements into you python path and not overwrite it. This can be done with `:`**<br/> <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;installing with `setup.py`: `python setup.py install`<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;add git submodule in contents directory:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`cd` into contents directory<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`git submodule add` https://github.com/user/repo<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;can be updated with `git pull`<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;git submodule deletion:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Delete the relevant section from the .gitmodules file.<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Stage the .gitmodules changes git add .gitmodules<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Delete the relevant section from .git/config.<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Run git rm --cached path_to_submodule (no trailing slash).<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Run rm -rf .git/modules/path_to_submodule (no trailing slash).<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Commit git commit -m "Removed submodule."<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Delete the now untracked submodule files rm -rf path_to_submodule<br/>
