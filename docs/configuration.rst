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
<http://flask.pocoo.org/docs/0.10/config/>`_.
Many configuration files will be very simple, and will consist of just
one directive instructing the server where to find the data repository;
example, we might have

.. code-block:: python

    DATA_SOURCE = "/path/to/registry.db"

For production deployments, we shouldn't need to add any more configuration
than this, as the other keys have sensible defaults. However,
all of Flask's `builtin configuration values <http://flask.pocoo.org/docs/0.10/config/>`_
are supported, as well as the extra custom configuration values documented
here. For information on preparing a data source see :ref:`datarepo` .

When debugging deployment issues, it can be very useful to turn on extra debugging
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

MAX_RESPONSE_LENGTH
    The approximate maximum size of the server buffer used when creating
    responses. This is somewhat smaller than the size of the JSON response
    returned to the client. When a client makes a search request with a given
    page size, the server will process this query and incrementally build
    a response until (a) the number of values in the page list is equal
    to the page size; (b) the size of the internal buffer in bytes
    is >= MAX_RESPONSE_LENGTH; or (c) there are no more results left in the
    query.

REQUEST_VALIDATION
    Set this to True to strictly validate all incoming requests to ensure that
    they conform to the protocol. This may result in clients with poor standards
    compliance receiving errors rather than the expected results.

INITIAL_PEERS
    When starting, you can set a list of initial peers to contact using a
    simple text file. Add a URL per line for peers you would like to add to
    the registry as initial peers. Each time the server starts, this set of
    peers will be announced and added to the registry.

LANDING_MESSAGE_HTML
    The server provides a simple landing page at its root. By setting this
    value to point at a file containing an HTML block element it is possible to
    customize the landing page. This can be helpful to provide support links
    or details about the hosted datasets.


------------------
Docker Deployment
------------------



