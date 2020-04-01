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
1.2.3
*****

Release note available from https://github.com/CanDIG/candig-server/releases/tag/v1.2.3

This release does not require any configuration changes.

*****
1.2.2
*****

Release note available from https://github.com/CanDIG/candig-server/releases/tag/v1.2.2

----

As indicated in the release note, the previous v1.2.1 release did not correctly preserve backware
compatibilities for access_list that uses null (not specifying anything) to indicate no access. It also
did not correctly process the information when an empty space is used.

This release fixed the issue.

----

If you are already using ``X`` to indicate no access when you upgraded to v1.2.1, no further action is required. You may
update to this version of candig-server without performing any additional changes.

----

If you are still using empty space, or null to indicate no access, please do not use ``v1.2.1``
release of the candig-server, use this one instead. It is still recommended to use ``X`` over
empty space or null to indicate no access.

- Step 1: Update the candig-server in your virtual environment to v1.2.2.
- Step 2: Replace all empty space with X.


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
