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
        l = dP.get_valid_servers(dP.get_ServerList())
        self.assertTrue(len(l) > 0)

    #testing if at least one server is not available
    def test_empty_servers(self):
        dP = mDP.DataPoster()
        serverList = dP.get_ServerList()
        serverList.append("http://shane-pi-iot.cfapps.io/bogus.html")
        l = dP.get_valid_servers(serverList)
        invalid = dP._invalid_servers
        self.assertTrue(len(invalid) >= 1)

    #Test post_to_valid_servers
    def test_post_to_valid_servers(self):
        dP = mDP.DataPoster()

        aData = dP.get_accelerometer_data()

        l = dP.get_valid_servers(dP.get_ServerList())
        print("This is valid_server list: {}".format(l))
        print("Length of l is {}".format(len(l)))
        post = dP.post_to_valid_servers(aData)
        print("Post returns: {}".format(post))
        self.assertTrue(post == len(l))









if __name__ == '__main__':
    unittest.main()