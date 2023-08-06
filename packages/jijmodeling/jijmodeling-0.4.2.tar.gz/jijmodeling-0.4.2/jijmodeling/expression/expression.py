from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List, Optional, Union, Tuple
import numbers
import copy
import inspect
import numpy as np
import pyqubo
from jijmodeling.expression.serializable import from_serializable, _cls_serializable_validation, to_serializable


FIXED_VAR_TYPE = Dict[str,
                      Union[int, float,
                            Dict[Union[int, Tuple[int, ...]],
                                 Union[int, float]]]]


class Children():
    def __init__(self, values=[]):
        from jijmodeling.variables.variable import Element
        self.values: List[Expression] = [Number(v) if isinstance(v, numbers.Number)
                                         else v for v in values]
        self.indices: List[Element] = []
        self.update_indices()

    def update_indices(self):
        """A method for updating the indices that depends on children when they are updated
        """
        # Collect the un-summarized indices of each child.
        from jijmodeling.variables.variable import Element
        self.indices = []
        for i, child in enumerate(self.values):
            if isinstance(child, Element):
                child_indices = [child]
            elif isinstance(child, str):
                child_indices = [Element(child)]
            elif isinstance(child, Expression):
                child_indices = child.indices
            elif isinstance(child, Number):
                child_indices = []
            else:
                child_indices = []
            ind_labels = [ind.label for ind in self.indices]
            self.indices += [c for c in child_indices
                             if c.label not in ind_labels]

    def __getitem__(self, key: int):
        return self.values[key]

    def __setitem__(self, key: int, value):
        self.values[key] = value
        self.update_indices()

    def append(self, value):
        self.values.append(value)
        self.update_indices()

    def __add__(self, value):
        new_values = self.values + value
        return Children(new_values)

    def __radd__(self, other):
        new_values = other + self.values
        return Children(new_values)

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        for v in self.values:
            yield v

    def __repr__(self) -> str:
        return str(self.values)


class Expression(metaclass=ABCMeta):
    """All component of JijModeling objects inheritance this class.
    This class provide computation rules and each component.

    When serializing, the value of arguments of __init__
    is obtained from the member variable of the object,
    so to make it a serializable Expression object,
    it is necessary to set the member variable that is the same as
    the argument name of __init__ or with underscore (_) prefix variable.
    Be careful about the above when creating a child class.

    Args:
        children (list): children objects list. list of :class:`Expression`,
                         int or float.

    Attributes:
        children (Children): children objects list. list of :class:`Expression`, int or float.
        indices (list[:class:`Expression`]): Index object list.
    """

    def __init__(self, children: list):
        self._children = Children(children)
        self._latex_math: Optional[str] = None

    @property
    def children(self):
        return self._children

    @property
    def indices(self) -> List[Expression]:
        return self.children.indices

    @property
    def is_operatable(self) -> bool:
        return True

    def set_latex(self, latex_math: str):
        """Change LaTeX representation

        Args:
            label (str): Modified LaTeX representation

        Example:
            By default, the LaTeX representation is determined by the child object, 
            but the LaTeX representation will be overwritten if set by this method.

            >>> from jijmodeling import Binary
            >>> x, y = Binary('x'), Binary('y')
            >>> term = x + y
            >>> term._repr_latex_()
            '$x + y$'
            >>> term.set_latex('t')
            >>> term._repr_latex()
            '$t$'
        """
        self._latex_math = latex_math

    def _repr_latex_(self):
        return "${}$".format(self.__latex__())

    def __make_latex__(self):
        return self.__repr__()

    def __latex__(self):
        if self._latex_math is None:
            return self.__make_latex__()
        else:
            return self._latex_math

    def __add__(self, other):
        # TODO: check type of other
        if other == 0:
            return self
        return Add([self, other])

    def __radd__(self, other):
        if other == 0:
            return self
        return Add([other, self])

    def __ladd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self.__add__(-1*other)

    def __rsub__(self, other):
        return Add([other, -1*self])

    def __lsub__(self, other):
        return Add([self, -1*other])

    def __mul__(self, other):
        if other == 1:
            return self
        if other == 0:
            return 0
        return Mul([self, other])

    def __rmul__(self, other):
        return self.__mul__(other)

    def __lmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return Div([self, other])

    def __rtruediv__(self, other):
        return Div([other, self])

    def __pow__(self, other):
        return Power([self, other])

    def __rpow__(self, other):
        return Power([other, self])

    def __mod__(self, other):
        return Mod([self, other])

    def __lt__(self, other):
        from jijmodeling.expression.condition import LessThan
        return LessThan([self, other])

    def __le__(self, other):
        from jijmodeling.expression.condition import LessThanEqual
        return LessThanEqual([self, other])

    def __gt__(self, other):
        from jijmodeling.expression.condition import GreaterThan
        return GreaterThan([self, other])

    def __ge__(self, other):
        from jijmodeling.expression.condition import GreaterThanEqual
        return GreaterThanEqual([self, other])

    def to_serializable(self) -> dict:
        """Convert to serializable object (dict)

        Returns:
            dict: serializable object
        """
        return to_serializable(self)

    def to_pyqubo(
            self,
            placeholder={},
            fixed_variables: FIXED_VAR_TYPE = {},
            index_values: Dict = {}) -> pyqubo.Base:
        """Convert to PyQUBO object

        Args:
            placeholder (dict, optional): A dictionary that contains the values that correspond to each placeholder object. Defaults to {}.
            fixed_variables (dict[tuple, int], optional): A dictionary that stores variables to be fixed. Defaults to {}.
            index_values (dict, optional): Value of each index. Defaults to {}.

        Returns:
            :class:`pyqubo.Base`: Converted PyQUBO object.

        Example:
            >>> from jijmodeling import Binary, Placeholder
            >>> x, y = Binary('x'), Binary('y')
            >>> d = Placeholder('d')
            >>> t = d*x*(y+1)
            >>> t.to_pyqubo({'d': 3}, {'y': 1})
            Binary(x)*Num(3.000000)*Num(2.000000)
            >>> import pyqubo as pyq
            >>> x_p = pyq.Binary('x')
            >>> x_p * 3 * (1+1) == t.to_pyqubo({'d': 3}, {'y': 1})
            True
        """
        from jijmodeling.transpilers import to_pyqubo
        return to_pyqubo(
            self,
            placeholder=placeholder,
            fixed_variables=fixed_variables,
            fixed_indices=index_values
        )

    @abstractmethod
    def calc_value(
            self,
            decoded_sol: Dict[str, Union[int, float, np.ndarray, list]],
            placeholder: Dict[str, Union[int, float, np.ndarray, list]],
            fixed_indices: Dict[str, int] = {}) -> Union[float, int]:
        pass


    @classmethod
    def from_serializable(cls, serializable: dict):
        """Create Expression object from serializable object (dict)

        Args:
            serializable (dict): serializable object which is created by `.to_serializable`

        Returns:
            :class:`jijmodeling.expression.expression.Expression`: Expression object
        """
        _cls_serializable_validation(serializable, cls)
        init_args = inspect.getfullargspec(cls.__init__).args
        init_args_values = {arg: from_serializable(serializable['attributes'][arg]) for arg in init_args if arg != 'self'}
        return cls(**init_args_values)


class Number(Expression):
    def __init__(self, value, dtype='float'):
        self.value = value
        if dtype == 'float':
            self.value = float(value)
        elif dtype == 'int':
            self.valut = int(value)
        self._dtype = dtype
        super().__init__(children=[])

    def calc_value(
            self,
            decoded_sol: Dict[str, Union[int, float, np.ndarray, list]],
            placeholder: Dict[str, Union[int, float, np.ndarray, list]],
            fixed_indices: Dict[str, int] = {}) -> Union[float, int]:
        return self.value

    def __add__(self, other):
        if isinstance(other, Number):
            _value = self.value + other.value
            return Number(_value)
        elif isinstance(other, numbers.Number):
            _value = self.value + other
            return Number(_value)
        return super().__add__(other)

    def __sub__(self, other):
        if isinstance(other, Number):
            _value = self.value - other.value
            return Number(_value)
        elif isinstance(other, numbers.Number):
            return Number(self.value - other)
        return super().__sub__(other)

    def __truediv__(self, other):
        if isinstance(other, Number):
            return Number(self.value/other.value)
        elif isinstance(other, numbers.Number):
            return Number(self.value/other)
        return super().__truediv__(other)

    def __rtruediv__(self, other):
        if isinstance(other, numbers.Number):
            return Number(other/self.value)
        return super().__rtruediv__(other)

    def __mul__(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)
        elif isinstance(other, numbers.Number):
            return Number(self.value * other)
        return super().__mul__(other)

    def __pow__(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value)
        elif isinstance(other, numbers.Number):
            return Number(self.value ** other)
        return super().__pow__(other)

    def __repr__(self) -> str:
        return str(self.value)


class Operator(Expression, metaclass=ABCMeta):
    """The Operator class is an object that represents 
    each operation generated from an operation (ex. +,*,&,...) on Express.
    """
    def __init__(self, children: list):
        _children = []
        for child in children:
            if isinstance(child, Expression):
                if not child.is_operatable:
                    raise ValueError(
                        "`{}` {} is not is_operatable."
                        .format(self.__class__.__name__, child))
                _children.append(child)
            else:
                _children.append(Number(child))

        super().__init__(copy.deepcopy(_children))

    @abstractmethod
    def operation(self, objects: list) -> Any:
        pass

    def calc_value(
            self,
            decoded_sol: Dict[str, Union[int, float, np.ndarray, list]],
            placeholder: Dict[str, Union[int, float, np.ndarray, list]],
            fixed_indices: Dict[str, int] = {}) -> Union[float, int]:
        def convert_value(child):
            if isinstance(child, Expression):
                return child.calc_value(
                            decoded_sol,
                            placeholder,
                            fixed_indices)
            else:
                return child
        value_list = [convert_value(c) for c in self.children]
        return self.operation(value_list)


class Add(Operator):

    def __init__(self, children: list):
        super().__init__([c for c in children if c != 0])

    def __add__(self, other):
        if isinstance(other, Add) and other._latex_math is None and self._latex_math is None:
            return sum([c for c in self.children] + [c for c in other.children])
        return Add([c for c in self.children]+[other])

    def __repr__(self):
        str_repr = ""
        for t in self.children:
            str_repr += t.__repr__() + ' + '
        return str_repr[:-3]

    def __make_latex__(self):
        str_repr = ""
        for t in self.children:
            if isinstance(t, Mul):
                latex_str = _latex_repr(t)
                if latex_str[0] == '-':
                    str_repr = str_repr[:-3]
                str_repr += _latex_repr(t) + ' + '
            elif isinstance(t, Expression):
                str_repr += _latex_repr(t) + ' + '
            else:
                if t < 0:
                    str_repr = str_repr[:-3]
                str_repr += str(t) + ' + '

        return str_repr[:-3]

    def operation(self, objects: list):
        return sum(objects)


class Mul(Operator):

    def __init__(self, children: list):
        if len(children) == 0:
            raise ValueError('children is not empty.')
        else:
            # remove multiplier unit
            _children = [c for c in children if c != 1]
            super().__init__(_children)

    def __mul__(self, other):
        if isinstance(other, Mul) and other._latex_math is None and self._latex_math is None:
            return Mul([c for c in self.children] + [c for c in other.children])
        return Mul([c for c in self.children]+[other])

    def __repr__(self):
        return self.__str_repr__('__repr__')

    def __make_latex__(self):
        latex_str = ""
        coeffs = 1.0
        for child in self.children:
            if isinstance(child, Expression):
                latex_str += _latex_repr(child)
            else:
                coeffs *= child
        if coeffs == -1.0:
            latex_str = '-' + latex_str
        elif coeffs != 1.0:
            latex_str = str(coeffs) + latex_str
        return latex_str

    def __str_repr__(self, func_name):
        str_repr = ""
        for t in self.children:
            if (isinstance(t, Add) and len(t.children) > 1) or isinstance(t, Number):
                str_repr += '({})'.format(eval('t.{}()'.format(func_name)))
            elif isinstance(t, (int, float)):
                str_repr += '{}'.format(str(t))
            else:
                str_repr += t.__repr__()
        return str_repr

    def operation(self, objects: list):
        term = 1
        for obj in objects:
            term = term * obj
        return term


class Div(Operator):
    def __init__(self, children: list):
        # TODO: raise error when divide zero
        # self.children = [numerator, denominator]
        super().__init__(children)

    def __repr__(self):
        return self.__str_repr__('__repr__')

    def __make_latex__(self):

        # The parentheses don't look good in fractions, so I'll remove them.
        latex0 = _latex_repr(self.children[0], with_brakets=False)
        latex1 = _latex_repr(self.children[1], with_brakets=False)
        return "\\frac{{ {} }}{{ {} }}".format(latex0, latex1)

    def __str_repr__(self, func_name):
        str_repr = ""
        def get_str(t):
            if isinstance(t, Add) and len(t.children) > 1:
                return '({})'.format(eval("t.{}()".format(func_name)))
            if isinstance(t, (int, float)):
                return '{}'.format(str(t))
            else:
                return t.__repr__()
        str_repr = get_str(self.children[0])
        str_repr += '/' + get_str(self.children[1])
        return str_repr

    def operation(self, objects):
        return objects[0]/objects[1]


class Power(Operator):
    @property
    def base(self):
        return self.children[0]

    @property
    def exponent(self):
        return self.children[1]

    def operation(self, objects: list):
        exponent = objects[1]
        if isinstance(objects[1], (int, float)):
            if int(objects[1]) == objects[1]:
                exponent = int(objects[1])
        return objects[0]**exponent

    def __repr__(self) -> str:
        return str(self.base) + '^' + str(self.exponent)

    def __make_latex__(self):
        from jijmodeling.expression.sum import SumOperator
        base_str = _latex_repr(self.base, forced_brakets=isinstance(self.base, SumOperator))
        exp_str = _latex_repr(self.exponent)
        return base_str + '^' + exp_str


class Mod(Operator):
    def __repr__(self):
        str_repr = ""

        def get_str(t):
            if isinstance(t, Add) and len(t.children) > 1:
                return '(%s)' % t.__repr__()
            if isinstance(t, (int, float)):
                return '{}'.format(t.__repr__())
            else:
                return t.__repr__()
        str_repr = get_str(self.children[0])
        str_repr += '%' + get_str(self.children[1])
        return str_repr

    def __make_latex__(self):
        str_repr = ""
        str_repr = _latex_repr(self.children[0]) 
        str_repr += '\\bmod ' + _latex_repr(self.children[1])
        return str_repr

    def operation(self, objects: list) -> Any:
        return objects[0] % objects[1]


def _latex_repr(term, with_brakets=True, forced_brakets=False):

    if isinstance(term, Expression) and term._latex_math is not None:
        with_brakets = False


    if (isinstance(term, Operator) and with_brakets) or forced_brakets:
        from jijmodeling.expression.mathfuncs import Log, Absolute
        if isinstance(term, (Log, Absolute, Mul, Div)) and not forced_brakets:
            return term.__latex__()
        bra, ket = r'\left(', r'\right)'
        return bra + term.__latex__() + ket
    elif isinstance(term, Expression):
        exp_str =  term.__latex__()
        if exp_str[0] == ':':
            return 'i_{{' + exp_str[1:] + '}}'
        return exp_str
    else:
        exp_str = str(term)
        if exp_str[0] == ':':
            return 'i_{{' + exp_str[1:] + '}}'
        return exp_str
