from typing import NamedTuple
from enum import Enum
import sublime

class FileType(Enum):
  HasFileName = 1
  HasName = 2

class MarkedFile(NamedTuple):
  file_type: FileType
  file_name: str
