#Test the yaml config

import unittest
import yml_config_from_url as y

class test_yaml_config():
    def __init__(self):
        pass

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

    #TODO put stuff here, check yaml format return w/ print statement in yml_config_from_url.py
