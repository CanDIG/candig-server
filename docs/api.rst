.. _api:

**************************
API Usage & Sample Queries
**************************

.. warning::

    This guide is a work in progress, and is incomplete.


This section will provide instructions on API usages. Upon logging in, you will see a
dashboard that gives high level overview of your authorized datasets.

When you click on the top right corner, you will see an `API Info` section, where a Swagger
UI is provided. That UI does not yet contain any information on `/search` and `/count`
endpoints. Please refer to the resources here for instructions on using these two endpoints.


.. warning::

    Please note that while reasonable efforts have been put in to validate the request and
    response schemas for the swagger UI definitions, at this time, we cannot guarantee it to
    be 100% accurate. Please open a ticket if you encounter any problems.

++++++++++++++++++++++++++++++++++++++++
Sample queries for all metadata services
++++++++++++++++++++++++++++++++++++++++

This includes all of the endpoints under Clinical and Pipeline Metadata Services.

Even though some of the sample queries below are made to specific endpoint, the same format applies to any pipeline or clinical metadata endpoint. Typically you will need to change the field in your filters, depending on which table you are querying on.


--------------
Fetch Datasets
--------------
Description: To fetch all of the datasets, make a query to datasets/search endpoint with an empty body. You need datasetId for subsequent queries to other endpoints.

Query:

.. code-block:: json

   {}


--------------
Sample Query I
--------------
Description: Fetch all of the items from the specified dataset from any clinical or pipeline metadata service endpoint.

Query:

.. code-block:: json

    {
        "datasetId": "WyIxa2dlbm9tZSJd"
    }

---------------
Sample Query II
---------------

Description: Fetch all of the items from the patients/search endpoint, whose gender is female.

.. note::
    We support a number of operators in the filters,
    which include: >, <, >=, <=, =, !=, and contains.

Query:

.. code-block:: json

    {
        "datasetId": "WyIxa2dlbm9tZSJd",
        "filters": [
            {
                "field": "gender",
                "operator": "=",
                "value": "female"
            }
        ]
    }


----------------
Sample Query III
----------------

Description: Fetch all of the items from the patients/search endpoint, whose gender is female and whose ethnicity is NOT ‘GBR’.

.. note::
    You can specify more than one filter under filters.

.. code-block:: json

    {
        "datasetId": "WyIxa2dlbm9tZSJd",
        "filters": [
            {
                "field": "gender",
                "operator": "=",
                "value": "female"
            },
            {
                "field": "ethnicity",
                "operator": "!=",
                "value": "GBR"
            }
        ]
    }


---------------
Sample Query IV
---------------

Description: Fetch all of the items from the patients/search endpoint, whose ethnicity is one of GBR, FIN or ESN.

.. note::
    Note that this query is very different from the previous ones.
    To specify a list of values you are interested in, you need to:
    Specify ``values`` in your filters, instead of ``value``.
    Specify a list of values that you are interested in.
    Specify ``in`` as the operator.

.. code-block:: json

    {
        "datasetId": "WyIxa2dlbm9tZSJd",
        "filters": [
            {
                "field": "ethnicity",
                "operator": "in",
                "values": [
                    "GBR",
                    "FIN",
                    "ESN"
                ]
            }
        ]
    }


++++++++++++++++++++++++++++++++++++++++
Sample queries for all variants services
++++++++++++++++++++++++++++++++++++++++



This mainly includes the /variantsets/search, /variants/search and /variantsbygene endpoints.

--------------
Sample Query I
--------------

Description: Fetch all of the variantsets associated with a particular dataset.
Endpoint: variantsets/search

.. note::
    This query is the same as Sample Query I under Metadata services,
    but it is the same across metadata, variantSets, referenceSets, etc.


Query:

.. code-block:: json

    {
        "datasetId": "WyIxa2dlbm9tZSJd"
    }

---------------
Sample Query II
---------------

Description: Search for variants within the range between the start and end
that are on chromesome 22, from the designated variantSets.

Endpoint: variants/search

.. code-block:: json

    {
        "start": "50158561",
        "end": "50158565",
        "referenceName": "22",
        "variantSetIds": [
            "yourVariantSetId1",
            "yourVariantSetId2"
        ]
    }

----------------
Sample Query III
----------------

Description: Search for variants within the range between the start and end
that are on chromesome 22, from all variantsets that are associated with one
particular dataset.

Endpoint: variants/search

.. warning::
    You should never attempt to specify both datasetId and variantSetIds.

.. code-block:: json

    {
        "datasetId": "WyIxa2dlbm9tZSJd",
        "start": "50158561",
        "end": "50158565",
        "referenceName": "22"
    }

---------------
Sample Query IV
---------------

Description: Search for variants that are associated with a particular gene.

Endpoint: /variantsbygenesearch

.. code-block:: json

    {
        "datasetId": "WyIxa2dlbm9tZSJd",
        "gene": "ABCD",
    }

+++++++++++++++++++++++++++++++++++++++++++++
Instructions for /search and /count endpoints
+++++++++++++++++++++++++++++++++++++++++++++

You need to write complex queries to be able to use the ``/search`` and ``/count`` endpoints.
It has 4 mandatory fields, ``datasetId``, ``logic``, ``components``, and ``results``. Queries
for both endpoints are largely the same, and the differences will be explained below.

You always need to specify datasetId in your query.

You may want to look at the sample queries first before you can look at the `how to`
instructions below.

-------------------
How to write logic
-------------------

Logic is where you specify the relationship between various components.
The only operators you will need to specify are either AND or OR.
When writing the logic, the operation becomes the key.
For example, conditionA and conditionB and condition C would be written as:

.. code-block:: json

    {
        "logic": {
            "and": [
                {
                    "id": "conditionA"
                },
                {
                    "id": "conditionB"
                },{
                    "id": "conditionC"
                }
            ]
        }
    }

There is one exception to this rule. When you only have 1 component in your query,
your logic part of the query will only have an id, which would look like this:

.. code-block:: json

    {
        "logic": {
            "id": "condition1"
        }
    }

The logic can get very complicated, with multiple nested operations involved,
the following example is the equivalent to ``(condition1 AND condition2) AND (condition3 OR condition4)``

.. code-block:: json

    {
        "logic": {
            "and": [
                {
                    "and": [
                        {
                            "id": "condition1"
                        },
                        {
                            "id": "condition2"
                        }
                    ]
                },
                {
                    "or": [
                        {
                            "id": "condition3"
                        },
                        {
                            "id": "condition4"
                        }
                    ]
                }
            ]
        }
    }

----------------------------
How to write components
----------------------------

The ``components`` part is a list, each corresponding to a filter of a specified table.
Be careful that the id has to match with the one you specified in the logic part of
your query. It can be almost any string, but they have to match.

In a component, you specify the tables you want to search on to be the
key, in this case, it was “patients”. You will also need to specify filters,
where you specify the field, operator and value.


.. code-block:: json

    {
        "components": [
            {
                "id": "condition1",
                "patients": {
                    "filters": [
                        {
                            "field": "provinceOfResidence",
                            "operator": "!=",
                            "value": "Ontario"
                        }
                    ]
                }
            }
        ]
    }

You write the filter objects the same you way you would write for individual endpoints.


--------------------
How to write results
--------------------

In the ``results`` part of your query, you will need to specify the table you want
the server to return. For a query made to the /search endpoint, you can
simply specify the table name.

.. warning::
    The only endpoints that are accepted here are all clinical and pipeline metadata
    endpoints, as well as ``variants``.


.. code-block:: json

    {
        "results": [
            {
                "table": "patients"
            }
        ]
    }

--------------
Sample Query I
--------------

Description: Return a list of patients, whose diseaseResponseOrStatus is “Complete Response”, AND have a courseNumber that is not 100.

Note: The example query below only works for the /search endpoint, as it did not specify a list of fields to aggregate on in the results section. Refer to Part III: Results under Basic Usages to remind yourself how to do it, or refer to Example Query 2.

Query:

.. code-block:: json

    {
        "datasetId": "yourDatasetId",
        "logic": {
            "and": [
                {
                    "id": "A"
                },
                {
                    "id": "B"
                }
            ]
        },
        "components": [
            {
                "id": "A",
                "outcomes": {
                    "filters": [
                        {
                            "field": "diseaseResponseOrStatus",
                            "operator": "==",
                            "value": "Complete Response"
                        }
                    ]
                }
            },
            {
                "id": "B",
                "treatments": {
                    "filters": [
                        {
                            "field": "courseNumber",
                            "operator": "!=",
                            "value": "100"
                        }
                    ]
                }
            }
        ],
        "results": [
            {
                "table": "patients"
            }
        ]
    }

---------------
Sample Query II
---------------

Description: Return the aggregated stats on patients’ gender and ethnicity
who have mutations present between “50158561” and “50158565” on chromosome 22,
from the list of variantsetIds.

.. code-block:: json

    {
        "datasetId": "yourDatasetId",
        "logic": {
            "id": "A"
        },
        "components": [
            {
                "id": "A",
                "variants": {
                    "start": "50158561",
                    "end": "50158565",
                    "referenceName": "22",
                    "variantSetIds": [
                        "yourVariantSetId_1",
                        "yourVariantSetId_2",
                        "yourVariantSetId_3",
                        "yourVariantSetId_4",
                        "yourVariantSetId_5",
                        "yourVariantSetId_6",
                        "yourVariantSetId_7",
                        "yourVariantSetId_8"
                           ]
                }
            }
        ],
        "results": [
            {
                "table": "patients",
                "fields": [
                    "gender",
                    "ethnicity"
                ]
            }
        ]
    }


----------------
Sample Query III
----------------

Description: Return the aggregated stats on patients’ gender and ethnicity,
who have mutations present between “50158561” and “50158565” on chromosome 22.

Note: Since a list of variantSetIds was not specified, the server will attempt to
locate all variantSets associated with the dataset. If you have a lot of variantSets
associated with this particular dataset, the query might take some time.

.. code-block:: json

    {
        "datasetId": "yourDatasetId",
        "logic": {
            "id": "A"
        },
        "components": [
            {
                "id": "A",
                "variants": {
                    "start": "50158561",
                    "end": "50158565",
                    "referenceName": "22"
                }
            }
        ],
        "results": [
            {
                "table": "patients",
                "fields": [
                    "gender",
                    "ethnicity"
                ]
            }
        ]
    }



---------------
Sample Query IV
---------------

Description: Retrieve all the variants between 50100000 and 50158565 on chromosome 22
associated with an individual ``[HG00105]``.


.. code-block:: json

    {
        "datasetId": "yourDatasetId",
        "logic": {
            "id": "A"
        },
        "components": [
            {
                "id": "A",
                "patients": {
                    "filters": [
                        {
                            "field": "patientId",
                            "operator": "==",
                            "value": "HG00105"
                        }
                    ]
                }
            }
        ],
        "results": [
            {
                "table": "variants",
                "start": "50100000",
                "end": "50158565",
                "referenceName": "22"
            }
        ]
    }


