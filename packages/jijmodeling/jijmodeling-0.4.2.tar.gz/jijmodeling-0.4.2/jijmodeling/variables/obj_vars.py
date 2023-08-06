import copy
from typing import Union, Dict, Tuple
import numpy as np
from jijmodeling.expression.expression import Expression, Number
from jijmodeling.expression.expression import FIXED_VAR_TYPE
from jijmodeling.variables.variable import Variable, Element
from jijmodeling.expression.sum import Sum
import jijmodeling.expression.mathfuncs as jm_func


class ObjectiveVariable(Variable):

    def decode_from_dict(
            self,
            sample: dict,
            placeholder: Dict[str, Union[int, float, np.ndarray, list]],
            fixed_variables: FIXED_VAR_TYPE):

        shape = self._shape_value(placeholder)
        array_value = np.full(shape, fill_value=np.nan)

        def set_value(subscript_values: list):
            if len(subscript_values) == self.dim:
                # When the number of `subscript_values` equals dimension of the array,
                # the elements of the array can finally be accessed.
                # The result of accessing and decoding the elements is stored in `array_value`.
                array_value[tuple(subscript_values)] = self._decode_element(
                                                            sample,
                                                            placeholder,
                                                            fixed_variables,
                                                            subscript_values)
            else:
                # When `len(subscript_values) < self.dim`,
                # the values of all indices to access elements
                # have not yet been determinded.
                # Next, we will determined the value of the next dimension's subscript
                # due to move on to the next recursive step.
                fixed_num = len(subscript_values)
                for i in range(shape[fixed_num]):
                    new_fixed = subscript_values + [i]
                    set_value(new_fixed)
        set_value([])

        return {self.label: array_value}

    def _decode_element(
            self,
            sample: dict,
            placeholder: Dict[str, Union[int, float, np.ndarray, list]],
            fixed_variables: FIXED_VAR_TYPE,
            subscript_values: list):
        label = self.label + ''.join(['[{}]'.format(s) for s in subscript_values])
        if self.label in fixed_variables:
            return np.array(fixed_variables[self.label])[tuple(subscript_values)]
        elif label in sample:
            return sample[label]

        return np.nan


    def _shape_value(
            self,
            placeholder: Dict[str, Union[int, float, np.ndarray, list]] = {}) -> Tuple[int, ...]:
        def script_to_value(obj):
            if isinstance(obj, Expression):
                return int(obj.calc_value({}, placeholder, {}))
            else:
                return obj
        shape = tuple([script_to_value(i) for i in self.subscripts])
        return shape


    def to_binary(self):
        raise NotImplementedError()


class Binary(ObjectiveVariable):
    def __init__(
            self,
            label: str,
            subscripts: list = [],
            shape: Union[list, tuple] = []):
        super().__init__(label, children=[], subscripts=subscripts, shape=shape)

    def __mul__(self, other):
        # x \in {0, 1} => x^2 = x
        if isinstance(other, self.__class__) and other.label == self.label:
            if self.subscripts == other.subscripts:
                return self
        return super().__mul__(other)

    def __pow__(self, other):
        if isinstance(other, Number) and int(other) != other:
            raise ValueError("Binary variable's exponent is only integer.")
        return self.__class__(self.label, self.subscripts.values, shape=self.shape)

    def __rtruediv__(self, other):
        raise ZeroDivisionError("'Binary' can take zero")

    def to_binary(self):
        return self


class Spin(Variable):
    def __init__(self, label: str, subscripts: list=[], shape:Union[list, tuple]=[]):
        super().__init__(label, children=[], subscripts=subscripts, shape=shape)

    def __mul__(self, other):
        # s \in \{1, -1\} => s*s = 1
        if isinstance(other, self.__class__) and other.label == self.label:
            if self.subscripts == other.subscripts:
                return 1
        return super().__mul__(other)

    def to_binary(self):
        binary = Binary(self.label, self.subscripts, self._shape)
        return binary - 1


def shape_validation(obj1: Variable, obj2: Variable):
    shape1 = obj1.shape
    shape2 = obj2.shape
    if obj1.remain_dim != obj2.remain_dim:
        raise ValueError("The dimensions of {}(dim={}) and {}(dim={}) "
                         .format(obj1, obj1.remain_dim,
                                 obj2, obj2.remain_dim) +
                         "should be equal")

    error_msg = "{} and {} should be same shape.".format(obj1, obj2)
    for s1, s2 in zip(shape1[-obj1.remain_dim:], shape2[-obj2.remain_dim:]):
        if type(s1) != type(s2):
            raise ValueError(error_msg)
        if isinstance(s1, Variable):
            if s1.label != s2.label:
                raise ValueError(error_msg)
        else:
            if s1 != s2:
                raise ValueError(error_msg)

class LogEncInteger(ObjectiveVariable):
    r"""Log encoded integer

    .. math::
        x = \frac{\text{upper}-\text{lower}}{2^l} \sum_{l=0}^{\text{bits}-1} 2^l s_l + \text{lower},~(s_l \in \{0, 1\}~ \forall l)

    .. math::
        \text{lower} \leq x \leq \text{upper}
    """
    def __init__(
            self,
            label: str,
            lower: Union[float, Variable],
            upper: Union[float, Variable],
            subscripts: list = [],
            shape: Union[list, tuple] = []):
        if not isinstance(lower, Variable):
            lower = Number(lower, 'int')
        if not isinstance(upper, Expression):
            upper = Number(upper, 'int')
        children = [copy.copy(lower), copy.copy(upper)]
        super().__init__(label, children=children, subscripts=subscripts, shape=shape)

        if isinstance(lower, Variable) and lower.dim != 0:
            shape_validation(lower, self)
        if isinstance(upper, Variable) and upper.dim != 0:
            shape_validation(upper, self)


    @property
    def lower(self) -> Expression:
        return self.children[0]

    @property
    def upper(self) -> Expression:
        return self.children[1]

    def to_binary(self):
        if not self.is_operatable:
            raise ValueError(
                    "`{}` cannot be converted to binary, ".format(self.label) +
                    "because `{}` is not scalar.".format(self.label))
        upper = _get_same_subcripts_property(self, self.upper)
        lower = _get_same_subcripts_property(self, self.lower)
        bits = jm_func.floor(jm_func.log(upper-lower, 2))
        remain_value = upper - lower - (2**bits - 1)

        enc_l = Element(self.label+'_enc_l', set=bits)

        subscripts = self.subscripts
        shape = list(self._shape) + [bits + 1]
        binary = Binary(self.label, subscripts, shape)

        encoded = Sum({enc_l: bits}, 2**enc_l * binary[enc_l])
        encoded += remain_value * binary[bits]
        return encoded + lower


class DisNum(ObjectiveVariable):
    r"""Discreated number class
    
    .. math::
        x = \frac{\text{upper}-\text{lower}}{2^{\text{bits}}-1} \sum_{l=0}^{\text{bits}-1} 2^l s_l + \text{lower},~
        (s_l \in \{0, 1\}~ \forall l)

    .. math::
        \text{lower} \leq x \leq \text{upper}
    """

    def __init__(
            self,
            label: str,
            lower: Union[float, Number] = 0.0,
            upper: Union[float, Number] = 1.0,
            bits: Union[int, Number] = 3,
            subscripts: list = [],
            shape: Union[list, tuple] = []):
        lower = Number(lower) if not isinstance(lower, Expression) else lower
        upper = Number(upper) if not isinstance(upper, Expression) else upper
        bits = Number(bits, 'int') if not isinstance(bits, Expression) else bits
        children = [copy.copy(lower), copy.copy(upper), copy.copy(bits)]

        super().__init__(label, children=children, subscripts=subscripts, shape=shape)

        if not isinstance(lower, Number):
            shape_validation(lower, self)
        if not isinstance(upper, Number):
            shape_validation(upper, self)
        if not isinstance(bits, Number):
            shape_validation(bits, self)

    @property
    def lower(self) -> Expression:
        return self.children[0]

    @property
    def upper(self) -> Expression:
        return self.children[1]

    @property
    def bits(self) -> Expression:
        return self.children[2]

    def to_binary(self):
        if not self.is_operatable:
            raise ValueError(
                    "`{}` cannot be converted to binary, ".format(self.label) +
                    "because `{}` is not scalar.".format(self.label))
        upper = _get_same_subcripts_property(self, self.upper)
        lower = _get_same_subcripts_property(self, self.lower)
        bits = _get_same_subcripts_property(self, self.bits)

        enc_l = Element(self.label + '_enc_l', set=bits)

        coeff = (upper - lower)/(2**bits - 1)

        shape = list(self._shape) + [bits]
        binary = Binary(self.label, self.subscripts, shape)

        encoded = coeff * Sum({enc_l: bits}, 2**enc_l * binary[enc_l])
    
        return encoded + lower


def _get_same_subcripts_property(obj: Variable, prop):
    _prop = copy.copy(prop)
    if isinstance(_prop, Variable) and _prop.dim != 0:
        _prop._subscripts = _prop._subscripts + obj._subscripts
        if _prop.remain_dim != 0:
            raise ValueError("The dimension of {} of {} is not match.".format(_prop, obj))
        return _prop
    else:
        return _prop
