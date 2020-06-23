- virtual environments: <br />
 * `pip install virtualenv` or ` pip install upgrade virtualenv`
 * `python3 -m virtualenv ~/.virtualenvs/[path]`
 * activated with `source ~/.virtualenvs/[path]/bin/activate`
    * this can be aliased in `.bash_profile`, `.zshrc`, etc as follows:
```
function workon_env {
source ~/.virtualenvs/[path]/bin/activate
}
```
