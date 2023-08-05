from os import path
from subprocess import run

from setuptools import setup


def git_describe():
    output = run(
        "git describe --tags --dirty --broken --long",
        capture_output=True,
        check=True,
        text=True,
    ).stdout
    parts = output.strip()[1:].split("-")
    if len(parts) == 3 and parts[1] == "0":
        return parts[0]
    else:
        parts[1] = f".post{parts[1]}" if parts[1] != "0" else ""
        parts[2] = f"+{'.'.join(parts[2:])}"
        del parts[3:]
        return "".join(parts)


def readme():
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
        return f.read()


setup(
    name="gitsafe",
    version=git_describe(),
    description="A tool to keep copies (aka backups) of git repositories.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/tammann/gitsafe",
    author="Tobias Ammann",
    author_email="tammann@ergonomics.ch",
    license="MIT",
    py_modules=["gitsafe"],
    install_requires=["colorama", "SQLObject", "sh", "tabulate", "tqdm", "typer"],
    extras_require={
        "dev": [
            "black",
            "wheel",
            "twine",
        ]
    },
    entry_points={
        "console_scripts": ["gitsafe=gitsafe:main"],
    },
    zip_safe=False,
)
