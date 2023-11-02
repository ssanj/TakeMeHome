import sublime
from typing import Optional, Dict, Any, List, Callable
from . import marked_file as MF

class ClearMarksAction:

  def __init__(self, window: sublime.Window, debug: Callable[[str], Any]) -> None:
    self.window = window
    self.debug = debug

  def run(self, view: sublime.View, args: Dict[str, Any], marked: List[MF.MarkedFile]):
    if len(marked) == 0:
      sublime.message_dialog("No files marked to clear.\nPlease mark one or more files to clear them here.")
      return

    if sublime.yes_no_cancel_dialog("Remove all marks?") == sublime.DIALOG_YES:
      marked.clear()
