#Login Interface Devlopment
#Date - 19/10/2018
#Mitchell Hardie

#Imported Modules
import tkinter as tk
from tkinter import ttk
from database import Database
#from interface_gui import InterfaceDisplay
from voice_recording import AudioGui
import time as t

#Constants
LARGE_FONT = ("roboto", 16)
#Program - Frame class that is accessed in interface_gui to display the loading screen and pass user details into the
#database. Acts a as bridge between interface_gui.py and database.py to limit what the user can pass through
class LoginProcess(tk.Frame):#tk.Tk
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #Private variables
        self.username = ""
        self.password = ""
        self.firstname = ""
        self.surname = ""

        label = ttk.Label(self, text="Loading",font=LARGE_FONT)
        label.grid(row=5,column=5)

        dot1 = ttk.Label(self, text=".",font=LARGE_FONT)
        dot1.grid_forget()
        dot2 = ttk.Label(self, text=".",font=LARGE_FONT)
        dot2.grid_forget()
        dot3 = ttk.Label(self, text=".",font=LARGE_FONT)
        dot3.grid_forget()

        # Centers the login menu
        self.grid_rowconfigure(4,weight=1)
        self.grid_columnconfigure(4,weight=1)
        self.grid_rowconfigure(7,weight=1)
        self.grid_columnconfigure(6,weight=1)

    #Public Functions
    def test(self):
        print(self.username, " + ", self.password)
    #Getters and Setters
    def set_username(self, username):
        self.username = username
    def get_username(self):
        return self.username
    def set_password(self, password):
        self.password = password
    def get_password(self):
        return self.password
    def set_firstname(self, firstname):
        self.firstname = firstname
    def get_firstname(self):
        return self.firstname
    def set_surname(self, surname):
        self.surname = surname
    def get_surname(self):
        return self.surname

    def login_request(self):
        print(self.username, " ", self.password)
        old_account = Database()
        old_account.set_username(self.username)
        old_account.set_password(self.password)
        old_account.order_databsae()
        correct = old_account.search_database()
        return correct

    def get_fs_name(self):
        get_database_info = Database()
        self.firstname = get_database_info.get_database_fn()
        self.surname = get_database_info.get_database_sn()
#A simple Frame that is called by the super class in interface_gui.py that allows the buttons to be displayed ontop of
#LoginProcess class GUI
class ButtonFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Loading Complete", font=LARGE_FONT)
        label.grid(row=5, column=5)

        button1 = ttk.Button(self, text="Continue",
                            command=lambda: controller.close_window())
        button1.grid(row=6,column=5)

        # Centers the login menu
        self.grid_rowconfigure(4,weight=1)
        self.grid_columnconfigure(4,weight=1)
        self.grid_rowconfigure(7,weight=1)
        self.grid_columnconfigure(6,weight=1)























        #Begin to capture
        #start_capture(user_firstname,user_surname)

    #def stop_loading(self):
        #self.destroy()


# class LoginCheck(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = ttk.Label(self, text="Loading",font=LARGE_FONT)
#         label.grid(row=5,column=5)
#
#         dot1 = ttk.Label(self, text=".",font=LARGE_FONT)
#         dot1.grid_forget()
#         dot2 = ttk.Label(self, text=".",font=LARGE_FONT)
#         dot2.grid_forget()
#         dot3 = ttk.Label(self, text=".",font=LARGE_FONT)
#         dot3.grid_forget()
#
#         button1 = ttk.Button(self, text="Continue",
#                             command=lambda: controller.stop_loading())
#         button1.grid(row=6,column=5)
#
#         # Centers the login menu
#         self.grid_rowconfigure(4,weight=1)
#         self.grid_columnconfigure(4,weight=1)
#         self.grid_rowconfigure(7,weight=1)
#         self.grid_columnconfigure(6,weight=1)



#app = LoginProcess()
#app.mainloop()