import bme590_assignment02.ECG_Class
from flask import Flask, jsonify, request
import numpy as np

app = Flask(__name__)


@app.route("/heart_rate/summary", methods = ['POST'])
def give_summary():
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
