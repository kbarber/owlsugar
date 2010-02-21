from owlsugar.universe import OwlUniverse
from owlsugar.constructs import *

# First initialise the universe
universe = OwlUniverse() 

a = Namespace()
a.newinit("foo", "<http://bob.sh/#>")

# Test Structure
ont = Ontology(
    ontologyURI=URI(uri="<http://bob.sh/>"), 
    annotations=[
        AnnotationByConstant(
            annotationURI=URI(uri="fooannotation"),
            annotationValue=Constant(value="foo", 
            datatypeURI=URI(uri="<http://foo.com/#fooType>"))),
        Label("Testing a label")
        ],
        
    axioms=[
        Declaration(entity=Individual(entityURI=URI(uri="#foot"))), 
        Declaration(entity=Individual(entityURI=URI(uri="#shin"))),
        ])

# Extract information from elements defined above
print "Axiom:", ont.axioms()
print "Annotations:", ont.annotations()
print "All classes:", universe.get_classes()
print "Ontology class:", universe.get_class("Ontology")
print "Ontology objects:", universe.get_objects("Ontology")
print "Declaration objects:", universe.get_objects("Declaration")
print "Individual objects:", universe.get_objects("Individual")
print "URI objects:", universe.get_objects("URI")
print "Annotation objects:", universe.get_objects("Annotation")
print "Annotation URI's:", [i.annotationURI().uri() for i in universe.get_objects("Annotation")]
print "Namespace:", [i.IRI() for i in universe.get_objects("Namespace")]
