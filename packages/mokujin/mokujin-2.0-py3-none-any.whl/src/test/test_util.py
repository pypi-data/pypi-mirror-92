import unittest

from src import util


class MyTestCase(unittest.TestCase):
    def test_get_content(self):
        content = ['Similar moves from armor_king', '**1**. d/f+2+3', '**2**. d/f+3', '**3**. d/f+2', '**4**. d/b+2, 3',
                   '**5**. d+2, 4, 3']
        result = util.get_character_name_from_content(content)
        self.assertEqual("armor_king", result)

        result = util.get_moves_from_content(content)
        self.assertIn("d/f+3", result)
