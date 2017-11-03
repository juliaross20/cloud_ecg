from bme590_assignment02.ECG_Class import ECG_Class
from flask import Flask, jsonify, request
import numpy as np

app = Flask(__name__)
count_requests = 0  # Global variable 


@app.route('/heart_rate/summary', methods=['POST'])
def get_data_for_summary():
    """
    Summary endpoint: Accepts user data and returns instantaneous heart rate and brady tachy annotations

    :return: resp: (json) instantaneous heart rate and brady tachy annotations
    """
    global count_requests
    count_requests += 1
    req = request.json  # Retrieve external data
    data = check_and_parse_summary(req)  # Validate the data and map to internal format
    out = calc_summary(data)  # Process the data
    resp = jsonify(out)  # Map internal data to external format
    return resp  # Respond to client


def check_and_parse_summary(dictionary):
    """
    This validates the user input data and turns it into a tuple (Map external-->internal)

    :param: dictionary: (dict) User data (time and voltage)
    :return: dat: (tuple) User data (time and voltage)
    """
    # Check that time and voltage data were provided
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
    dat = (np.array(d1), np.array(d2))
    # Check that time and voltage data have same number of elements
    if len(dat[0]) != len(dat[1]):
        return send_error('Time and voltage arrays must have same number of elements', 400)
    # Check that data isn't entirely negative
    if np.all(np.where(dat[1] < 0, 1, 0)):
        return send_error('Data is entirely negative', 400)
    return dat


def calc_summary(dat):
    """
    This calculates the average heart rate and brady tachy annotations

    :param: dat: (tuple) User data (time and voltage)
    :return: output: (dict) Contains time, instantaneous HR, and brady tachy cardia annotations
    """

    #   try:
    ecg_object = ECG_Class(dat)
    #   except: # this should be made much more specific
    #       return send_error('stop giving me bad data dummy', 400)

    hr = ecg_object.instHR
    ta = ecg_object.tachy('inst')
    ba = ecg_object.brady('inst')
    output = {'time': dat[0],
              'instantaneous_heart_rate': hr.tolist(),
              'tachycardia_annotations': ta,
              'bradycardia_annotations': ba
              }
    return output


@app.route('/heart_rate/average', methods=['POST'])
def get_data_for_average():
    """
    Average endpoint: Accepts user data and returns average heart rate and brady tachy annotations

    :return: resp: (json) average heart rate and brady tachy annotations
    """
    global count_requests
    count_requests += 1
    req = request.json  # Retrieve external data
    dat, ap = check_and_parse_average(req)  # Validate the data and map to internal format
    out = calc_average_summary(dat, ap)  # Process the data
    resp = jsonify(out)  # Map internal data to external format
    return resp  # Respond to client


def check_and_parse_average(dictionary):
    """
    This validates the user input data and turns it into a tuple (Map external-->internal)

    :return: dictionary: (dict) User data (time and voltage)
    """
    # Check that time, voltage, and averaging period data were provided
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
    if 'averaging_period' in dictionary.keys():
        ap = dictionary['averaging_period']
    else:
        return send_error('Dictionary does not contain valid ''averaging_period'' data', 400)
    dat = (np.array(d1), np.array(d2))
    # Check that time and voltage data have same number of elements
    if len(dat[0]) != len(dat[1]):
        return send_error('Time and voltage arrays must have same number of elements', 400)
    # Check that there is enough data for averaging during the specified averaging period
    if dat[0][-1] < ap:
        return send_error('Not enough data for averaging', 400)
    # Check that data isn't entirely negative
    if np.all(np.where(dat[1] < 0, 1, 0)):
        return send_error('Data is entirely negative', 400)
    return dat


def calc_average_summary(dat, avg_secs):
    """

    :param dat: (tuple) User data (time and voltage)
    :param avg_secs: (int) Number of seconds to average over (bin size)
    :return: output: (json) Contains the time interval, averaging period,
    average heart rate, and brady and tachy diagnoses
    """
    ecg_object = ECG_Class(dat, avg_secs)
    ahr = ecg_object.avg()
    ta = ecg_object.tachy('avg')
    ba = ecg_object.brady('avg')
    output = {'time_interval': dat[0],
              'averaging_period': avg_secs,
              'average_heart_rate': ahr,
              'tachycardia_annotations': ta,
              'bradycardia_annotations': ba
              }
    return output


@app.route('/heart_rate/requests', methods=['GET'])
def requests():
    """
    Returns the number of requests made to the server since its last reboot

    :return: resp: (int) The number of requests
    """
    global count_requests
    count_requests += 1
    resp = jsonify(count_requests)
    return resp


def send_error(message, code):  # Suyash error function
    err = {
        "error": message,
    }
    return jsonify(err), code
