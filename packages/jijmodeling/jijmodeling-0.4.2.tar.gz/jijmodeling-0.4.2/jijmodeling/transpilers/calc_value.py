from jijmodeling.expression.expression import Expression
from typing import Dict, Union
import numpy as np


def calc_value(
        term,
        decoded_sol: Dict[str, Union[int, float, np.ndarray, list]],
        placeholder: Dict[str, Union[int, float, np.ndarray, list]],
        fixed_indices: Dict[str, int] = {}) -> Union[float, int]:

    if isinstance(term, Expression):
        return term.calc_value(
                    decoded_sol=decoded_sol,
                    placeholder=placeholder,
                    fixed_indices=fixed_indices)
    else:
        return term
