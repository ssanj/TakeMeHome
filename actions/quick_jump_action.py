import sublime
from typing import Optional, Dict, Any, List, Callable, Set
from .. import marked_file as MF

class QuickJumpAction:

  def __init__(self, window: sublime.Window, debug: Callable[[str], Any]) -> None:
    self.window = window
    self.debug = debug

  def run(self, view: sublime.View, args: Dict[str, Any], marked: List[MF.MarkedFile]):
    if "index" in args:
      index: int = args["index"]
      return self.quick_jump(view, index, marked)
    else:
      self.debug("index not specified for quick_jump.")

  def quick_jump(self,view: sublime.View, index: int, marked: List[MF.MarkedFile]):
    num_marked = len(marked)
    if num_marked == 0:
      sublime.message_dialog("No files marked.\nPlease mark one or more files to quick jump to it")
      return

    if index > 0 and index <= num_marked:
      jump_mark = marked[index - 1]
      if jump_mark.view.is_valid():
        self.window.focus_view(jump_mark.view)
      else:
        marked.remove(jump_mark)
        sublime.message_dialog(f"View {view} is invalid; can't jump to it.\nIt's been removed from the mark list.")
    else:
      sublime.message_dialog(f"Invalid jump index {index}. Index must be between 1 to number of marked views")
