Install
=======


Requirements
------------

:py:mod:`edxia` requires 

* `Python`_ 3 (tested with python versions 3.6 and 3.7). 
* `scipy`_/`numpy`_/`matplotlib`_
* `pandas`_
* `Glue`_ (version >0.15)
* `py_expression_eval`_..

.. _python: https://www.python.org/
.. _scipy: https://www.scipy.org/
.. _numpy: https://numpy.org/
.. _matplotlib: https://matplotlib.org/
.. _pandas: https://pandas.pydata.org/
.. _Glue: http://glueviz.org/index.html
.. _py_expression_eval: https://pypi.org/project/py-expression-eval/

.. note::
    The `Anaconda distribution <https://www.anaconda.com/distribution>`_ might be used to install these dependances.

    
Installation
------------

Installation with conda
^^^^^^^^^^^^^^^^^^^^^^^

With a valid `anaconda distribution <https://www.anaconda.com/distribution>`_ installation (anaconda or miniconda), the :py:mod:`edxia` package can be installed with the requirements using the conda command

.. code:: bash

    conda install -c specmicp edxia

To update a previous installation, the following command can be executed:

.. code:: bash

    conda update -c specmicp edxia


Installation with pip
^^^^^^^^^^^^^^^^^^^^^

The :py:mod:`edxia` package is uploaded to Pypi, the `Python Package Index <https://pypi.org/project/edxia/>`_. Therefore it is possible to install the latest version with its requirements very easily in any valid python installation:

.. code:: bash

    pip install edxia

By default, this command attempt a system-wide installation. The package can be installed for the user only:

.. code:: bash

    pip install edxia --user
    
To update a previous installation, the following command can be executed:

.. code:: bash

    pip install edxia --upgrade

Installation from sources
^^^^^^^^^^^^^^^^^^^^^^^^^


The package can be installed directly from the `sources <https://bitbucket.org/specmicp/edxia/src/master/>`_. The latest version can be dowloaded directly from the git repository:

.. code:: bash

    git clone https://bitbucket.org/specmicp/edxia.git
    
It can then be installed with the following commands

.. code:: bash
    
    cd edxia
    python setup.py install
 
