import sublime
from typing import Optional, Dict, Any, List, Callable, Tuple
from .. import marked_file as MF
from functools import partial
import os

class ReorderMarksAction:

  def __init__(self, window: sublime.Window, debug: Callable[[str], Any]) -> None:
    self.window = window
    self.debug = debug

  def run(self, view: sublime.View, args: Dict[str, Any], marked: List[MF.MarkedFile]):
    filename_marked_pairs = [(m.file_name, m) for m in marked]
    filename_marked_dict: Dict[str, MF.MarkedFile] = dict(filename_marked_pairs)

    input_lines = ",".join(filename_marked_dict.keys())
    on_reordered = partial(self.reorder_selection, marked, filename_marked_dict)
    self.window.show_input_panel("reorder", input_lines, on_done=on_reordered, on_cancel=None, on_change=None)

  def reorder_selection(self, marked: List[MF.MarkedFile], old_hash: Dict[str, MF.MarkedFile], input: str):
    # Also remove any duplicate names?
    new_order: List[Tuple[str, MF.MarkedFile]] = [(f, old_hash[f]) for f in input.split(",") if len(f.strip()) > 0 if f in old_hash]
    old_mark_count = len(old_hash.keys())
    new_mark_count = len(new_order)
    if old_mark_count < new_mark_count:
      sublime.message_dialog(f'Can\'t add new marks through reorder. Add it through \'Mark File\'')
    else:
      # option1: We have the same number of marks old and new
      # option2: Marks have been slated for removal, confirm with the user that that's what they intended.
      if old_mark_count == new_mark_count or (old_mark_count > new_mark_count and sublime.yes_no_cancel_dialog("Close removed marks?") == sublime.DIALOG_YES):
        # assume the content is valid. Check in another iteration
        new_marked: List[MF.MarkedFile] = []
        for (_, mark) in new_order:
          # can we parse not validate? We already checked this above so it *shouldn't* fail
          new_marked.append(mark)

        marked.clear()
        marked.extend(new_marked)
        sublime.message_dialog(f"reordered: {str(marked)}")


  def add_hint(self, view: sublime.View, file_name: str, message: str):
    short_file_name = os.path.basename(file_name)
    markup = '''
    <H2>{} {}</H2>
    '''.format(message, short_file_name)

    view.show_popup(
      content = markup,
      max_width=600
    )

  def get_project_dir(self) -> Optional[str]:
    window = self.window
    if window:
      variables = window.extract_variables()
      if variables:
        return variables.get('folder') # could be None
      else:
        return None
    else:
      return None
