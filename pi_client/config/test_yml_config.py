#Test the yaml config

from pi_client.config import yml_config_from_url as y
import unittest

class test_yaml_config(unittest.TestCase):

    def setup(self):
        return

    def test_yml_config_from_url(self, url):
        url = 'https://raw.githubusercontent.com/JohnFunkCode/getconfig/master/yamlconfigfromurl/test.yml'
        y2 = y.YamlConfig()
        y2.yml_config_from_url(url)
        self.assertTrue(y2.passwd == 'mysecret password')

        #
        # mysql:
        #     host: localhost
        #     user: root
        #     passwd: my secret password
        #     db: write-math

if __name__ == '__main__':

    print("Starting Tests.")
    unittest.main()
