import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dropbox-pi-cli",
    version="0.0.5",
    author="Germán Martinez",
    author_email="germand_m@hotmail.com",
    description="A command line tool for raspberry py",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/martinezger/dropbox-pi-cli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    py_modules=["commands",],
    install_requires=["Click",],
    entry_points="""
        [console_scripts]
        dropbox-pi=commands:dropbox_cli
    """,
)
