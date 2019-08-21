#Interface Devlopment
#Date - 19/10/2018
#Mitchell Hardie

#Imported Modules
import tkinter as tk
import time as t
from tkinter import ttk
import string
from database import Database
from user_login import LoginProcess
from voice_recording import AudioGui
from voice_recording import LiveAudio
from user_login import ButtonFrame

#Constants
LARGE_FONT = ("roboto", 16)
#Program - Main calling class that acts as super class to all classes in this file and user_login.py
class InterfaceDisplay(tk.Tk):
    def __init__(self, *args, **kwargs):
        #Creates the main window application
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default="")
        tk.Tk.wm_title(self, "Speech Recognition Ai")
        width = tk.Tk.winfo_screenwidth(self)
        height = tk.Tk.winfo_screenheight(self)
        res = str(width)+"x"+str(height)
        tk.Tk.geometry(self,res)
        #Container for frame where all other frames, buttons, labels etc will go
        container = tk.Frame(self)
        container.pack(side="top", fill="both",expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        #Variables - Private
        self.username = ""
        self.password = ""
        self.firstname = ""
        self.surname = ""
        self.pressed = False
        self.closed = True
        self.userid = 0
        #Frame system - this works by creating a list of all classes that are subclasses to the super class,
        #lopping through them one by one to load them, and then display them on screen when they are called.
        #Helps add the contraints and display locations of frames(classes)
        self.frames = {}
        for F in (LoginPage, PageOne, CreateAccount, LoginProcess, ButtonFrame, ErrorFrame):
            if F == ErrorFrame:
                frame = F(container, self)
                self.frames[F] = frame
                frame.grid(row=0, column=0, sticky="s", pady=300)
            else:
                frame = F(container,self)
                self.frames[F] = frame
                frame.grid(row=0, column=0,sticky="nsew")
        self.show_frame(LoginPage)

    #Functions - Public
    #Responsible for displaying the frames, can be called anywhere or overriden
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    #Login screen
    #Checks user details and then displays loading screen if correct
    def login_to_account(self,usernameE,passwordE):
        username = usernameE.get()
        password = passwordE.get()
        self.set_username(username)
        self.set_password(password)
        #self.destroy()
        LoginProcess.set_username(self,username)
        LoginProcess.set_password(self,password)
        LoginProcess.test(self)
        correct = LoginProcess.login_request(self)
        if correct == True:
            LoginProcess.get_fs_name(self)
            self.show_frame(LoginProcess)
            self.show_frame(ButtonFrame)
            self.closed = False
        elif correct == False:
            print("Try again")
            self.show_frame(ErrorFrame)
        else:
            print("Error")
            self.show_frame(ErrorFrame)

    #Create Account Screen
    #Ensures that the details entered to create an account are correct and dont repeat usernames in the database
    def send_to_database(self,usernameE,passwordE,firstnameE,surnameE):
        username = usernameE.get()
        password = passwordE.get()
        firstname = firstnameE.get()
        surname = surnameE.get()
        check = self.check_user_details(username, password, firstname, surname)
        if check == True:
            self.set_username(username)
            self.set_password(password)
            self.set_firstname(firstname)
            self.set_surname(surname)
            self.pressed = True
            #self.show_frame(LoginProcess)
            #self.show_frame(ButtonFrame)
            self.closed = False
            new_account = Database()
            new_account.set_username(username)
            new_account.set_password(password)
            new_account.set_firstname(firstname)
            new_account.set_surname(surname)
            new_account.order_databsae()
            user_check = new_account.check_existing_accounts()
            if user_check == True:
                print("Try Again")
            elif user_check == False:
                print("Creating New Account")
                # new_account.generate_id()
                new_account.create_account()
                print("Account Added")
                self.destroy()
            else:
                print("Error")
        else:
            print("Username or password is to short and could have wrong characters")
            self.show_frame(ErrorFrame)

    #A physical check of user details to ensure they meet the criteria given
    # And to stop SQL Injections by not allowing special chars
    def check_user_details(self, username, password, firstname, surname):
        invalidChars = set(string.punctuation.replace("_", ""))
        if (len(username) and len(password) >= 8) and (not(any(chr in invalidChars for chr in username))): #Stops SQL injections
            if (len(firstname) and len(surname) > 0) and ((not(any(chr in invalidChars for chr in firstname))) and (not(any(chr in invalidChars for chr in surname)))): #Stop SQL injections
                return True
            else:
                return False
        else:
            return False

    #Getters and Setters
    def set_username(self,username):
        self.username = username
    def get_username(self):
        return self.username
    def set_password(self,password):
        self.password = password
    def get_password(self):
        return self.password
    def set_firstname(self,firstname):
        self.firstname = firstname
    def get_firstname(self):
        return self.firstname
    def set_surname(self,surname):
        self.surname = surname
    def get_surname(self):
        return self.surname
    def set_userid(self, userid):
        self.userid = userid
    def get_userid(self):
        return self.userid
    def get_pressed(self):
        return self.pressed
    def get_closed(self):
        return self.closed

    #Sends user details to database and then sends a request to pull information, order, and search it
    def login_request(self):
        print(self.username, " ", self.password)
        old_account = Database()
        old_account.set_username(self.username)
        old_account.set_password(self.password)
        old_account.order_databsae()
        old_account.search_database()

    #Handles swapping windows - e.g. closing login screen when correct and opening main window
    def timed_wait(self):
        t.sleep(2)
    def close_window(self):
        self.destroy()

#Login Page - Displays details of frame for logging in, such as buttons and entry boxes etc
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Login",font=LARGE_FONT)
        label.grid(row=5,column=5)

        usernameL = ttk.Label(self, text="Username", font=LARGE_FONT)
        usernameL.grid(row=6,column=4)
        usernameE = ttk.Entry(self, font=LARGE_FONT)
        usernameE.grid(row=6,column=5)

        passwordL = ttk.Label(self, text="Password", font=LARGE_FONT)
        passwordL.grid(row=7,column=4)
        passwordE = ttk.Entry(self,show="*",font=LARGE_FONT)
        passwordE.grid(row=7,column=5)

        button1 = ttk.Button(self, text="Continue",
                            command=lambda: controller.login_to_account(usernameE,passwordE))
        button1.grid(row=9,column=5)
        button2 = ttk.Button(self, text="Create Account",
                            command=lambda: controller.show_frame(CreateAccount))
        button2.grid(row=9,column=4)

        #Centers the login menu
        self.grid_rowconfigure(4,weight=1)
        self.grid_columnconfigure(3,weight=1)
        self.grid_rowconfigure(10,weight=1)
        self.grid_columnconfigure(6,weight=1)

#Test Frame - Used to test whether the system work
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page One",font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(LoginPage))
        button1.pack()
        button2 = ttk.Button(self, text="Create Account",
                            command=lambda: controller.show_frame(CreateAccount))
        button2.pack()

#Create Account - frame for handling create account information
class CreateAccount(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Create Account",font=LARGE_FONT)
        label.grid(row=5,column=5)

        usernameL = ttk.Label(self, text="Username", font=LARGE_FONT)
        usernameL.grid(row=6, column=4)
        usernameE = ttk.Entry(self)
        usernameE.grid(row=6, column=5)

        passwordL = ttk.Label(self, text="Password", font=LARGE_FONT)
        passwordL.grid(row=7, column=4)
        passwordE = ttk.Entry(self, show="*")
        passwordE.grid(row=7, column=5)

        firstnameL = ttk.Label(self, text="First Name", font=LARGE_FONT)
        firstnameL.grid(row=8, column=4)
        firstnameE = ttk.Entry(self)
        firstnameE.grid(row=8, column=5)

        surnameL = ttk.Label(self, text="Surname", font=LARGE_FONT)
        surnameL.grid(row=9, column=4)
        surnameE = ttk.Entry(self)
        surnameE.grid(row=9, column=5)

        button1 = ttk.Button(self, text="Confirm",
                             command=lambda: controller.send_to_database(usernameE,passwordE,firstnameE,surnameE))
        button1.grid(row=11, column=5)
        button2 = ttk.Button(self, text="Return",
                             command=lambda: controller.show_frame(LoginPage))
        button2.grid(row=11, column=4)

        #Centers the login menu
        self.grid_rowconfigure(4,weight=1)
        self.grid_columnconfigure(3,weight=1)
        self.grid_rowconfigure(12,weight=1)
        self.grid_columnconfigure(6,weight=1)

#Error Frame - Used to display the error message on the gui to the user when their login, create account or edit details
#are incorrect
class ErrorFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background='gray')
        label = ttk.Label(self, text="Username or password is to short and could have wrong characters", font=LARGE_FONT, background='white', foreground='black')
        label.grid(row=1, column=1)
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(2,weight=1)
        self.grid_columnconfigure(2,weight=1)







#app = InterfaceDisplay()
#app.mainloop()