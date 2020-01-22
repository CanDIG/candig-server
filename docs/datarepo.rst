.. _datarepo:

**********************
Command Line Interface
**********************

With the exception of using ``ingest`` to ingest the clinical and pipeline metadata
in bulk, ``candig_repo`` command line interface is used for all other operation.

The registry contains links to files, as well as some metadata.

.. warning::
    Because the data model objects returned via APIs are created at server start-up,
    at this time, you have to restart the server for the data you ingest to be reflected.

For instructions on adding metadata in bulk, see ingest_.

When you are done ingesting data, you may start up your server instance by running the
``candig_server`` command, see `Start up candig-server`_ for more information.

++++++++++++++++++++++++++++
Initialize/Remove Dataset
++++++++++++++++++++++++++++


This section contains commands that initialize the dataset, give you the overview
of the data repository, as well as deleting the dataset.

You do not need to use ``init`` to initialize the dataset if you already prepared
a json file of clinical information. You can run the ``ingest`` command directly and
it will take care of everything for you.

----
init
----

.. warning::
    If you already prepared a json file that conforms to our standard clinical or
    pipeline metadata, you can run ``ingest`` command directly without running ``init``.

    For detailed instructions, see ingest_.

The ``init`` command initialises a new registry DB at a given
file path. Unless you have a clinical json file ready that can be ingested with ``ingest``,
you need to run this to initialize your DB.

.. argparse::
    :module: candig.server.cli.repomanager
    :func: getRepoManagerParser
    :prog: candig_repo
    :path: init
    :nodefault:


**Examples:**

.. code-block:: bash

    $ candig_repo init registry.db

----
list
----

The ``list`` command is used to print the contents of a repository
to the screen. It is an essential tool for administrators to
understand the structure of the repository that they are managing.

.. note:: The ``list`` command is under development and will
   be much more sophisticated in the future. In particular, the output
   of this command should improve considerably in the near future.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: list
   :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo list registry.db

------
verify
------

The ``verify`` command is used to check that the integrity of the
data in a repository. The command checks each container object in turn
and ensures that it can read data from it. Read errors can occur for
any number of reasons (for example, a VCF file may have been moved
to another location since it was added to the registry), and the
``verify`` command allows an administrator to check that all is
well in their repository.

.. note:: The ``verify`` command is currently under review.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: verify
   :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo verify registry.db

-----------
add-dataset
-----------

Creates a new dataset in a repository. A dataset is an arbitrary collection
of ReadGroupSets, VariantSets, VariantAnnotationSets and FeatureSets. Each
dataset has a name, which is used to identify it in the repository manager.

.. warning::
    If you already prepared a json file that conforms to our standard clinical or
    pipeline metadata, you can run ``ingest`` command directly without running ``add-dataset``.

    For detailed instructions, see ingest_.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: add-dataset
   :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo add-dataset registry.db 1kg -d 'Example dataset using 1000 genomes data'

Adds the dataset with the name ``1kg`` and description
``'Example dataset using 1000 genomes data'`` to the
registry database ``registry.db``.


----------------------
add-dataset-duo
----------------------

Create/update new Data Use Ontology Information for an existing dataset. Note that you have to
have an existing dataset to be able to use this command. When you need to update the DUO info,
simply run the command with updated DUO Json file.


.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: add-dataset-duo
   :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo add-dataset-duo registry.db mock1 duo.json

Adds the Data Use Ontology info to the  dataset with the name ``mock1``.

To learn about how to prepare a json file that contains DUO info for a dataset, and a list
of DUO IDs that are allowed, see the ``Data Use Ontology`` section under :ref:`data`.


--------------
remove-dataset
--------------

Removes a dataset from the repository and recursively removes all
objects (ReadGroupSets, VariantSets, etc) within this dataset.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-dataset
   :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo remove-dataset registry.db dataset1

Deletes the dataset with name ``dataset1`` from the repository
represented by ``registry.db``


----------------------
remove-dataset-duo
----------------------

Remove new Data Use Ontology Information for an existing dataset.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-dataset-duo
   :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo remove-dataset-duo registry.db mock1

Removes the Data Use Ontology info to the  dataset with the name ``mock1``.


+++++++++++++++++++++++++++++++++++++++
Add/Remove Clinical & Pipeline Metadata
+++++++++++++++++++++++++++++++++++++++

This section contains commands that let you ingest data into the clinical and pipeline
metadata tables, as well as the commands that delete them.

The ``ingest`` command is the only way to ingest clinical or pipeline data in bulk.
It encapsulates all the write operations into a single transaction. To learn about preparing
the json files for the ``ingest`` command, see :ref:`data`

All of the ``remove`` commands for removing clinical tables require you to specify their
``name``, note that the ``name`` here is actually their unique identifier, typically is composed
of their patientId, sometimes along with some other ID or timestamp information. This is the same
``name`` you see in the records of these clinical or pipeline data records.

------
ingest
------
The ``ingest`` command is the preferred way to import metadata in bulk. It does not come with
candig-server by default, to use it, you need to install `candig-ingest` by running:

`pip install candig-ingest`

To import metadata in bulk, you need to have a specially formatted json file. A mock json
file is available from https://github.com/CanDIG/candig-ingest/blob/master/candig/ingest/mock_data/clinical_metadata_tier1.json

To ingest the data, you need to run

.. code-block:: bash

    usage: ingest registryPath datasetName metadataPath

If the dataset does not exist, it will create a new dataset of this name. There is no need
to run ``init`` command before running ``ingest``.

**Examples:**

.. code-block:: bash

    $ ingest registry.db mock1 mock_data.json

--------------
remove-patient
--------------

remove a patient.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-patient
   :nodefault:

Examples:

.. code-block:: bash

    $ candig_repo remove-patient registry.db mock1 PATIENT_81202

-------------------
remove-enrollment
-------------------

remove a enrollment.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-enrollment
   :nodefault:

Examples:

.. code-block:: bash

    $ candig_repo remove-enrollment registry.db mock1 PATIENT_81202_2005-08-23


-------------------
remove-treatment
-------------------

remove a treatment.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-treatment
   :nodefault:

Examples:

.. code-block:: bash

    $ candig_repo remove-treatment registry.db mock1 PATIENT_81202_2005-08-23


--------------
remove-sample
--------------

remove a sample.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-sample
   :nodefault:

Examples:

.. code-block:: bash

    $ candig_repo remove-sample registry.db mock1 PATIENT_81202_SAMPLE_33409


-------------------
remove-diagnosis
-------------------

remove a diagnosis.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-diagnosis
   :nodefault:

Examples:

.. code-block:: bash

    $ candig_repo remove-diagnosis registry.db mock1 PATIENT_81202_SAMPLE_33409


-------------------
remove-tumourboard
-------------------

remove a tumourboard.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-tumourboard
   :nodefault:

Examples:

.. code-block:: bash

    $ candig_repo remove-tumourboard registry.db mock1 PATIENT_81202_SAMPLE_33409


--------------
remove-outcome
--------------

remove a outcome.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-outcome
   :nodefault:

Examples:

.. code-block:: bash

    $ candig_repo remove-outcome registry.db mock1 PATIENT_81202_2016-10-11


-------------------
remove-complication
-------------------

remove a complication.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-complication
   :nodefault:

Examples:

.. code-block:: bash

    $ candig_repo remove-complication registry.db mock1 PATIENT_81202_2016-10-11


--------------
remove-consent
--------------

remove a consent.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-consent
   :nodefault:

Examples:

.. code-block:: bash

    $ candig_repo remove-consent registry.db mock1 PATIENT_81202_2016-10-11


-------------------
remove-chemotherapy
-------------------

remove a chemotherapy.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-chemotherapy
   :nodefault:

Examples:

.. code-block:: bash

    $ candig_repo remove-chemotherapy registry.db mock1 PATIENT_81202_2016-10-11


------------------------
remove-immunotherapy
------------------------

remove a immunotherapy.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-immunotherapy
   :nodefault:

Examples:

.. code-block:: bash

    $ candig_repo remove-immunotherapy registry.db mock1 PATIENT_81202_2016-10-11


-------------------
remove-radiotherapy
-------------------

remove a radiotherapy.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-radiotherapy
   :nodefault:

Examples:

.. code-block:: bash

    $ candig_repo remove-radiotherapy registry.db mock1 PATIENT_81202_2016-10-11


------------------------
remove-celltransplant
------------------------

remove a celltransplant.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-celltransplant
   :nodefault:

Examples:

.. code-block:: bash

    $ candig_repo remove-celltransplant registry.db mock1 PATIENT_81202_2016-10-11


--------------
remove-surgery
--------------

remove a surgery.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-surgery
   :nodefault:

Examples:

.. code-block:: bash

    $ candig_repo remove-surgery registry.db mock1 PATIENT_81202_2016-10-11


--------------
remove-study
--------------

remove a study.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-study
   :nodefault:

Examples:

.. code-block:: bash

    $ candig_repo remove-study registry.db mock1 PATIENT_81202_2016-10-11


--------------
remove-slide
--------------

remove a slide.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-slide
   :nodefault:

Examples:

.. code-block:: bash

    $ candig_repo remove-slide registry.db mock1 PATIENT_81202_2016-10-11


--------------
remove-labtest
--------------

remove a labtest.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-labtest
   :nodefault:

Examples:

.. code-block:: bash

    $ candig_repo remove-labtest registry.db mock1 PATIENT_81202_2016-10-11



++++++++++++++++++++++++
Add/Remove Genomics Data
++++++++++++++++++++++++

----------------
add-referenceset
----------------

Adds a reference set derived from a FASTA file to a repository. Each
record in the FASTA file will correspond to a Reference in the new
ReferenceSet. The input FASTA file must be compressed with ``bgzip``
and indexed using ``samtools faidx``. Each ReferenceSet contains a
number of metadata values (.e.g. ``species``) which can be set
using command line options.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: add-referenceset
   :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo add-referenceset registry.db hs37d5.fa.gz \
        --description "NCBI37 assembly of the human genome" \
        --species '{"termId": "NCBI:9606", "term": "Homo sapiens"}' \
        --name NCBI37 \
        --sourceUri ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/phase2_reference_assembly_sequence/hs37d5.fa.gz

Adds a reference set used in the 1000 Genomes project using the name
``NCBI37``, also setting the ``species`` to 9606 (human).

------------
add-ontology
------------

.. warning::
    This command, as well as all ontology-related operations are under review. They might undergo
    changes in the near future.


Adds a new ontology to the repository. The ontology supplied must be a text
file in `OBO format
<http://owlcollab.github.io/oboformat/doc/obo-syntax.html>`_. If you wish to
serve sequence or variant annotations from a repository, a sequence ontology
(SO) instance is required to translate ontology term names held in annotations
to ontology IDs. Sequence ontology definitions can be downloaded from
the `Sequence Ontology site <https://github.com/The-Sequence-Ontology/SO-Ontologies>`_.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: add-ontology
   :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo add-ontology registry.db path/to/so-xp.obo

Adds the sequence ontology ``so-xp.obo`` to the repository using the
default naming rules.

--------------
add-variantset
--------------

Adds a variant set to a named dataset in a repository. Variant sets are
currently derived from one or more non-overlapping VCF/BCF files which
may be either stored locally or come from a remote URL. Multiple VCF
files can be specified either directly on the command line or by
providing a single directory argument that contains indexed VCF files.
If remote URLs are used then index files in the local file system must be
provided using the ``-I`` option.

Note: Starting from 0.9.3, you now need to specify a ``patientId`` and a ``sampleId``. The server
does not validate either, so please double check to make sure the IDs are correct.

.. argparse::
    :module: candig.server.cli.repomanager
    :func: getRepoManagerParser
    :prog: candig_repo
    :path: add-variantset
    :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo add-variantset registry.db 1kg PATIENT_123 SAMPLE_123 1kgPhase1/ -R NCBI37

Adds a new variant set to the dataset named ``1kg`` in the repository defined
by the registry database ``registry.db`` using the VCF files contained in the
directory ``1kgPhase1`` that belong to PATIENT_123 and SAMPLE_123. Note that this
directory must also contain the corresponding indexes for these files. We associate
the reference set named ``NCBI37`` with this new variant set. Because we do not provide a ``--name``
argument, a name is automatically generated using the default name generation
rules.

.. code-block:: bash

    $ candig_repo add-variantset registry.db 1kg PATIENT_123 SAMPLE_123 \
        1kgPhase1/chr1.vcf.gz -n phase1-subset -R NCBI37

Like the last example, we add a new variant set to the dataset ``1kg``, with one VCF
and the corresponding patientId and sampleId. We also specify the
name for this new variant set to be ``phase1-subset``.

.. code-block:: bash

    $ candig_repo add-variantset registry.db 1kg PATIENT_123 SAMPLE_123 \
        --name phase1-subset-remote -R NCBI37 \
        --indexFiles ALL.chr1.phase1_release_v3.20101123.snps_indels_svs.genotypes.vcf.gz.tbi ALL.chr2.phase1_release_v3.20101123.snps_indels_svs.genotypes.vcf.gz.tbi \
        ftp://ftp.ncbi.nlm.nih.gov/1000genomes/ftp/release/20110521/ALL.chr1.phase1_release_v3.20101123.snps_indels_svs.genotypes.vcf.gz \

This example performs the same task of creating a subset of the phase1
VCFs, but this time we use the remote URL directly and do not keep a
local copy of the VCF file. Because we are using remote URLs to define
the variant set, we have to download a local copy of the corresponding
index files and provide them on the command line using the ``--indexFiles``
option.

----------------
add-readgroupset
----------------

Adds a readgroup set to a named dataset in a repository.  Readgroup sets are
currently derived from a single indexed BAM file, which can be either
stored locally or based on a remote URL. If the readgroup set is based on
a remote URL, then the index file must be stored locally and specified using
the ``--indexFile`` option.

Each readgroup set must be associated with the reference set that it is aligned
to. The ``add-readgroupset`` command first examines the headers of the BAM file
to see if it contains information about references, and then looks for a
reference set with name equal to the genome assembly identifer defined in the
header. (Specifically, we read the ``@SQ`` header line and use the value of the
``AS`` tag as the default reference set name.) If this reference set exists,
then the readgroup set will be associated with it automatically. If it does not
(or we cannot find the appropriate information in the header), then the
``add-readgroupset`` command will fail. In this case, the user must provide the
name of the reference set using the ``--referenceSetName`` option.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: add-readgroupset
   :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo add-readgroupset registry.db 1kg \
        path/to/HG00114.chrom11.ILLUMINA.bwa.GBR.low_coverage.20120522.bam

Adds a new readgroup set for an indexed 1000 Genomes BAM file stored on the
local file system. The index file follows the usual convention and is stored in
the same directory as the BAM file and has an extra ``.bai`` extension. The
name of the readgroup set is automatically derived from the file name, and the
reference set automatically set from the BAM header.

.. code-block:: bash

    $ candig_repo add-readgroupset registry.db 1kg PATIENT_123 SAMPLE_123 candig-example-data/HG00096.bam \
        -R GRCh37-subset -n HG0096-subset

Adds a new readgroup set based on a subset of the 1000 genomes reads for the
HG00096 sample from the example data used in the reference server. In this case
we specify that the reference set name ``GRCh37-subset`` be associated with the
readgroup set. We also override the default name generation rules and specify
the name ``HG00096-subset`` for the new readgroup set.

.. code-block:: bash

    $ candig_repo add-readgroupset registry.db 1kg PATIENT_123 SAMPLE_123 \
        -n HG00114-remote
        -I /path/to/HG00114.chrom11.ILLUMINA.bwa.GBR.low_coverage.20120522.bam.bai
        ftp://ftp.ncbi.nlm.nih.gov/1000genomes/ftp/phase3/data/HG00114/alignment/HG00114.chrom11.ILLUMINA.bwa.GBR.low_coverage.20120522.bam

Adds a new readgroups set based on a 1000 genomes BAM directly from the NCBI
FTP server. Because this readgroup set uses a remote FTP URL, we must specify
the location of the ``.bai`` index file on the local file system.

------------------------
add-featureset
------------------------

.. warning::
    Before you add the feature set, you should make sure to index some of the columns in your
    generated DB. Specifically, you should make sure that you both ``gene_name`` and ``type``
    should be indexed. If you don't, queries to this endpoint, and endpoints that depend on this,
    e.g., ``variants/gene/search`` will be very very slow.

    To create a composite index on aforementioned fields, open the featureset DB
    you generated via the sqlite browser,
    then run ``CREATE INDEX name_type_index ON FEATURE (gene_name, type);``.
    You should carefully review your use-case and index other fields accordingly.

Adds a feature set to a named dataset in a repository. Feature sets
must be in a '.db' file. An appropriate '.db' file can
be generate from a GFF3 file using scripts/generate_gff3_db.py.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: add-featureset
   :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo add-featureset registry.db 1KG gencode.db \
        -R hg37 -O so-xp-simple

Adds the feature set `gencode` to the registry under the `1KG`
dataset. The flags set the reference genome to be hg37 and the ontology to
use to `so-xp-simple`.

------------------------
add-continuousset
------------------------

Adds a continuous set to a named dataset in a repository. Continuous sets
must be in a bigWig file. The bigWig format is described here:
http://genome.ucsc.edu/goldenPath/help/bigWig.html. There are directions for
converting wiggle files to bigWig files on the page also. 
Files in the bedGraph format can be converted using bedGraphToBigWig
(https://www.encodeproject.org/software/bedgraphtobigwig/).

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: add-continuousset
   :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo add-continuousset registry.db 1KG continuous.bw \
        -R hg37

Adds the continuous set `continuous` to the registry under the `1KG`
dataset. The flags set the reference genome to be hg37.

-------------------------
init-rnaquantificationset
-------------------------

Initializes a rnaquantification set.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: init-rnaquantificationset
   :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo init-rnaquantificationset repo.db rnaseq.db

Initializes the RNA Quantification Set with the filename rnaseq.db.

---------------------
add-rnaquantification
---------------------

Adds a rnaquantification to a RNA quantification set.

RNA quantification formats supported are currently kallisto and RSEM.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: add-rnaquantification
   :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo add-rnaquantification rnaseq.db data.tsv \
             kallisto candig-example-data/registry.db brca1 \
            --biosampleName HG00096 --featureSetNames gencodev19
            --readGroupSetName HG00096rna --transcript

Adds the data.tsv in kallisto format to the `rnaseq.db` quantification set with
optional fields for associating a quantification with a Feature Set, Read Group
Set, and Biosample.

------------------------
add-rnaquantificationset
------------------------

When the desired RNA quantification have been added to the set, use this command
to add them to the registry.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: add-rnaquantificationset
   :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo add-rnaquantificationset registry.db brca1 rnaseq.db \
        -R hg37 -n rnaseq

Adds the RNA quantification set `rnaseq.db` to the registry under the `brca1`
dataset. The flags set the reference genome to be hg37 and the name of the
set to `rnaseq`.

---------------------------
add-phenotypeassociationset
---------------------------

Adds an rdf object store.  The cancer genome database
Clinical Genomics Knowledge Base http://nif-crawler.neuinfo.org/monarch/ttl/cgd.ttl,
published by the Monarch project, is the supported format for Evidence.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: add-phenotypeassociationset
   :nodefault:


Examples:

.. code-block:: bash

    $ candig_repo add-phenotypeassociationset registry.db dataset1 /monarch/ttl/cgd.ttl -n cgd


-------------------
remove-referenceset
-------------------

Removes a reference set from the repository. Attempting
to remove a reference set that is referenced by other objects in the
repository will result in an error.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-referenceset
   :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo remove-referenceset registry.db NCBI37

Deletes the reference set with name ``NCBI37`` from the repository
represented by ``registry.db``

---------------
remove-ontology
---------------

Removes an ontology from the repository. Attempting
to remove an ontology that is referenced by other objects in the
repository will result in an error.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-ontology
   :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo remove-ontology registry.db so-xp

Deletes the ontology with name ``so-xp`` from the repository
represented by ``registry.db``

-----------------
remove-variantset
-----------------

Removes a variant set from the repository. This also deletes all
associated call sets and variant annotation sets from the repository.

.. argparse::
    :module: candig.server.cli.repomanager
    :func: getRepoManagerParser
    :prog: candig_repo
    :path: remove-variantset
    :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo remove-variantset registry.db dataset1 phase3-release

Deletes the variant set named ``phase3-release`` from the dataset
named ``dataset1`` from the repository represented by ``registry.db``.

-------------------
remove-readgroupset
-------------------

Removes a read group set from the repository.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-readgroupset
   :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo remove-readgroupset registry.db dataset1 HG00114

Deletes the readgroup set named ``HG00114`` from the dataset named
``dataset1`` from the repository represented by ``registry.db``.

-----------------
remove-featureset
-----------------

Removes a feature set from the repository.

.. argparse::
    :module: candig.server.cli.repomanager
    :func: getRepoManagerParser
    :prog: candig_repo
    :path: remove-featureset
    :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo remove-featureset registry.db 1KG gencode-genes

Deletes the feature set named ``gencode-genes`` from the dataset
named ``1KG`` from the repository represented by ``registry.db``.

--------------------
remove-continuousset
--------------------

Removes a continuous set from the repository.

.. argparse::
    :module: candig.server.cli.repomanager
    :func: getRepoManagerParser
    :prog: candig_repo
    :path: remove-continuousset
    :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo remove-continuousset registry.db 1KG continuous

Deletes the feature set named ``continuous`` from the dataset
named ``1KG`` from the repository represented by ``registry.db``.

---------------------------
remove-rnaquantificationset
---------------------------

Removes a rna quantification set from the repository.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-rnaquantificationset
   :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo remove-rnaquantificationset registry.db dataset1 ENCFF305LZB

Deletes the rnaquantification set named ``ENCFF305LZB`` from the dataset named
``dataset1`` from the repository represented by ``registry.db``.

------------------------------
remove-phenotypeassociationset
------------------------------

Removes an rdf object store.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-phenotypeassociationset
   :nodefault:

Examples:

.. code-block:: bash

    $ candig_repo remove-phenotypeassociationset registry.db dataset1  cgd



-------------
add-biosample
-------------

.. warning::

    This command is deprecated, and may be removed soon in future. Use ingest command
    to add Sample-related information.

Adds a new biosample to the repository. The biosample argument is
a JSON document according to the GA4GH JSON schema.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: add-biosample
   :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo add-biosample registry.db dataset1 HG00096 '{"individualId": "abc"}'

Adds the biosample named HG00096 to the repository with the individual ID
"abc".

--------------
add-individual
--------------

.. warning::

    This command is deprecated, and may be removed soon in future. Use ingest command
    to add Patient-related information.


Adds a new individual to the repository. The individual argument is
a JSON document following the GA4GH JSON schema.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: add-individual
   :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo add-individual registry.db dataset1 HG00096 '{"description": "A description"}'



----------------
remove-biosample
----------------

Removes a biosample from the repository.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-biosample
   :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo remove-biosample registry.db dataset1 HG00096

Deletes the biosample with name ``HG00096`` in the dataset
``dataset1`` from the repository represented by ``registry.db``

-----------------
remove-individual
-----------------

Removes an individual from the repository.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-individual
   :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo remove-individual registry.db dataset1 HG00096

Deletes the individual with name ``HG00096`` in the dataset
``dataset1`` from the repository represented by ``registry.db``


++++++++++++++++++++++
Start up candig-server
++++++++++++++++++++++

-------------
candig_server
-------------

There are a number of optional parameters to start up the server.

When no paramters are set, running ``candig-server`` would start up the server at
``http://127.0.0.1:8000``.

You may supply your own config file (.py), as indicated below. This ``config.py`` specifies
the ``DATA_SOURCE`` to be at a custom location, and the ``DEFAULT_PAGE_SIZE`` to be 1500, overridding the default values for both.

.. code-block:: python

    DATA_SOURCE = '/home/user/dev/data.db'
    DEFAULT_PAGE_SIZE = 1500

.. code-block:: text

    usage: candig_server [-h] [--port PORT] [--host HOST] [--config CONFIG]
                         [--config-file CONFIG_FILE] [--tls] [--gunicorn]
                         [--certfile CERTFILE] [--keyfile KEYFILE]
                         [--dont-use-reloader] [--workers WORKERS]
                         [--timeout TIMEOUT] [--worker_class WORKER_CLASS]
                         [--epsilon EPSILON] [--version]
                         [--disable-urllib-warnings]

**Examples:**

.. code-block:: bash

    $ candig_server --host 0.0.0.0 --port 3000 --config-file config.py


-----------
add-peer
-----------

Adds a new peer server.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: add-peer
   :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo add-peer registry.db https://candig.test.ca


-----------
remove-peer
-----------

Removes a peer server.

.. warning::
    If you did not add a trailing path when you add the peer URL, a trailing path is added automatically,
    therefore, as the examples show, if you add ``https://candig.test.ca``, when you delete
    it, you will need to run ``https://candig.test.ca/``.

.. argparse::
   :module: candig.server.cli.repomanager
   :func: getRepoManagerParser
   :prog: candig_repo
   :path: remove-peer
   :nodefault:

**Examples:**

.. code-block:: bash

    $ candig_repo remove-peer registry.db https://candig.test.ca/
