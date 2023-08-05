from datetime import timezone, datetime
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
        Repository.fresh(source)


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
