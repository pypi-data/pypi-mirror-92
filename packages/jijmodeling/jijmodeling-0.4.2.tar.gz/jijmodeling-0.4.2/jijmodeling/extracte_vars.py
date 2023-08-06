from jijmodeling.variables import variable
from jijmodeling.variables.var_array import PlaceholderArray
from jijmodeling.expression.sum import SumOperator
from jijmodeling.variables.variable import Element
from jijmodeling.variables.placeholders import ArraySizePlaceholder
from typing import Dict
from functools import singledispatch
from jijmodeling.variables.variable import Variable
from jijmodeling.variables.obj_vars import DisNum, LogEncInteger, ObjectiveVariable
from jijmodeling.expression.expression import Expression
from jijmodeling import Placeholder


def extracte_variables(term) -> Dict[str, Dict[str, Variable]]:
    vars = {
        'placeholders': {},
        'obj_vars': {},
        'array': {}
    }
    return _extracte_variables(term, vars)


@singledispatch
def _extracte_variables(term, variables: dict) -> Dict[str, Dict[str, Variable]]:
    if isinstance(term, Expression):
        for child in term.children:
            variables = _extracte_variables(child, variables)
    return variables


def extracte_from_shape_subscripts(term: Variable, variables: dict):
    for s in term._shape:
        if s is not None and isinstance(s, Expression):
            variables = _extracte_variables(s, variables)
    for s in term.subscripts:
        if s is not None and isinstance(s, Expression):
            variables = _extracte_variables(s, variables)
    return variables


@_extracte_variables.register(Placeholder)
def placeholder_extracte_variables(term: Placeholder, variables: dict):
    variables = extracte_from_shape_subscripts(term, variables)
    for child in term.children:
        variables = _extracte_variables(child, variables)
    if term.label in variables['placeholders']:
        return variables
    variables['placeholders'][term.label] = term
    return variables


@_extracte_variables.register(ObjectiveVariable)
def objvar_extracte_variables(term: ObjectiveVariable, variables: dict):
    variables = extracte_from_shape_subscripts(term, variables)
    if term.label in variables['obj_vars']:
        return variables
    variables['obj_vars'][term.label] = term

    for child in term.children:
        if isinstance(child, Placeholder):
            if child.label not in variables['placeholders']:
                variables['placeholders'][child.label] = child
    return variables


@_extracte_variables.register(SumOperator)
def sum_extracte_variables(term: SumOperator, variables: dict):
    for child in term.children:
        variables = _extracte_variables(child, variables)
    for key in term.sum_indices:
        variables = _extracte_variables(key, variables)
        variables = _extracte_variables(key.set, variables)
    return variables


@_extracte_variables.register(Element)
def element_extracte_variables(term: Element, variables: dict):
    return variables


@_extracte_variables.register(ArraySizePlaceholder)
def arraysize_extracte_variables(term: ArraySizePlaceholder, variables: dict):
    for child in term.children:
        variables = _extracte_variables(child, variables)
    return variables
