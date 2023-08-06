"Python class definitions for SQL INTERVAL types that are based on month"
from __future__ import annotations

from typing import Dict, Tuple, Union
from datetime import date
from ..util import MetaType, mk_nullable, MetaInfo, ValMapper, ValMapperMaker


class MonthsDelta(int):
	_sql_type = '?'

	def sqlrepr(self) -> str:
		s = str(self)
		sign, val = s[0].rstrip(), s[1:]
		return f"INTERVAL {sign}'{val}' {self._sql_type}"

	__repr__ = sqlrepr

	def addto(self, val: Union[date, int, MonthsDelta]) -> Union[date, int, MonthsDelta]:
		"add months to a date or datetime value"
		if isinstance(val, date):
			months = val.year * 12 + val.month + self
			return val.replace(year=months // 12, month=months % 12)

		if isinstance(val, MonthsDelta):
			return self.__class__(int(self) + int(val))

		return int.__add__(self, val)

	__add__ = addto

	def _abs_str(self) -> str:
		raise NotImplementedError()

	def __str__(self) -> str:
		return ('-' if self < 0 else ' ') + self._abs_str()

	@classmethod
	def mk_conv_fn(cls, m: MetaInfo) -> ValMapper:
		return mk_nullable(cls.parse) if m[MetaType("MayBeNull")] else cls.parse

	@classmethod
	def parse(cls, s: str) -> MonthsDelta:
		if s[0] == '-':
			mult = -1
			s = s[1:]
		else:
			mult = 1
			s = s.lstrip()

		return cls(mult * cls._parse_val(s))

	@classmethod
	def _parse_val(cls, s: str) -> int:
		raise NotImplementedError()


class Month(MonthsDelta):
	_sql_type = 'MONTH'

	@property
	def value(self) -> int:
		return int(self)

	def _abs_str(self) -> str:
		return str(abs(self))

	@classmethod
	def _parse_val(cls, s: str) -> int:
		return int(s)


class Year(MonthsDelta):
	_sql_type = 'YEAR'

	@property
	def value(self) -> int:
		return self // 12

	def _abs_str(self) -> str:
		return str(abs(self) // 12)

	@classmethod
	def _parse_val(cls, s: str) -> int:
		return int(s) * 12


class YearToMonth(MonthsDelta):
	_sql_type = 'YEAR TO MONTH'

	@property
	def value(self) -> Tuple[int, int]:
		y, m = self // 12, self % 12
		if y < 0 and m > 0:
			y += 1
			m -= 12
		return (y, m)

	def _abs_str(self) -> str:
		return str(abs(self) // 12) + '-' + format(abs(self) % 12, '02d')

	@classmethod
	def _parse_val(cls, s: str) -> int:
		y, m = s.split('-')
		return int(y) * 12 + int(m)


def register_conv_fn() -> Dict[str, ValMapperMaker]:
	return {'INTERVAL ' + cls._sql_type: cls.mk_conv_fn for cls in [Month, Year, YearToMonth]}
