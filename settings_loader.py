import sublime

from . import take_me_home_setting as SETTING

class SettingsLoader:

  default_debug: bool = True

  def __init__(self, settings: sublime.Settings) -> None:
    self.settings = settings

  def log(self, message: str):
    print(f'[TakeMeHome][WARN] - {message}')

  def load(self) -> SETTING.TakeMeHomeSetting:
    debug: bool = self.get_debug()

    return SETTING.TakeMeHomeSetting(debug)

  def get_debug(self) -> bool:
    if self.settings.has("debug"):
      return self.settings.get("debug")
    else:
      self.log(f'debug setting not defined, defaulting to {SettingsLoader.default_debug}')
      return SettingsLoader.default_debug

