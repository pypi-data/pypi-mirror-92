from __future__ import annotations

from typing import Callable, Optional, Any, Dict, TypeVar, NewType, Union

T = TypeVar('T')
U = TypeVar('U')
MetaType = NewType('MetaType', str)

MetaInfo = Dict[MetaType, Any]                       # JSON parsed dictionary containing metadata
ValMapperReqd = Callable[[T], U]                     # A function that maps a value of type T to another value of type U
ValMapperOpt = Callable[[Optional[T]], Optional[U]]  # A function that maps an optional value of type T to another value of type U
ValMapper = Union[ValMapperReqd, ValMapperOpt]
ValMapperMaker = Callable[[MetaInfo], ValMapperReqd]  # A function that accepts col meta data and retuns a ValMapper function


def mk_nullable(f: ValMapperReqd) -> ValMapperOpt:
	"returns a wrapped function that returns None if the first arg is None, otherwise call the wrapped function"
	def wrapper(arg: Optional[T]) -> Optional[U]:
		return None if arg is None else f(arg)
	return wrapper
