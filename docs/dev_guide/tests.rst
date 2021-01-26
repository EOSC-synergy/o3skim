Tests
==================================


Tests should run using tox_, an automation is used to simplify the 
testing process.

.. _tox: https://tox.readthedocs.io/en/latest/


To install it with pip use:

.. code-block:: bash
    
    $ pip install tox

Tests are divided into two types:

- Black-Box tests: Based on pytest_ framework, test the functionality 
  of the application without peering into its internal structures or 
  workings.
- White tests: Based on unittest_ framework, test the internal 
  structures of the application.

.. _pytest: https://docs.pytest.org/en/stable/
.. _unittest: https://tox.readthedocs.io/en/latest/

To run White and Black-Box tests use:

.. code-block:: bash

    $ tox tests o3skim/*.py
    ...
    py36: commands succeeded
    ...

This command generates a complete test report together with a 
coverage and pep8 report.


Black-Box tests:
----------------

The framework used is pytest_ to provide a simple syntax to 
test all possible combinations from the user point of view.

Pytest detects directly all tests following the test_discovery_
naming conventions. Therefore all Black-Box tests should be 
located on the **tests** folder at the package root and start 
with **test**. For example *test_sources.py*.

More than 500 test combinations are generated using which otherwise 
might not be feasible using other python test frameworks. 

.. _pytest: https://docs.pytest.org/en/stable/
.. _test_discovery: https://docs.pytest.org/en/reorganize-docs/new-docs/user/naming_conventions.html

To run only Black-Box tests simply call tox followed by the 
folder with the test location:

.. code-block:: bash

    $ tox tests
    ...
    py36: commands succeeded
    ...


White tests:
------------

The framework used is unittest_, a simple and extended test framework
which ships by default together with python.

The usage is very simple and straight forward for simple test, but
the difficulty to parametrize and combine multiple test fixtures 
makes it not suitable for Black-Box testing without a very complex
customization.

To simplify code usage and testing, the white tests should be located
on the same file than the function / class are supposed to test.

To run only White tests simply call tox followed by the module files
you would like to test. You can also use the wildcard '*' to selected
and test all python modules:

.. code-block:: bash

    $ tox o3skim/*.py
    ...
    py36: commands succeeded
    ...


Coverage and Pep8 reports:
--------------------------

One of the benefits of tox test automation is the capability to 
generate code reports during testing.

The last coverage report output is produced at **htmlcov** which 
can be displayed in html format accessing to **index.html**.


The last Pep8 report produced by flake8 at the output file
**flake8.log**.

