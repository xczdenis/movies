from __future__ import annotations

from dataclasses import dataclass


class Term:
    AND = "AND"
    OR = "OR"


@dataclass
class Filter:
    lookups: dict
    term: str = Term.AND
