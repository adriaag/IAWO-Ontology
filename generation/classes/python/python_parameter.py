from typing import List, Union
from classes.core.expression import AlgebraicExpression
from classes.core.parameter import LiteralValue
from ontology_generation.common import *
from classes.core.engine_parameter import EngineFactorParameter, EngineNumericParameter, EngineTextParameter

class PythonParameter:
    def __init__(self, control_parameter=False, **kwargs):
        super().__init__(engine=cb.Python, **kwargs)
        self.is_control_parameter = control_parameter #Indicates if the parameter tunes the function or is used to render the template

class PythonNumericParameter(PythonParameter, EngineNumericParameter):
    def __init__(self, key:str, datatype:URIRef, expression:AlgebraicExpression, default_value:Union[URIRef, LiteralValue], control_parameter=False):
        super().__init__(key=key, datatype=datatype, expression=expression, default_value=default_value, control_parameter=control_parameter)

class PythonTextParameter(PythonParameter, EngineTextParameter):
    def __init__(self, key:str, base_parameter:URIRef, default_value:Union[URIRef, LiteralValue], control_parameter=False):
        super().__init__(key=key, base_parameter=base_parameter, default_value=default_value, control_parameter=control_parameter)

class PythonFactorParameter(PythonParameter, EngineFactorParameter):
    def __init__(self, key:str, levels: dict, base_parameter:URIRef, default_value:Union[URIRef, LiteralValue], control_parameter=False):
        super().__init__(key=key, levels=levels, base_parameter=base_parameter, default_value=default_value, control_parameter=control_parameter)