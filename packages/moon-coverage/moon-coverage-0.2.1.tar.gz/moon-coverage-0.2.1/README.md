ESA Moon Coverage Toolbox
=========================

Install
-------
```bash
git clone https://gitlab.univ-nantes.fr/esa-juice/moon-coverage.git moon-coverage
cd moon-coverage
pip install -e .
```

Tests
-----
Install:
```bash
pip install -r tests/requirements.txt
```

Linter:
```bash
pylint --rcfile=setup.cfg moon_coverage/ tests/**.py setup.py
flake8 moon_coverage/ tests/ setup.py
```

Test suite:
```bash
pytest --cov moon_coverage tests/
```

Docs
----
Install:
```bash
pip install -r docs/requirements.txt
```
Build the docs:
```bash
sphinx-build docs docs/_build --color -W -bhtml
```
