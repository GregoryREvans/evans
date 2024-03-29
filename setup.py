import setuptools

install_requires = [
    "abjad",
    "numpy",
    "scipy",
    "quicktions",
]

# dependency_links=[
#     "https://github.com/GregoryREvans/tsmakers/tarball/master#egg=package-1.0"
# ]


keywords = [
    "abjad",
    "music composition",
    "music notation",
    "formalized score control",
    "lilypond",
]

if __name__ == "__main__":
    setuptools.setup(
        author="Gregory Rowland Evans",
        author_email="gregoryrowlandevans@gmail.com",
        install_requires=install_requires,
        keywords=", ".join(keywords),
        name="evans",
        packages=["evans"],
        platforms="Any",
        url="https://github.com/GregoryREvans/evans",
        version="2.0",
    )
