import scipy.io as sio
import numpy as np
import os 

#Load the .mat file as input and store its contents in result
inDir = "./matLabels/"

for file in os.listdir(inDir):
    inputMat = os.path.join(inDir, file)
    fileName = os.path.splitext(file)[0]
    print("Converting {}".format(fileName))
    resMat = sio.loadmat(inputMat)
    result = resMat['result']
    result = np.array(result)
    result = result[0]

    #lists of start and end times for speech and silence moments 
    speechStarts = []
    speechEnds = []
    silenceStarts = []
    silenceEnds = []
    index = 0

    arraySize = result.size
    output = open('./{}.txt'.format(fileName), 'w')


    #if the array starts with silence
    if(result[0] == 0):
        print("Starts in silence")
        silenceStarts.append(0)
        lastSample = 0
        for sample in result:
            index += 1
            #if current sample is speech and the last sample was silence
            if(lastSample == 0 and sample == 1):
                
                speechStarts.append(round((index / 8000),2))  #add current index as a speech start point
                silenceEnds.append(round(((index-1)/8000), 2))
            elif(lastSample == 1 and sample == 0):
                
                silenceStarts.append(round((index / 8000),2)) 
                speechEnds.append(round(((index-1)/8000), 2))

            lastSample = sample

    elif(result[0] == 1):
        print("Starts in speech")
    forIndex = 0

    numSilenceStarts = len(silenceStarts)
    numSilenceEnds = len(silenceEnds)

    forIndex = 0
    if(result[0] == 0):
        if(numSilenceStarts > numSilenceEnds):
            for silenceStart in silenceStarts:
                if forIndex < numSilenceStarts-1:
                    output.write("X\tX\tX\tSAD\tX\t{}\t{}\tnon-speech\t0.500000\n".format(silenceStart, silenceEnds[forIndex]))
                    output.write("X\tX\tX\tSAD\tX\t{}\t{}\tspeech\t0.500000\n".format(speechStarts[forIndex], speechEnds[forIndex]))
                elif forIndex == numSilenceStarts-1:
                    output.write("X\tX\tX\tSAD\tX\t{}\t{}\tnon-speech\t0.500000".format(silenceStart, round((arraySize/8000),2)))
                forIndex += 1