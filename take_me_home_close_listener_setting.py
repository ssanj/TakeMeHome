class TakeMeHomeCloseListenerSetting:
  def __init__(self, debug: bool) -> None:
    self.debug = debug

  def __str__(self) -> str:
    return f"TakeMeHomeCloseListenerSetting(debug={self.debug})"

  def __repr__(self) -> str:
    return self.__str__()
