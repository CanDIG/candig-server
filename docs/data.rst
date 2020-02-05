.. _data:

***************************
Prepare Data For Ingestion
***************************

.. warning::

    This part is a work in progress.

The candig-server has a general guideline on which data are accepted.

The following sections will talk about how to prepare for the data that is accepted
by the candig-server, and provide you with some mock data for testing.

------------------------------------
Clinical and Pipeline Metadata
------------------------------------

+++++++++++++++++++++++++++++++++++
File format required for ingestion
+++++++++++++++++++++++++++++++++++

At this time, ``ingest`` command is the only way to ingest any clinical and pipeline
metadata, detailed instructions for ingestion can be found under :ref:`datarepo`.

However, before you run the ``ingest`` command, you need to prepare for a json file
that conforms to the  ingest standard format.

For clinical data, it is a json object, with `metadata` as the key. However, for pipeline
data, its key is `pipeline_metadata`. Make sure you have the correct key specified.

The value of the key is a list of objects. Each object should have the table name as the
key, and the object as its value. Therefore, it is possible to specify multiple tables in
one single object. However, each table can only specified once, due to the uniqueness of
the key in the object.

If you need to specify, for example, two samples for one patient. You should specify the
second sample as an independent object in the list, as shown below. For all clinical data
objects, you always need to specify `patientId`.

.. warning::

    Please do not include Tier information yourself. Use the `load_tier` that comes with
    `candig-ingest` to load tiers. More details follow.


.. code-block:: json

    {
        "metadata": [
            {
                "Patient": {
                    "patientId": "Patient_12345",
                    "patientIdTier": 0
                },
                 "Sample": {
                    "sampleId": "Sample_1",
                    "sampleIdTier": 0,
                    "patientId": "Patient_12345",
                    "patientIdTier": 4
                }
            }
            {
                "Sample": {
                    "sampleId": "Sample_2",
                    "sampleIdTier": 0,
                    "patientId": "Patient_12345",
                    "patientIdTier": 4
                },
            }
        ]
    }

Similar structure is used for pipeline metadata, however, for all pipeline metadata objects,
you should always include ``sampleId``.

++++++++++++++++++++++++
How to load tiers
++++++++++++++++++++++++

If you have a valid json file, but missing tier information, you should use the ``load_tier``
utility provided by the `candig-ingest` to load the tier information.


The ``load_tiers`` command is the preferred way to load tier information. It does not come with
candig-server by default, to use it, you need to install `candig-ingest` by running:

`pip install candig-ingest`


To tier the data, you need to run

.. code-block:: bash

    usage: load_tiers <project_name> <json_filepath> <tier_filepath> <output_filepath>

**Examples:**

.. code-block:: bash

    $ load_tiers pog mock.json tier.tsv mock_tier.json


+++++++++++++++++++++
Mock data for testing
+++++++++++++++++++++

We provide some mock data files, should you want to use them to quickly test your server.

They are available from https://github.com/CanDIG/candig-ingest/tree/master/candig/ingest/mock_data
Use the ``clinical_metadata_tier[1,2,3].json`` files.

.. note::
    If you are interested in testing the 1k genome data, you can find a ``ingest-compliant``
    clinical mock dataset here https://github.com/CanDIG/candig-ingest/releases/tag/v1.3.1

    This contains all individuals information.

++++++++++++++++++++++++++++++
Migrate data from RedCap Cloud
++++++++++++++++++++++++++++++

If your clinical meta data is on RedCapCloud, we provide a script that would transform
the related data into ready-to-ingest format.

It is available from here: https://github.com/CanDIG/redcap-cloud


------------------
Data Use Ontology
------------------

To enable future automated discovery, we have adopted the use of `Data Use Ontology (DUO)`
Terms to describe our datasets. For the current version of candig-server, you have
the option to use a json file to define your dataset.

You can find a list of DUO Terms through this `csv file <https://github.com/EBISPOT/DUO/blob/master/src/ontology/duo.csv>`_.
You can also use an ontology parsing tool of your choice to visualize/parse a more complete list
of DUO's `raw OWL definition <https://github.com/EBISPOT/DUO/blob/master/src/ontology/duo-basic.owl>`_.

.. warning::
    We only support a limited subset of the DUO terms.

    Terms whose ID is between `DUO:0000031` and `DUO:0000039`, as well as `DUO:0000022` and `DUO:0000025` are not
    supported, as we expect these terms to be updated in the near future.

    If you think an ID should be supported, but is not. You can let us know by opening an issue
    on our Github repo.

    The supported IDs are listed below.

.. code-block:: json

    [
        "DUO:0000001", "DUO:0000004", "DUO:0000005",
        "DUO:0000006", "DUO:0000007", "DUO:0000011", "DUO:0000012", "DUO:0000014",
        "DUO:0000015", "DUO:0000016", "DUO:0000017", "DUO:0000018", "DUO:0000019",
        "DUO:0000020", "DUO:0000021", "DUO:0000024", "DUO:0000026", "DUO:0000027"
        "DUO:0000028", "DUO:0000029", "DUO:0000042"
    ]

.. note::
    We do not currently provide API to look up the definitions via their ID.

    If one of the supported ids listed above is not in the csv file provided above, you may
    be able to look up their definitions via `EBI's DUO page <https://www.ebi.ac.uk/ols/ontologies/duo>`_.


To ingest the DUO Terms, you need to prepare a json file listed like below. You should only
specify `id` in a single DUO object, unless the `modifier` is also required, then you specify
the `id` along with the `modifier`.

.. code-block:: json

    {
        "duo": [
            {
                "id": "DUO:0000021"
            },
            {
                "id": "DUO:0000024",
                "modifier": "2020-01-01"
            }
        ]
    }

.. warning::
    For now, `DUO:0000024` is the only DUO Term that requires `modifier`. The modifier
    has to be formatted exactly like `YYYY-MM-DD`, invalid dates will be rejected.

When your file is ready, run the `add-dataset-duo` command to populate the DUO information
of the dataset. Please note that this command will always overwrite the existing DUO
information stored.


------------------------------------
Reads, Variants and References Data
------------------------------------

If you are interested in testing the candig-server with some variants data, we provide
a mock dataset here: https://github.com/CanDIG/test_data/releases

Currently, there are three groups of test data provided, containing clinical, pipeline
metadata, as well as the variants data. We have provided a loading script, note that
you might need to modify the DB path, or the dataset name.

We provide three `group` datasets since we often use it to test federation of three test
servers.

