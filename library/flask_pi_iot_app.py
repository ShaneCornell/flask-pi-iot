from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import requests
#from library.pi_iot_data import pi_iot_data as pid
from library.data_storage import stored_reading as stored

app = Flask(__name__)

dataStore = stored.StoredReadings()

@app.route('/test', methods=['POST','GET'])
def my_test():
    if request.method == 'POST':
        print("/test")
        d = request.form
        # print(d["serial-no"])
        dataStore.add_readings(d["serial-no"], d["timestamp"], d["x"], d["y"], d["z"])
        dataStore.add_readings_to_db(d["serial-no"], d["timestamp"], d["x"], d["y"], d["z"])
        print("serial-no: {}, timestamp: {}, x: {}, y: {}, z: {}".format(d["serial-no"], d["timestamp"], d["x"], d["y"],
                                                                         d["z"]))
        print(dataStore.get_number_of_readings())
    return ("hello")


@app.route('/all_data.html', methods=['POST', 'GET'])
def all_data():
    print("/all_data")
    d = dataStore.get_all_data_as_list()
    print("/all_data:d{}".format(d))
    print(dataStore.get_number_of_readings())
    print(len(d))
    # Also "hook it up" here. For assignment 3.
    return render_template('all_data.html',data=d)


@app.route('/yaml')
def my_yaml_microservice():
    pass
    #return ymlify({'Hello':'World'})


@app.route('/')
@app.route('/index.html')
def main_page():
    return render_template('index.html')

@app.route('/johnpi.html',methods=['POST','GET'])
def john_page():
    if request.method == 'POST':
        print("JohnPi got a post")
        print(request.form)
    return render_template('johnpi.html')

@app.route('/meganpi.html',methods=['POST','GET'])
def megan_page():
    if request.method == 'POST':
        print("MeganPi got a post")
        print(request.form)
    return render_template('meganpi.html')


@app.route('/katiepi.html',methods=['POST','GET'])
def katie_page():
    if request.method == 'POST':
        print("KatiePi got a post")
        print(request.form)
    return render_template('katiepi.html')

@app.route('/davidpi.html',methods=['POST','GET'])
def david_page():
    if request.method == 'POST':
        print("DavidPi got a post")
        print(request.form)
    return render_template('davidpi.html')

