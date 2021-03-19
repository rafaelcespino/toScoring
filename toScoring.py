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




'''
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
                '''