from numbers import Number
from jijmodeling.variables.placeholders import ArraySizePlaceholder
from jijmodeling.variables.placeholders import Placeholder
from jijmodeling.variables.set import Set
import warnings
import numpy as np


def array_size(s, placeholder):
    if isinstance(s, (int, np.int)):
        return s
    elif isinstance(s, ArraySizePlaceholder):
        if s.array.label in placeholder:
            array_value = placeholder[s.array.label]
        else:
            array_value = s.array.calc_value({}, placeholder, {})
        return np.array(array_value).shape[s.dimension]
    elif isinstance(s, Placeholder):
        return placeholder[s.label]
    else:
        raise TypeError(
                "{}'s shape should be " +
                'int, ArraySizePlaceholder or Placeholder, not {}'
                .format(s, type(s)))


def variables_validation(placeholder: dict, variables: dict):
    array = variables['array']
    ph_values = variables['placeholders']
    for label, var in placeholder.items():
        if isinstance(var, Number):
            pass
        elif isinstance(var, (list, np.ndarray)):
            if label not in ph_values and label not in array:
                warnings.warn('"{}" is not found in your model.'.format(label))
                continue
            if label not in ph_values:
                continue
            var_obj = ph_values[label]
            if isinstance(var_obj, Set):
                continue
            var_shape = tuple([array_size(s, placeholder)
                               for s in var_obj.shape])
            var = np.array(var)
            if var.shape != var_shape:
                raise TypeError('The shape of "{}" should be {}, not {}'
                                .format(label, var_shape, var.shape))
