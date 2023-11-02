import sublime
from typing import Optional, Dict, Any, List, Callable
from .. import marked_file as MF
import os

class MarkCurrentFileAction:

  def __init__(self, window: sublime.Window, debug: Callable[[str], Any]) -> None:
    self.window = window
    self.debug = debug

  def run(self, view: sublime.View, args: Dict[str, Any], marked: List[MF.MarkedFile]):
    file_name: Optional[str] = view.file_name()
    name: Optional[str] = view.name()
    if file_name:
      if not marked.__contains__(MF.MarkedFile(MF.FileType.HasFileName, file_name, view)):
        marked.append(MF.MarkedFile(MF.FileType.HasFileName, file_name, view))
        self.add_hint(view, file_name, "Marked")
      else:
        sublime.message_dialog("This file is already marked.")
    elif name:
      if not marked.__contains__(MF.MarkedFile(MF.FileType.HasName, name, view)):
        marked.append(MF.MarkedFile(MF.FileType.HasName, name, view))
        self.add_hint(view, name, "Marked")
      else:
        sublime.message_dialog("This file is already marked.")
    else:
      sublime.message_dialog("Only views that have a file name or name can be marked.")

  def add_hint(self, view: sublime.View, file_name: str, message: str):
    short_file_name = os.path.basename(file_name)
    markup = '''
    <H2>{} {}</H2>
    '''.format(message, short_file_name)

    view.show_popup(
      content = markup,
      max_width=600
    )

