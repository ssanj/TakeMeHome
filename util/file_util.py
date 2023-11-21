import sublime
from typing import Optional
import os

class FileUtil:

  def get_project_dir(self, window: sublime.Window) -> Optional[str]:
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

  def get_project_relative_filename(self, window: sublime.Window, file_name: str) -> str:
    project_dir = self.get_project_dir(window)
    if project_dir:
      project_relative_filename = self.removeprefix(file_name, project_dir)
      # Remove leading /
      return self.removeprefix(project_relative_filename, os.path.sep)
    else:
      return file_name
