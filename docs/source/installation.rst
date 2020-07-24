Installation
============

Perllan works on OSX, Unix/Linux, and Windows with Python 3.6+.

Installing Perllan
------------------

Install packages in the Perllan network from their respective `GitHub` repository,
    via `git` (https://git-scm.com/)

Install ``abjad-ext-microtones``::

    ~$ git clone https://github.com/GregoryREvans/abjad-ext-microtones.git
    ~$ cd abjad-ext-microtones
    abjad-ext-microtones$ pip install -e .

Install ``evans``::

    ~$ git clone https://github.com/GregoryREvans/evans.git
    ~$ cd evans
    evans$ pip install -e .

Install ``tsmakers``::

    ~$ git clone https://github.com/GregoryREvans/tsmakers.git
    ~$ cd tsmakers
    tsmakers$ pip install -e .

Installing dependencies
--------------------------------

Installing Lilypond
````````````````````````

Install Lilypond::

    wget -q -O ~/Applications/lilypond_versions http://lilypond.org/download/binaries/linux-64//lilypond-2.19.84-1.linux-64.sh
    sh ~/Applications/lilypond_versions --batch

Installing Abjad
````````````````````````

Install Abjad::

    ~$ git clone https://github.com/Abjad/abjad.git
    ~$ cd abjad
    abjad$ pip install -e .

Virtual environments
--------------------

We strongly recommend installing packages into a virtual environment, especially
if you intend to hack on Perllan's own source code. Virtual environments allow
you to isolate `Python` packages from your systems global collection of
packages. They also allow you to install Python packages without ``sudo``. The
`virtualenv` package provides tools for creating Python virtual environments,
and the `virtualenvwrapper` package provides additional tools which make
working with virtual environments incredibly easy.

To install and setup `virtualenv` and `virtualenvwrapper`:

::

    ~$ pip install virtualenvwrapper
    ...
    ~$ mkdir -p $WORKON_HOME
    ~$ export WORKON_HOME=~/.virtualenvs
    ~$ source /usr/local/bin/virtualenvwrapper.sh

Make the last two lines teaching your shell about the virtual environment
tools "sticky" by adding them to your profile:

::

    ~$ echo "export WORKON_HOME=~/.virtualenvs" >> ~/.profile
    ~$ echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.profile

With the virtual environment tools installed, create and activate a virtual
environment. You can now install Perllan packages into that environment:

::

    ~$ mkvirtualenv my-abjad-env
    ...
    (my-abjad-env) ~$ git clone https://github.com/Abjad/abjad.git
    (my-abjad-env) ~$ cd abjad
    (my-abjad-env) abjad$ pip install -e ".[development]"

See the `virtualenvwrapper` documentation for instructions on how to use the
provided tools for working creating, deleting, activating and deactivating
virtual environments: ``mkvirtualenv``, ``rmvirtualenv``, ``workon`` and
``deactivate``.
