
from bme590_assignment02.ECG_Class import ECG_Class
from flask import Flask, jsonify, request
import numpy as np

app = Flask(__name__)
count_requests = 0  # Global variable 


@app.route('/heart_rate/summary', methods=['POST'])
def give_summary():
    '''
    This is the endpoint for the data summary
    
    :return: output: (json) A json containing time, instantaneous HR, and
        brady and tachy cardia diagnoses
    '''

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
                    return send_error('Dictionary does not contain valid ''time'' data', 400)
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
                    return send_error('Dictionary does not contain valid ''voltage'' data', 400)
    dat = (np.array(d1),np.array(d2))
 #   try:
    ecg_object = ECG_Class(dat)
 #   except: # this should be made much more specific
 #       return send_error('stop giving me bad data dummy', 400)

    hr = ecg_object.instHR
    ta = ecg_object.tachy('inst')
    ba = ecg_object.brady('inst')
    output = {'time': d1,
              'instantaneous_heart_rate': hr.tolist(),
              'tachycardia_annotations': ta,
              'bradycardia_annotations': ba
              }
    ret = jsonify(output)
    return ret


@app.route('/heart_rate/average', methods=['POST'])
def give_avg_summary():
    ''' 
    This is the endpoint for the averaging commands
    
    :return: output: (json) A json containing the time interval, averaging period,
    average heart rate, and brady and tachy diagnoses
    '''

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
                    return send_error('Dictionary does not contain valid ''time'' data', 400)
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
                    return send_error('Dictionary does not contain valid ''voltage'' data', 400)
    if 'averaging_period' in dictionary.keys():[MaAD
        ap = dictionary['averaging_period']
    else:
        return send_error('Dictionary does not contain valid ''averaging_period'' data', 400)
    dat = (np.array(d1), np.array(d2))
    ecg_object = ECG_Class(dat, avemins=ap)
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
    '''
    This is the request endpoint

    :returns: ret: (int) the number of times a request has been made
    '''
    
    global count_requests
    count_requests += 1
    ret = jsonify(count_requests)
    return ret


def send_error(message, code):  # Suyash error function
    err = {
        "error": message,
    }
    return jsonify(err), code

