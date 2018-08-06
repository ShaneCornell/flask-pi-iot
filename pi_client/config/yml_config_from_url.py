
import yaml
import requests

class YamlConfig():
    def __init__(self):
        pass

    def yml_config_from_url(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            config = yaml.load(response.text)
            print(type(config))
            print(config)

        return config

if __name__ == '__mann__':
    aYC = YamlConfig()
    aYC.yml_config_from_url("https://raw.githubusercontent.com/ShaneCornell/flask-pi-iot/master/pi_client/config/config.yml")