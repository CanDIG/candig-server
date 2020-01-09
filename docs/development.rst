.. _development:

-----------------
Development Setup
-----------------

Thanks for your interest in the candig-server. If you have any questions,
`please let us know <https://github.com/candig/candig-server/issues>`_

.. warning::

    This guide is a work in progress, and is incomplete.

******************************
Standalone candig-server Setup
******************************

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

The script has been tested on CentOS machines, and we expect the install to
run OK on most unix distributions. You can run it on `MacOS`, but `wget` likely won't
work and you should either download the files yourself, or use a replacement for `wget`.

See :ref:`datarepo` for more information regarding ingesting data and starting up server.

.. warning::
    Please note that by default, the script installs the server on the directory
    `test_server`. You can either change it, or make sure that you do not have a
    `test_server` directory.


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

    wget https://raw.githubusercontent.com/CanDIG/candig-ingest/master/candig/ingest/mock_data/clinical_metadata_tier1.json
    wget https://raw.githubusercontent.com/CanDIG/candig-ingest/master/candig/ingest/mock_data/clinical_metadata_tier2.json
    ingest candig-example-data/registry.db mock1 clinical_metadata_tier1.json
    ingest candig-example-data/registry.db mock2 clinical_metadata_tier2.json

    echo "test server set up has completed."

    candig_server --host 0.0.0.0 --port 3000


Optionally, you can run two servers with federation set up. Assume you have server A running
at ``0.0.0.0:3000``, you need to run the script again to set up a server B.
Use `this file <https://raw.githubusercontent.com/CanDIG/candig-ingest/master/candig/ingest/mock_data/clinical_metadata_tier3.json>`_
as the clinical data for your server B, and run your server B at ``0.0.0.0:3001``.

Now that you have both servers installed, you need to add them to be the peer of each other

For server A, you need to run

.. code-block:: bash

    candig_repo add-peer candig-example-data/registry.db http://0.0.0.0:3001

For server B, you need to run

.. code-block:: bash

    candig_repo add-peer candig-example-data/registry.db http://0.0.0.0:3001

You do not need to have anything running on the peer when you execute the `add-peer` command.
It simply registeres that URL as a peer.

Now, you will get federated response
from both servers A and B. You can certainly choose to run them on different ports, or different
servers, the script makes these assumptions only for your convenience.


**********************
Tyk and Keycloak Setup
**********************

It is possible to run set up a local test server, with Tyk and Keycloak set up. These two
components provide authentication capabilities.

For more information, refer to https://github.com/CanDIG/candig_tyk.