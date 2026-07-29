from dataclasses import dataclass
from pathlib import Path


@dataclass
class FileRecord:
    path: str
    name: str
    extension: str
    size_bytes: int
    modified_at: float
    parent: str
