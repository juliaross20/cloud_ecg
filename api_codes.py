from flask import Flask, jsonify, request
import numpy as np

app = Flask(__name__)


@app.route("/heart_rate/summary", methods=['POST'])
def give_summary():
    dict = request.json
    if 'time' in dict.keys():
        d1 = dict['time']
    else:
        try:
            d1 = dict['t']
        except ValueError:
            print("Dictionary does not contain valid time")
    if 'voltage' in dict.keys():
        d2 = dict['voltage']
    else:
        try:
            d2 = dict['v']
        except ValueError:
            print("Dictionary does not contain valid voltage")
    dat = [d1, d2]
    ecg_object = ECG_Class('api', dat=dat)
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
    dict = request.json
    if 'time' in dict.keys():
        d1 = dict['time']
    else:
        try:
            d1 = dict['t']
        except ValueError:
            print("Dictionary does not contain valid time")
    if 'voltage' in dict.keys():
        d2 = dict['voltage']
    else:
        try:
            d2 = dict['v']
        except ValueError:
            print("Dictionary does not contain valid voltage")
    if 'averaging_period' in dict.keys():
        ap = dict['averaging_period']
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
