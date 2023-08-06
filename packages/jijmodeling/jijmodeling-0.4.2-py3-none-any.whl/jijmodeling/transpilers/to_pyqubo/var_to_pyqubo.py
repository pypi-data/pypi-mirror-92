from typing import Dict, List, Tuple, Type

import numpy as np
from jijmodeling.variables.variable import Variable, Element
from jijmodeling.variables.placeholders import ArraySizePlaceholder, Placeholder
from jijmodeling.variables.obj_vars import Binary, Spin, DisNum, LogEncInteger, Spin
import pyqubo as pyq


def _var_to_pyqubo(
        term: Variable,
        term_label: str,
        placeholder: dict = {},
        fixed_variables: dict = {},
        fixed_indices: dict = {},
        cache: dict = {}
        ) -> pyq.Base:

    if type(term) == Placeholder:
        return pyq.Placeholder(term_label)
    elif type(term) == Element:
        return fixed_indices[term.label]
    elif type(term) == ArraySizePlaceholder:
        array = term.array.calc_value({}, placeholder, fixed_indices)
        if not isinstance(array, np.ndarray):
            array = np.array(array)
        return array.shape[term.dimension]

    indices = [int(ind.calc_value({}, placeholder, fixed_indices))
               for ind in term.subscripts]

    # Objective variables -----------------------
    if isinstance(term, Binary):
        return pyq.Binary(term_label)
    elif isinstance(term, Spin):
        return pyq.Spin(term_label)

    elif isinstance(term, DisNum):
        binary = term.to_binary()
        return binary.to_pyqubo(placeholder, fixed_variables, fixed_indices)

    elif isinstance(term, LogEncInteger):
        binary = term.to_binary()
        return binary.to_pyqubo(placeholder, fixed_variables, fixed_indices)

    else:
        raise TypeError("`{}` cannot convert pyqubo object."
              .format(term.__class__.__name__))
