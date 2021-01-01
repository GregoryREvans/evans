import sphinx_rtd_theme
from pygments.formatters.latex import LatexFormatter
from sphinx.highlighting import PygmentsBridge


class CustomLatexFormatter(LatexFormatter):
    def __init__(self, **options):
        super(CustomLatexFormatter, self).__init__(**options)
        self.verboptions = r"""formatcom=\footnotesize"""


PygmentsBridge.latex_formatter = CustomLatexFormatter

### CORE ###

add_function_parentheses = True
copyright = "2018-2020, Gregory Rowland Evans"
exclude_patterns = []

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.graphviz",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "abjad.ext.sphinx",
    "sphinx_autodoc_typehints",
    "uqbar.sphinx.api",
    "uqbar.sphinx.book",
    "uqbar.sphinx.inheritance",
    "uqbar.sphinx.style",
]

html_favicon = "_static/notes.ico"
html_logo = "_static/perllan-logo.png"
master_doc = "index"
project = "Perllan API"
pygments_style = "sphinx"
release = "0.3"
source_suffix = ".rst"
templates_path = ["_templates"]
version = "0.3"

### HTML ###

html_last_updated_fmt = "%b %d, %Y"
html_show_sourcelink = True
html_static_path = ["_static"]
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "collapse_navigation": True,
    "navigation_depth": -1,
    "sticky_navigation": True,
    "style_external_links": True,
    "display_version": True,
    "style_nav_header_background": "#556B2F",
}
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

### HTML HELP ###

htmlhelp_basename = "PerllanAPIdoc"

### LATEX ###

latex_elements = {
    "inputenc": r"\usepackage[utf8x]{inputenc}",
    "utf8extra": "",
    "papersize": "letterpaper",
    "pointsize": "10pt",
    "preamble": r"""
    \usepackage{upquote}
    \pdfminorversion=5
    \setcounter{tocdepth}{2}
    \definecolor{VerbatimColor}{rgb}{0.95,0.95,0.95}
    \definecolor{VerbatimBorderColor}{rgb}{1.0,1.0,1.0}
    \hypersetup{unicode=true}
    """,
}

latex_documents = [
    ("index", "PerllanAPI.tex", "Perllan API", "Gregory Rowland Evans", "manual")
]

latex_domain_indices = False

### EXTESNIONS ###

autodoc_member_order = "groupwise"
graphviz_dot_args = ["-s32"]
graphviz_output_format = "svg"
intersphinx_mapping = {
    "http://josiahwolfoberholtzer.com/uqbar/": None,
    "http://www.sphinx-doc.org/en/master/": None,
    "https://docs.python.org/3.7/": None,
}
todo_include_todos = True

uqbar_api_title = "Perllan API"
uqbar_api_source_paths = ["evans", "abjadext.microtones", "tsmakers"]
uqbar_api_root_documenter_class = "uqbar.apis.SummarizingRootDocumenter"
uqbar_api_module_documenter_class = "uqbar.apis.SummarizingModuleDocumenter"
uqbar_api_member_documenter_classes = [
    "uqbar.apis.FunctionDocumenter",
    "uqbar.apis.SummarizingClassDocumenter",
]

uqbar_book_console_setup = [
    "import abjad",
    "from abjad import *",
    "import abjadext",
    "import fractions",
]
try:
    from abjadext import rmakers  # noqa

    uqbar_book_console_setup.append("from abjadext import rmakers")
except ImportError:
    raise Exception("Could not import rmakers from abjadext")

try:
    from abjadext import microtones  # noqa

    uqbar_book_console_setup.append("from abjadext import microtones")
except ImportError:
    raise Exception("Could not import microtones from abjadext")

try:
    import baca  # noqa

    uqbar_book_console_setup.append("import baca")
except ImportError:
    raise Exception("Could not import baca")

try:
    import evans  # noqa

    uqbar_book_console_setup.append("import evans")
except ImportError:
    raise Exception("Could not import evans")

try:
    import tsmakers  # noqa

    uqbar_book_console_setup.append("import tsmakers")
except ImportError:
    raise Exception("Could not import tsmakers")

try:
    import quicktions  # noqa

    uqbar_book_console_setup.append("import quicktions")
except ImportError:
    raise Exception("Could not import quicktions")

uqbar_book_console_teardown = []
uqbar_book_extensions = [
    "uqbar.book.extensions.GraphExtension",
    "abjad.ext.sphinx.LilyPondExtension",
]
uqbar_book_strict = False
uqbar_book_use_black = True
uqbar_book_use_cache = True
