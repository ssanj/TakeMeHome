from typing import NamedTuple
import sublime

class MarkedFile(NamedTuple):
  file_name: str
  view: sublime.View
