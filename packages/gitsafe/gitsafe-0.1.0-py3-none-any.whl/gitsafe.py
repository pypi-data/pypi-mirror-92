from configparser import ConfigParser
from datetime import timezone, datetime
from glob import glob
from os import getcwd
from os.path import exists
from subprocess import run
from time import time
from typing import List
from uuid import uuid4

from sqlobject import connectionForURI, sqlhub, SQLObject, StringCol, DateTimeCol
from tabulate import tabulate
from typer import Typer, echo, style, colors


class Repository(SQLObject):
    uuid = StringCol(alternateID=True)
    source = StringCol(alternateID=True)
    added = DateTimeCol(default=DateTimeCol.now, notNone=True)
    updated = DateTimeCol()

    @classmethod
    def fresh(cls, source):
        return Repository(
            uuid=str(uuid4()),
            source=source,
            added=datetime.now(tz=timezone.utc),
            updated=None,
        )


main = Typer()

ROOT = getcwd()


@main.callback()
def context_callback(debug: bool = False):
    sqlhub.processConnection = connectionForURI(f"sqlite:/{ROOT}/gitsafe.sqlite3")
    Repository._connection.debug = debug
    Repository.createTable(ifNotExists=True)


@main.command()
def list():
    print(
        tabulate(
            [
                (repo.uuid, repo.source, repo.added, repo.updated)
                for repo in Repository.select()
            ],
            headers=("Uuid", "Source", "Added", "Last Updated"),
        )
    )


@main.command()
def add(sources: List[str]):
    for source in sources:
        try:
            Repository.fresh(source)
        except Exception as exception:
            echo(style(f"Adding {source} failed: {exception}"))


@main.command()
def add_remotes(pattern: str):
    detected = []
    for path in glob(f"{pattern}/.git/config", recursive=True):
        config = ConfigParser()
        config.read(path)
        url = config['remote "origin"']["url"]

        if "github.com" in url:
            url = url.replace("ssh://git@github.com/", "https://github.com/")

            if "github.com" in url and url.endswith(".git"):
                url = url.replace("git://github.com/", "https://github.com/").replace(
                    "git@github.com:", "https://github.com/"
                )[:-4]

            echo(style("GITHUB", fg=colors.BRIGHT_GREEN) + f" {url}")
            detected.append(url)
        else:
            echo(style("UNHANDLED", fg=colors.RED) + f" {url}")

    echo(style(f"Importing {len(detected)} repositories...", fg=colors.BLUE))
    add(detected)


@main.command()
def update(fast: bool = True):
    for repo in Repository.select():
        if fast and repo.updated:
            age = (datetime.utcnow() - repo.updated).total_seconds()
            if age <= 86400:
                continue

        echo(style(repo.source, fg=colors.BRIGHT_BLUE))
        echo(f"    Uuid: " + style(repo.uuid, fg=colors.YELLOW))

        t = -time()
        path = f"{ROOT}/{repo.uuid}"
        if exists(path):
            echo(f"    Mode: " + style("UPDATING", fg=colors.BRIGHT_MAGENTA))
            cmd = f"git --git-dir={path} remote update --prune"
        else:
            echo(f"    Mode: " + style("CLONING", fg=colors.BRIGHT_MAGENTA))
            cmd = f"git clone --mirror {repo.source} {path}"

        try:
            process = run(
                cmd,
                capture_output=True,
                check=True,
                text=True,
            )
            echo(f"  Stdout: " + style(process.stdout.strip(), fg=colors.BRIGHT_BLACK))
            echo(f"  Stderr: " + style(process.stdout.strip(), fg=colors.MAGENTA))
            echo(f"  Return: " + style(str(process.returncode), fg=colors.CYAN))
            repo.updated = datetime.now(tz=timezone.utc)
        except Exception as e:
            echo(f" Failure: " + style(str(e), fg=colors.RED))

        t += time()

        echo(f"    Time: {t:.3f} s")
        echo()


if __name__ == "__main__":
    main()
