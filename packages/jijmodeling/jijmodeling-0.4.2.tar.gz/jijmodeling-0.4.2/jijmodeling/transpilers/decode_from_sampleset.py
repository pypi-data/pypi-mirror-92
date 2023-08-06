"""
In this module, we provide functions to decode solutions
from dimod.SampleSet and openjij.Response
into a form that can be easily analyzed.

Ex.
When jijmodeling generates a `Tensor` object to create a QUBO,
a key is assigned to it in the form of "x[0][1]",
but it is difficult to parse the solution with a dictionary type
whose key is this string.
So the function decodes the key of Tensor Variables created
by the object are returned as `numpy.ndarray`,
and variables defined as integers such as `LogEncInt` are encoded as integers.
"""

from jijmodeling.expression.expression import Number, Expression
from typing import Tuple
from functools import singledispatch
from jijmodeling.variables.variable import Variable
from jijmodeling.variables.placeholders import Placeholder
from jijmodeling.variables.placeholders import ArraySizePlaceholder
from jijmodeling.variables.obj_vars import Binary, DisNum, LogEncInteger
from jijmodeling.transpilers.calc_value import calc_value
import numpy as np


def decode_variable(
        term: Variable,
        sample: dict,
        placeholder: dict,
        fixed_variables: dict):
    
    # shape is converted to an `int` value
    shape: Tuple[int, ...] = tuple([convert_to_int(s, placeholder)
                                    for s in term.shape])

    array_value = np.full(shape, np.nan, dtype=np.float)

    # Based on the `self.shape`, we recursively call `set_value`
    # and add the decoded value to the `array_value`.
    def set_value(fixed_indices: list):
        if len(fixed_indices) == len(shape):
            # When the number of `fixed_indices` equals dimension of the array,
            # i.e. len(shape), the elements of the array
            # can finally be accessed.
            # The result of accessing and decoding the elements is
            # stored in `array_value`.
            decoded_value = _decode_var(
                                term,
                                sample,
                                placeholder=placeholder,
                                fixed_variables=fixed_variables,
                                indices=tuple(fixed_indices))
            array_value[tuple(fixed_indices)] = decoded_value
        else:
            # When `len(fixed_indices) < len(shape)`,
            # the values of all indices to access elements
            # have not yet been determinded.
            # Next, we will determined the value of the next dimension's
            # due to move on to the next recursive step.
            fixed_num = len(fixed_indices)
            for i in range(shape[fixed_num]):
                new_fixed = fixed_indices + [i]
                set_value(new_fixed)
    set_value([])
    return {term.label: array_value}


@singledispatch
def _decode_var(
        term: Variable,
        sample: dict,
        placeholder: dict,
        fixed_variables: dict,
        indices: Tuple[int, int, int]):
    pass


def from_fixed_vars(
        term: Variable,
        fixed_variables: dict,
        indices: Tuple[int, int, int]):
    if term.label in fixed_variables:
        if len(term.subscripts) == 0:
            return fixed_variables[term.label]
        else:
            if indices in fixed_variables[term.label]:
                return fixed_variables[term.label][indices]
    return None


@_decode_var.register(Binary)
def decode_binary(
        term: Binary,
        sample: dict,
        placeholder: dict,
        fixed_variables: dict,
        indices: Tuple[int, ...]) -> dict:
    fixed_var = from_fixed_vars(term, fixed_variables, indices)
    if fixed_var is not None:
        return fixed_var
    var_label = term.label + ''.join(['[{}]'.format(ind) for ind in indices])
    return sample.get(var_label, np.nan)


@_decode_var.register(LogEncInteger)
def decode_logencint(
        term: LogEncInteger,
        sample: dict,
        placeholder: dict,
        fixed_variables: dict,
        indices: Tuple[int, ...]):

    fixed_var = from_fixed_vars(term, fixed_variables, indices)
    if fixed_var is not None:
        return fixed_var

    upper: int = convert_to_int(
                    term.upper, placeholder=placeholder, indices=indices)
    lower: int = convert_to_int(
                    term.lower, placeholder=placeholder, indices=indices)
    bits = int(np.log2(upper - lower))
    remain_value = upper - lower - (2**bits - 1)
    var_label = term.label + ''.join(['[{}]'.format(ind) for ind in indices])
    value = 0.0
    for bit in range(bits):
        var_indices = var_label + '[{}]'.format(bit)
        value += 2**bit * sample.get(var_indices, np.nan)

    var_indices = var_label + '[{}]'.format(bits)
    if var_indices not in sample:
        return np.nan
    value += remain_value * sample.get(var_indices, np.nan)
    value = int(value + lower)
    return value


@_decode_var.register(DisNum)
def decode_DisNum(
        term: DisNum,
        sample: dict,
        placeholder: dict,
        fixed_variables: dict,
        indices: Tuple[int, ...]):
    r"""decoded discreated number from binary representation
    Example case:
        y[i] \in R
        Binary representation
            => y[i] = (u-d)/(2^(L-1))sum_{l=0}^{L-1} 2^l y_{i,l} + d
            where u is upperbound and d is lower bound of y[i]

    Args:
        term (DisNum): [description]
        sample (dict): [description]
        placeholder (dict): [description]
        fixed_variables (dict): [description]
        indices (Tuple[int, ...]): [description]

    Returns:
        [type]: [description]
    """

    fixed_var = from_fixed_vars(term, fixed_variables, indices)
    if fixed_var is not None:
        return fixed_var

    upper: int = convert_to_int(
                    term.upper, placeholder=placeholder, indices=indices)
    lower: int = convert_to_int(
                    term.lower, placeholder=placeholder, indices=indices)
    bits: int = convert_to_int(
                    term.bits, placeholder=placeholder, indices=indices)
    label = term.label + ''.join(['[{}]'.format(ind) for ind in indices])
    value = 0.0
    for bit in range(bits):
        var_indices = label + '[{}]'.format(bit)
        value += 2**bit * sample.get(var_indices, np.nan)
    coeff = (upper - lower)/(2**bits-1)
    value = coeff * value + lower
    return value


def convert_to_int(obj, placeholder={}, indices=None) -> int:
    if isinstance(obj, int):
        return obj
    elif isinstance(obj, ArraySizePlaceholder):
        array_value = obj.array.calc_value({}, placeholder, {})
        return np.array(array_value).shape[obj.dimension]
    elif isinstance(obj, Placeholder):
        ph_obj = obj.calc_value({}, placeholder, {})
        if obj.dim > 0:
            return np.array(ph_obj)[tuple(indices)]
        else:
            return ph_obj
    elif isinstance(obj, Number):
        return int(obj.value)
    elif isinstance(obj, Expression):
        return int(obj.calc_value({}, placeholder, {}))
    else:
        raise TypeError('summation index type is ' +
                        'int, ArraySizePlaceholder or Placeholder, ' +
                        'not {} ({}).'.format(type(obj), obj))
