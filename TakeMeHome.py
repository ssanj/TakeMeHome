import sublime
import sublime_plugin
from typing import Callable, Optional, List, Any, Dict, Union, Set
from . import take_me_home_setting as SETTING
from . import settings_loader as SETTING_LOADER
from . import marked_file as MF
from TakeMeHome.actions import mark_current_file_action as MCFA
from TakeMeHome.actions import unmark_current_file_action as UCFA
from TakeMeHome.actions import list_marks_action as LMA
from TakeMeHome.actions import clear_marks_action as CMA
from TakeMeHome.actions import close_unmarked_action as CUA
from TakeMeHome.actions import quick_jump_action as QJA
from TakeMeHome.actions import reorder_marks_action as RMA
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
        actions_map: Dict[str, Callable[[sublime.View, Dict[str, Any], List[MF.MarkedFile]], None]] = {};
        actions_map['mark']           = MCFA.MarkCurrentFileAction(self.window, self.debug).run
        actions_map['unmark']         = UCFA.unmarkCurrentFileAction(self.window, self.debug).run
        actions_map['list']           = LMA.ListMarksAction(self.window, self.debug).run
        actions_map['clear']          = CMA.ClearMarksAction(self.window, self.debug).run
        actions_map['close_unmarked'] = CUA.CloseUnmarkedAction(self.window, self.debug).run
        actions_map['quick_jump']     = QJA.QuickJumpAction(self.window, self.debug).run
        actions_map['reorder']        = RMA.ReorderMarksAction(self.window, self.debug).run

        action_to_perform = actions_map.get(action_key);
        if action_to_perform:
          action_to_perform(view, args, self.marked)
        else:
          valid_actions = actions_map.keys()
          self.debug(f"Unknown action: {action_key}. Valid actions are: {valid_actions}")

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
