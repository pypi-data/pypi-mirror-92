from jijmodeling.expression.expression import Expression
from typing import Union, Optional
from jijmodeling.variables.obj_vars import Binary, DisNum, LogEncInteger
from jijmodeling.variables.placeholders import Placeholder


def BinaryArray(label: str, shape: Union[int, tuple, Placeholder]) -> Binary:
    return Binary(label, shape=shape)


def PlaceholderArray(
        label: str,
        dim: Optional[int] = None,
        shape: Union[int, tuple, Placeholder] = None) -> Placeholder:
    if shape is None and isinstance(dim, int):
        _shape = tuple(None for _ in range(dim))
        return Placeholder(label, shape=_shape)
    elif shape is not None:
        shape = (shape, ) if isinstance(shape, int) else shape
        return Placeholder(label, shape=shape)
    else:
        raise ValueError("Input shape or dim.")


def DisNumArray(
        label: str,
        shape,
        lower: Union[float, Expression] = 0.0,
        upper: Union[float, Expression] = 1.0,
        bits: Union[float, Expression] = 3) -> DisNum:
    return DisNum(label, shape=shape, lower=lower, upper=upper, bits=bits)


def LogEncIntArray(
        label: str,
        shape,
        lower: Union[int, Expression],
        upper: Union[int, Expression]) -> LogEncInteger:
    return LogEncInteger(label, shape=shape, lower=lower, upper=upper)
