from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense
import numpy as np
import random
import time
import primes


inData = list()
outData = list()

def getNewData():
    global inData, outData
    mixedData = primes.mixedData()
    random.shuffle(mixedData)

    inData = list(map(lambda x: x[0], mixedData))
    outData = list(map(lambda x: x[1], mixedData))

    print inData[1]
    print outData[1]

    return (inData, outData)

def generateNewModel():
    model = Sequential()
    model.add(Dense(random.randint(3,30), input_dim=3, kernel_initializer="random_uniform", activation='relu'))
    model.add(Dense(random.randint(50,500), activation='relu'))
    model.add(Dense(random.randint(50,500), activation='softmax'))
    model.add(Dense(random.randint(50,500), activation='softmax'))
    model.add(Dense(1, activation='sigmoid'))
    return model

def train(model):
    global inData, outData
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    model.fit(inData, outData, epochs=100, batch_size=100, shuffle=True)
    return model

def cycle(forcenew = False):
    dataz = getNewData()
    inData = dataz[0]
    outData = dataz[1]

    testdataz = getNewData()
    testInData = dataz[0]
    testOutData = dataz[1]

    saved_model = load_model('saved_model.h5')
    saved_model_scores = saved_model.evaluate(inData,outData)
    saved_score = saved_model_scores[1]
    print("\n\nBase Metric -- \n%s: %.10f%%" % (saved_model.metrics_names[1], saved_score*100))

    if forcenew:
        model = train(generateNewModel())
        print("\n\nForcibly Get New Model!")
    else:
        model = train(saved_model)

    scores = model.evaluate(testInData,testOutData)
    new_score = scores[1]

    print("\n\nOld Metric -- \n%s: %.10f%%" % (saved_model.metrics_names[1], saved_score*100))
    print("\n\nFinal Metric -- \n%s: %.10f%%" % (model.metrics_names[1], new_score*100))
    print("\n\nCompare Scored Metric -- %.10f%% vs: %.10f%%" % (saved_score*100, new_score*100))

    final_score = saved_score;

    if saved_score < new_score:
        final_score = new_score
        model.save('saved_model.h5')
        print("\n\nSaved Model!")

    time.sleep(5)
    cycle(final_score < 60)

cycle()
