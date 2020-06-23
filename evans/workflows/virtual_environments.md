- virtual environments: <br />
 * get `pip`
 * `pip install virtualenv` or ` pip install upgrade venv`
 * use `virtualenv` over `venv`
    * `virtualenv` puts `pip` in the environment
    * `venv` does not put `pip` in the environment?
 * `python3 -m virtualenv ~/.virtualenvs/[path]`
 * activated with `source ~/.virtualenvs/[path]/bin/activate`
    * this can be aliased in `.bash_profile`, `.zshrc`, etc as follows:
```
function workon_env {
source ~/.virtualenvs/[path]/bin/activate
}
```
