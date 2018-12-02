# Import the ADXL345 module.
import Adafruit_ADXL345
import requests
import time
import datetime

accel = Adafruit_ADXL345.ADXL345()

class DataPoster():

    def __init__(self):
        return

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
        ServerList = ['http://megan-pi-iot.cfapps.io/index.html', 'http://katie-pi-iot.cfapps.io/index.html', 'http://david-pi-iot.cfapps.io/index.html', 'http://jpf-flask-pi-iot.cfapps.io/index.html', 'http://shane-pi-iot.cfapps.io/index.html']
        return ServerList

    def get_valid_servers(self):
        sl = self.get_ServerList()
        for server in sl:
            print('server name: ' + server)
            r = requests.get(server)
            print('status return: {0}'.format(r.status_code))

            if r.status_code != 200:
                print('removed {0}' .format(server))
                sl.remove(server)

        return(sl)

if __name__ == '__main__':
    while True:
        x,y,z=accel.read()
        print('X={0}, Y={1}, Z={2}'.format(x, y, z))
        ts=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        myserial = getserial()
        aData={'serial-number': myserial, 'timestamp': ts,  'x': x, 'y': y, 'z': z}
        print(aData)
        r=requests.post('http://megan-pi-iot.cfapps.io/test',data=aData)