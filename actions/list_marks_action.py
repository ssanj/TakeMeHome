import sublime
from typing import Optional, Dict, Any, List, Callable
from functools import partial
from .. import marked_file as MF
import os
import pathlib

class ListMarksAction:

  def __init__(self, window: sublime.Window, debug: Callable[[str], Any]) -> None:
    self.window = window
    self.debug = debug

  def run(self, view: sublime.View, args: Dict[str, Any], marked: List[MF.MarkedFile]):
    files = [self.create_quick_panel_item(i+1, f.file_name) for i, f in enumerate(marked)]
    if len(files) == 0:
      sublime.message_dialog("No files marked.\nPlease mark one or more files to list them here.")

    self.window.show_quick_panel(
      files,
      on_select = partial(self.on_mark_selected, marked),
      flags=sublime.MONOSPACE_FONT | sublime.WANT_EVENT,
      placeholder="Enter to select and Shift + Enter to remove"
    )

  def create_quick_panel_item(self, index: int, file_name: str) -> sublime.QuickPanelItem:
    file_name_only = os.path.basename(file_name)
    project_dir: Optional[str] = self.get_project_dir()
    self.debug(f"file_name: {file_name}, project_dir:{project_dir}")
    parent_dir = self.get_relative_path(file_name, project_dir) if project_dir else pathlib.PurePath(file_name).parent.name
    details = [parent_dir]
    return sublime.QuickPanelItem(file_name_only, details, str(index), kind=sublime.KIND_NAVIGATION)


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

  def removeprefix(self, original: str, prefix: str) -> str:
    if original.startswith(prefix):
      return original[len(prefix):]
    else:
      return original

  # removesuffix is added in Python 3.9+
  def removesuffix(self, original: str, prefix: str) -> str:
    if original.endswith(prefix):
      return original[:-len(prefix)]
    else:
      return original


  def get_relative_path(self, file_name: str, project_dir: str) -> str:
    relative_path = self.removeprefix(file_name, project_dir)
    file_name_only = os.path.basename(file_name)
    path_only = self.removesuffix(relative_path, file_name_only)
    path_without_pre_post_slashes = self.removeprefix(self.removesuffix(path_only, os.path.sep), os.path.sep)
    return path_without_pre_post_slashes if path_without_pre_post_slashes else "[project]"


  def on_mark_selected(self, marked: List[MF.MarkedFile], index: int, event: Dict[str, Any]):
    if index >= 0 and index < len(marked):
      m = marked[index]
      view = m.view
      if 'modifier_keys' in event and 'shift' in event['modifier_keys'] and event['modifier_keys']['shift']:
        file_name = os.path.basename(m.file_name)
        if sublime.yes_no_cancel_dialog(f"Remove mark from {file_name}?") == sublime.DIALOG_YES:
          marked.remove(m)
          active_view = self.window.active_view()
          if active_view:
            self.add_hint(active_view, file_name, "Unmarked")
      else:
        if view.is_valid():
          self.window.focus_view(view)
        else:
          marked.remove(marked[index])
          sublime.message_dialog(f"View selected {view} is now invalid. Removing from marked list")

  def add_hint(self, view: sublime.View, file_name: str, message: str):
    short_file_name = os.path.basename(file_name)
    markup = '''
    <H2>{} {}</H2>
    '''.format(message, short_file_name)

    view.show_popup(
      content = markup,
      max_width=600
    )
