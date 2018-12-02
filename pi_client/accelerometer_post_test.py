# Test the accelerometer code

import unittest
import accelerometer_post as ap

class test_accelerometer_post(unittest.TestCase):

    def setUp(self):
        return

    # Test the host name list
    def test_get_serverlist(self):
        l=ap.get_serverlist()
        self.assertTrue(type(l)==type(list()))
        self.assertTrue(len(l) > 0)

    def test_servers(self):
        l=ap.get_valid_servers()
        self.assertTrue(len(l) > 0)


if __name__ == '__main__':
    unittest.main()