'''Code to get config info from a yaml file at a given url. Made by Katie & David, still married... unbelievably'''

import yaml
import requests

class YAMLConfig():
    def get_config_from_url(self,url):
        response = requests.get(url)
        if (response.status_code ==200):
            d = yaml.load(response.text)
        else:
            print("This file is not valid")
        #print(d)
        l = d['serverList']
        return l

if __name__ == '__main__':
    YConfig = YAMLConfig()
    serverlist =YConfig.get_config_from_url("https://raw.githubusercontent.com/ShaneCornell/flask-pi-iot/master/pi_client/config/config.yml")
    print(serverlist)