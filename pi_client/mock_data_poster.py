# Mock Pi file

import requests
import time
import datetime
import random



class DataPoster():

    def __init__(self):
        self._valid_servers = []
        self._invalid_servers = []
        self._server_list = ['http://megan-pi-iot.cfapps.io/test',
                     'http://katie-pi-iot.cfapps.io/test',
                    'http://david-pi-iot.cfapps.io/test',
                    'http://jpf-flask-pi-iot.cfapps.io/test',
                    'http://shane-pi-iot.cfapps.io/test']

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
            cpuserial = "ERROR000000000"

        return cpuserial

    def get_ServerList(self):
        return self._server_list

    def get_valid_servers(self, serverList):
        self._valid_servers = []
        self._invalid_servers = []
        sl = serverList
        for server in sl:
            r = requests.get(server)
            if r.status_code != 200:
                self._invalid_servers.append(server)
                # print('Added {} to INVALID server list' .format(server))
            else:
                self._valid_servers.append(server)
                # print('Added {} to VALID server list'.format(server))
        return(self._valid_servers)

    def accel_read(self):
        x = random.randrange(0, 10, 1)
        y = random.randrange(0, 10, 1)
        z = random.randrange(0, 10, 1)
        return (x, y, z)

    # def refind_valid_servers(self):
    #     self._valid_servers = []
    #     self.get_valid_servers()
    #     return(self._valid_servers)

    def post_to_valid_servers(self, aData):
        self.get_valid_servers(self.get_ServerList())
        n = 0
        for server in self._valid_servers:
            r = requests.post(server, data=aData)
            if r.status_code != 200:
                print("server: {} returned error code: {}".format(server, r.status_code))
            else:
                n = n + 1
        return n

    def update_active_server_cach(self):
        pass

    def get_accelerometer_data(self):
        x, y, z = self.accel_read()
        print('X={0}, Y={1}, Z={2}'.format(x, y, z))
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        myserial = self.getserial()
        aData = {'serial-number': myserial, 'timestamp': ts, 'x': x, 'y': y, 'z': z}
        print(aData)
        return aData

if __name__ == '__main__':
    dP = DataPoster()
    while True:
        aData = dP.get_accelerometer_data()
        dP.post_to_valid_servers(aData)

        #tbd wrap above in a loop to periodically check for valid servers
