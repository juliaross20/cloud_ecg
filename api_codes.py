
import bme590_assignment02.ECG_Class
from flask import Flask, jsonify, request
import numpy as np

app = Flask(__name__)
count_requests = 0  # Global variable 


@app.route("/heart_rate/summary", methods=['POST'])
def give_summary():
    global count_requests
    count_requests += 1
    dictionary = request.json
    if 'time' in dictionary.keys():
        d1 = dictionary['time']
    else:
        try:
            d1 = dictionary['t']
        except ValueError:
            try:
                d1 = dictionary['T']
            except ValueError:
                try:
                    d1 = dictionary['Time']
                except ValueError:
                    print("Dictionary does not contain valid time")
                    # Here, assign dummy value to d1 to get rid of pep8 error
    if 'voltage' in dictionary.keys():
        d2 = dictionary['voltage']
    else:
        try:
            d2 = dictionary['v']
        except ValueError:
            try:
                d2 = dictionary['V']
            except ValueError:
                try:
                    d2 = dictionary['Voltage']
                except ValueError:
                    print("Dictionary does not contain valid voltage")
                    # Here, assign dummy value to d2 to get rid of pep8 error
    dat = [d1, d2]  # Pep8: local variables referenced before assignment
    ecg_object = ECG_Class(dat)
    
    hr = ecg_object.instHR
    ta = ecg_object.tachyT
    ba = ecg_object.bradyT
    output = {'time': d1,
              'instantaneous_heart_rate': hr,
              'tachycardia_annotations': ta,
              'bradycardia_annotations': ba
              }
    ret = jsonify(output)
    return ret


@app.route('/heart_rate/average')
def give_avg_summary():
    global count_requests
    count_requests += 1
    dictionary = request.json
    if 'time' in dictionary.keys():
        d1 = dictionary['time']
    else:
        try:
            d1 = dictionary['t']
        except ValueError:
            print("Dictionary does not contain valid time")
    if 'voltage' in dictionary.keys():
        d2 = dictionary['voltage']
    else:
        try:
            d2 = dictionary['v']
        except ValueError:
            print("Dictionary does not contain valid voltage")
    if 'averaging_period' in dict.keys():
        ap = dictionary['averaging_period']
    else:
        raise ValueError("Dictionary does not contain valid period")
    dat = [d1, d2]
    ecg_object = ECG_Class.ECG_Class('api', dat=dat, avemins=ap)
    ahr = ecg_object.avg()
    ta = ecg_object.tachyT
    ba = ecg_object.bradyT
    output = {'time_interval': d1,
              'averaging_period': ap,
              'average_heart_rate': ahr,
              'tachycardia_annotations': ta,
              'bradycardia_annotations': ba
              }
    ret = jsonify(output)
    return ret


@app.route("/heart_rate/num_requests", methods=['GET'])
def num_requests():
    global count_requests
    count_requests += 1
    return count_requests

