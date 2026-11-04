from rdflib import Graph, URIRef, BNode
from owlrl import DeductiveClosure, RDFS_Semantics
from pyshacl import validate


# --------------------------------------------------
# 1. Load the three RDF graphs
# --------------------------------------------------

data_graph = Graph()
data_graph.parse("equipment_four_stations_EQ.jsonld", format="json-ld")

vocab_graph = Graph()
vocab_graph.parse("cim17.vocab.rdfs.ttl", format="turtle")

shapes_graph = Graph()
shapes_graph.parse("nbnl-equipment.prof.shacl.jsonld", format="json-ld")


# --------------------------------------------------
# 2. Create a combined graph for reasoning
# --------------------------------------------------

reasoning_graph = Graph()

for triple in data_graph:
    reasoning_graph.add(triple)

for triple in vocab_graph:
    reasoning_graph.add(triple)


# --------------------------------------------------
# 3. Compute the RDFS closure
# --------------------------------------------------

DeductiveClosure(RDFS_Semantics).expand(reasoning_graph)


# --------------------------------------------------
# 4. Extract inferred instance-level triples
# --------------------------------------------------

# Keep the original data graph as the validation graph.
# This avoids accidentally treating ontology declarations
# themselves as instance data during SHACL validation.

validation_graph = Graph()

for triple in data_graph:
    validation_graph.add(triple)

# Resources occurring in the original instance data.
instance_nodes = {
    term
    for triple in data_graph
    for term in (triple[0], triple[2])
    if isinstance(term, (URIRef, BNode))
}

# Add inferred triples concerning instance resources.
original_triples = set(data_graph)

for triple in reasoning_graph:
    if triple not in original_triples and triple[0] in instance_nodes:
        validation_graph.add(triple)


# --------------------------------------------------
# 5. Validate using pySHACL
# --------------------------------------------------

conforms, results_graph, results_text = validate(
    data_graph=validation_graph,
    shacl_graph=shapes_graph,
    inference="none",
    abort_on_first=False,
    meta_shacl=True,
    advanced=False
)


# --------------------------------------------------
# 6. Display the validation report
# --------------------------------------------------

print("Conforms:", conforms)
print(results_text)

# Optional: save the enriched graph and validation report.
validation_graph.serialize(
    destination="enriched-data.ttl",
    format="turtle"
)

results_graph.serialize(
    destination="validation-report.ttl",
    format="turtle"
)

