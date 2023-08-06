import copy
from jijmodeling.expression.condition import Condition, Equal
from jijmodeling.expression.condition import GreaterThan, GreaterThanEqual
from jijmodeling.expression.condition import LessThanEqual, LessThan
from jijmodeling.variables.placeholders import Placeholder
from jijmodeling.expression.expression import Expression, _latex_repr
from jijmodeling.expression.sum import Sum
from typing import Dict, Optional, Union, List
import numpy as np


class Penalty(Expression):
    def __init__(self, label: str, penalty_term, with_multiplier: bool = True):
        self.label = label
        self.penalty_term = penalty_term
        self.with_multiplier = with_multiplier
        if with_multiplier:
            # multiple placeholder (for the Lagrange multiplier)
            pl_mul = Placeholder(self.label)
            pl_mul.set_latex('\\lambda_{{\\mathrm{{{}}}}}'.format(self.label))
            child_term = pl_mul * penalty_term
        else:
            child_term = penalty_term
        super().__init__([child_term])

    @property
    def total_term(self) -> Expression:
        return self.children[0]

    def __latex__(self):
        return _latex_repr(self.children[0], with_brakets=False)

    def calc_value(
            self,
            decoded_sol: Dict[str, Union[int, float, np.ndarray, list]],
            placeholder: Dict[str, Union[int, float, np.ndarray, list]],
            fixed_indices: Dict[str, int]) -> Union[float, int]:

        return self.total_term.calc_value(
                    decoded_sol,
                    placeholder,
                    fixed_indices)


class Constraint(Expression):
    """
    Attributes:
        label (str): label of constraint.
        term (:obj:`Condition`): Condition representation of constraint.
        condition (str): '=='
        constant (int/float): 0.0
        with_penalty (bool): add penalty to QUBO. Defaults to True.
        with_mul (bool): penalty with lagrange multiplier. Defaults to True.
        slack_range (tuple, None): the range of slack variable. Defaults to None.
        slack_dtype (str): data type of slack variable. 'int' or 'float'. Defaults to 'int'.
    """
    def __init__(
            self,
            label: str,
            term: Union[Condition, Expression],
            condition='==', constant=0,
            with_penalty: bool = True,
            with_mul: bool = True,
            slack_range: Optional[tuple] = None,
            slack_dtype: str = 'int'):
        r"""[summary]

        Args:
            label (str): label of constraint.
            term (:obj:`Condition`/:obj:`Expression`): expression of constarint.
            condition (str, optional): condition. Defaults to '=='.
            constant (int, optional): right hand constant of condition. Defaults to 0.
            with_penalty (bool, optional): add penalty to QUBO. Defaults to True.
            with_mul (bool, optional): penalty with lagrange multiplier. Defaults to True.
            slack_range (tuple, None): the range of slack variable. Defaults to None.
            slack_dtype (str): data type of slack variable. 'int' or 'float'. Defaults to 'int'.

        Raises:
            ValueError: [description]
        
        Example:
            create :math: `\left(\sum_{i=0}^n x_{i,t}-1\right)^2=0,~\forall_{t \in \{0, T-1\}, t > 5}`
            >>> from jijmodeling import BinaryArray, Constraint, Element, Placeholder
            >>> t = Element('t')
            >>> T = Placeholder('T')
            >>> x = BinaryArray('x', shape=(T, T))
            >>> Constraint('const1', (x[:, t]-1)**2, '==', 0)

            create :math: `\sum_{i=0}^n x_{i,t} \leq C_t,~\forall_{t \in \{0, T-1\}, t > 5}`
            >>> from jijmodeling import BinaryArray, Constraint, Element, Placeholder
            >>> t = Element('t')
            >>> T = Placeholder('T')
            >>> C = PlaceholderArray('C')
            >>> x = BinaryArray('x', shape=(T, T))
            >>> Constraint('const1', x[:, t] <= C[t]).forall({t: T}, t > 5)
        """
        self.label = label
        self.with_penalty = with_penalty
        self.with_mul = with_mul

        if isinstance(term, Condition):
            # any constraint convert to left less than right
            if isinstance(term, GreaterThan):
                _term = LessThan(term.children[::-1])
            elif isinstance(term, GreaterThanEqual):
                _term = GreaterThanEqual(term.children[::-1])
            else:
                _term = term
            if _term.children[1] != 0:
                _term = _term.__class__([term.children[0]-term.children[1], 0])
        else:
            # convert Condition class
            if condition == '==':
                _term = Equal([term-constant, 0])
            elif condition == '<':
                _term = LessThan([term-constant, 0])
            elif condition == '<=':
                _term = LessThanEqual([term-constant, 0])
            else:
                raise ValueError('condition only support ==, <= or <')

        pena_term = _term.children[0]
        if with_penalty:
            self._penalty = Penalty(label, pena_term, with_multiplier=with_mul)
            super().__init__([self._penalty])
        else:
            self._penalty = None
            super().__init__([term])

        self.term: Condition = _term
        if isinstance(_term, Equal):
            self.condition = '=='
        elif isinstance(_term, LessThan):
            self.condition = '<'
        elif isinstance(_term, LessThanEqual):
            self.condition = '<='
        self.constant = 0.0

        self.slack_range = slack_range
        self.slack_dtype = slack_dtype

    def forall(
            self,
            forall_indices: Union[Dict, List[Dict]],
            forall_conditions: Optional[Union[Condition, List]] = None):
        r"""

        Example:
            create :math: `\left(\sum_{i=0}^n x_{i,t}-1\right)^2=0,~\forall_{t \in \{0, T-1\}, t > 5}`
            >>> from jijmodeling import BinaryArray, Constraint, Element, Placeholder
            >>> t = Element('t')
            >>> T = Placeholder('T')
            >>> x = BinaryArray('x', shape=(T, T))
            >>> Constraint('const1', (x[:, t]-1)**2, '==', 0).forall({t: (0, T)}, t > 5)
        """
        if not isinstance(forall_indices, list):
            forall_indices = [forall_indices]
        if not isinstance(forall_conditions, list):
            forall_conditions = [forall_conditions]

        term = copy.deepcopy(self)

        if len(forall_conditions) == 0 or len(forall_conditions) == 0:
            raise ValueError("input indices and conditions.")

        for i, indices in enumerate(forall_indices):
            condition = forall_conditions[i] if len(forall_conditions) > i else None
            term = Sum(indices, term, condition)

        return term

    @property
    def penalty(self):
        if self.with_penalty:
            return self._penalty
        else:
            return self.term

    def calc_value(
            self,
            decoded_sol: Dict[str, Union[int, float, np.ndarray, list]],
            placeholder: Dict[str, Union[int, float, np.ndarray, list]],
            fixed_indices: Dict[str, int]) -> Union[float, int]:
        term_value = self.penalty.calc_value(decoded_sol, placeholder, fixed_indices)
        if self.condition == '==' and term_value == self.constant:
            return 0.0
        elif self.condition == '<=' and term_value <= self.constant:
            return 0.0
        else:
            return term_value - self.constant
