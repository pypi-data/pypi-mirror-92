# pointwise-libs
library functions for pointwise polisci research

## How to build package

First, ensure that there's a `.pypirc` in your home directory `~/`
that looks like this:

```
[pypi]
    username = __token__
    password = pypi-GET_API_TOKEN_FROM_PYPI_ACCOUNT
```

Then build with

```
python3 -m pip install --user --upgrade setuptools wheel
python3 -m pip install --user --upgrade twine
rm -r dist
# Increment the version in `setup.py`
python3 setup.py sdist bdist_wheel
twine upload dist/*
```


