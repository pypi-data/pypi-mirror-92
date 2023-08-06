from typing import Union, Dict, Optional, Tuple
import copy
import numpy as np
from jijmodeling.expression.expression import Expression, Number, _latex_repr, Children
from jijmodeling.expression.expression import FIXED_VAR_TYPE


class Variable(Expression):
    def __init__(
            self,
            label: str,
            children: list = [],
            subscripts: list = [],
            shape: Union[list, tuple] = []):
        self._label = label
        for s in subscripts:
            if not isinstance(s, (Expression, int)):
                raise TypeError(
                        "The type of subscripts is list " +
                            "of Element or int. not {}.".format(type(s)))
        self._subscripts = Children(subscripts)

        self._shape = tuple(shape) if isinstance(shape, (list, tuple)) else (shape, )
        super().__init__(children=children)

    @property
    def label(self):
        return self._label

    @property
    def subscripts(self):
        return self._subscripts

    @property
    def dim(self) -> int:
        return len(self.shape)

    @property
    def remain_dim(self) -> int:
        return len(self.shape) - len(self.subscripts)

    @property
    def is_operatable(self) -> bool:
        return len(self.subscripts) == self.dim

    @property
    def indices(self):
        return self.children.indices + self.subscripts.indices

    @property
    def shape(self):
        # None shape size convert to ArraySizePlaceholder
        from jijmodeling.variables.placeholders import ArraySizePlaceholder
        shape = []
        for i, s in enumerate(self._shape):
            if s is None:
                array_size = ArraySizePlaceholder(
                    label=self.label + '_shape_%d' % i,
                    array=self,
                    array_dim=len(self._shape),
                    dimension=i
                )
                shape.append(array_size)
            else:
                shape.append(s)
        return shape

    def length(self):
        if self.remain_dim == 0:
            raise ValueError("{} is scalar.".format(self))
        return self.shape[0]

    def calc_value(
            self,
            decoded_sol: Dict[str, Union[int, float, np.ndarray, list]],
            placeholder: Dict[str, Union[int, float, np.ndarray, list]],
            fixed_indices: Dict[str, int] = {}) -> Union[float, int]:

        if self.label in decoded_sol:
            sol = np.array(decoded_sol[self.label])
        elif self.label in placeholder:
            sol = np.array(placeholder[self.label])
        elif self.label in fixed_indices:
            return fixed_indices[self.label]
        else:
            raise ValueError('"{}" is not found in placehoder and solution.'
                             .format(self.label))

        if self.dim != len(sol.shape):
            raise ValueError("{}'s dimension mismatch. ".format(self.label)
                             + "{} expect {}-dim array. not {}-dim."
                             .format(self.label,
                                     self.dim, len(sol.shape)))

        def subscript_to_value(obj):
            if isinstance(obj, Expression):
                _value = obj.calc_value(
                            decoded_sol, placeholder, fixed_indices)
                _value = np.array(_value, dtype=int)
                return _value
            else:
                return obj

        s_values = [subscript_to_value(s) for s in self.subscripts]
        try:
            value = np.array(sol)[tuple(s_values)]
        except IndexError as e:
            raise ValueError(
                    "{}.\nThe shape of '{}' is {}, "
                    .format(e, self.label, np.array(sol).shape) +
                    "but access indices are {}."
                    .format(s_values))

        if value is np.nan:
            return 0
        return value

    def decode_from_dict(
            self,
            sample: dict,
            placeholder: Dict[str, Union[int, float, np.ndarray, list]],
            fixed_variables: FIXED_VAR_TYPE):
        raise NotImplementedError("need `decode_from_dict`")

    def __repr__(self) -> str:
        subscripts_str = ''
        for i in self.subscripts:
            subscripts_str += '[%s]' % i
        return self.label + subscripts_str

    def __make_latex__(self):
        subscripts_str = ','.join([_latex_repr(i, False) for i in self.subscripts])
        return self.label + "_{" + subscripts_str + "}"

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Variable):
            return False
        if o.__class__ != self.__class__:
            return False
        if o.label != self.label or o.dim != self.dim:
            return False

        for s, os in zip(self.subscripts, o.subscripts):
            if isinstance(s, Variable):
                if not isinstance(os, Variable):
                    return False
                if s != o:
                    return False
            elif isinstance(s, Expression):
                if s.__class__ != os.__class__:
                    return False
                elif str(s) != str(os):
                    return False
        return True

    def __getitem__(self, key):
        if not isinstance(key, tuple):
            key = (key, )
        if self.remain_dim < len(key):
            raise ValueError("{} is {}-dimentional array, not {}-dim."
                             .format(self, self.remain_dim, len(key)))
        subscripts = []
        summation_index = []
        for i, k in enumerate(key):
            if isinstance(k, slice):
                # for syntaxsugar x[:]
                # If a slice [:] is used for a key,
                # it is syntax-sugar that represents Sum
                # and the index is automatically created and assigned.
                # i.e. x[:] => Sum({':x_0': n}, x[':x_0'])
                # This created index is stored in summation_index
                # as Sum will be added later.
                element_set = self.shape[i]
                key_element = Element(':{}_{}'
                                      .format(self.label, i), element_set)
                summation_index.append((i, key_element))
            elif isinstance(k, str):
                element_set = self.shape[i]
                key_element = Element(k, element_set)
            elif isinstance(k, Expression):
                key_element = k
            elif isinstance(k, int):
                key_element = Number(k, dtype='int')
            else:
                raise TypeError(
                        'subscripts of {} is `str`, '.format(type(k)) +
                        '`int` or `Expression`, not {}.')
            subscripts.append(key_element)

        if self.remain_dim < len(subscripts):
            raise ValueError(
                    "The dimension of {} is {},".format(self, self.dim) +
                    " but the number of subscripts" +
                    " you have accesed is {}".format(len(subscripts)))

        variable = copy.copy(self)
        variable._subscripts = self.subscripts + Children(subscripts)

        from jijmodeling.expression.sum import Sum
        for i, ind in summation_index:
            variable = Sum({ind: self.shape[i]}, variable)

        return variable


class Range(Variable):
    def __init__(self, lower, upper):
        if isinstance(lower, Variable):
            if lower.remain_dim > 0:
                raise ValueError("Range's lower only scalar, " +
                                 "not {}-dim array ({})."
                                 .format(lower.remain_dim, lower))
        if isinstance(upper, Variable):
            if upper.remain_dim > 0:
                raise ValueError("Range's upper only scalar, " +
                                 "not {}-dim array ({})."
                                 .format(upper.remain_dim, upper))

        children = [lower, upper]
        subscripts = []
        shape = None
        label = 'range_' + str(lower) + '_' + str(upper)
        super().__init__(
                label,
                children=children,
                subscripts=subscripts, shape=shape)

    @property
    def lower(self):
        return self.children[0]

    @property
    def upper(self):
        return self.children[1]

    def calc_value(
            self,
            decoded_sol: Dict[str, Union[int, float, np.ndarray, list]],
            placeholder: Dict[str, Union[int, float, np.ndarray, list]],
            fixed_indices: Dict[str, int]) -> Union[float, int]:
        lower = self.lower.calc_value(decoded_sol, placeholder, fixed_indices)
        upper = self.upper.calc_value(decoded_sol, placeholder, fixed_indices)
        return np.arange(lower, upper)


class Element(Variable):
    def __init__(
            self,
            label: str,
            set: Union[Tuple, Variable]):
        
        if isinstance(set, tuple):
            _set = Range(set[0], set[1])
        elif isinstance(set, Range):
            _set = set
        elif isinstance(set, Variable) and set.remain_dim > 0:
            _set = set
        else:
            _set = Range(0, set)

        shape = []
        if _set.remain_dim == 0:
            raise ValueError(
                    "`{}` is scalar, so cannot assign a set of {}"
                    .format(set, self.label))
        remain_dim = _set.remain_dim
        if remain_dim == 1:
            shape = []
        else:
            shape = list(_set.shape)[-(remain_dim-1):]

        super().__init__(label, children=[_set], subscripts=[], shape=shape)

    @property
    def set(self):
        return self.children[0]

    def __hash__(self) -> int:
        return self.label.__hash__()

    def calc_value(
            self,
            decoded_sol: Dict[str, Union[int, float, np.ndarray, list]],
            placeholder: Dict[str, Union[int, float, np.ndarray, list]],
            fixed_indices: Dict[str, int]) -> Union[float, int]:

        if self.label in fixed_indices:
            return fixed_indices[self.label]

        set_value = self.calc_set_value(
                        decoded_sol,
                        placeholder,
                        fixed_indices)
        s_value = [s.calc_value(decoded_sol, placeholder, fixed_indices)
                   for s in self.subscripts]
        value = set_value
        for s in s_value:
            value = value[int(s)]
        return value

    def calc_set_value(
            self,
            decoded_sol,
            placeholder,
            fixed_indices):
        return self.set.calc_value(decoded_sol, placeholder, fixed_indices)

    def is_scalar(self):
        return self.dim == 0
