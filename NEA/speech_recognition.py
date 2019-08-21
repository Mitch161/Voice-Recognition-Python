#Imported Modules
from __future__ import division, print_function, absolute_import
import os
import cv2
import numpy as np
import pylab
import wave
from gtts import gTTS
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import tflearn
import speech_data
import tensorflow as tf
#from tensorflow import keras
from keras.models import load_model, save_model
from commands_file import Commands

#Main class responsible for allowing all nerual network a deep learning system to function
class SpeechRecognition():
    def __init__(self):
        #Private variables
        self.categories = ["open", "close", "exit", "use", "search", "play", "history", "profile", "logout", "yes", "no",
                           "backward", "down", "eight", "five", "forward", "four", "go", "left", "nine", "off", "on", "one",
                           "right", "seven", "six", "stop", "three", "two", "up", "zero"]
        #self.categories = ["yes", "no"]
        self.filepath = '/home/mitchell/Documents/speech_data_files/models/test/my_model'
        #self.audiopath = '/home/mitchell/Documents/speech_data_files/yes/test/1.wav'
        self.audiopath = '/home/mitchell/Documents/speech_data_files/user_audio/user_input.wav'
        self.imgpath = '/home/mitchell/Documents/speech_data_files/spectrograms/spectrogram_v0.png'
        self.command_dict = {}
        self.cmd = Commands()

    #Public Functions
    def neural_network(self):
        # Hyperparameters
        learning_rate = 0.0001  # lower = more accuracy
        # For testing and nea reasons this is set to a lower value so that it can complete, in practice this would be 300000 steps.
        training_iters = 150  # training steps
        batch_size = 64

        width = 20  # mfcc features
        height = 80  # (max) length of utterance
        classes = 10  # amount of digits

        batch = word_batch = speech_data.mfcc_batch_generator(batch_size)
        X, Y = next(batch)
        trainX, trainY = X, Y
        testX, testY = X, Y  # overfit for now

        # Network building
        net = tflearn.input_data([None, width, height])
        net = tflearn.lstm(net, 128, dropout=0.8)
        net = tflearn.fully_connected(net, classes, activation='softmax')
        net = tflearn.regression(net, optimizer='adam', learning_rate=learning_rate, loss='categorical_crossentropy')

        # Training
        # tflearn_logs is the folder location
        model = tflearn.DNN(net, tensorboard_verbose=0)
        for iters in range(training_iters):  # training_iters
            model.fit(trainX, trainY, n_epoch=10, validation_set=(testX, testY), show_metric=True,
                      batch_size=batch_size)  # n_epoch the amount of iterations it will do per loop
            _y = model.predict(X)
        model.save("/home/mitchell/Documents/speech_data_files/models/my_model")
        # save_model(model,"/home/mitchell/Documents/speech_data_files/models/my_model", overwrite=True, include_optimizer=True)
        print(_y)

    #Load model function that is responsbile for loading models from the correct directory
    def load_model(self):
        print("Loading Model...")
        net = tflearn.input_data([None, 20, 80])
        net = tflearn.lstm(net, 128, dropout=0.8)
        net = tflearn.fully_connected(net, 10, activation='softmax')
        net = tflearn.regression(net, optimizer='adam', learning_rate=0.0001, loss='categorical_crossentropy')
        model = tflearn.DNN(net, tensorboard_verbose=0)
        model.load(self.filepath, weights_only=True)
        print("Successfully Loaded")
        return model

    #-------------------------------------------------------------------------------------------------------------------
    #Audio spectrogram converter that is responsible for ensuring that all user input data is converted into the correct
    #format.
    def audio_to_spectrogram(self):
        sound_info, frame_rate = self.get_wav_info(self.audiopath)
        fig = pylab.figure(num=None, figsize=(19, 12))
        pylab.subplot(111)
        pylab.axes([0, 0, 1, 1])
        pylab.axis('off')
        pylab.specgram(sound_info, Fs=frame_rate)
        filename = "/home/mitchell/Documents/speech_data_files/spectrograms/spectrogram_v0"
        pylab.savefig(filename)
    def get_wav_info(self, wav_file):
        wav = wave.open(wav_file, 'r')
        frames = wav.readframes(-1)
        sound_info = pylab.fromstring(frames, 'int16')
        frame_rate = wav.getframerate()
        wav.close()
        return sound_info, frame_rate
    #-------------------------------------------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------------------------------------------
    #Function used to predict the model against the spectorgram image, giving of good to okay accuaracy during testing
    #runs
    def predict_model(self, model):
        prediction = model.predict([self.prepare(self.imgpath)])
        print(self.categories[int(prediction[0][0])])
        return (self.categories[int(prediction[0][0])])
    def prepare(self, filepath):
        img_width = 20
        img_height = 80
        img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        new_array = cv2.resize(img_array, (img_width, img_height))
        # return new_array.reshape(-1, img_size,img_size, 1)
        return new_array.reshape(img_width, img_height)
    #-------------------------------------------------------------------------------------------------------------------

    #Commands fucntions allows communication between the commands_file.py and the current file
    def commands(self,speech_data, action, query, filepath, prev_path):
        file = self.read_command()
        lines = file.readlines()
        for amount in lines:
            self.command_dict[(amount.rstrip("\n"))] = (amount.lower().rstrip("\n"))
        try:
            current_cmd = self.command_dict[speech_data.upper()]
            if speech_data == current_cmd:
                if speech_data == "open" or speech_data == "close" or speech_data == "exit" or speech_data == "use" or speech_data == "search" or speech_data == "play":
                    speech_data = (speech_data+"ing ", action)
                    self.speak_words(speech_data)
                    self.cmd.command_picker(current_cmd, action, query, filepath, prev_path)
                elif speech_data == "history" or speech_data == "profile" or speech_data == "logout":
                    speech_data = ("opening ", speech_data)
                    self.speak_words(speech_data)
                    self.cmd.command_picker(current_cmd, action, query, filepath, prev_path)
                else:
                    print("Error")
                    self.speak_words("Error")
            else:
                print("Invaild command entered")
                self.speak_words("Invalid command entered")
        except:
            print("Invalid command entered")
            self.speak_words("Invalid command entered")

    #Read and write command are used to ensure that the commands_file exists and then read from it so the commands fucntion
    #can execute it accordingly within its dictionsry
    def write_command(self):
        file = open("/home/mitchell/Documents/speech_data_files/commands/commands_list.txt","w")
        file.write("OPEN\nCLOSE\nEXIT\nUSE\nSEARCH\nPLAY\nHISTORY\nPROFILE\nLOGOUT")
        return file
    def read_command(self):
        create = False
        while create == False:
            try:
                file = open("/home/mitchell/Documents/speech_data_files/commands/commands_list.txt","r")
                print("Reading commands_list.txt...")
                create = True
            except:
                print("Creating commands_list.txt...")
                file = self.write_command()
                file.close()
        return file

    #Function used to turn text into speach
    def speak_words(self, command):
        tts = gTTS(str(command), lang='en')
        tts.save("/home/mitchell/Documents/speech_data_files/voice_commands/voice_command.mp3")
        os.system("mpg321 /home/mitchell/Documents/speech_data_files/voice_commands/voice_command.mp3")























categories = ["Yes","No"]
filepath = '/home/mitchell/Documents/speech_data_files/models/my_model'
audiopath = '/home/mitchell/Documents/speech_data_files/yes/test/1.wav'
imgpath = '/home/mitchell/Documents/speech_data_files/spectrograms/spectrogram_v0.png'

def graph_spectrogram(wav_file):
    #amount = len([name for name in os.listdir('/home/mitchell/Documents/speech_data_files/spectrograms') if os.path.isfile(name)])
    sound_info, frame_rate = get_wav_info(wav_file)
    fig = pylab.figure(num=None, figsize=(19, 12))
    pylab.subplot(111)
    pylab.axes([0, 0, 1, 1])
    pylab.axis('off')
    pylab.specgram(sound_info, Fs=frame_rate)
    filename = "/home/mitchell/Documents/speech_data_files/spectrograms/spectrogram_v0"
    pylab.savefig(filename)
def get_wav_info(wav_file):
    wav = wave.open(wav_file, 'r')
    frames = wav.readframes(-1)
    sound_info = pylab.fromstring(frames, 'int16')
    frame_rate = wav.getframerate()
    wav.close()
    return sound_info, frame_rate

def predict_model(model, filepath):
    prediction = model.predict([prepare(filepath)])
    print(categories[int(prediction[0][0])])
def prepare(filepath):
    img_width = 20
    img_height = 80
    img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array,(img_width,img_height))
    #return new_array.reshape(-1, img_size,img_size, 1)
    return new_array.reshape(img_width,img_height)

def speak_words(command):
    tts = gTTS(str(command), lang='en')
    tts.save("/home/mitchell/Documents/speech_data_files/voice_commands/voice_command.mp3")
    os.system("mpg321 /home/mitchell/Documents/speech_data_files/voice_commands/voice_command.mp3")

def summ():
    print("Loading Model...")
    net = tflearn.input_data([None, 20, 80])
    net = tflearn.lstm(net, 128, dropout=0.8)
    net = tflearn.fully_connected(net, 10, activation='softmax')
    net = tflearn.regression(net, optimizer='adam', learning_rate=0.0001, loss='categorical_crossentropy')
    #tf.reshape(net, (-1, -1, 20, 80, -1))
    model = tflearn.DNN(net, tensorboard_verbose=0)
    model.load('/home/mitchell/Documents/speech_data_files/models/my_model', weights_only=True)
    print("Sucessfully Loaded")
    #saved_model_path = tf.contrib.saved_model.save_keras_model(model, "./saved_models")
    #model.load('/home/mitchell/Documents/speech_data_files/models/my_model.h5')
    #model.summary()
    return model

def main():
    #Hyperparameters
    learning_rate = 0.0001 #lower = more accuracy
    #For testing and nea reasons this is set to a lower value so that it can complete, in practice this would be 300000 steps.
    training_iters = 500  #training steps
    batch_size = 64

    width = 20  # mfcc features
    height = 80  # (max) length of utterance
    classes = 10  # amount of digits

    batch = word_batch = speech_data.mfcc_batch_generator(batch_size)
    X, Y = next(batch)
    trainX, trainY = X, Y
    testX, testY = X, Y #overfit for now

    # Network building
    net = tflearn.input_data([None, width, height])
    net = tflearn.lstm(net, 128, dropout=0.8)
    net = tflearn.fully_connected(net, classes, activation='softmax')
    net = tflearn.regression(net, optimizer='adam', learning_rate=learning_rate, loss='categorical_crossentropy')

    # Training
    #tflearn_logs is the folder location
    model = tflearn.DNN(net, tensorboard_verbose=0)
    for iters in range(training_iters): #training_iters
      model.fit(trainX, trainY, n_epoch=10, validation_set=(testX, testY), show_metric=True,
              batch_size=batch_size) #n_epoch the amount of iterations it will do per loop
      _y=model.predict(X)
    model.save("/home/mitchell/Documents/speech_data_files/models/my_model")
    #save_model(model,"/home/mitchell/Documents/speech_data_files/models/my_model", overwrite=True, include_optimizer=True)
    print(_y)

#ai = SpeechRecognition()
#ai.neural_network()
#model = ai.load_model()
#ai.audio_to_spectrogram()
#ai.predict_model(model)

#ai.commands("open", "google", "", "", "")
#ai.commands("close", "google")
#ai.commands("use", "google", "youtube")
#ai.commands("search", "","commands_list.txt", "/home/mitchell/Documents/", "/home/mitchell/")
#ai.commands("play","","youtube nyan cat","","")
#cmd = Commands()

#speak_words("hello, i am Iris")
#speak_words("yeet")





#main()
#model = summ()
#graph_spectrogram(audiopath)
#predict_model(model, imgpath)