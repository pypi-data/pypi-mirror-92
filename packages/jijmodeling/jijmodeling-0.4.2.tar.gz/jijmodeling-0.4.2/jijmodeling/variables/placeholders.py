from jijmodeling.expression.expression import Children
from typing import Union, Dict
import numpy as np
from jijmodeling.variables.variable import Variable


class Placeholder(Variable):
    def __init__(
            self,
            label: str,
            subscripts: list = [],
            shape: Union[list, tuple] = []):
        super().__init__(
                label,
                children=[],
                subscripts=subscripts,
                shape=shape)


class ArraySizePlaceholder(Placeholder):
    def __init__(
            self,
            label: str,
            array: Variable,
            array_dim: int,
            dimension: int,
            subscripts: list = []):
        if not isinstance(array, Variable):
            raise TypeError("array of ArraySizePlaceholder " +
                            "is Variable, not {}."
                            .format(type(array)))
        self.array_dim = array_dim
        self.dimension = dimension
        shape = [None for _ in range(len(subscripts))]
        super().__init__(label, subscripts=subscripts, shape=shape)
        self._children = Children([array])

    @property
    def array(self):
        return self.children[0]

    def __make_latex__(self):
        dim_str = str(self.dimension + 1)
        return "|" + self.array.label + "|_" + "{" + dim_str + "}"

    def calc_value(
            self,
            decoded_sol: Dict[str, Union[int, float, np.ndarray, list]],
            placeholder: Dict[str, Union[int, float, np.ndarray, list]],
            fixed_indices: Dict[str, int]) -> Union[float, int]:
        array_value = self.array.calc_value(
                        decoded_sol,
                        placeholder,
                        fixed_indices)
        if isinstance(array_value, np.ndarray):
            return array_value.shape[self.dimension]

        list_value = array_value
        for s in self.subscripts:
            s_value = s.calc_value(decoded_sol, placeholder, fixed_indices)
            list_value = list_value[int(s_value)]
        return len(list_value)
