- virtual environments: <br />
 * `pip install venv` or ` pip install upgrade venv`
 * `python3 -m venv ~/.virtualenvs/[path]`
 * activated with `source ~/.virtualenvs/[path]/bin/activate`
    * this can be aliased in `.bash_profile`, `.zshrc`, etc as follows:
```
function workon_env {
source ~/.virtualenvs/[path]/bin/activate
}
```
