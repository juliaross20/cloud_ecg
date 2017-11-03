import api_codes as ac
import pytest
import unittest
import numpy as np

testdictrightsum = {"time":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],
                 "voltage":[0, 1, 7, 1, 0, -1, 10, 10, 3, 2, 0, 4,5, 0, 9, 10, 11, 10, 0, 1, 2, 4, 3,
                            8.5,8.6, 8, 1, 2, 3]}
testdictrightave = {"averaging_period" : 10,
                    "time":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],
                 "voltage":[0, 1, 7, 1, 0, -1, 10, 10, 3, 2, 0, 4,5, 0, 9, 10, 11, 10, 0, 1, 2, 4, 3,
                            8.5,8.6, 8, 1, 2, 3]}
testdictwrongvarnames = {"tee":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],
                         "vee":[0, 1, 7, 1, 0, -1, 10, 10, 3, 2, 0, 4,5, 0, 9, 10, 11, 10, 0, 1, 2, 4, 3,
                                8.5,8.6, 8, 1, 2, 3]}


def test_jsonparsesum():

    checker = ac.check_and_parse_summary(testdictrightsum)
    assert type(checker) is tuple
    assert type(checker[0]) is np.ndarray
    assert checker[0]== np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])
    assert checker[1] == np.array([0, 1, 7, 1, 0, -1, 10, 10, 3, 2, 0, 4,5, 0, 9, 10, 11, 10, 0, 1, 2, 4, 3,
                                  8.5,8.6, 8, 1, 2, 3])

def test_jsonparseave():

    checker,cp = ac.check_and_parse_average(testdictrightave)
    assert cp == 10
    assert type(checker) is tuple
    assert type(checker[0]) is np.ndarray
    assert checker[0] == np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                                   21, 22, 23, 24, 25, 26, 27, 28])
    assert checker[1] == np.array([0, 1, 7, 1, 0, -1, 10, 10, 3, 2, 0, 4, 5, 0, 9, 10, 11, 10, 0, 1, 2, 4, 3,
                                   8.5, 8.6, 8, 1, 2, 3])

def test_sumoutput():
    testtup = (np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]),
               np.array([0, 1, 7, 1, 0, -1, 10, 10, 3, 2, 0, 4,5, 0, 9, 10, 11, 10, 0, 1, 2, 4, 3, 8.5,8.6, 8, 1, 2, 3]))
    outdict = ac.calc_summary(testtup)
    assert type(outdict) is dict
    keysofout = outdict.keys()
    assert "time" in keysofout
    assert "instantaneous_heart_rate" in keysofout
    assert "tachycardia_annotations" in keysofout
    assert "bradycardia_annotations" in keysofout
    assert outdict['time'] == [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
    assert outdict["instantaneous_heart_rate"] == [0, 1, 7, 1, 0, -1, 10, 10, 3, 2, 0, 4,5, 0, 9, 10, 11, 10, 0, 1, 2, 4, 3,
                                  8.5,8.6, 8, 1, 2, 3]
    assert outdict['bradycardia_annotations'] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert outdict['tachycardia_annotations'] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def test_aveoutput():
    testtup = (np.array(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]),
               np.array(
                   [0, 1, 7, 1, 0, -1, 10, 10, 3, 2, 0, 4, 5, 0, 9, 10, 11, 10, 0, 1, 2, 4, 3, 8.5, 8.6, 8, 1, 2, 3]))
    outdict = ac.give_average_summary(testtup,5)
    assert type(outdict) is dict
    keysofout = outdict.keys()
    assert "time" in keysofout
    assert "instantaneous_heart_rate" in keysofout
    assert "tachycardia_annotations" in keysofout
    assert "bradycardia_annotations" in keysofout
    assert "average_heart_rate" in keysofout
    assert "averaging_interval" in keysofout
    assert "averaging_period" in keysofout
    assert "averaging_period" == 5
    assert outdict['time'] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
                               25, 26, 27, 28]
    assert outdict["instantaneous_heart_rate"] == [0, 1, 7, 1, 0, -1, 10, 10, 3, 2, 0, 4, 5, 0, 9, 10, 11, 10, 0, 1, 2,
                                                   4, 3, 8.5, 8.6, 8, 1, 2, 3]
    assert outdict['bradycardia_annotations'] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                                  1, 1, 1, 1, 1, 1]
    assert outdict['tachycardia_annotations'] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                  0, 0, 0, 0, 0, 0]
    assert outdict['average_heart_rate'] == [0, 0, 0, 0, 0, 0, 0, 2.5714285714285716, 4.0, 4.2857142857142856, 3.5714285714285716, 3.4285714285714284, 4.0, 4.8571428571428568, 3.4285714285714284, 3.2857142857142856, 4.2857142857142856, 5.5714285714285712, 7.0, 6.4285714285714288, 5.8571428571428568, 6.1428571428571432, 5.4285714285714288, 4.4285714285714288, 4.0714285714285712, 3.8714285714285714, 5.0142857142857142, 5.0142857142857142, 5.0142857142857142]


class MyTestCase(unittest.TestCase):

    def test_valcheckssum(self):
        self.assertRaises(ValueError, ac.check_and_parse_summary(testdictwrongvarnames))

    def test_valchecksave(self):
        self.assertRaises(ValueError,ac.check_and_parse_average(testdictrightsum))