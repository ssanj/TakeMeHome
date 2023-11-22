import sublime
from typing import Optional, Dict, Any, List, Callable, Tuple, Set
from .. import marked_file as MF
from ..util import file_util as FU
from functools import partial
import os

class ReorderMarksAction:

  def __init__(self, window: sublime.Window, debug: Callable[[str], Any]) -> None:
    self.window = window
    self.debug = debug
    self.file_util = FU.FileUtil()

  def run(self, view: sublime.View, args: Dict[str, Any], marked: List[MF.MarkedFile]):
    if marked:
      relative_filename: Callable[[str], str] = partial(self.file_util.get_project_relative_filename, self.window)
      relative_filename_marked_dict: Dict[str, MF.MarkedFile] = dict([(relative_filename(m.file_name), m) for m in marked])

      input_lines = ",".join(relative_filename_marked_dict.keys())
      on_reordered = partial(self.reorder_selection, marked, relative_filename_marked_dict)
      self.window.show_input_panel("reorder", input_lines, on_done=on_reordered, on_cancel=None, on_change=None)
    else:
      sublime.message_dialog("No marks to edit. Please add a few marks and then choose to reorder")

  def reorder_selection(self, marked: List[MF.MarkedFile], old_hash: Dict[str, MF.MarkedFile], input: str):

    # Also remove any duplicate names?
    # Only return matching marked files; this removes new files or typos etc
    new_order: List[Tuple[str, MF.MarkedFile]] = [(f.strip(), old_hash[f.strip()]) for f in input.split(",") if len(f.strip()) > 0 if f.strip() in old_hash]
    old_mark_count = len(old_hash.keys())
    new_mark_count = len(new_order)

    # option1: We have the same number of marks old and new
    # option2: Marks have been slated for removal, confirm with the user that that's what they intended.
    # We don't have to cater for when we have new files in the input as we filter it out when creating `new_order`
    supplied_keys = set([f for (f, _) in new_order])
    existing_keys = set(old_hash.keys())
    to_be_removed = existing_keys.difference(supplied_keys)
    to_be_removed_files = "\n  ".join(to_be_removed)

    if old_mark_count == new_mark_count or (old_mark_count > new_mark_count and sublime.yes_no_cancel_dialog(f"Close the following marks?\n{to_be_removed_files}") == sublime.DIALOG_YES):
      # assume the content is valid. Check in another iteration
      new_marked: List[MF.MarkedFile] = []
      for (_, mark) in new_order:
        # can we parse not validate? We already checked this above so it *shouldn't* fail
        new_marked.append(mark)

      marked.clear()
      marked.extend(new_marked)

      sublime.message_dialog(f"Order changed")
