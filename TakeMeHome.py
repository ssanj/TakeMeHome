import sublime
import sublime_plugin
from typing import Callable, Optional, List, Any, Dict, Union, Set
from . import take_me_home_setting as SETTING
from . import settings_loader as SETTING_LOADER
from . import marked_file as MF
import os
import pathlib

class TakeMeHomeCommand(sublime_plugin.WindowCommand):

  print("take_me_home command has loaded.")

  def __init__(self, window: sublime.Window) -> None:
    super().__init__(window)
    self.marked: list[MF.MarkedFile] = []

  def run(self, **args) -> None:
    if self:
      self.log("take_me_home is running")
      self.settings: SETTING.TakeMeHomeSetting = self.load_settings()
      self.debug(f'settings: {self.settings}')
      self.handle_actions(args)
    else:
      sublime.message_dialog("Could not initialise plugin")

  def handle_actions(self, args: Dict[str, Any]):
    self.debug(f"Got args: {args}")
    action_asked_for = args.get("action")
    if action_asked_for:
      view = self.window.active_view();
      if view:
        self.perform_actions(action_asked_for, view, args)
      else:
        self.debug("no active view")
    else:
      self.debug(f"Could not find valid 'action' key  and value in arguments supplied: {args}")


  def perform_actions(self, action_key: str, view: sublime.View, args: Dict[str, Any]):
        actions_map: Dict[str, Callable[[sublime.View, Dict[str, Any]], None]] = {};
        actions_map['mark']           = self.mark_current_file;
        actions_map['unmark']         = self.unmark_current_file;
        actions_map['list']           = self.list_marks;
        actions_map['clear']          = self.clear_marks;
        actions_map['close_unmarked'] = self.close_unmarked;
        actions_map['quick_jump']     = self.perform_quick_jump;

        action_to_perform = actions_map.get(action_key);
        if action_to_perform:
          action_to_perform(view, args)
        else:
          valid_actions = actions_map.keys()
          self.debug(f"Unknown action: {action_key}. Valid actions are: {valid_actions}")

  def quick_jump(self, view: sublime.View, index: int):
    num_marked = len(self.marked)
    if num_marked == 0:
      sublime.message_dialog("No files marked.\nPlease mark one or more files to quick jump to it")
      return

    if index > 0 and index <= num_marked:
      jump_mark = self.marked[index - 1]
      if jump_mark.view.is_valid():
        self.window.focus_view(jump_mark.view)
      else:
        self.marked.remove(jump_mark)
        sublime.message_dialog(f"View {view} is invalid; can't jump to it.\nIt's been removed from the mark list.")
    else:
      sublime.message_dialog(f"Invalid jump index {index}. Index must be between 1 to number of marked views")

  def perform_quick_jump(self, view: sublime.View, args: Dict[str, Any]):
    if "index" in args:
      index: int = args["index"]
      return self.quick_jump(view, index)
    else:
      self.debug("index not specified for quick_jump.")

  def close_unmarked(self, view: sublime.View, args: Dict[str, Any]):
    if len(self.marked) == 0:
      sublime.message_dialog("No files marked.\nPlease mark one or more files to close unmarked views")
      return

    if sublime.yes_no_cancel_dialog("Close all unmarked views?") == sublime.DIALOG_YES:
      self.close_other_views(view)

  def close_other_views(self, view: sublime.View):
    all_views: Set[sublime.View] =  set(self.window.views())
    marked_views = [m.view for m in self.marked]
    views_to_close = all_views.difference(marked_views)

    for v in views_to_close:
      v.close()

  def mark_current_file(self, view: sublime.View, args: Dict[str, Any]):
    file_name: Optional[str] = view.file_name()
    name: Optional[str] = view.name()
    if file_name:
      if not self.marked.__contains__(MF.MarkedFile(MF.FileType.HasFileName, file_name, view)):
        self.mark_view_with_file_name(view, file_name)
        self.add_hint(view, file_name, "Marked")
      else:
        sublime.message_dialog("This file is already marked.")
    elif name:
      if not self.marked.__contains__(MF.MarkedFile(MF.FileType.HasName, name, view)):
        self.mark_view_with_name(view, name)
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

  def unmark_current_file(self, view: sublime.View, args: Dict[str, Any]):
    file_name: Optional[str] = view.file_name()
    name: Optional[str] = view.name()
    if file_name:
      self.unmark_view_with_file_name(view, file_name)
      self.add_hint(view, file_name, "Unmarked")
    elif name:
      self.unmark_view_with_name(view, name)
      self.add_hint(view, name, "Unmarked")
    else:
      sublime.message_dialog("Only views that have a file name can be marked or unmarked.")

  def clear_marks(self, view: sublime.View, args: Dict[str, Any]):
    if len(self.marked) == 0:
      sublime.message_dialog("No files marked to clear.\nPlease mark one or more files to clear them here.")
      return

    if sublime.yes_no_cancel_dialog("Remove all marks?") == sublime.DIALOG_YES:
      self.marked.clear()

  def list_marks(self, view: sublime.View, args: Dict[str, Any]):
    files = [self.create_quick_panel_item(i+1, f.file_name) for i, f in enumerate(self.marked)]
    if len(files) == 0:
      sublime.message_dialog("No files marked.\nPlease mark one or more files to list them here.")

    self.window.show_quick_panel(files, on_select = self.on_mark_selected)

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


  def create_quick_panel_item(self, index: int, file_name: str) -> sublime.QuickPanelItem:
    file_name_only = os.path.basename(file_name)
    project_dir: Optional[str] = self.get_project_dir()
    self.debug(f"file_name: {file_name}, project_dir:{project_dir}")
    parent_dir = self.get_relative_path(file_name, project_dir) if project_dir else pathlib.PurePath(file_name).parent.name
    details = [parent_dir]
    return sublime.QuickPanelItem(file_name_only, details, str(index), kind=sublime.KIND_NAVIGATION)


  def get_relative_path(self, file_name: str, project_dir: str) -> str:
    relative_path = self.removeprefix(file_name, project_dir)
    file_name_only = os.path.basename(file_name)
    path_only = self.removesuffix(relative_path, file_name_only)
    path_without_pre_post_slashes = self.removeprefix(self.removesuffix(path_only, os.path.sep), os.path.sep)
    return path_without_pre_post_slashes if path_without_pre_post_slashes else "[project]"


  def on_mark_selected(self, index: int):
    # unselected index is -1, so watch out for that
    if index >= 0 and index < len(self.marked):
      view = self.marked[index].view
      if view.is_valid():
        self.window.focus_view(view)
      else:
        self.marked.remove(self.marked[index])
        sublime.message_dialog(f"View selected {view} is now invalid. Removing from marked list")


  def mark_view_with_file_name(self, view: sublime.View, file_name: str):
    self.marked.append(MF.MarkedFile(MF.FileType.HasFileName, file_name, view))

  def mark_view_with_name(self, view: sublime.View, name: str):
    self.marked.append(MF.MarkedFile(MF.FileType.HasName, name, view))

  def unmark_view_with_file_name(self, view: sublime.View, file_name: str):
    m = MF.MarkedFile(MF.FileType.HasFileName, file_name, view)
    self.marked.remove(m)

  def unmark_view_with_name(self, view: sublime.View, name: str):
    m = MF.MarkedFile(MF.FileType.HasName, name, view)
    self.marked.remove(m)

# ----------------------------------------------------------------------------------------------------------------------
# Infrastructure related
# ----------------------------------------------------------------------------------------------------------------------

  def is_enabled(self) -> bool:
    return True


  def is_visible(self) -> bool:
    return True

  def load_settings(self) -> SETTING.TakeMeHomeSetting:
    loaded_settings: sublime.Settings = sublime.load_settings('TakeMeHome.sublime-settings')
    return SETTING_LOADER.SettingsLoader(loaded_settings).load()


  def log_with_context(self, message: str, context: Optional[str]):
    if context is not None:
      print(f'[TakeMeHome][{context}] - {message}')
    else:
      print(f'[TakeMeHome] - {message}')


  def log(self, message: str):
    self.log_with_context(message, context=None)


  def debug(self, message: str):
    if self.settings.debug:
      self.log_with_context(message, context="DEBUG")
