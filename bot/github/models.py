from dataclasses import dataclass
from typing import Optional


@dataclass
class Issue:
    number: int
    title: str
    body: str
    url: str
    author: Optional[str]
