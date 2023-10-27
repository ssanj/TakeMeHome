import unittest

import take_me_home_setting as S

# Example test with valid imports and a test to get started.
class SettingTest(unittest.TestCase):

  def test_str(self):
    settings = S.TakeMeHomeSetting(debug = True)
    self.assertEqual("TakeMeHomeSetting(debug=True)", str(settings))
