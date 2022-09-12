Tox command examples
====================================

Tests tco3 load functions with specific python version
------------------------------------------------------
Pattern: :code:`tox -e <py-version> tests/requirements/test_tco3.py`

Examples:
 - Python 3.8 :code:`tox -e py38 tests/requirements/test_tco3.py`
 - Python 3.9 :code:`tox -e py39 tests/requirements/test_tco3.py`


Tests zmo3 load functions with specific python version
------------------------------------------------------
Pattern: :code:`tox -e <py-version> tests/requirements/test_zmo3.py`

Examples:
 - :code:`tox -e py38 tests/requirements/test_zmo3.py`
 - :code:`tox -e py39 tests/requirements/test_zmo3.py`


Tests Code style requirements
------------------------------------------------------
Pattern: :code:`tox -e qc.sty`


Tests Units with coverage
------------------------------------------------------
Pattern: :code:`tox -e qc.uni`


Tests Documentation build
------------------------------------------------------
Pattern: :code:`tox -e qc.uni`

.. note::
    Requires pandoc~=2.12 executables in your system.

Tests Security software
------------------------------------------------------
Pattern: :code:`tox -e qc.sec`


Tests forcing recreation of virtual environments
------------------------------------------------------
Pattern: :code:`tox --recreate -e <environment>`

Examples:
 - :code:`tox -r -e py38 tests/requirements/test_zmo3.py`
 - :code:`tox --recreate -e qc.uni`

