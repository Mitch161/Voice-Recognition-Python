#Imported Modules
import pyaudio
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as Animation
import matplotlib.patches
from matplotlib import style
style.use("ggplot")
import time
import string
import pyaudio
import wave
import tkinter as tk
from tkinter import ttk
from tkinter import TclError
from database import Database
from speech_recognition import SpeechRecognition
from commands_file import Commands

#Constants----------------------------------------------
#These are repsonsible for the pre derfined areas of the wave form graph, allowing it to be created everytime without
#change. Due to them being global constants, the graph can easily be constructed and none of the values should be
#accidently change.
LARGE_FONT = ("roboto", 16)
TOP_FONT = ("roboto", 32)
LEFT_FONT = ("Roboto", 16)

CHUNK = 1024 * 2
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
f = Figure(figsize=(15, 7), dpi=100)
f.set_facecolor('white')#2f2f2f
a = f.add_subplot(111)

#ca = f.add_subplot(111)
#r = 5
#t = np.arange(0,2*np.pi,.01)
#cy = r*np.sin(t)
#cx = r*np.cos(t)
#c_line, = ca.plot(cx, cy)

x = np.arange(0, 2 * CHUNK, 2)
line, = a.plot(x, np.random.rand(CHUNK), '-', lw=2)

a.set_xlabel('samples')
a.set_ylabel('volume')
a.set_ylim(-4000, 4000)
a.set_xlim(0, 2 * CHUNK)
a.xaxis.set_visible(False)
a.yaxis.set_visible(False)
a.set_facecolor('white')
#a.xaxis.cla()
#a.yaxis.cla()
#-----------------------------------------------------
#Mainc calling class in this file that is responsible for creating the whole GUI of the main program
#The advantage to this is that this class acts as a super class to all other classes in the file, allowing for other
#classes/frames to call from or override from AudioGui. Not only that, but by using this system composition aggregation
#and inheritance can be used between the classes. This is the same with interface_gui.py
class AudioGui(tk.Tk):#tk.Tk
    def __init__(self,firstname,surname,userid,username,password, *args, **kwargs):
        #initilise class from neural network
        self.ai = SpeechRecognition()
        #Create window for gui
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default="")
        tk.Tk.wm_title(self, "Voice Recognition")
        width = tk.Tk.winfo_screenwidth(self)
        height = tk.Tk.winfo_screenheight(self)
        res = str(width)+"x"+str(height)
        tk.Tk.geometry(self,res)
        #create container within window that will allow other frames/classes to be displayed
        container = tk.Frame(self)
        container.configure(background='white') #1d1e21
        container.pack(side="top", fill="both",expand=True)
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(3, weight=1)
        container.grid_columnconfigure(2, weight=1)
        #Creates the microphone input so it can connect with the program and be displayed on the graph, creating the
        #waveform
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            output=True,
            frames_per_buffer=CHUNK
        )

        self.firstname = firstname
        self.surname = surname
        self.userid = userid
        self.username = username
        self.password = password
        print("You are in AudioGui: ",self.firstname, " ", self.surname)

        #More advanced system to the show frames function list. This time many conditions have been put in place
        #to give greater control over how i construct the GUI, allowing me to place frames in specific loctaions within
        #container of AudioGui. This trys to replicate modern layouts but not enough time was avaliable.
        self.frames = {}
        for F in (LiveAudio, TopFrame, WestFrame, ProfileFrame, OptionsFrame):
            if F == ProfileFrame:
                frame = F(container, self,  self.firstname, self.surname, self.userid, self.username, self.password)
                self.frames[F] = frame
                frame.grid(row=2, column=1, sticky="nsew")
            else:
                frame = F(container, self)
                self.frames[F] = frame
                if F == LiveAudio:
                    frame.grid(row=2, column=1, sticky="nsew")
                elif F == TopFrame:
                    frame.grid(row=0, column=0, sticky="new", columnspan=3)
                elif F == WestFrame:
                    frame.grid(row=1, column=0, sticky="nsw", rowspan=5)
                elif F == OptionsFrame:
                    frame.grid(row=2, column=1, sticky="nsew")
                else:
                    print("Error with Frame display")
        self.show_frame(LiveAudio)

    #Public Functions

    #Artifical Intelegence--------------------------------------------------------------------------------------------
    #This area of code creates the object for the speech recongition program within speech_recognition
    #It also contains the code for the queue that will execute the commands and read all strings within it one by one
    #as well as allowing for the model to be trained further is needed with train_RNN
    def call_iris(self):
        queue = []
        cmd= ["open","close","exit","use","search","play","history","profile","logout"]
        ai = SpeechRecognition()
        model = ai.load_model()
        ai.audio_to_spectrogram()
        words = ai.predict_model(model)
        wordlist = str(words).split()
        for word in wordlist:
            queue.append(word)
        for amount in queue:
            for check in cmd:
                if amount == check:
                    command = amount
                elif amount !=check:
                    action = amount
                elif amount.endswith(".txt") or amount.endswith(".png") or amount.endswith(".jpg"):
                    query = amount
                else:
                    print("error")
                    command =""
                    action=""
                    query=""

        ai.commands(command,action,query,"/home/mitchell/", "/home/")
    def train_RNN(self):
        ai = SpeechRecognition()
        ai.neural_network()
    #-----------------------------------------------------------------------------------------------------------------

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    #This function is responsible for the creation of the waveform on the graph, ensuring that it accuratly reproduces it
    def animate(self, i):
        frame_count = 0
        start_time = time.time()
        data = self.stream.read(CHUNK)
        data_int = np.fromstring(data, dtype=np.int16)
        line.set_ydata(data_int)
        try:
            frame_count += 1
        except TclError:
            frame_rate = frame_count / (time.time() - start_time)
            print("stream stopped")
            print("average frame rate = {:.0f} FPS".format(frame_rate))
        return line

    #Getters and Setters
    def get_f(self):
        return f

    def set_firstname(self, firstname):
        self.firstname = firstname
    def get_firstname(self):
        return self.firstname

    def set_surname(self, surname):
        self.surname = surname
    def get_surname(self):
        return self.surname

    def set_username(self, username):
        self.username = username
    def get_username(self):
        return self.username

    def set_password(self, password):
        self.password = password
    def get_password(self):
        return self.password

    #Microphone Recording System-------------------------------------------------------------------------------------
    #Once the record button is pushed this function is executed and the microphone will begin to capture and save the
    #audio file into the correct direcotry. Not only that, but all audio is saved .wav file.
    def micOnOff(self, option):
        if option == True:
            FORMAT = pyaudio.paInt16
            CHANNELS = 2
            RATE = 44100
            CHUNK = 1024
            RECORD_SECONDS = 5
            WAVE_OUTPUT_FILENAME = "/home/mitchell/Documents/speech_data_files/user_audio/user_input.wav"

            audio = pyaudio.PyAudio()

            # start Recording
            stream = audio.open(format=FORMAT, channels=CHANNELS,
                                rate=RATE, input=True,
                                frames_per_buffer=CHUNK)
            print("Recording...")
            frames = []

            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)
            print("Finished Recording")

            # stop Recording
            stream.stop_stream()
            stream.close()
            audio.terminate()

            waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            waveFile.setnchannels(CHANNELS)
            waveFile.setsampwidth(audio.get_sample_size(FORMAT))
            waveFile.setframerate(RATE)
            waveFile.writeframes(b''.join(frames))
            waveFile.close()
            self.call_iris()
        else:
            print("Mic transition failed")
    #-----------------------------------------------------------------------------------------------------------------

    def logout_account(self):
        self.destroy()
        print("Logging Out....")
        from main import Main
        login_again = Main()
        login_again.info()

    def quit_program(self):
        self.destroy()

#Class that displays the graph within AudioGui
class LiveAudio(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='white') #2f2f2f

        print("Recording...")

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0)
        canvas.get_tk_widget().configure(highlightcolor='black', highlightbackground='black')

        record = tk.Button(self, text="Record", font=LEFT_FONT, width="6", height="1", highlightthickness=1, highlightbackground='black', background='white', foreground='black', relief='groove'
                           , command=lambda: controller.micOnOff(True))
        record.grid(row=2, column=0, pady=2)

        label = ttk.Label(self, text="Commands List:\n1) OPEN\n2) CLOSE\n3) EXIT\n4) USE\n5) SEARCH\n6) PLAY\n7) HISTORY\n8) PROFILE\n9) LOGOUT", font=TOP_FONT, background='white', foreground='black')
        label.grid(row=0, column=2)

#Class that displays the Top Bar on AudioGui - updated top and side frames to make more appealing and user friendly
class TopFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='#6200EE')

        firstname = controller.get_firstname()
        surname = controller.get_surname()

        label = ttk.Label(self, text=firstname,font=TOP_FONT, background='#000000', foreground='white')
        label.grid(row=1,column=1)
        label2 = ttk.Label(self, text=" ",font=TOP_FONT, background='#000000', foreground='white')
        label2.grid(row=1,column=2)
        label3 = ttk.Label(self, text=surname,font=TOP_FONT, background='#000000', foreground='white')
        label3.grid(row=1,column=3)

        spacelabel = tkk.Label(self, text="           ", font=TOP_FONT, background='#000000', foreground='white')
        spacelabel.grid(row=1,column=5)
        mainlabel = tkk.Label(self, text="Iris", font=TOP_FONT, background='#000000', foreground='white')
        mainlabel.grid(row=1,column=6)



#Class that displays the left hand side bar with button on Audio Gui
class WestFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='#6200EE')

        p_button = tk.Button(self, text="Profile", font=LEFT_FONT, width="6", height="1", highlightthickness=0, highlightbackground='#3e4143', background='#000000', foreground='white', relief='flat'
                             , command=lambda: controller.show_frame(ProfileFrame))
        p_button.grid(row=3, column=0, pady=10)
        s_button = tk.Button(self, text="Settings", font=LEFT_FONT, width="6", height="1", highlightthickness=0, highlightbackground='#3e4143', background='#000000', foreground='white', relief='flat'
                             , command = lambda: controller.show_frame(OptionsFrame))
        s_button.grid(row=5, column=0, pady=10)
        t_button = tk.Button(self, text="Record", font=LEFT_FONT, width="6", height="1", highlightthickness=0, highlightbackground='#3e4143', background='#000000', foreground='white', relief='flat'
                             , command = lambda: controller.show_frame(LiveAudio))
        t_button.grid(row=1, column=0, pady=10)

        div1 = ttk.Separator(self, orient='horizontal')
        div1.grid(row=0,column=0, sticky='ew')
        div2 = ttk.Separator(self, orient='horizontal')
        div2.grid(row=2,column=0, sticky='ew')
        div3 = ttk.Separator(self, orient='horizontal')
        div3.grid(row=4,column=0, sticky='ew')
        div4 = ttk.Separator(self, orient='horizontal')
        div4.grid(row=6,column=0, sticky='ew')
        div5 = ttk.Separator(self, orient='horizontal')
        div5.grid(row=8,column=0, sticky='ew')
        div6 = ttk.Separator(self, orient='horizontal')
        div6.grid(row=10,column=0, sticky='ew')
        div7 = ttk.Separator(self, orient='horizontal')
        div7.grid(row=12,column=0, sticky='ew')

        self.rowconfigure(7, weight=1)
        logout_b = tk.Button(self, text="Logout", font=LEFT_FONT, width="6", height="1", highlightthickness=0, highlightbackground='#3e4143', background='#3e4143', foreground='white', relief='flat',
                             command=lambda: controller.logout_account())
        logout_b.grid(row=9, column=0, pady=10)
        quit_b = tk.Button(self, text="Quit", font=LEFT_FONT, width="6", height="1", highlightthickness=0, highlightbackground='#3e4143', background='#3e4143', foreground='white', relief='flat',
                           command=lambda: controller.quit_program())
        quit_b.grid(row=11,column=0, pady=10)

#Class used to display the Profile Page on AudioGui window as well as being a parent class to ProfileDisplay and
#EditiOptions and ErrorFrame. These three classes are then subclasses to ProfileFrame where ProileFrame is a subclass to
#AudioGui.
#ProfileFrame is therefore responsible for display ProfileDisplay, EditOptions, and ErrorFrame within its self and then
#displaying on AudioGui
class ProfileFrame(tk.Frame, AudioGui):
    def __init__(self, parent, controller, firstname, surname, userid, username, password):
        #Private Variales
        self.firstname = firstname
        self.surname = surname
        self.userid = userid
        self.username = username
        self.password = password
        print("You are in ProfileFrame: ", self.firstname + self.surname)

        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='white', highlightthickness=1, highlightbackground='black')

        container = tk.Frame(self)
        container.configure(background='white')
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(2, weight=1)
        container.grid_columnconfigure(2, weight=1)

        self.frames = {}
        for F in (Editoptions,ProfileDisplay, ErrorFrame):
            if F == ErrorFrame:
                frame = F(container, self)
                self.frames[F] = frame
                frame.grid(row=1, column=1, sticky="s")
            else:
                frame = F(container, self, self.firstname, self.surname, self.userid, self.username, self.password)
                self.frames[F] = frame
                if F == ProfileDisplay:
                    frame.grid(row=1, column=1, sticky="nsew")
                elif F == Editoptions:
                    frame.grid(row=1, column=1, sticky="nsew")
                else:
                    print("Error with Profile Frame display")
        self.show_frame(ProfileDisplay)

    #Public functions that override AudioGui as shown by the symbols next to the line number
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def set_firstname(self, firstname):
        self.firstname = firstname
    def get_firstname(self):
        return self.firstname

    def set_surname(self, surname):
        self.surname = surname
    def get_surname(self):
        return self.surname

    def get_userid(self):
        return self.userid

    def set_username(self, username):
        self.username = username
    def get_username(self):
        return self.username

    def set_password(self, password):
        self.password = password
    def get_password(self):
        return self.password

    def send_info_database(self, firstname, surname, username, password):
        check = self.check_user_details(username, password, firstname, surname)
        if check == True:
            user_edit_options = Database()
            userid = self.get_userid()
            user_edit_options.set_firstname(firstname)
            user_edit_options.set_surname(surname)
            user_edit_options.set_username(username)
            user_edit_options.set_password(password)
            user_edit_options.set_userid_file(userid)
            user_edit_options.set_profileid_file(userid)
            user_edit_options.order_databsae()
            exist = user_edit_options.username_search()
            if exist == True:
                print("Details already exist")
                self.show_frame(ErrorFrame)
            elif exist == False:
                user_edit_options.update_user_info()
                self.set_username(username)
                self.set_password(password)
                self.set_firstname(firstname)
                self.set_surname(surname)
                ProfileDisplay.set_username(self, username)
                ProfileDisplay.set_password(self, password)
                ProfileDisplay.set_firstname(self, firstname)
                ProfileDisplay.set_surname(self, surname)
            else:
                print("Error")
        else:
            print("Username or password is to short and could have wrong characters")
            self.show_frame(ErrorFrame)

    def check_user_details(self, username, password, firstname, surname):
        print("you here")
        invalidChars = set(string.punctuation.replace("_", ""))
        if (len(username) and len(password) >= 8) and (not(any(chr in invalidChars for chr in username))):
            if (not(any(chr in invalidChars for chr in firstname))) and (not(any(chr in invalidChars for chr in surname))):
                return True
            else:
                return False
        else:
            return False

    def delete_account(self):
        user_edit_options = Database()
        user_edit_options.delete_user(self.userid)

#Class used to display User profiles options
class ProfileDisplay(ProfileFrame):
    def __init__(self, parent, controller, firstname, surname, userid, username, password):
        #ProfileFrame.__init__(self, parent,controller, firstname, surname)
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='white', highlightthickness=0, highlightbackground='black')

        #Private Variables
        self.firstname = firstname
        self.surname = surname
        self.userid = userid
        self.username = username
        self.password = password

        #self.test = AudioGui

        label = ttk.Label(self, text="Profile", font=TOP_FONT, background='white', foreground='black')
        label.grid(row=1, column=1)

        fnameL = ttk.Label(self, text="First Name:", font=LARGE_FONT, background='white', foreground='black')
        fnameL.grid(row=3, column=1)
        snameL = ttk.Label(self, text="Surname:", font=LARGE_FONT, background='white', foreground='black')
        snameL.grid(row=4, column=1)
        userL = ttk.Label(self, text="Username:", font=LARGE_FONT, background='white', foreground='black')
        userL.grid(row=5, column=1)
        passwordL = ttk.Label(self, text="Password:", font=LARGE_FONT, background='white', foreground='black')
        passwordL.grid(row=6, column=1)

        ftextL = ttk.Label(self, text=self.firstname, font=LARGE_FONT, background='white', foreground='black')
        ftextL.grid(row=3, column=2)
        stextL = ttk.Label(self, text=self.surname, font=LARGE_FONT, background='white', foreground='black')
        stextL.grid(row=4, column=2)
        utextL = ttk.Label(self, text=self.username, font=LARGE_FONT, background='white', foreground='black')
        utextL.grid(row=5, column=2)
        passtextL = ttk.Label(self, text=self.password, font=LARGE_FONT, background='white', foreground='black')
        passtextL.grid(row=6, column=2)

        edit = tk.Button(self, text="Edit", font=LEFT_FONT, width="6",height="1", highlightthickness=1, highlightbackground='black', background='white', foreground='black', relief='groove',
                         command=lambda: controller.show_frame(Editoptions))
        edit.grid(row=8, column=1, pady=20)

        button9 = tk.Button(self, text="Delete Account", font=LEFT_FONT, height="1", highlightthickness=1, highlightbackground='black', background='white', foreground='black', relief='groove',
                         command=lambda: controller.delete_account())
        button9.grid(row=8, column=2, pady=20)


        #Centers the login menu
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(9,weight=1)
        self.grid_columnconfigure(3,weight=1)

#Class used to display the entry boxes that allow the user to edit their profile options and then send the information
#to the databsae
class Editoptions(ProfileFrame):
    def __init__(self, parent, controller, firstname, surname, userid, username, password):
        #ProfileFrame.__init__(self, parent,controller, firstname, surname)
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='white', highlightthickness=0, highlightbackground='black')
        #Private variables
        self.firstname = firstname
        self.surname = surname
        self.userid = userid
        self.username = username
        self.password = password

        label = ttk.Label(self, text="Profile", font=TOP_FONT, background='white', foreground='black')
        label.grid(row=1, column=1)
        fnameL = ttk.Label(self, text="First Name:", font=LARGE_FONT, background='white', foreground='black')
        fnameL.grid(row=3, column=1)
        snameL = ttk.Label(self, text="Surname:", font=LARGE_FONT, background='white', foreground='black')
        snameL.grid(row=4, column=1)
        userL = ttk.Label(self, text="Username:", font=LARGE_FONT, background='white', foreground='black')
        userL.grid(row=5, column=1)
        passwordL = ttk.Label(self, text="Password:", font=LARGE_FONT, background='white', foreground='black')
        passwordL.grid(row=6, column=1)

        fnameE= tk.Entry(self, font=LARGE_FONT)
        fnameE.grid(row=3, column=2)
        snameE = tk.Entry(self, font=LARGE_FONT)
        snameE.grid(row=4, column=2)
        userE = tk.Entry(self, font=LARGE_FONT)
        userE.grid(row=5, column=2)
        passwordE =tk.Entry(self, font=LARGE_FONT)
        passwordE.grid(row=6, column=2)

        apply = tk.Button(self, text="Apply", font=LEFT_FONT, width="6", height="1", highlightthickness=1,
                         highlightbackground='black', background='white', foreground='black', relief='groove',
                          command=lambda: controller.send_info_database(fnameE.get(), snameE.get(),userE.get(), passwordE.get()))
        apply.grid(row=7, column=1, padx=4, pady=20)
        cancel = tk.Button(self, text="Cancel", font=LEFT_FONT, width="6", height="1", highlightthickness=1,
                         highlightbackground='black', background='white', foreground='black', relief='groove',
                           command=lambda: controller.show_frame(ProfileDisplay))
        cancel.grid(row=7, column=2, padx=4, pady=20)

        #Centers the login menu
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(8,weight=1)
        self.grid_columnconfigure(3,weight=1)

#OptionsFrame is the same as ProfileFrame, whereby it is a subclass to AudioGui but a superclass to Options_buttons.
#This again gives greater control on how the gui is layed out, splitting it into further dimensions - overriding also
#occurs here
class OptionsFrame(tk.Frame, AudioGui):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='white', highlightthickness=1, highlightbackground='black')

        container = tk.Frame(self)
        container.configure(background='white')
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(2, weight=1)
        container.grid_columnconfigure(2, weight=1)

        self.frames = {}
        F = (Options_buttons)
        frame = F(container, self)
        self.frames[F] = frame
        if F == Options_buttons:
            frame.grid(row=1, column=1, sticky="nsew")
        else:
            print("Error with Profile Frame display")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

#Options_buttons is used to display the acutal options that can be change with the program its self
class Options_buttons(OptionsFrame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='white', highlightthickness=0, highlightbackground='black')

        label = ttk.Label(self, text="Options", font=TOP_FONT, background='white', foreground='black')
        label.grid(row=0, column=1)

        label = ttk.Label(self, text="Dark & Light Mode:", font=LEFT_FONT, background='white', foreground='black')
        label.grid(row=1, column=1)

        dl_button = tk.Button(self, text="Mode", font=LEFT_FONT, width="6", height="1", highlightthickness=1,
                         highlightbackground='black', background='white', foreground='black', relief='groove')
        dl_button.grid(row=1, column=2, padx=5)

#Class that displays the error message to the user when they dont enter the correct details into the edit options box
class ErrorFrame(ProfileFrame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='#3e4143')
        label = ttk.Label(self, text="Username or password is to short and could have wrong characters", font=LARGE_FONT, background='white', foreground='black')
        label.grid(row=0, column=0)



















#test = AudioGui("test", "test", 4532)
#ani = Animation.FuncAnimation(f, test.animate, interval=1)
#test.mainloop()