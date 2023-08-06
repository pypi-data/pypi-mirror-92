huscy.pseudonyms
======

![PyPi Version](https://img.shields.io/pypi/v/huscy-pseudonyms.svg)
![PyPi Status](https://img.shields.io/pypi/status/huscy-pseudonyms)
![PyPI Downloads](https://img.shields.io/pypi/dm/huscy-pseudonyms)
![PyPI License](https://img.shields.io/pypi/l/huscy-pseudonyms?color=yellow)
![Python Versions](https://img.shields.io/pypi/pyversions/huscy-pseudonyms.svg)
![Django Versions](https://img.shields.io/pypi/djversions/huscy-pseudonyms)
[![Coverage Status](https://coveralls.io/repos/bitbucket/huscy/pseudonyms/badge.svg)](https://coveralls.io/bitbucket/huscy/pseudonyms)


Requirements
------

- Python 3.6+
- A supported version of Django

Tox tests on Django versions 2.1, 2.2, 3.0 and 3.1.


Installation
------

To install `husy.pseudonyms` simply run:
```
pip install huscy.pseudonyms
```



Configuration
------

First of all, the `huscy.pseudonyms` application has to be hooked into the project.

1. Add `huscy.pseudonyms` and further required apps to `INSTALLED_APPS` in settings module:

```python
INSTALLED_APPS = (
	...

	'huscy.pseudonyms',
	'huscy.subjects',
)
```

2. Create database tables by running:

```
python manage.py migrate
```


Development
------

After checking out the repository you should activate any virtual environment.
Install all development and test dependencies:

```
make install
```

Create migration files and database tables:

```
make migrate
```

We assume you're having a running postgres database with a user `huscy` and a database also called `huscy`.
You can easily create them by running

```
sudo -u postgres createuser -d huscy
sudo -u postgres createdb huscy
sudo -u postgres psql -c ";ALTER DATABASE huscy OWNER TO huscy"
sudo -u postgres psql -c "ALTER USER huscy WITH PASSWORD '123';"
```
