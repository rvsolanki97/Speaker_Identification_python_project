##################################
import glob
import os
import sys
import time
import tkinter as tk
import warnings
import wave
from shutil import copyfile
from tkinter import filedialog

import matplotlib.pyplot as plt
import numpy as np
import winsound

#################################

# For Ignoring the Deprecated Function Warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

###############################
# this Fun will Plot the Wave of the Select File By User
def plotWave(dir):
    spf = wave.open(dir, "r")

    # Extract Raw Audio from Wav File
    signal = spf.readframes(-1)
    signal = np.fromstring(signal, "Int16")  # Int16 Will Store More Range of Numbers From Numpy

    # If MONO
    if spf.getnchannels() == 2:
        print("Mono files")

    plt.figure(1)
    plt.title("Signal Wave...")
    plt.plot(signal)
    plt.show()
    plt.close()

###########################################
# this Function Will Match The signals in 3 Different Patterns and return True on
# matching 1 of the Pattern (matching from start, end match, full match ) and give output
def matchingMaxProb(wav1,wav2):
    count:int=0
    itr2=0
    val:int =int(wav1.size/2)
    #End(half) Match
    for itr1 in range(val,wav1.size):
        if itr1<wav2.size:
            if wav1[itr1]==wav2[itr2]:
                count+=1
        itr2+=1
    # if 1/4 Result is Same there is A good Enough Probability to be Matched function
    if count< (wav1.size/4):
        count=0
        itr2=0
        # Full Match
        for itr1 in range(0, wav1.size):
            if itr1 < wav2.size:
                if wav1[itr1] == wav2[itr2]:
                    count += 1
            itr2 += 1
    else:
        return True
    ## if Full Match is 1/2 Macthed Then 50% probability to be Matched
    if count<(wav1.size/2):
        count = 0
        itr2 = 0
        #Start(half) Match
        for itr1 in range(0, val):
            if itr1 < wav2.size:
                if wav1[itr1] == wav2[itr2]:
                    count += 1
            itr2 += 1
        # if 1/4 Result is Same there is A good Enough Probability to be Matched
        if count>(wav1.size/4):
            return True
    else:
        return True
    return False

##############################
# DailogBox to Select File
root = tk.Tk()
root.withdraw()
data =filedialog.askopenfilename()
###########################
#checking extension of the File and Conversion accordingly
check = True
given = ''
if data.partition(".")[2]=="mp3":
    #### If you are Getting Errors then just Try the .wav files Your System Path(ffmpeg/bin)missing
    #### or your ffprobe is missing .. You can Convert Any File From This site https://online-audio-converter.com/

    ## These Lines Will convert The .mp3 file to .wav file For Fast comparison
    given = data.partition(".")[0] + ".wav"
    #sound=AudioSegment.from_mp3(data).export(data.partition(".")[0]+".wav",format="wav")
elif data.partition(".")[2]=='wav':
    given = data
else:
    # if Other Then mp3 or wav file is given It will not go further
    check = False
##################################
if check:
    i = 0
    dirt = []
    names = []
    files = []
    plotWave(given) ## function Call
    prnt_dir = 'D:/ravi project/wavfiles'  ## You can Change It by Yourself( Parent Directory)
    w2 = wave.open(given,'r')
    signal2 = w2.readframes(-1)
    signal2 = np.frombuffer(signal2,"Int16")
    flag = False
    for root, dirs, _ in os.walk(prnt_dir):
        for d in dirs:
            dirt.append(os.path.join(root, d))
            names.append(d)
    j = 1
    winsound.PlaySound(given, winsound.SND_ASYNC | winsound.SND_ALIAS)  # Playing Sound Asyn mode
    for dir in dirt:
        print("\nMatching with " + names[i] + " Data", end=""),
        for file in glob.glob(os.path.join(dir, '*.wav')):
            print(".", end=""),
            w = wave.open(file, 'r')
            signal = w.readframes(-1)
            signal = np.frombuffer(signal, "Int16")

            if matchingMaxProb(signal,signal2):
                ### For Additional Dir It Will Show The File Name
                ### Otherwise It tend to show the Directory Name
                if names[i]=='Additional':
                    print("\nMatched!! Its -> " + file.partition(names[i]+"\\")[2])
                else:
                    print("\nMatched!! Its -> "+names[i])
                flag=True
                break
            w.close()
            j += 1
        if flag:
            break
        else:
            i += 1
    #####################################################
    #If Data is Not Find In the DateBase it Will Keep the File In the Additional Folder
    #And Ask the user Give a Name to That File
    if flag == False:
        print("\nSorry! Can't Find it in the DataBase")
        print("Learning...")
        path=os.path.join(prnt_dir,'Additional')
        ###Checking If the Dir Additional Exists
        try:
            os.makedirs(path, exist_ok=True)
            print("Additional Directory Created.")
        except OSError as error:
            print("")
        name=input("Enter File Name : ")
        #Copying The File to its dataBase
        copyfile(given,path+"/"+name+".wav")

    else:
        print("Thank You!!!")
        time.sleep(12)
else:
    print("Only .wav and .mp3 files Are Acceptable....")
    sys.exit()