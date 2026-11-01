from dataclasses import dataclass
from collections import UserList

@dataclass
class Source:
    id: int
    source_name: str
    source_url: str | None


class SourceList(UserList):
    def get_by_name(self, name) -> Source:
        res, = [i for i in self if i.source_name == name]
        return res