import ECG_Class
from flask import Flask, jsonify, request
import numpy as np
app = Flask(__name__)

@app.route("heart_rate/summary", method='POST')
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
    dat = [d1,d2]
    ecg_object = ECG_Class('api',dat)
    hr = ecg_object.instHR
    ta = ecg_object.tachyT
    ba = ecg_object.bradyT
    output = {'time': d1,
            'instantaneous_heart_rate':hr,
            'tachycardia_annotations':ta,
            'bradycardia_annotations':ba
            }
    ret = jsonify(output)
    return ret
