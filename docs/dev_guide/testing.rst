Test guidelines
==================================

Testing is based on sqa-baseline_ criteria, tox_ automation is used to 
simplify the testing process.

.. _sqa-baseline: https://indigo-dc.github.io/sqa-baseline/
.. _tox: https://tox.readthedocs.io/en/latest/

To install it with pip use:

.. code-block:: bash
    
    $ pip install tox

To run unit and functional tests together with reports use:

.. code-block:: bash

    $ tox
    ...
    clean: commands succeeded
    stylecheck: commands succeeded
    bandit: commands succeeded
    docs: commands succeeded
    py36: commands succeeded
    report: commands succeeded
    ...

The last coverage report output is produced at **htmlcov** which 
can be displayed in html format accessing to **index.html**.

The last Pep8 report produced by flake8 at the output file
**flake8.log**.

However, you can also run different test configurations using 
different tox environments:


Code Style [QC.Sty]
-----------------------
Test pep8 maintenance style conventions based on pylint format. 
To run stylecheck use:

.. code-block:: bash

    $ tox -e stylecheck
    ...
    stylecheck: commands succeeded
    ...


Functional Testing [QC.Fun]
---------------------------
Located inside tests package folder (./tests). Functional testing is
used to test the system from a general overview of the application.
To run functional tests use:

.. code-block:: bash

    $ tox -e functional
    ...
    functional: commands succeeded
    ...

This environment also provide a coverage term report for the tests.
The framework used is pytest_ to provide a simple syntax to test all 
possible combinations from the user point of view.

Pytest detects directly all tests following the test_discovery_
naming conventions. Therefore all functional tests should be 
located on the **tests** folder at the package root and start 
with **test**. For example *test_sources.py*.

.. _pytest: https://docs.pytest.org/en/stable/
.. _test_discovery: https://docs.pytest.org/en/reorganize-docs/new-docs/user/naming_conventions.html

More than 500 test combinations are generated using which otherwise 
might not be feasible using other python test frameworks.


Security [QC.Sec]
-----------------------
Security checks are performed by bandit_, a tool designed to find 
common security issues in Python code.
To run security checks use:

.. code-block:: bash

    $ tox -e functional
    ...
    functional: commands succeeded
    ...

.. _bandit: https://pypi.org/project/bandit/


Documentation [QC.Doc]
-----------------------
Documentation is build using sphinx_, a tool designed to create 
documentation based on code.
To run documentation build checks use:

.. code-block:: bash

    $ tox -e docs
    ...
    docs: commands succeeded
    ...

.. _sphinx: https://www.sphinx-doc.org/en/master/

The HTML pages are build inside in docs/_build.

