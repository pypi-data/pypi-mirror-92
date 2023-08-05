from setuptools import setup, find_packages

exec(open("trio3270/_version.py", encoding="utf-8").read())

LONG_DESC = open("README.rst", encoding="utf-8").read()

setup(
    name="trio3270",
    version=__version__,
    description="A IBM3270 trionic library",
    long_description=LONG_DESC,
    author="Clovis Fabricio Costa",
    author_email="python.nosklo@0sg.net",
    license="GPLv3 or later",
    packages=find_packages(),
    package_data={
            'trio3270': ['data/*.exe'],
    },
    install_requires=[
        "trio", "tricycle"
    ],
    keywords=[
        "async", "io", "networking", "IBM3270", "IBM", "trio",
    ],
    python_requires=">=3.6",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Framework :: Trio",
        # COOKIECUTTER-TRIO-TODO: Remove any of these classifiers that don't
        # apply:
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        # COOKIECUTTER-TRIO-TODO: Consider adding trove classifiers for:
        #
        # - Development Status
        # - Intended Audience
        # - Topic
        #
        # For the full list of options, see:
        #   https://pypi.org/classifiers/
    ],
)
