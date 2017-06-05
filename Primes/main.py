from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Embedding, SimpleRNN
import numpy as np
import random
import time
import primes
import os.path
import primefactors

DATA_LIMIT = 5000
data_main = primefactors.primesonly(DATA_LIMIT, 2)

print(data_main[-1][0])

MAX_DIGITS = len(str(data_main[-1][0]))+1
STEPS = 1000

print(len(data_main), MAX_DIGITS)

data1 = data_main[0:-1]
data2 = data_main[0:-1]
data3 = data_main[0:-1]


def prime_to_array(prime, number_of_digits):
    outputSplitList = list(0.0 for d in range(0,number_of_digits))
    outputSplitListLen = len(outputSplitList)

    primeStringList = list((float(d) / 10.0) for d in str(prime))
    primeStringLen = len(primeStringList)

    index = outputSplitListLen - primeStringLen
    for digit in primeStringList:
        outputSplitList[index] = digit
        index += 1

    return outputSplitList


def getNewData(mixedData):
    global MAX_DIGITS
    primes_list = list(map(lambda x: x[0], mixedData))
    fullData = list(map(lambda (i,x): prime_to_array(x, MAX_DIGITS), enumerate(primes_list)))
    inData = fullData[2:(len(fullData)-2)]
    outData = fullData[3:(len(fullData)-1)]

    return (inData, outData)

def generateNewModel():
    global MAX_DIGITS
    model = Sequential()
    # model.add(Dense(60, input_dim=MAX_DIGITS, kernel_initializer="random_uniform", activation='sigmoid'))
    # model.add(Embedding(256, 128, input_length=MAX_DIGITS))
    # model.add(Dense(512, input_dim=MAX_DIGITS, activation='sigmoid'))
    model.add(Embedding(2, 2, input_length=MAX_DIGITS))
    model.add(LSTM(512))
    # model.add(Dense(256, activation='softmax'))
    model.add(Dense(MAX_DIGITS, activation='softmax'))
    model.summary()
    return model

def train(model, inData, outData, testInData, testOutData):
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    model.fit(inData, outData, epochs=1000, batch_size=5)
    return model

def hardTest(model):
    global data1
    print("Saved model seems super accurate. Lets test it.");
    loops = 50
    while loops > 0:
        loops -= 1
        testdataz = getNewData(data1)
        testInData = testdataz[0]
        testOutData = testdataz[1]
        scores = model.evaluate(testInData,testOutData)
        print('Test score: ', scores[1])

    return model

def cycle(forcenew = False):
    global data2, data3

    dataz = getNewData(data2)
    inData = dataz[0]
    outData = dataz[1]

    testdataz = getNewData(data3)
    testInData = testdataz[0]
    testOutData = testdataz[1]

    saved_model = None
    saved_score = 0

    saved_model_filename = 'saved_models/saved_model_lstm.h5'

    if os.path.isfile(saved_model_filename):
        saved_model = load_model(saved_model_filename)
        saved_model_scores = saved_model.evaluate(inData,outData)
        saved_score = saved_model_scores[1]
        print("\n\nBase Metric -- \n%s: %.10f%%" % (saved_model.metrics_names[1], saved_score*100))
    else:
        forcenew = True

    if saved_score > 0.99:
        return hardTest(saved_model)

    if forcenew:
        model = train(generateNewModel(), inData, outData, testInData, testOutData)
        print("\n\nForcibly Get New Model!")
    else:
        model = train(saved_model, inData, outData, testInData, testOutData)

    scores = model.evaluate(testInData,testOutData)
    new_score = scores[1]

    if saved_model:
        print("\n\nOld Metric -- \n%s: %.10f%%" % (saved_model.metrics_names[1], saved_score*100))
    print("\n\nFinal Metric -- \n%s: %.10f%%" % (model.metrics_names[1], new_score*100))
    print("\n\nCompare Scored Metric -- %.10f%% vs: %.10f%%" % (saved_score*100, new_score*100))

    final_score = saved_score;

    if saved_score < new_score:
        final_score = new_score
        model.save(saved_model_filename)
        print("\n\nSaved Model!")

    time.sleep(5)
    cycle(final_score < 0.6)

cycle(True)
