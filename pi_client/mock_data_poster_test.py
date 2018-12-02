#Test the accelerometer code

import unittest
import mock_data_poster as mDP
import time, datetime

class test_accelerometer_post(unittest.TestCase):

    def setUp(self):
        return

    #test the host name list
    def test_get_ServerList(self):
        dP = mDP.DataPoster()
        l = dP.get_ServerList()
        self.assertTrue(type(l) == type(list()))
        self.assertTrue(len(l) > 0)

   def test_get_valid_servers(self):
    dP = mDP.DataPoster()




    def test_servers(self):
        l = dP.get_valid_servers()
        self.assertTrue(len(l) > 0)

    #testing if no servers are available
    def test_empty_servers(self):
        l = dP.get_valid_servers()
        self.assertTrue(len(l) == 0)








if __name__ == '__main__':
    unittest.main()