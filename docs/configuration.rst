.. _configuration:

*********************
Production Deployment
*********************

The candig-server has a  `Configuration file`_. allows Flask and application
specific configuration values to be set.

------------------
Configuration file
------------------

The candig-server is a `Flask application <http://flask.pocoo.org/>`_
and uses the standard `Flask configuration file mechanisms
<https://flask.palletsprojects.com/en/1.1.x/config/>`_.
Many configuration files will be very simple, and will consist of just
one directive instructing the server where to find the data repository;
example, we might have

.. code-block:: python

    DATA_SOURCE = "/path/to/registry.db"

For production deployments, we shouldn't need to add any more configuration
than this, as the other keys have sensible defaults. However,
all of Flask's builtin configuration values
are supported, as well as the extra custom configuration values documented
here. For information on ingesting data, see :ref:`datarepo`.

When debugging deployment issues, it may be useful to turn on extra debugging
information as follows:

.. code-block:: python

    DEBUG = True

.. warning::

    Debugging should only be used temporarily and not left on by default.
    Running the server with Flask debugging enable is insecure and should
    never be used in a production environment.

++++++++++++++++++++
Configuration Values
++++++++++++++++++++

DEFAULT_PAGE_SIZE
    The default maximum number of values to fill into a page when responding
    to search queries. If a client does not specify a page size in a query,
    this value is used.

    Depending on your audiences or your dataset, you could choose to set a number between 1000 to
    4000. If you are part of a federated network, it is best to choose a single number and use
    that within the federated network.

MAX_RESPONSE_LENGTH
    The approximate maximum size of the server buffer used when creating
    responses. This is somewhat smaller than the size of the JSON response
    returned to the client. When a client makes a search request with a given
    page size, the server will process this query and incrementally build
    a response until (a) the number of values in the page list is equal
    to the page size; (b) the size of the internal buffer in bytes
    is >= MAX_RESPONSE_LENGTH; or (c) there are no more results left in the
    query.

    The default is 1024 * 1024, which is equivalent to roughly 1 MB.  You can make this bigger,
    though we don't recommend setting anything too big, e.g., bigger than 10 MB.

REQUEST_VALIDATION
    Set this to True to strictly validate all incoming requests to ensure that
    they conform to the protocol. This may result in clients with poor standards
    compliance receiving errors rather than the expected results.

    This defaults to `True`. Don't change this unless you have a particularly good reason to.

------------------
Docker Deployment
------------------

Refer to this page for Docker installation instructions

https://github.com/CanDIG/candig_compose


------------------
Access List Setup
------------------

An example access list file looks like below. It is a tab-separated file. The server
default name for the file is ``access_list.txt`` (not .tsv) due to backward compatibility reasons.

You can place your own access_list file anywhere you like, but you will need to specify the location
at `ACCESS_LIST`. Under production environment, you should define the location of the file
to be somewhere secure.

.. warning::

    As of candig-server==1.2.1, it is recommended that you use letter X to indicate that the
    user has no access to a dataset, instead of an empty space.


.. code-block:: text

    issuer	username	project1	project2	project3	projectN

    https://candigauth.bcgsc.ca/auth/realms/candig	userA	4	4	4	4
    https://candigauth.bcgsc.ca/auth/realms/candig	userB	4	X	0	1

    https://candigauth.uhnresearch.ca/auth/realms/CanDIG	userC	4	3	2	1
    https://candigauth.uhnresearch.ca/auth/realms/CanDIG	userD	X	X	4	4
