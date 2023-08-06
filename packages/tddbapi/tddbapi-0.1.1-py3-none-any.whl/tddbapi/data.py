"Data fixing decorator and ancilliary data conversion functions"
from collections import defaultdict
from contextlib import AbstractContextManager
from json import loads
from typing import (Any, Dict, Iterator, List, Optional, Protocol, Sequence,
					Type, TypeVar)

from .interval import months, seconds
from .util import MetaInfo, ValMapper, ValMapperMaker, mk_nullable, MetaType

conv_fn: Dict[str, ValMapperMaker] = defaultdict(lambda: lambda _: lambda x: x)


class Cursor(AbstractContextManager, Iterator, Protocol):
	def __init__(self, *args: Any, **kwargs: Any): ...
	def fetchone(self) -> Sequence[Any]: ...
	def nextset(self) -> Optional[bool]: ...
	def execute(self, *args: Any, **kwargs: Any) -> Any: ...
	def executemany(self, *args: Any, **kwargs: Any) -> Any: ...


def char_sizer(m: MetaInfo) -> ValMapper:
	"returns a function that truncates not-None input string paramenter larger than passed size"
	size: int = m[MetaType("MaxCharacterCount")]

	def wrapper(s: str) -> str:
		return s[:size]

	return mk_nullable(wrapper) if m[MetaType("MayBeNull")] else wrapper


T = TypeVar('T')
conv_fn["CHAR"] = char_sizer
conv_fn.update(months.register_conv_fn())
conv_fn.update(seconds.register_conv_fn())


def fix_data(cls: Type[Cursor]) -> Type[Cursor]:
	"Class Decorator that applies data conversion functions on cursor data"
	class Wrapper(cls):
		def __init__(self, *args: Any, **kwargs: Any):
			super().__init__(*args, **kwargs)
			self._meta: Optional[List[MetaInfo]] = None
			self._fmap: Optional[List[ValMapper]] = None  # A list of data conversion functions for each column in the result set

		def _readmeta(self) -> Any:
			self._meta = self._fmap = None
			meta = super().fetchone()
			if meta is not None and len(meta) >= 8:
				self._meta = loads(meta[7])
				if self._meta is not None:
					self._fmap = [conv_fn[m[MetaType("TypeName")]](m) for m in self._meta]

			super().nextset()

		def executemany(self, *args: Any, **kwargs: Any) -> Any:
			xs = super().executemany(*args, **kwargs)
			self._readmeta()
			return xs

		def nextset(self) -> Optional[bool]:
			self._readmeta()
			return super().nextset()

		def __next__(self) -> List[Any]:
			row = super().__next__()
			if self._fmap is None or not row:
				return row

			return [f(v) for f, v in zip(self._fmap, row)]

		__iter__ = cls.__iter__
		__enter__ = cls.__enter__
		__exit__ = cls.__exit__

	return Wrapper
