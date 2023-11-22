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
    marked_views = [m.file_name for m in marked]
    all_views_hash: Dict[str, sublime.View] = dict([(self.get_valid_name(v), v) for v in self.window.views()])

    all_views: Set[str] =  set(all_views_hash.keys())
    views_to_close = all_views.difference(marked_views)

    for filename in views_to_close:
      if filename in all_views_hash:
        v = all_views_hash[filename]
        v.close()

  def get_valid_name(self, view: sublime.View) -> str:
    file_name: Optional[str] = view.file_name()
    name: Optional[str] = view.name()

    if file_name:
      return file_name
    elif name:
      return name
    else:
      return "[Untitled]"
