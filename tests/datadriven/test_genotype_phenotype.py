"""
Data-driven tests for g2p.
"""

import os
import rdflib

import candig.server.datamodel.genotype_phenotype as genotype_phenotype
import candig.server.datamodel.datasets as datasets
import tests.datadriven as datadriven
import tests.paths as paths

import candig.schemas.protocol as protocol


def testG2P():
    testDataDir = os.path.join(
        paths.testDataDir, 'datasets/dataset1/phenotypes')
    for test in datadriven.makeTests(testDataDir, PhenotypeAssociationSetTest):
        yield test


class PhenotypeAssociationSetTest(datadriven.DataDrivenTest):
    def __init__(self, localId, baseDir):
        self._dataset = datasets.Dataset("ds")
        super(PhenotypeAssociationSetTest, self).__init__(localId, baseDir)
        self.phenotypeAssocationSet = self.getDataModelInstance(
            localId, baseDir)

    def getDataModelInstance(self, localId, dataPath):
        return genotype_phenotype.RdfPhenotypeAssociationSet(
            self._dataset, localId, dataPath)

    def getProtocolClass(self):
        return protocol.PhenotypeAssociationSet

    def testDetailTuples(self):
        test_uriRefs = [
            rdflib.term.URIRef('http://ohsu.edu/cgd/27d2169c'),
            rdflib.term.URIRef('http://ohsu.edu/cgd/87752f6c')
        ]
        details = self.phenotypeAssocationSet._detailTuples(test_uriRefs)
        self.assertEqual(len(details), 6)
        sample1 = {
            'predicate': 'http://www.w3.org/2000/01/rdf-schema#label',
            'object': 'GIST with decreased sensitivity to therapy',
            'subject': 'http://ohsu.edu/cgd/87752f6c',
        }
        sample2 = {
            'predicate': 'http://purl.obolibrary.org/obo/RO_0002200',
            'object': 'http://ohsu.edu/cgd/87752f6c',
            'subject': 'http://ohsu.edu/cgd/27d2169c',
        }
        self.assertIn(sample1, details)
        self.assertIn(sample2, details)

    def testBindingsToDict(self):
        bindings = {
            rdflib.term.Variable('association'):
            rdflib.term.URIRef('http://ohsu.edu/cgd/fe484b5c'),
            rdflib.term.Variable('feature'):
            rdflib.term.URIRef(
                'http://cancer.sanger.ac.uk/cosmic/mutation/overview?id=965'
            ),
            rdflib.term.Variable('phenotype_label'):
            rdflib.term.Literal(
                'Papillary thyroid carcinoma with sensitivity to therapy'
            ),
            rdflib.term.Variable('environment_label'):
            rdflib.term.Literal('sunitinib'),
            rdflib.term.Variable('environment'):
            rdflib.term.URIRef('http://www.drugbank.ca/drugs/DB01268'),
            rdflib.term.Variable('evidence_type'):
            rdflib.term.URIRef('http://purl.obolibrary.org/obo/ECO_0000033'),
            rdflib.term.Variable('sources'):
            rdflib.term.Literal(
                'http://www.ncbi.nlm.nih.gov/pubmed/21470995|'
                'http://www.ncbi.nlm.nih.gov/pubmed/21470995'),
            rdflib.term.Variable('phenotype'):
            rdflib.term.URIRef('http://ohsu.edu/cgd/30ebfd1a'),
            rdflib.term.Variable('feature_label'):
            rdflib.term.Literal('COSM965'),
        }
        myDict = self.phenotypeAssocationSet._bindingsToDict(bindings)
        sampleDict = {
            'environment_label': 'sunitinib',
            'feature_label': 'COSM965',
            'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000033',
            'feature':
            'http://cancer.sanger.ac.uk/cosmic/mutation/overview?id=965',
            'environment': 'http://www.drugbank.ca/drugs/DB01268',
            'sources':
            'http://www.ncbi.nlm.nih.gov/pubmed/21470995|'
            'http://www.ncbi.nlm.nih.gov/pubmed/21470995',
            'phenotype': 'http://ohsu.edu/cgd/30ebfd1a',
            'phenotype_label':
            'Papillary thyroid carcinoma with sensitivity to therapy',
            'association': 'http://ohsu.edu/cgd/fe484b5c',
        }
        self.assertEqual(myDict, sampleDict)

    def testGetDetails(self):
        uriRef = 'http://www.drugbank.ca/drugs/DB01268'
        associations_details = [
            {'predicate': 'http://purl.obolibrary.org/obo/RO_0002606',
             'object': 'http://ohsu.edu/cgd/54039374',
             'subject': 'http://www.drugbank.ca/drugs/DB01268'},
            {'predicate': 'http://purl.obolibrary.org/obo/RO_0002606',
             'object': 'http://ohsu.edu/cgd/983a1528',
             'subject': 'http://www.drugbank.ca/drugs/DB01268'},
            {'predicate': 'http://purl.obolibrary.org/obo/RO_0002606',
             'object': 'http://ohsu.edu/cgd/71fe9f0f',
             'subject': 'http://www.drugbank.ca/drugs/DB01268'},
            {'predicate': 'http://www.w3.org/2000/01/rdf-schema#subClassOf',
             'object': 'http://purl.obolibrary.org/obo/CHEBI_23888',
             'subject': 'http://www.drugbank.ca/drugs/DB01268'}
        ]
        sample_details = {
            'http://purl.obolibrary.org/obo/RO_0002606':
            'http://ohsu.edu/cgd/71fe9f0f',
            'http://www.w3.org/2000/01/rdf-schema#subClassOf':
            'http://purl.obolibrary.org/obo/CHEBI_23888',
            'id': 'http://www.drugbank.ca/drugs/DB01268'}
        details = self.phenotypeAssocationSet._getDetails(
            uriRef, associations_details)
        self.assertEqual(details, sample_details)

    def testToNamespaceURL(self):
        sample_term = 'DrugBank:DB01268'
        result = self.phenotypeAssocationSet._toNamespaceURL(sample_term)
        self.assertEqual('http://www.drugbank.ca/drugs/DB01268', result)

    def testGetIdentifier(self):
        sample_url = 'http://www.drugbank.ca/drugs/DB01268'
        result = self.phenotypeAssocationSet._getIdentifier(sample_url)
        self.assertEqual('DB01268', result)

    def testGetPrefix(self):
        sample_url = 'http://www.drugbank.ca/drugs/'
        result = self.phenotypeAssocationSet._getPrefix(sample_url)
        self.assertEqual('DrugBank', result)

    def testGetPrefixURL(self):
        sample_url = 'http://www.drugbank.ca/drugs/DDD'
        result = self.phenotypeAssocationSet._getPrefixURL(sample_url)
        self.assertEqual('http://www.drugbank.ca/drugs/', str(result))

    def testExtractAssociationsDetails(self):
        sample_query = """
        PREFIX OBAN: <http://purl.org/oban/>
            PREFIX OBO: <http://purl.obolibrary.org/obo/>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT
                ?association
                ?environment
                ?environment_label
                ?feature
                ?feature_label
                ?phenotype
                ?phenotype_label
                (GROUP_CONCAT(?source; separator="|") AS ?sources)
                ?evidence_type
                WHERE {
                    ?association  a OBAN:association .
                    ?association    OBO:RO_0002558 ?evidence_type .
                    ?association    OBO:RO_has_environment ?environment   .
                    OPTIONAL { ?association  dc:source ?source } .
                    ?association    OBAN:association_has_subject ?feature .
                    ?association    OBAN:association_has_object ?phenotype .
                    ?environment  rdfs:label ?environment_label  .
                    ?phenotype  rdfs:label ?phenotype_label  .
                    ?feature  rdfs:label ?feature_label  .
                    FILTER ((?feature = <http://ohsu.edu/cgd/27d2169c> ))
                    }
            GROUP  BY ?association
            ORDER  BY ?association
        """
        sample_associations = \
            self.phenotypeAssocationSet._rdfGraph.query(sample_query)
        result = self.phenotypeAssocationSet._extractAssociationsDetails(
            sample_associations)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].toPython(), 'http://ohsu.edu/cgd/27d2169c')
        self.assertEqual(
            result[1].toPython(),
            'http://www.drugbank.ca/drugs/DB00619')
        self.assertEqual(result[2].toPython(), 'http://ohsu.edu/cgd/87752f6c')

    def testToGA4GH(self):
        sample_associations = {
            'environment_label': 'sunitinib',
            'feature_label': 'RET M918T missense mutation',
            'evidence_type': 'http://purl.obolibrary.org/obo/ECO_0000033',
            'feature': {
                'http://purl.obolibrary.org/obo/GENO_0000408':
                'http://www.ncbi.nlm.nih.gov/gene/5979',
                'http://purl.obolibrary.org/obo/GENO_reference_amino_acid':
                'M',
                'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
                'http://purl.obolibrary.org/obo/SO_0001059',
                'http://biohackathon.org/resource/faldo#location':
                'http://www.monarchinitiative.org/_918918UniProtKB:'
                'P07949#P07949-1Region',
                'http://purl.obolibrary.org/obo/GENO_reference_nucleotide':
                'T',
                'http://purl.obolibrary.org/obo/'
                'GENO_results_in_amino_acid_change':
                'T',
                'http://purl.obolibrary.org/obo/RO_0002200':
                'http://ohsu.edu/cgd/3774b1d2',
                'http://purl.obolibrary.org/obo/RO_0002205':
                'http://www.ncbi.nlm.nih.gov/CCDS/CcdsBrowse.cgi?'
                'REQUEST=CCDS&DATA=7200.1',
                'http://purl.obolibrary.org/obo/GENO_altered_nucleotide':
                'C',
                'http://www.w3.org/2000/01/rdf-schema#label':
                'RET M918T missense mutation',
                'id': 'http://cancer.sanger.ac.uk/cosmic/mutation/'
                'overview?id=965',
                'http://www.w3.org/2002/07/owl#sameAs':
                'http://www.ncbi.nlm.nih.gov/SNP/74799832',
            },
            'evidence': 'http://ohsu.edu/cgd/sensitivity',
            'environment': {
                'http://purl.obolibrary.org/obo/RO_0002606':
                'http://ohsu.edu/cgd/71fe9f0f',
                'http://www.w3.org/2000/01/rdf-schema#subClassOf':
                'http://purl.obolibrary.org/obo/CHEBI_23888',
                'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
                'http://www.w3.org/2002/07/owl#Class',
                'http://www.w3.org/2000/01/rdf-schema#label': 'sunitinib',
                'id': 'http://www.drugbank.ca/drugs/DB01268',
            },
            'sources':
            'http://www.ncbi.nlm.nih.gov/pubmed/21470995|'
            'http://www.ncbi.nlm.nih.gov/pubmed/21470995',
            'phenotype': {
                'http://purl.obolibrary.org/obo/BFO_0000159':
                'http://ohsu.edu/cgd/sensitivity',
                'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
                'http://purl.obolibrary.org/obo/DOID_3969',
                'http://www.w3.org/2000/01/rdf-schema#label':
                'Papillary thyroid carcinoma with sensitivity to therapy',
                'id': 'http://ohsu.edu/cgd/30ebfd1a',
            },
            'phenotype_label':
            'Papillary thyroid carcinoma with sensitivity to therapy',
            'id': 'http://ohsu.edu/cgd/fe484b5c',
            'association': 'http://ohsu.edu/cgd/fe484b5c',
        }
        result = self.phenotypeAssocationSet._toGA4GH(sample_associations)
        self.assertEqual(
            result.__class__.__name__, 'FeaturePhenotypeAssociation')
        fpa_dict = protocol.toJsonDict(result)
        description = 'Association: genotype:[RET M918T missense mutation]' \
                      ' phenotype:[Papillary thyroid carcinoma with ' \
                      'sensitivity to therapy] environment:[sunitinib]' \
                      ' evidence:[sensitivity] publications:' \
                      '[http://www.ncbi.nlm.nih.gov/pubmed/21470995|' \
                      'http://www.ncbi.nlm.nih.gov/pubmed/21470995]'

        self.assertEqual(fpa_dict['description'], description)
        self.assertIn('featureIds', list(fpa_dict.keys()))
        self.assertIn('evidence', list(fpa_dict.keys()))
        self.assertIn('environmentalContexts', list(fpa_dict.keys()))
        self.assertEqual(len(fpa_dict['featureIds']), 1)
        self.assertEqual(len(fpa_dict['evidence']), 1)
        self.assertEqual(len(fpa_dict['environmentalContexts']), 1)
