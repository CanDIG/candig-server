.. _development:

-----------------
Development Setup
-----------------

Thanks for your interest in the candig-server. If you have any questions,
`please let us know <https://github.com/candig/candig-server/issues>`_

.. warning::

    This guide is a work in progress, and is incomplete.

***********************
Development environment
***********************

You will need Python 3.6.x to successfully run the candig-server.

First, create a virtualenv with Python 3.6.x

and run

.. code-block:: bash

    pip clone https://github.com/CanDIG/candig-server.git
    pip install dev-requirements.txt

The default DB location for development server is `candig-example-data/registry.db`.

Assume your local `python3` instance is of Python 3.6, with sqlite3 and other required
modules built, you can run the following script to set up a dev server in a few minutes.
Even better, it will be populated with two datasets with mock data.

Test has been done on CentOS and MacOS, we expect the install to run OK on most unix
distributions. We have not tested deployment on Windows, and do not expect it to work.


.. code-block:: bash

    # Wipe previous virtualenv
    if [ -d test_server ];
         then rm -r test_server;
    fi


    # Server 1
    echo "setting up test_server"
    python3 -m venv test_server
    cd test_server
    source bin/activate
    pip install -U pip
    pip install -U setuptools


    pip install candig-server
    pip install candig-ingest==1.3.1

    mkdir candig-example-data

    wget https://raw.githubusercontent.com/CanDIG/PROFYLE_ingest/develop/PROFYLE_ingest/clinical_metadata_tier.json1
    wget https://raw.githubusercontent.com/CanDIG/PROFYLE_ingest/develop/PROFYLE_ingest/clinical_metadata_tier.json2
    ingest candig-example-data/registry.db mock1 clinical_metadata_tier.json1
    ingest candig-example-data/registry.db mock2 clinical_metadata_tier.json2


    echo "server 190918 set up complete"

    candig_server --host 0.0.0.0 --port 3000
