"""
A port of a variety of tools from Josiah Wolf Oberholtzer's ``Consort`` to `Abjad 3.1`.
"""
from .LogicalTieCollection import LogicalTieCollection
from .RatioPartsExpression import RatioPartsExpression
from .TimespanCollection import TimespanCollection
from .TimespanSimultaneity import TimespanSimultaneity
from .iterate_nwise import iterate_nwise

__all__ = [
    "LogicalTieCollection",
    "RatioPartsExpression",
    "TimespanCollection",
    "TimespanSimultaneity",
    "iterate_nwise",
]
