from jijmodeling.expression.expression import Expression, Add, Number
from jijmodeling.variables.obj_vars import ObjectiveVariable


def has_class(term: Expression, cls: type) -> bool:
    if isinstance(term, cls):
        return True
    for child in term.children:
        result = has_class(child, cls)
        if not result:
            continue
        return result
    return False


def extract_constant(term: Expression):
    if isinstance(term, Number):
        return term.value
    elif not isinstance(term, Expression):
        return term
    value = 0.0
    if isinstance(term, Add):
        for child in term.children:
            value += extract_constant(child)
    if not has_class(term, ObjectiveVariable):
        value += term
    return value
