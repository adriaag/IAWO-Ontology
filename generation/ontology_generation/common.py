import sys
from rdflib.collection import Collection
from rdflib import Namespace, Graph, URIRef, Literal, Variable, BNode, RDF, RDFS, SH, OWL, XSD

dmop = Namespace('http://www.e-lico.eu/ontologies/dmo/DMOP/DMOP.owl#')
tb = Namespace('https://dtak.upc.edu/IAWO/tbox#')
cb = Namespace('https://dtak.upc.edu/IAWO/cbox#')
ab = Namespace('https://dtak.upc.edu/IAWO/abox#')
dolce = Namespace('http://ontologydesignpatterns.org/ont/dul/DUL.owl#')
sh = Namespace('http://www.w3.org/ns/shacl#')

def get_graph_IAWO():
    g = Graph()
    g.bind('tb', tb)
    g.bind('cb', cb)
    g.bind('ab', ab)
    g.bind('dmop', dmop)
    g.bind('dolce', dolce)
    return g