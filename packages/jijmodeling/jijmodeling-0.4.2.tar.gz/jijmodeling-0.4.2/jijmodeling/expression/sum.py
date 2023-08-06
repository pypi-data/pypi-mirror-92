import copy
from typing import List, Dict, Optional, Union
import numpy as np
from jijmodeling.variables.variable import Element, Range
from jijmodeling.expression.expression import Add, Children, Expression
from jijmodeling.expression.expression import _latex_repr
from jijmodeling.expression.condition import Condition, Equal, GreaterThan
from jijmodeling.expression.condition import GreaterThanEqual, LessThan
from jijmodeling.expression.condition import LessThanEqual, NotEqual
from jijmodeling.variables.set import Set

class SumOperator(Expression):
    r"""Class that represents the sum.

    Args:
        sum_indices (List[Union[str, Element]]): summation index list.
        index_sets (List[Union[Array,
                               Union[int, Placeholder],
                               Tuple[Union[int, Placeholder],
                               Union[int, Placeholder]]]]):
                   index set of each summation indices.
        inner_term (:class: `Expression`): inner term of sum operator.
        condition (Optional[:class: `Condition`]): summation condition.
                                                   default None.

    Attributes:
        sum_indices (List[Element]): summation index list.
        index_sets (List[Union[Array, Union[int, Placeholder],
                         Tuple[Union[int, Placeholder],
                         Union[int, Placeholder]]]]):
                   index set of each summation indices.
        children (:class: `Children`): children=[inner_term].
        condition (:class:`Condition`): conditions of summation.

    Example:
        Create :math:`\sum_{i=0}^n d_i x_i`

        >>> from jijmodeling import PlaceholderArray, BinaryArray, SumOperator
        >>> d = PlaceholderArray('d', dim=1)
        >>> n = d.shape[0]
        >>> x = BinaryArray('x', shape=n)
        >>> SumOperator(sum_indices=['i'], index_sets=[n],
            inner_term=d['i']*x['i'], condition=None)
        Σ_{i}(d[i]x[i])
    """
    def __init__(
            self,
            sum_indices: List[Element],
            inner_term: Expression,
            condition: Optional[Condition] = None) -> None:

        # sum_indices's element is element.
        for e in sum_indices:
            if not isinstance(e, Element):
                raise TypeError('sum_indices is list of `Element` object.')

        self.sum_indices: List[Element] = copy.deepcopy(sum_indices)
        children = [copy.deepcopy(inner_term)]
        super().__init__(children=children)

        self.condition = condition

    @property
    def inner_term(self):
        return self.children[0]

    @property
    def indices(self):
        index_sets = []
        for ind in self.sum_indices:
            index_sets.append(ind.set)
        children: Children = self.children + Children(index_sets)
        remain_indices = [ind for ind in children.indices
                          if ind not in self.sum_indices]
        return remain_indices

    def calc_value(
            self,
            decoded_sol: Dict[str, Union[int, float, np.ndarray, list]],
            placeholder: Dict[str, Union[int, float, np.ndarray, list]],
            fixed_indices: Dict[str, int] = {}) -> Union[float, int]:
        # convert index set values
        # Example:
        # {i: n, t: T} => ind_set_list = [[0,1,...,n-1], [0,...,T-1]]
        ind_set_list = [ind.calc_set_value({}, placeholder, fixed_indices)
                        for ind in self.sum_indices]

        # calculate summation
        value = 0.0
        for ind_set in zip(*ind_set_list):
            # Example:
            # ind_set_list = [[0,1,...,n-1], [0,...,T-1]]
            # zip(*ind_set_list) => [[0, 0], [1, 1],...,[n-1, T-1]]
            sum_index = {ind.label: ind_set[_i]
                         for _i, ind in enumerate(self.sum_indices)}
            sum_index.update(fixed_indices)
            if self.condition is not None:
                if not self.condition.calc_value(
                                        decoded_sol, placeholder, sum_index):
                    continue
            child_val = self.children[0].calc_value(
                                        decoded_sol, placeholder, sum_index)
            value += child_val

        return value

    def __repr__(self):
        repr_str = 'Σ_{'
        for i in self.sum_indices:
            repr_str += str(i) + ', '
        term = self.children[0]
        repr_str = repr_str[:-2] + '}}({})'.format(term.__repr__())
        return repr_str

    def __make_latex__(self):
        ind_str = ""
        ind_end = ""
        for ind, ind_set in zip(self.sum_indices, self.index_sets):
            ind_latex = _latex_repr(ind)
            ind_conds = []
            if len(ind_latex.split(' ')) == 3:
                ind_conds = ind_latex.split(' ')[1:]
                ind_latex = ind_latex.split(' ')[0]
            if isinstance(ind_set, Set):
                ind_str += r"{} \in {}, ".format(
                                            ind_latex, _latex_repr(ind_set))
            elif isinstance(ind_set, tuple):
                iset0 = _latex_repr(ind_set[0])
                ind_end += _latex_repr(ind_set[1]) + '- 1' + ", "
                ind_str += "{} = {}".format(ind_latex, iset0) + ", "
            else:
                ind_end += _latex_repr(ind_set) + '- 1' + ", "
                ind_str += "{} = 0".format(ind_latex) + ", "

            if len(ind_conds) > 0:
                cond_latex = {
                                '!=': r'\neq',
                                '==': '=',
                                '<=': r'\leq',
                                '>=': r'\geq',
                                '<': '<', '>': '>'}
                ind_str = ind_str[:-2]
                ind_str += '({} {} {}), '.format(
                                        ind_latex,
                                        cond_latex[ind_conds[0]],
                                        ind_conds[1])

        if isinstance(self.children[0], Add):
            term = _latex_repr(self.children[0])
        else:
            term = _latex_repr(self.children[0], False)

        return r"\sum_{" + ind_str[:-2] + "}^{"\
               + ind_end[:-2] + " " + str(term)


def convert_index_set(
        index_set,
        decoded_sol: Dict[str, Union[int, float, np.ndarray, list]],
        placeholder: Dict[str, Union[int, float, np.ndarray, list]],
        fixed_indices: Dict[str, int]):

    from jijmodeling.variables.set import Set

    if isinstance(index_set, Set):
        index_set_value = index_set.calc_value(
                            decoded_sol, placeholder, fixed_indices)
    elif isinstance(index_set, Element):
        if isinstance(index_set.set, Set):
            index_set_value = index_set.calc_value(
                                    decoded_sol=decoded_sol,
                                    placeholder=placeholder,
                                    fixed_indices=fixed_indices
                                )
        index_set_value = fixed_indices[index_set.label]
        if not isinstance(index_set_value, (list, np.ndarray)):
            index_set_value = np.arange(0, index_set_value)

    elif not isinstance(index_set, (list, np.ndarray)):
        if not isinstance(index_set, tuple):
            index_set = (0, index_set)
        s_range = [s.calc_value(decoded_sol, placeholder, fixed_indices)
                   if isinstance(s, Expression) else s for s in index_set]
        index_set_value = np.arange(s_range[0], s_range[1])
    # else:
    #     raise TypeError("index_set is tuple or Array, not {}"
    #                     .format(type(index_set)))

    return index_set_value


def Sum(
        indices: Union[dict, Element, List[Union[dict, Element]]],
        term: Expression,
        condition: Optional[Union[Condition, List[Optional[Condition]]]] = None
        ) -> SumOperator:
    r"""[summary]

    Args:
        indices (Union[dict, List[dict]]): [description]
        term (Expression): [description]
        condition (Optional[Union[Condition, List[Condition]]], optional):
        summation conditions. Defaults to None.

    Returns:
        SumOperator: [description]

    Example:
        Create :math:`\sum_{i=0}^n d_i x_i`

        >>> from jijmodeling import PlaceholderArray, BinaryArray, Sum
        >>> d = PlaceholderArray('d', dim=1)
        >>> n = d.shape[0]
        >>> x = BinaryArray('x', shape=n)
        >>> Sum({'i': n}, d['i']*x['i'])
        Σ_{i}(d[i]x[i])
    """

    indices_list: List[dict] = []
    condition_list: List[Optional[Condition]] = []
    if isinstance(indices, list):
        if condition is not None and not isinstance(condition, list):
            raise TypeError("When `indices` is list, " +
                            "`condition` should be list, not {}"
                            .format(type(condition)))
        if condition is None:
            condition = [None for _ in range(len(indices))]
        indices_list, condition_list = indices, condition
    else:
        if isinstance(condition, list):
            raise TypeError("When `indices` is dict, " +
                            "`condition` should be Condition, not list.")
        indices_list = [indices]
        condition_list = [condition]

    if len(indices_list) == 0 or len(condition_list) == 0:
        raise ValueError("input sum_indices and condition")

    # Example
    # indices_list   => [{i: n}, {j: n}]
    # condition_list => [None,  jm.(i, j)]

    sum_term = term
    for index_dict, cond in zip(indices_list[::-1], condition_list[::-1]):
        sum_indices = list(index_dict.keys())
        index_sets = []
        for i, ind in enumerate(sum_indices):

            index_sets.append(index_dict[ind])

            # Example
            # ind => i
            # index_set => n

            # if `ind` is written like 'i != j',
            # it is converted to {i: *} and jm.neq(i, j)
            ind_list = ind.split(' ') if isinstance(ind, str) else []
            if len(ind_list) > 1:
                left_i = Element(ind_list[0], index_sets[-1])
                right_j = Element(ind_list[2], index_sets[-1])
                if ind_list[1] == '==':
                    cond_obj = Equal([left_i, right_j])
                elif ind_list[1] == '<=':
                    cond_obj = LessThanEqual([left_i, right_j])
                elif ind_list[1] == '<':
                    cond_obj = LessThan([left_i, right_j])
                elif ind_list[1] == '>=':
                    cond_obj = GreaterThanEqual([left_i, right_j])
                elif ind_list[1] == '>':
                    cond_obj = GreaterThan([left_i, right_j])
                elif ind_list[1] == '!=':
                    cond_obj = NotEqual([left_i, right_j])
                else:
                    raise ValueError("`{}` cannot use as condition.", ind)
                sum_indices[i] = Element(ind_list[0], index_sets[-1])
                if cond is None:
                    cond = cond_obj
                else:
                    cond = cond & cond_obj

            elif isinstance(ind, str):
                sum_indices[i] = Element(ind, index_sets[-1])

            elif isinstance(ind, Element):
                sum_indices[i] = Element(ind.label, index_sets[-1])

            else:
                TypeError('summation index is str or Element, not {}.'
                          .format(type(ind)))

        sum_term = SumOperator(
            sum_indices=sum_indices,
            inner_term=sum_term,
            condition=cond
        )

    return sum_term
