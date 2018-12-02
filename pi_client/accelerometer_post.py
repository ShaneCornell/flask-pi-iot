# Import the ADXL345 module.
import Adafruit_ADXL345
import requests
import time
import datetime

accel = Adafruit_ADXL345.ADXL345()

def getserial():
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

def get_serverlist():
    serverlist = ['https://katie-pi-iot.cfapps.io/', 'https://megan-pi-iot.cfapps.io/','https://david-pi-iot.cfapps.io/','http://jpf-flask-pi-iot.cfapps.io/','https://shane-pi-iot.cfapps.io/']
    return serverlist

def get_valid_servers():
    sl=get_serverlist()
    for server in sl:
        print("servername: " + server)
        r = requests.get(server)
        print("Status returned:{0} ".format(r.status_code))
        if r.status_code != 200:
            sl.remove(server)
            print("Removed{0} ".format(server))
    return sl

if __name__ == '__main__':
    while True:
        x,y,z=accel.read()
        print('X={0}, Y={1}, Z={2}'.format(x, y, z))
        ts=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        serial=getserial()
        aData={'serial-no':serial,'timestamp':ts,'x':x,'y':y,'z':z}
        print(aData)
        r=requests.post('https://katie-pi-iot.cfapps.io/',data=aData)