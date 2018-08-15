from SPARQLWrapper import SPARQLWrapper, JSON


class NCIT(object):

    def __init__(self):
        pass

    def _get_ncit_term(self, gene):
        _sparql = SPARQLWrapper("https://stars-app.renci.org/ncitgraph/sparql")
        query = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX gene: <http://purl.obolibrary.org/obo/NCIT_C16612>
            SELECT DISTINCT ?gene
            FROM <http://purl.obolibrary.org/obo/ncit.owl>
            FROM <http://purl.obolibrary.org/obo/ncit/ncit-property-graph-redundant.ttl>
            WHERE {
                ?gene rdfs:subClassOf* gene: .
                ?gene rdfs:label ?gene_label .
                #%FILTER%
            }
        """
        filter = """
            FILTER regex(?gene_label, "{} Gene")
        """.format(gene)

        query = query.replace("#%FILTER%", filter)

        _sparql.setReturnFormat(JSON)
        _sparql.setQuery(query)

        results = _sparql.query().convert()

        return results["results"]["bindings"][0]['gene']['value']

    def get_genetic_abnormalities(self, gene):
        _sparql = SPARQLWrapper("https://stars-app.renci.org/ncitgraph/sparql")
        query = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX #%FILTER%
            PREFIX MolecularAbnormalityInvolvesGene: <http://purl.obolibrary.org/obo/NCIT_R177>
            SELECT DISTINCT ?abnormality_label
            FROM <http://purl.obolibrary.org/obo/ncit.owl>
            FROM <http://purl.obolibrary.org/obo/ncit/ncit-property-graph-redundant.ttl>
            WHERE {
            ?abnormality MolecularAbnormalityInvolvesGene: gene: .
            ?abnormality rdfs:label ?abnormality_label .
            } limit 5
        """
        filter = """
            gene: <{}>
        """.format(self._get_ncit_term(gene))

        query = query.replace("#%FILTER%", filter)

        _sparql.setQuery(query)
        _sparql.setReturnFormat(JSON)
        results = _sparql.query().convert()

        return results["results"]["bindings"]

    def get_diseases(self, gene):
        _sparql = SPARQLWrapper("https://stars-app.renci.org/ncitgraph/sparql")
        query = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX  #%FILTER%
            PREFIX DiseaseMappedToGene: <http://purl.obolibrary.org/obo/NCIT_R176>
            SELECT DISTINCT ?disease ?disease_label
            FROM <http://purl.obolibrary.org/obo/ncit.owl>
            FROM <http://purl.obolibrary.org/obo/ncit/ncit-property-graph-redundant.ttl>
            WHERE {
            ?disease DiseaseMappedToGene: gene: .
            ?disease rdfs:label ?disease_label .
            } limit 5
        """
        filter = """
            gene: <{}>
        """.format(self._get_ncit_term(gene))

        query = query.replace("#%FILTER%", filter)

        _sparql.setQuery(query)
        _sparql.setReturnFormat(JSON)
        results = _sparql.query().convert()

        return results["results"]["bindings"]
