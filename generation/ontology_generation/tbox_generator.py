from ontology_generation.common import *


def add_class(graph, nodes):
    l = nodes if isinstance(nodes, list) else [nodes]
    for node in l:
        graph.add((node, RDF.type, OWL.Class))


def add_union(graph, nodes):
    sequence = Collection(graph, BNode(), nodes)
    union = BNode()
    graph.add((union, OWL.unionOf, sequence.uri))
    return union


def add_object_property(graph, property, domain, range):
    graph.add((property, RDF.type, OWL.ObjectProperty))
    if domain:
        graph.add((property, RDFS.domain, add_union(graph, domain) if isinstance(domain, list) else domain))
    if range:
        graph.add((property, RDFS.range, add_union(graph, range) if isinstance(range, list) else range))


def add_datatype_property(graph, property, domain, range):
    if isinstance(range, list):
        for r in range:
            assert r in XSD
    else:
        assert range in XSD
    graph.add((property, RDF.type, OWL.DatatypeProperty))
    if domain:
        graph.add((property, RDFS.domain, add_union(graph, domain) if isinstance(domain, list) else domain))
    if range:
        graph.add((property, RDFS.range, add_union(graph, range) if isinstance(range, list) else range))


def add_property(graph, property, domain, range):
    graph.add((property, RDF.type, RDF.Property))
    if domain:
        graph.add((property, RDFS.domain, add_union(graph, domain) if isinstance(domain, list) else domain))
    if range:
        graph.add((property, RDFS.range, add_union(graph, range) if isinstance(range, list) else range))


def get_graph_IAWO():
    g = Graph()
    g.bind('tb', tb)
    g.bind('cb', cb)
    g.bind('ab', ab)
    g.bind('dmop', dmop)
    g.bind('dolce', dolce)
    return g


def init_ontology() -> Graph:
    ontology = get_graph_IAWO()

    ontology.add((URIRef(str(tb)), RDF.type, OWL.Ontology))
    ontology.add((URIRef(str(tb)), RDFS.label, Literal("IAWO Ontology TBox")))
    return ontology


def add_classes(ontology: Graph):
    classes = [
        tb.User,
        tb.Intent,
        #tb.Requirement,
        tb.MetricValue,
        tb.LiteralValue,
        tb.Task,
        tb.Algorithm,
        tb.Implementation,
        tb.LearnerImplementation,
        tb.ApplierImplementation,
        tb.Parameter,
        tb.ParameterSpecification,
        tb.ParameterValue,
        tb.Component,
        tb.Workflow,
        tb.Step,
        tb.Data,
        tb.Dataset,
        tb.Model,
        tb.DataCharacteristic,
        tb.DataPort,
        tb.DataPortCharacteristic,
        tb.Rule,
        tb.AlgebraicExpression,
        tb.Operation,
        tb.FactorParameter,
        tb.NumericParameter,
        tb.BaseParameter,
        tb.DerivedParameter,
        tb.FactorLevel,
        tb.Engine,
        tb.EngineImplementation,
        tb.EngineParameter,
        tb.Feature,
        tb.Constraint,
        tb.AlgorithmConstraint,
        tb.ComponentConstraint,
        tb.ImplementationConstraint,
        tb.WorkflowConstraint,

    ]
    add_class(ontology, classes)

    #ontology.add((tb.CopyTransformation, RDFS.subClassOf, tb.Transformation))
    #ontology.add((tb.LoaderTransformation, RDFS.subClassOf, tb.Transformation))

    ontology.add((tb.LearnerImplementation, RDFS.subClassOf, tb.Implementation))
    ontology.add((tb.ApplierImplementation, RDFS.subClassOf, tb.Implementation))
    ontology.add((tb.LearnerImplementation, OWL.disjointWith, tb.ApplierImplementation))

    ontology.add((tb.Model, RDFS.subClassOf, tb.Data))
    ontology.add((tb.Dataset, RDFS.subClassOf, tb.Data))
    ontology.add((dmop.TabularDataset, RDFS.subClassOf, tb.Dataset))
    ontology.add((dmop.TensorDataset, RDFS.subClassOf, tb.Dataset))

    ontology.add((tb.FactorParameter, RDFS.subClassOf, tb.Parameter))
    ontology.add((tb.NumericParameter, RDFS.subClassOf, tb.Parameter))
    ontology.add((tb.BaseParameter, RDFS.subClassOf, tb.Parameter))
    ontology.add((tb.DerivedParameter, RDFS.subClassOf, tb.Parameter))
    ontology.add((tb.FactorParameter, OWL.disjointWith, tb.NumericParameter))
    ontology.add((tb.BaseParameter, OWL.disjointWith, tb.DerivedParameter))

    ontology.add((tb.EngineParameter, RDFS.subClassOf, tb.Parameter))

    ontology.add((tb.AlgorithmConstraint, RDFS.subClassOf, tb.Constraint))
    ontology.add((tb.ComponentConstraint,  RDFS.subClassOf, tb.Constraint))
    ontology.add((tb.ImplementationConstraint,  RDFS.subClassOf, tb.Constraint))            
    ontology.add((tb.WorkflowConstraint,  RDFS.subClassOf, tb.Constraint))
    ontology.add((tb.Constraint, RDFS.subClassOf, SH.NodeShape))

    ontology.add((tb.AlgorithmConstraint, SH.targetClass,  tb.Algorithm))
    ontology.add((tb.ComponentConstraint, SH.targetClass,   tb.Component))
    ontology.add((tb.ImplementationConstraint, SH.targetClass,   tb.Implementation))         
    ontology.add((tb.WorkflowConstraint,  SH.targetClass, tb.Workflow))
        
        
def add_properties(ontology: Graph):
    properties = [
        #User
        (tb.defines, tb.User, tb.Intent),
        # Intent
        (tb.overData, tb.Intent, tb.Data),
        (tb.specifies, tb.Intent, tb.Algorithm),
        (tb.specifiesValue, tb.Intent, tb.ParameterValue),
        (tb.hasConstraint, tb.Intent, tb.Constraint),
        #(tb.hasRequirement, tb.Intent, tb.Requirement),
        (tb.has_component_threshold, tb.Intent, XSD.double),
        (tb.has_complexity, tb.Intent, XSD.unsignedInt),
        # ParameterValue
        (tb.forParameter, tb.ParameterValue, tb.Parameter),
         # Task
        (tb.subtaskOf, tb.Task, tb.Task),
        (tb.tackles, tb.Task, tb.Intent),
        # Workflow
        (tb.generatedFor, tb.Workflow, tb.Intent),
        (tb.hasStep, tb.Workflow, tb.Step),
        # Workflow Characteristics
        ### TO BE DEFINED
        # Model Evaluatoin
        #(tb.specifiesMetric, tb.ModelEvaluation, tb.Metric),
        #(tb.hasValue, tb.ModelEvaluation, XSD.double),
        # Constraint
        #(tb.constrainedBy, tb.Intent, tb.ExperimentConstraint),
        #(tb.isHard, tb.ExperimentConstraint, XSD.boolean),
        #(tb.constraintType, tb.ExperimentConstraint, XSD.string),
        ### tb.on is TO BE DEFINED
        # Constraint Value
        #(tb.hasConstraintValue, tb.ExperimentConstraint, tb.ConstraintValue),
        #(tb.hasOptionExplorerName, tb.ExperimentConstraint, XSD.string),
        #(tb.hasMinValue, tb.RangeValue, XSD.double),
        #(tb.hasMaxValue, tb.RangeValue, XSD.double),
        #(tb.hasLiteralValue, tb.LiteralValue, XSD.string),
        ### tb.hasValue is TO BE DEFINED
        # Algorithm
        (tb.solves, tb.Algorithm, tb.Task),
        # Implementation
        (tb.implements, tb.Implementation, tb.Algorithm),
        (tb.hasParameter, tb.Implementation, tb.Parameter),
        (tb.hasLearner, tb.ApplierImplementation, tb.LearnerImplementation),
        (tb.hasApplier, tb.LearnerImplementation, tb.ApplierImplementation),
        (tb.specifiesInput, tb.Implementation, tb.DataPort),
        (tb.specifiesOutput, tb.Implementation, tb.DataPort),
        (tb.has_engine, tb.EngineImplementation, tb.Engine),
        (tb.compatibleWith, tb.Implementation, tb.Engine),
        # Engine Implementation
        #TODO: to be defined
        # Component
        (tb.hasTransformation, tb.Component, RDF.List),
        (tb.hasImplementation, tb.Component, tb.Implementation),
        (tb.specifiesParameter, tb.Component, tb.ParameterSpecification),
        (tb.hasRule, tb.Component, tb.Rule),
        # Step
        (tb.followedBy, tb.Step, tb.Step),
        (tb.hasInput, tb.Step, tb.Data),
        (tb.hasOutput, tb.Step, tb.Data),
        (tb.runs, tb.Step, tb.Component),
        (tb.usesParameter, tb.Step, tb.Parameter),
        # Parameter
        (tb.hasBaseParameter, tb.ParameterSpecification, tb.BaseParameter),
        (tb.has_datatype, tb.Parameter, None),
        (tb.has_defaultvalue, tb.Parameter, None),

        (tb.hasLevel, tb.FactorParameter, tb.FactorLevel),
        (tb.derivedFrom, tb.DerivedParameter, tb.AlgebraicExpression),

        #Algebraic Operation
        #(tb.hasTerm1, tb.AlgebraicExpression, tb.Parameter),
        #(tb.hasTerm1, tb.AlgebraicExpression, tb.AlgebraicOperation),
        #(tb.hasTerm1, tb.AlgebraicExpression, XSD.numeric),
        #(tb.hasTerm2, tb.AlgebraicExpression, tb.Parameter),
        #(tb.hasTerm2, tb.AlgebraicExpression, tb.AlgebraicOperation),
        #(tb.hasTerm2, tb.AlgebraicExpression, XSD.numeric),
        (tb.hasOperation, tb.AlgebraicExpression, tb.Operation),

        #Engine parameter
        #TODO: to be defined

        # Hyperparameter Specification
        (tb.hasValue, tb.ParameterSpecification, None),
        # Data
        #(dolce.hasQuality, tb.Data, tb.DataCharacteristics),
        (tb.hasMetricValue, tb.Data, tb.MetricValue),
        (tb.hasMetricValue, tb.Feature, tb.MetricValue),
        # Data Characteristics
        #(tb.hasValue, tb.DataCharacteristics, XSD.string),
        # DataPort
        (tb.characterizedBy, tb.DataPort, tb.DataPortCharacteristic),
        # tb.DataPortCharacteristic
        (tb.hasCharacteristic, tb.DataPortCharacteristic, tb.DataCharacteristic),
        (tb.hasImportanceLevel, tb.DataPortCharacteristic, XSD.unsignedInt),
        # Rule
        (tb.relatedtoTask, tb.Rule, tb.Task),
        (tb.relatedtoCharacteristic, tb.Rule, tb.DataCharacteristic),
        (tb.hasScore, tb.Rule, XSD.unsignedInt),
        #Dataset
        (tb.hasFeature, tb.Dataset, tb.Feature),
    ]
    for s, p, o in properties:
        add_object_property(ontology, s, p, o)

    ontology.add((tb.subtaskOf, RDF.type, OWL.TransitiveProperty))

    dproperties = [
        # Transformation
        #(tb.copy_input, tb.CopyTransformation, XSD.integer),
        #(tb.copy_output, tb.CopyTransformation, XSD.integer),
        #(tb.transformation_language, tb.Transformation, XSD.string),
        #(tb.transformation_query, tb.Transformation, XSD.string),
        # Data
        (tb.has_position, [tb.Data, tb.DataPort, tb.Step, tb.Parameter], XSD.integer),
        (tb.has_condition, tb.Parameter, XSD.string)
    ]

    for s, p, o in dproperties:
        add_datatype_property(ontology, s, p, o)

    subproperties = [
        # Column
        (dmop.hasColumnName, dmop.ColumnInfoProperty),
        (dmop.hasDataPrimitiveTypeColumn, dmop.ColumnInfoProperty),
        (dmop.hasPosition, dmop.ColumnInfoProperty),
        (dmop.isCategorical, dmop.ColumnInfoProperty),
        (dmop.isFeature, dmop.ColumnInfoProperty),
        (dmop.isLabel, dmop.ColumnInfoProperty),
        (dmop.isUnique, dmop.ColumnInfoProperty),
        (dmop.containsNulls, dmop.ColumnValueInfoProperty),
        (dmop.hasMeanValue, dmop.ColumnValueInfoProperty),
        (dmop.hasStandardDeviation, dmop.ColumnValueInfoProperty),
        (dmop.hasMaxValue, dmop.ColumnValueInfoProperty),
        (dmop.hasMinValue, dmop.ColumnValueInfoProperty),
        (dmop.isNormalDistribution, dmop.ColumnInfoProperty),
        (dmop.hasOutliers, dmop.ColumnInfoProperty),

        # Dataset
        (dmop.delimiter, dmop.DatasetPhysicalProperty),
        (dmop.doubleQuote, dmop.DatasetPhysicalProperty),
        (dmop.encoding, dmop.DatasetPhysicalProperty),
        (dmop.fileFormat, dmop.DatasetPhysicalProperty),
        (dmop.hasHeader, dmop.DatasetPhysicalProperty),
        (dmop.isNormalized, dmop.DatasetValueInfoProperty),
        (dmop.lineDelimiter, dmop.DatasetPhysicalProperty),
        (dmop.numberOfColumns, dmop.DatasetInfoProperty),
        (dmop.numberOfRows, dmop.DatasetInfoProperty),
        (dmop.path, dmop.DatasetPhysicalProperty),
        (dmop.quoteChar, dmop.DatasetPhysicalProperty),
        (dmop.skipInitialSpace, dmop.DatasetPhysicalProperty),
        (dmop.isTrainDataset, dmop.DatasetInfoProperty),
        (dmop.isTestDataset, dmop.DatasetInfoProperty),
        (dmop.isNormallyDistributed, dmop.DatasetInfoProperty),
        (dmop.containsOutliers, dmop.DatasetInfoProperty),
    ]

    for s, o in subproperties:
        ontology.add((s, RDFS.subPropertyOf, o))


def main(dest: str = './tbox.ttl') -> None:
    ontology = init_ontology()
    add_classes(ontology)
    add_properties(ontology)
    ontology.serialize(dest, format='turtle')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
