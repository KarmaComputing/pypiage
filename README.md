# pypiage

A package for finding the least updated packages your project depends on.


# Install

```
pip install pypiage
```

# Usage

Quickly get the least updated packages referenced in your requirements.txt:
```
cat requirements.txt | pypiage
```

Find our when a certain python package was last updated:

```
echo django | pypiage
```

# Output

You get a pipe `|` separated list of `<package-name>|<upload-date>`
where `upload-date` is the last recorded time the package was uploaded
to PyPi.

For example:

Given a requirements.txt like:

```
Flask==2.2.0
requests==2.28.0
numpy==1.24.2
```

When you give that file to `pypiage`:

```
pypiage requirements.txt
```

The output will list the latest uploaded date of the packages you gave `pypiage`:

```
INFO:pypiage:Getting package info for Flask
INFO:pypiage:Getting package info for requests
INFO:pypiage:Getting package info for numpy
requests|2023-01-12 16:24:54
numpy|2023-02-05 20:12:05
Flask|2023-02-15 22:43:57
```

> Note: <br />
  If you don't like the `INFO` log output, then
  you can turn logging off with: `PYTHON_LOGLEVEL=ERROR pypiage requirements.txt` to get less verbose output:

```
requests|2023-01-12 16:24:54
numpy|2023-02-05 20:12:05
Flask|2023-02-15 22:43:57
```

Remember you can also `cat` a list of packages to `pypiage` and it
will read from standard input:

```
cat requirements.txt | pypiage
```

## Why does this exist?

I found myself with a large codebase and wanted to quicky get a sense of which package dependencies were likley no longer maintained (and therefore candidates for removal), and checking their last upload date is a reasonable first pass check.
