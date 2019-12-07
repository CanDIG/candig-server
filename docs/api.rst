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

----------------------------
How to write filter objects
----------------------------
As you can see from Sample Queries II to IV, it is possible to submit optional `filters`
list along with your request.

`filters` is a list of `filter` objects. There are two types of filter objects.

::::::::::::::::::::::::::::::::::::::::::::::::::
Type I: Compare the `field`'s value to a string
::::::::::::::::::::::::::::::::::::::::::::::::::

.. code-block:: json

    {
        "field": "gender",
        "operator": "=",
        "value": "female"
    }

In the filter object above, you specify `gender` as the field, and value to be the `female`,
`=` as the operator. This filter object asks server to find records whose `gender` is female.

.. note::
    For Type I filter object, the supported operators are >, <, >=, <=, =, ==, !=, contains.
    Note that `=` and `==` are equivalent.

::::::::::::::::::::::::::::::::::::::::::::::::::::
Type II: Check if a record's field belongs to a list
::::::::::::::::::::::::::::::::::::::::::::::::::::

.. code-block:: json

    {
        "field": "provinceOfResidence",
        "operator": "in",
        "values": ["British Columbia", "Ontario"]
    }

In the filter object above, you specify `provinceOfResidence` as the field, and `values`
to be the `["British Columbia", "Ontario"]`, `in` as the operator.

This filter object asks server to find records whose `provinceOfResidence` is one of
`British Columbia` or `Ontario`.

.. note::
    For Type II filter object, `in` is the only supported operator. Also, you specify `values`,
    instead of `value`.

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

Endpoint: `variantsets/search`

.. note::
    This query is the same as Sample Query I under Metadata services,
    but it is the same across metadata, variantSets, referenceSets, etc.


.. code-block:: json

    {
        "datasetId": "WyIxa2dlbm9tZSJd"
    }

---------------
Sample Query II
---------------

Description: Search for variants within the range between the start and end
that are on chromesome 22, from the designated variantSets.

Endpoint: `variants/search`

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

Endpoint: `variants/search`

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

.. warning::
    Do not use ``/variantsbygenesearch`` endpoint, it has been deprecated.

Endpoint: `/variantsbygenesearch`  or `/variants/gene/search`

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

.. warning::
    You may specify ``pageToken`` only when you see a ``nextPageToken`` returned in the
    previous response. You cannot set ``pageSize`` for requests made to ``/search`` and
    ``/count`` endpoints.

-------------------
How to write logic
-------------------

Logic is where you specify the relationship between various components.
The only operators you will need to specify are either AND or OR.
When writing the logic, the operation becomes the key.


::::::::::::::::::::::::::::::::::::
Write Logic for multiple components
::::::::::::::::::::::::::::::::::::

This is possibly the most common use-case, where you want to find records that satisfy
multiple filters you set.

For example, conditionA and conditionB and condition C would be written as below.

In this example, the records will have to satisfy conditions of all three components.

.. code-block:: json

    {
        "logic": {
            "and": [
                {
                    "id": "conditionA"
                },
                {
                    "id": "conditionB"
                },
                {
                    "id": "conditionC"
                }
            ]
        }
    }

In the above example, you can replace the `and` key with `or`. In this case, the records
will only need to fulfill the condition of any single component.

::::::::::::::::::::::::::::::
Write Logic for 1 component
::::::::::::::::::::::::::::::

When you only have 1 component in your query, however, you may only specify `id`.


.. code-block:: json

    {
        "logic": {
            "id": "condition1"
        }
    }

For this case only, that is, when you only have one single `id` in your logic. Optionally, you can specify
the `negate` flag, which would basically negate the logic of the componenet.


.. code-block:: json

    {
        "logic": {
            "id": "condition1",
            "negate": true
        }
    }

:::::::::::::::::::::::::::::::::
Write Logic for nested components
:::::::::::::::::::::::::::::::::

It is possible to write more complex logic, with multiple nested operations involved. However, the
examples explained above should suffice most basic needs.

As an example, the following request is the equivalent to ``A∩B∩(C∪D)``,
which is equivalent to ``(A∩B) ∩ (C∪D)``.


.. code-block:: json

    {
        "logic": {
            "and": [
                {
                    "id": "A"
                },
                {
                    "id": "B"
                },
                {
                    "or": [
                        {
                            "id": "C"
                        },
                        {
                            "id": "D"
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

In a ``component``, you specify the tables you want to search on to be the
key.

There are 3 different types of ``components`` objects.

::::::::::::::::::::::::::::::
Components for Clinical tables
::::::::::::::::::::::::::::::


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

You write the filter objects the same way you would write for individual endpoints.
If you need a reminder on that, check `How to write filter objects`_.

::::::::::::::::::::::::::::::::::::::::::::::::::::
Components for /variants/search endpoint
::::::::::::::::::::::::::::::::::::::::::::::::::::

.. code-block:: json

    {
        "components": [
            {
                "id": "condition1",
                "variants": {
                    "start": "100000",
                    "end": "500000",
                    "referenceName": "1"
                }
            }
        ]
    }

Note that you can also specify `variantSetIds` in here, which will limit the scope to
your list of `variantSetIds`. If you don't specify any, by default, it will try to search
through all variantSets associated with this dataset.

::::::::::::::::::::::::::::::::::::::::::::::::::::
Components for /variantsbygenesearch endpoint
::::::::::::::::::::::::::::::::::::::::::::::::::::

.. warning::
    Note that this component is deprecated, and may be removed in subsequent releases.
    Use `Components for /variants/gene/search endpoint`_.

.. code-block:: json

    {
        "components": [
            {
                "id": "condition1",
                "variantsByGene": {
                    "gene": "MUC1"
                }
            }
        ]
    }

::::::::::::::::::::::::::::::::::::::::::::::::::::
Components for /variants/gene/search endpoint
::::::::::::::::::::::::::::::::::::::::::::::::::::

.. code-block:: json

    {
        "components": [
            {
                "id": "condition1",
                "variants": {
                    "gene": "MUC1"
                }
            }
        ]
    }

--------------------
How to write results
--------------------

In the ``results`` part of your query, you will need to specify the table you want
the server to return. For a query made to the /search endpoint, you can
simply specify the table name.

.. warning::
    The only endpoints that are accepted here are all clinical metadata
    endpoints, as well as ``variants``.

:::::::::::::::::::::::::::::::::::::::
Results section for Clinical tables
:::::::::::::::::::::::::::::::::::::::


.. code-block:: json

    {
        "results": {
            "table": "patients",
            "fields": ["gender", "ethnicity"]
        }
    }

.. warning::
    `fields` is a list of fields that you want the server to return. It is optional for /search
    endpoint, but mandatory for `/count` endpoint. If you do not specify this in `/search`
    endpoint, the server will just return all the fields.


::::::::::::::::::::::::::::::::::::::::::::::::::::
Results section for /variants endpoint
::::::::::::::::::::::::::::::::::::::::::::::::::::

.. warning::
    Please be considerate when you are submitting any `/variants` request, we recommend you
    to not search more than 1 million bps at a time. If you have a lot of variantSets, you should
    limit your search size to 100,000.

.. code-block:: json

    {
        "results": {
            "table": "variants",
            "start": "1232555",
            "end": "1553222",
            "referenceName": "1"
        }
    }

::::::::::::::::::::::::::::::::::::::::::::::::::::::
Results section for /variantsbygenesearch endpoint
::::::::::::::::::::::::::::::::::::::::::::::::::::::

.. warning::
    This endpoint is deprecated. Use `Results section for /variants/gene/search endpoint`_.

.. warning::
    Please note that while you need to specify the table name to be `variantByGene`, it still
    returns a list of variants in its response.


.. code-block:: json

    {
        "results": {
            "table": "variantsByGene",
            "gene": "MUC1"
        }
    }

::::::::::::::::::::::::::::::::::::::::::::::::::::::
Results section for /variants/gene/search endpoint
::::::::::::::::::::::::::::::::::::::::::::::::::::::

.. code-block:: json

    {
        "results": {
            "table": "variants",
            "gene": "MUC1"
        }
    }

--------------
Sample Query I
--------------

Description: Return a list of patients, whose diseaseResponseOrStatus is “Complete Response”, AND have a courseNumber that is not 100.

.. warning::
    The example query below only works for the /search endpoint, as it did not specify `fields`.

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

.. note::

    Note: Since a list of ``variantSetIds`` was not specified, the server will attempt to
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


