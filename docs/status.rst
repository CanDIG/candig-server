.. _status:

------
Status
------

Please refer to https://github.com/CanDIG/candig-server/releases for the latest release
notes.

++++++++++++++++++
Upgrade Guidelines
++++++++++++++++++

This section is mainly prepared for system administrators.

*****
1.2.1
*****

Release note available from https://github.com/CanDIG/candig-server/releases/tag/v1.2.1

----

As indicated in the release note, ``X`` is now used to indicate no access. You may see a newly-updated
sample access_list file from :ref:`configuration`.

If you have used empty space to indicate no access, you should:

- Step 1: Update the candig-server in your virtual environment to v1.2.1.
- Step 2: Replace all empty space with X.

You should always restart the candig-server service when you update to a new candig-server.

----

As indicated in the release note, ``DUO:0000002`` and ``DUO:0000003`` are no longer valid DUO
ids.

If you have specified one of these two for one or more of your datasets, you should

- Step 1: Remove ``DUO:0000002`` and ``DUO:0000003`` from the json file that holds info regarding your data use restrictions.
- Step 2: Re-run the ``add-dataset-duo`` command.

You should restart the candig-server service when you make changes to the data.

*****
1.2.0
*****
https://github.com/CanDIG/candig-server/releases/tag/v1.2.0

*****
1.1.0
*****
https://github.com/CanDIG/candig-server/releases/tag/v1.1.0

*****
1.0.3
*****
https://github.com/CanDIG/candig-server/releases/tag/v1.0.3


*****
1.0.2
*****
https://github.com/CanDIG/candig-server/releases/tag/v1.0.2

*****
1.0.1
*****
https://github.com/CanDIG/candig-server/releases/tag/v1.0.1


*****
1.0.0
*****
https://github.com/CanDIG/candig-server/releases/tag/v1.0.0
