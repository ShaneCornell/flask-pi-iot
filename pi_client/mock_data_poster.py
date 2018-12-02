# Mock Pi file
realPi=False

if realPi:
    import Adafruit_ADXL345
    accel = Adafruit_ADXL345.ADXL345()


import requests
import time
import datetime
import random
import math
from config import config


class DataPoster():

    def __init__(self):
        self._validServers = []
        self._invalidServers = []
        '''self._serverList = ['http://megan-pi-iot.cfapps.io/test',
                     'http://katie-pi-iot.cfapps.io/test',
                    'http://david-pi-iot.cfapps.io/test',
                    'http://jpf-flask-pi-iot.cfapps.io/test',
                    'http://shane-flask-pi-iot.cfapps.io/test']'''
        YConfig = config.YAMLConfig()
        self._serverList = YConfig.get_config_from_url(
            "https://raw.githubusercontent.com/ShaneCornell/flask-pi-iot/master/pi_client/config/config.yml")

    def getserial(self):
        # Extract serial from cpuinfo file
        cpuserial = "0000000000000000"
        try:
            f = open('/proc/cpuinfo', 'r')
            for line in f:
                if line[0:6] == 'Serial':
                    cpuserial = line[10:26]
            f.close()
        except:
            cpuserial = "KATIE000000000"

        return cpuserial

    def get_ServerList(self):
        return self._serverList

    def get_valid_servers(self, sl):
        self._validServers = []
        print("In get_valid_servers() server list passed to us is {}" .format(sl))
        for server in sl:
            url_to_send_to = server + "/index.html"
            r = requests.get(url_to_send_to)
            if r.status_code != 200:
                self._invalidServers.append(server)
                # print('Added {} to INVALID server list' .format(server))
            else:
                self._validServers.append(server)
                #print('In get_valid_servers() added {} to VALID server list'.format(server))
        return(self._validServers)

    def mock_accel_read(self):
        x = random.randrange(0, 10, 1)
        y = random.randrange(0, 10, 1)
        z = random.randrange(0, 10, 1)
        return (x, y, z)

    def post_to_valid_servers(self, aData):
        #self.get_valid_servers(self.get_ServerList())
        n = 0
        for server in self._validServers:
            print("Sending to server {}".format(server))
            url_to_send_to = server + "/test"
            r = requests.post(url_to_send_to, data = aData)
            if r.status_code != 200:
                print("server: {} returned error code: {}".format(server, r.status_code))
            else:
                n = n + 1
                print("Successfully sent data to: {}".format(server))
        return n

    def get_aData(self):
        if realPi:
            x, y, z = accel.read()
        else:
            x, y, z = self.mock_accel_read()

        print('X={0}, Y={1}, Z={2}'.format(x, y, z))
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        myserial = self.getserial()
        aData = {'serial-no': myserial, 'timestamp': ts, 'x': x, 'y': y, 'z': z}
        return (aData)


if __name__ == '__main__':
    dP = DataPoster()
    dP.get_valid_servers(dP.get_ServerList())
    oldtime = time.time()
    oldx = oldy = oldz = 0
    old_composite = oldx + oldy + oldz

    while True:
        reading = dP.get_aData()
        newx = reading["x"]
        newy = reading["y"]
        newz = reading["z"]
        new_composite = newx + newy + newz

        newtime = math.floor(time.time())
        postit = False

        if( 10 <= abs(new_composite - old_composite)): #if data hasn't changed don't send it
            postit=True

        if(1 <= (newtime - oldtime)):  # if one second goes by with not change send the reading anyways
            postit = True

        if(postit==True):
           dP.post_to_valid_servers(reading)
           oldx = newx
           oldy = newy
           oldz = newz
           old_composite = new_composite
           oldtime = newtime

        #This refreshes serverlist every 10 seconds
        if 60 <= newtime - oldtime:
            print("Refreshing server list...")
            dP.get_valid_servers(dP.get_ServerList())
            oldtime = time.time()
            print("In the main loop valid server list {}" .format(dP.get_valid_servers(dP.get_ServerList())))


