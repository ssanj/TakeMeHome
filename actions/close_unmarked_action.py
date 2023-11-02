import sublime
from typing import Optional, Dict, Any, List, Callable, Set
from .. import marked_file as MF

class CloseUnmarkedAction:

  def __init__(self, window: sublime.Window, debug: Callable[[str], Any]) -> None:
    self.window = window
    self.debug = debug

  def run(self, view: sublime.View, args: Dict[str, Any], marked: List[MF.MarkedFile]):
    if len(marked) == 0:
      sublime.message_dialog("No files marked.\nPlease mark one or more files to close unmarked views")
      return

    if sublime.yes_no_cancel_dialog("Close all unmarked views?") == sublime.DIALOG_YES:
      self.close_other_views(marked)

  def close_other_views(self, marked: List[MF.MarkedFile]):
    all_views: Set[sublime.View] =  set(self.window.views())
    marked_views = [m.view for m in marked]
    views_to_close = all_views.difference(marked_views)

    for v in views_to_close:
      v.close()
