from src import configurator
import unittest, os

dir_path = os.path.dirname(os.path.realpath(__file__))

config = configurator.Configurator(dir_path + "/test_config.json")

class MyTestCase(unittest.TestCase):

    def test_read_config(self):
        self.assertEqual("Test", config.read_config()['Test'])

    def test_write_config(self):

        data = config.read_config()
        data['Test2'] = "Test2"

        config.write_config(data)

        self.assertEqual("Test2",config.read_config()['Test2'])

    def test_get_autodelete(self):

        result = config.get_auto_delete_duration("test_channel_id")
        self.assertEqual(100,result)

    def test_write_autodelete(self):

        config.save_auto_delete_duration(2, 70)
        result = config.get_auto_delete_duration(2)
        self.assertEqual(70,result)
