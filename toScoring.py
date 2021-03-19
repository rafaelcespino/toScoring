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
    results = resMat['result']
    results = np.array(results)
    results = results[0]

    #lists of start and end times for speech and silence moments 


    arraySize = results.size
    output = open('./txtLabels/{}.txt'.format(fileName), 'w')
    nonSpeechLine = "X\tX\tX\tSAD\tX\t{}\t{}\tnon-speech\t0.500000\n"
    speechLine = "X\tX\tX\tSAD\tX\t{}\t{}\tspeech\t0.500000\n"

    if(results[0] == 0):
        isSilence = True
        lastSilenceStart = 0
        for index, result in enumerate(results):

            #switching from silence to speech 
            if isSilence and result == 1:
                isSilence = False
                silenceEnd = round(((index - 1)/8000), 2)
                output.write(nonSpeechLine.format(lastSilenceStart, silenceEnd))
                lastSpeechStart = round(((index-1)/8000),2)
                isSilence = False

            #switching from speech to silence 
            if not isSilence and result == 0:
                isSilence = True
                speechEnd = round(((index - 1)/8000), 2)
                output.write(speechLine.format(lastSpeechStart, speechEnd))
                lastSilenceStart = round(((index-1)/8000),2)
                isSilence = True

            #if silence until the end of the file
            if isSilence and index == arraySize-1:
                silenceEnd = round(((index - 1)/8000), 2)
                output.write(nonSpeechLine.format(lastSilenceStart, silenceEnd))
                break

            #if speech until the end of the file 
            if not isSilence and index == arraySize-1:
                speechEnd = round(((index - 1)/8000), 2)
                output.write(speechLine.format(lastSpeechStart, speechEnd))
                break




