Test guidelines
==================================

Testing is based on sqa-baseline_ criteria, tox_ automation is used to 
simplify the testing process.

.. _sqa-baseline: https://indigo-dc.github.io/sqa-baseline/
.. _tox: https://tox.readthedocs.io/en/latest/

To install it with pip use:

.. code-block:: bash
    
    $ pip install tox

To run style checks, coverage, functional and security tests,
go to the project root folder and run :code:`tox`:

.. code-block:: bash

    $ tox
    ...
    qc.sty: commands succeeded
    qc.uni: commands succeeded
    qc.sec: commands succeeded


Code Style [QC.Sty]
-----------------------
Test pep8 maintenance style conventions based on pylint format. 
To run stylechecks use:

.. code-block:: bash

    $ tox -e qc.sty
    ...
    qc.sty: commands succeeded
    ...

The last Pep8 report produced by flake8 at the output file
**flake8.log**.


Unit Testing [QC.Uni]
---------------------------
Located inside tests package folder (./tests). Functional testing is
used to test the system from a general overview of the application.
To run functional tests use:

.. code-block:: bash

    $ tox -e qc.uni
    ...
    qc.uni: commands succeeded
    ...

The last coverage report output is produced at the folder **htmlcov**
which can be displayed in html format accessing to **index.html**.

This environment also provide a coverage term report for the tests.
The framework used is pytest_ to provide a simple syntax to test all 
possible combinations from the user point of view.

.. _pytest: https://docs.pytest.org/en/stable/

More than 300 test combinations are generated using which otherwise 
might not be feasible using other python test frameworks.


Security [QC.Sec]
-----------------------
Security checks are performed by bandit_, a tool designed to find 
common security issues in Python code.
To run security checks use:

.. _bandit: https://pypi.org/project/bandit/

.. code-block:: bash

    $ tox -e functional
    ...
    functional: commands succeeded
    ...

Security report is printed at terminal.


Documentation [QC.Doc]
-----------------------
Documentation is build using sphinx_, a tool designed to create 
documentation based on code.  To run documentation build checks use:

.. code-block:: bash

    $ tox -e qc.doc
    ...
    qc.doc: commands succeeded
    ...

.. _sphinx: https://www.sphinx-doc.org/en/master/

The HTML pages are build inside in docs/_build.

.. note::
    Requires pandoc~=2.12 executables in your system.
