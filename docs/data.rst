.. _data:

***************************
Prepare data for the server
***************************

.. warning::

    This part is a work in progress.

The candig-server has a general guideline on which data are accepted.

The following sections will talk about how to prepare for the data that is accepted
by the candig-server.

------------------------------------
Clinical and Pipeline Metadata
------------------------------------

+++++++++++++++++++++++++++++++++++
File format required for ingestion
+++++++++++++++++++++++++++++++++++

At this time, ``ingest`` command is the only way to ingest any clinical and pipeline
metadata, detailed instructions for ingestion can be found at :ref:`datarepo`.

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
                    "sampleIdTier": 0
                    "patientId": "Patient_12345",
                    "patientIdTier": 4
                }
            }
            {
                "Sample": {
                    "sampleId": "Sample_2",
                    "sampleIdTier": 0
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

    $ load_tiers pog mock.json


+++++++++++++++++++++
Mock data for testing
+++++++++++++++++++++

We provide some mock data files, should you want to use them to quickly test your server.

They are available from https://github.com/CanDIG/candig-ingest/tree/master/candig/ingest/mock_data


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

You can find a list of DUO Terms `here <https://github.com/EBISPOT/DUO/blob/master/src/ontology/duo.csv>`_.

.. warning::
    `DUO:0000025` and `DUO:0000022` are not currently supported. Attempts to ingest them two
    DUO Terms will be rejected.

To ingest the DUO Terms, you need to prepare a json file listed like below.

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

