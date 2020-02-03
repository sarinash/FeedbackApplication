import requests, urllib, json, time, demjson, playsound, threading
from statistics import mean
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np


## Target sensor specification
targetSensor = 'xxxx'
peerSensors = ['yyyy', 'zzzz']

## TODO extract the corelation values between the targetSensor and peerSensors,
## and average them at each moment.
## -> 'To what degree the targetSensor is synchronizing with peers in the same group.'

# set corArray
threshUpdate =[]
corArray =[]
avgCorrelationArray =[]

#set counter
# counter = 0

# Variable for keeping time range of the current/previous time window in the correlation array.
iHead = 0
iTail = 0
# iHead_prev = 0
# iTail_prev = 0
tWinHead = time.time()

# duration of the time window to average correlaiton
durWin = 1
#durWin = 3

# threshold for feedback
thres_FB = 0.2

# starttime = time.time()

#epochTime
# starttime = time.time()
# epoch = int(round(starttime*1000))
#print (epoch)
##################################3


## ************************************
# play function
#
def play():
    #if avgCorrelationArray[counter]<0.013:# threshhold
    playsound.playsound('song.mp3', True)


def start_play():
    w = threading.Thread(name='thread_play', target=play)
    w.start()




## ************************************
#crosscorrelation average function
#
#def correlationAverage(counter):
def correlationAverage():

    # Instead of assuming fixed 1000 data points, you need to expect variable length of correlation array.
    # average/mean can be obtained much simpler by a function
    # package numpy
    correlationaverage = mean(corArray[iHead:iTail])
    print("Debug ; #data points = ", (iTail-iHead+1))
    if not avgCorrelationArray:
        print("List is empty")
    else:
        avgCorrelationArray.pop(0)
    avgCorrelationArray.append(correlationaverage)
    #print(correlationaverage)
    print(avgCorrelationArray)




## ************************************
# query correlation to SV server.
#
#buttonClicked = False
def queryCorr(epoch):
    meanCorrArrey=[]

    #GET Value
    url ='http://192.168.13.100/api/correlations/'+str(epoch)
    req=requests.get(url).json()
    r=json.dumps(req)
    r=json.loads(r)
    IDs=r['data']
    cross=IDs['354708094967841']
    crosscorrelation=cross['crosscorrelations']
    # value = crosscorrelation[0]["value"]
    # corArray.append(value)
    ##adding code for atrget sensor data *************************************************************************************
    for i in range(0,len(crosscorrelation)):

        value=crosscorrelation[i]["value"]
        meanCorrArrey.append(abs(value))
        #print(i,value)
    meanvalue=mean(meanCorrArrey)
    corArray.append(meanvalue)
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # TODO extract the corelation values between the targetSensor and peerSensors,
    # and average them at each moment.
    # -> 'To what degree the targetSensor is synchronizing with peers in the same group.'

    #corArray.append(value)
    #print(corArray)



### main process

#if buttonClicked ==False:
    #queryCorr(counter)
#else:
   # print("done")


def threshholdUpdate():

    thres_FB_UP =mean(corArray[len(corArray)-21:len(corArray)-1])


    threshUpdate.append(thres_FB_UP)




for i in range(1,1000000000000):

    # this queryCorr takes longer time than 1 ms
    # To be real-time, spent time should be changed instead of count.
    currentTime = time.time()
    epoch = int(round(currentTime*1000))
    queryCorr(epoch)
    iTail += 1
    if  len(corArray)%30==0:
        threshholdUpdate()
        thres_FB_UP=threshUpdate[-1]

        thres_FB = thres_FB_UP%0.1






    if currentTime - tWinHead > durWin and iTail > iHead:
        correlationAverage()
        print("thresh",thres_FB)
        if avgCorrelationArray[0] > thres_FB:
#            play()
            start_play()
            print(avgCorrelationArray)



        tWinHead = tWinHead + 1
        iHead = iTail + 1
        iTail = iHead
    df = pd.DataFrame({'threshold':threshUpdate})
    writer =ExcelWriter('xxx.xlsx')


    df.to_excel(writer,'sheet1',index=False)
    writer.save()
