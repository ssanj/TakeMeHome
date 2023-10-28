import sublime
import sublime_plugin
from typing import Optional, List, Any, Dict, Union, Set
from . import take_me_home_setting as SETTING
from . import settings_loader as SETTING_LOADER
from . import marked_file as MF
import os

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
    if args.get("action"):
      action = args.get("action")
      self.debug(f"action: {action}")

      view = self.window.active_view();
      if view:
        file_name = view.file_name()
        if file_name:
          if action == "mark":
            return self.mark_current_file(view, file_name)
          elif action == "unmark":
            return self.unmark_current_file(view, file_name)
          elif action == "list":
            return self.list_marks(view)
          elif action == "clear":
            return self.clear_marks(view)
          elif action == "close_unmarked":
            return self.close_unmarked(view)
          else:
            self.debug(f"Unknown action: {action}. Valid actions are: mark, unmark, list, clear")
        else:
          sublime.message_dialog("Only views that have a file name can be marked.")
      else:
        self.debug("no active view or view has no file name")

  def close_unmarked(self, view: sublime.View):
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

  def mark_current_file(self, view: sublime.View, file_name: str):
    if not self.marked.__contains__(MF.MarkedFile(file_name, view)):
      self.mark_view(view)
      self.add_hint(view, file_name, "Marked")
    else:
      sublime.message_dialog("This file is already marked.")

  def add_hint(self, view: sublime.View, file_name: str, message: str):
    short_file_name = os.path.basename(file_name)
    markup = '''
    <H2>{} {}</H2>
    '''.format(message, short_file_name)

    view.show_popup(
      content = markup,
      max_width=600
    )

  def unmark_current_file(self, view: sublime.View, file_name: str):
    self.unmark_view(view)
    self.add_hint(view, file_name, "Unmarked")

  def clear_marks(self, view: sublime.View):
    if len(self.marked) == 0:
      sublime.message_dialog("No files marked to clear.\nPlease mark one or more files to clear them here.")
      return

    if sublime.yes_no_cancel_dialog("Remove all marks?") == sublime.DIALOG_YES:
      self.marked.clear()

  def list_marks(self, view: sublime.View):
    files = ["{} - {}".format(i+1, f.file_name) for i, f in enumerate(self.marked)]
    if len(files) == 0:
      sublime.message_dialog("No files marked.\nPlease mark one or more files to list them here.")

    self.window.show_quick_panel(files, on_select = self.on_mark_selected)

  def on_mark_selected(self, index: int):
    # unselected index is -1, so watch out for that
    if index >= 0 and index < len(self.marked):
      view = self.marked[index].view
      if view.is_valid():
        self.window.focus_view(view)

  def mark_view(self, view: sublime.View):
      file_name = view.file_name()
      if file_name:
        self.marked.append(MF.MarkedFile(file_name, view))

  def unmark_view(self, view: sublime.View):
      file_name = view.file_name()
      if file_name:
        m = MF.MarkedFile(file_name, view)
        self.marked.remove(m)


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
