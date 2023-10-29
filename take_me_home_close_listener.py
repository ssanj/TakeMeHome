import sublime
import sublime_plugin
from typing import Optional
from . import take_me_home_close_listener_setting as SETTING
from . import close_listener_settings_loader as SETTING_LOADER

class TakeMeHomeCloseListenerCommand(sublime_plugin.ViewEventListener):

  print("take_me_home event listener has loaded.")

  @classmethod
  def is_applicable(cls, settings):
    return True

  @classmethod
  def applies_to_primary_view_only(cls):
      return False

  def __init__(self, view: sublime.View) -> None:
    super().__init__(view)
    self.settings: SETTING.TakeMeHomeCloseListenerSetting = self.load_settings()
    self.debug(f'settings: {self.settings}')

  def on_pre_close(self):
    self.debug("about to close")
    view = self.view
    window = view.window()
    if window and view and view.is_valid():
      window.run_command('take_me_home', {"action": "listener_close", "view_id": view.id()})

  def load_settings(self) -> SETTING.TakeMeHomeCloseListenerSetting:
    loaded_settings: sublime.Settings = sublime.load_settings('TakeMeHome.sublime-settings')
    return SETTING_LOADER.SettingsLoader(loaded_settings).load()

  def log_with_context(self, message: str, context: Optional[str]):
    if context is not None:
      print(f'[TakeMeHomeCloseListener][{context}] - {message}')
    else:
      print(f'[TakeMeHomeCloseListener] - {message}')

  def log(self, message: str):
    self.log_with_context(message, context=None)

  def debug(self, message: str):
    if self.settings.debug:
      self.log_with_context(message, context="DEBUG")
