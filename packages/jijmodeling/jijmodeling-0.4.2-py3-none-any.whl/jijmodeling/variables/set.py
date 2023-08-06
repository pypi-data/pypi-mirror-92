from jijmodeling.variables.placeholders import Placeholder
import numpy as np
from typing import Union, Dict


class Set(Placeholder):
    def __init__(self, label: str, dim: int, subscripts: list = []):
        shape = tuple([None for _ in range(dim)])
        super().__init__(label, subscripts=subscripts, shape=shape)

    def calc_value(
            self,
            decoded_sol: Dict[str, Union[int, float, np.ndarray, list]],
            placeholder: Dict[str, Union[int, float, np.ndarray, list]],
            fixed_indices: Dict[str, int]) -> Union[float, int]:
        ph_value = placeholder[self.label]
        s_list = [s.calc_value(decoded_sol, placeholder, fixed_indices)
                  for s in self.subscripts]
        for s in s_list:
            ph_value = ph_value[int(s)]
        return ph_value


def List(label: str, dim: int, subscripts: list = []):
    return Set(label, dim, subscripts)
