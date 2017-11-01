
import bme590_assignment02.ECG_Class
from flask import Flask, jsonify, request
import numpy as np

app = Flask(__name__)
count_requests = 0  # Global variable 


@app.route('/heart_rate/summary', methods=['POST'])
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
                    print('Dictionary does not contain valid time')
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
                    print('Dictionary does not contain valid voltage')
    dat = [d1, d2]
    ecg_object = ECG_Class(dat)
    
    hr = ecg_object.HRinst(ecg_object.data)  # I think this is right?
    ta = ecg_object.tachy('inst')
    ba = ecg_object.brady('inst')
    output = {'time': d1,
              'instantaneous_heart_rate': hr,
              'tachycardia_annotations': ta,
              'bradycardia_annotations': ba
              }
    ret = jsonify(output)
    return ret


@app.route('/heart_rate/average', methods=['POST'])
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
            print('Dictionary does not contain valid time')
    if 'voltage' in dictionary.keys():
        d2 = dictionary['voltage']
    else:
        try:
            d2 = dictionary['v']
        except ValueError:
            print('Dictionary does not contain valid voltage')
    if 'averaging_period' in dict.keys():
        ap = dictionary['averaging_period']
    else:
        raise ValueError('Dictionary does not contain valid period')
    dat = [d1, d2]
    ecg_object = ECG_Class.ECG_Class('api', dat=dat, avemins=ap)
    ahr = ecg_object.avg()
    ta = ecg_object.tachy('avg')
    ba = ecg_object.brady('avg')
    output = {'time_interval': d1,
              'averaging_period': ap,
              'average_heart_rate': ahr,
              'tachycardia_annotations': ta,
              'bradycardia_annotations': ba
              }
    ret = jsonify(output)
    return ret


@app.route('/heart_rate/requests', methods=['GET'])
def requests():
    global count_requests
    count_requests += 1
    ret = jsonify(count_requests)
    return ret


def send_error(message, code):  # Suyash error function
    err = {
        "error": message,
    }
    return jsonify(err), code

