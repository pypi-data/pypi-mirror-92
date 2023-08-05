# gitsafe

A tool to keep copies (aka backups) of git repositories.

## Usage
```shell
gitsafe add https://github.com/...

gitsafe update
https://github.com/...
    Uuid: 8516fdb5-6c32-4d7f-8edc-03a7c1d66d4d
    Mode: CLONING
  Stdout:
  Stderr:
  Return: 0
    Time: 0.998 s

gitsafe add /local/repository

gitsafe list
Uuid                                  Source                  Added                       Last Updated
------------------------------------  ----------------------  --------------------------  --------------------------
8516fdb5-6c32-4d7f-8edc-03a7c1d66d4d  https://github.com/...  2021-01-20 00:36:55.005998  2021-01-20 00:37:02.957920
db0dd9d0-57a7-4b1c-8221-a293ea678501  /local/repository       2021-01-20 00:38:33.769500

```

## Development
```shell
black .
rm -rv dist/
python setup.py sdist bdist_wheel
twine upload dist/*
```
