import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sipcp",
    version="0.3.1",
    author="Federico Torrielli",
    author_email="evilscript@protonmail.com",
    description="An example program querying the YAPO ontology",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/federicotorrielli/modsem",
    packages=["sipcp"],
    entry_points={'console_scripts': [
        'sipcp = sipcp.sipcp:app',
    ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["click==7.1.2", "isodate==0.6.0", "pyparsing==2.4.7", "PyYAML==5.3.1", "rdflib==5.0.0",
                      "six==1.15.0", "typer==0.3.2", "SPARQLWrapper==1.8.5", "fuzzywuzzy==0.18.0",
                      "levenshtein==0.12.0"]
)
