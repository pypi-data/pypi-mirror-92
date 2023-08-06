"DB API connect method"
from typing import Any
from teradatasql import TeradataConnection, TeradataCursor
from .excp import fix_excp
from .data import fix_data


@fix_data
class TDDBApiCursor(TeradataCursor):
	"Cursor object that modifies data and exception types"
	nextset = fix_excp(TeradataCursor.nextset)
	close = fix_excp(TeradataCursor.close)
	executemany = fix_excp(TeradataCursor.executemany)

	__iter__ = TeradataCursor.__iter__
	__next__ = fix_excp(TeradataCursor.__next__)
	__enter__ = TeradataCursor.__enter__
	__exit__ = TeradataCursor.__exit__


class TDDBApiConnection(TeradataConnection):
	"Customize class with overriden connection parmeters and cursor method"
	def __init__(self, *args: Any, **kwargs: Any):
		kwargs["fake_result_sets"] = "true"
		super().__init__(*args, **kwargs)

	def cursor(self) -> TDDBApiCursor:
		"Return overriden cursor object"
		return TDDBApiCursor(self)

	close = fix_excp(TeradataConnection.close)

	__enter__ = TeradataConnection.__enter__
	__exit__ = TeradataConnection.__exit__


@fix_excp
def connect(*args: Any, **kwargs: Any) -> TDDBApiConnection:
	"Return connection object with overriden methods"
	return TDDBApiConnection(*args, **kwargs)
