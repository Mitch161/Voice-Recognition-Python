#imported modules
from interface_gui import InterfaceDisplay
from database import Database
import tkinter as tk
from user_login import LoginProcess
from voice_recording import AudioGui
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
import matplotlib.animation as Animation
from matplotlib import style
style.use("ggplot")

#Main calling class that controls the whole program
class Main():
    def __init__(self):
        # Initilise login GUI
        self.login_win = InterfaceDisplay() #Creates interface display object
        self.login_win.mainloop() #Handles the main control loop for window
        self.new_account = Database() #Creates main control for database through this file

    #Start capture - Creates the voice_recording.py window and passes through user details.
    #              - Creates animation for graph displayed on main window of the program
    def start_capture(self, firstname, surname, userid, username, password):
        rec_voice = AudioGui(firstname, surname, userid, username, password)
        f = rec_voice.get_f()
        ani = Animation.FuncAnimation(f, rec_voice.animate, interval=1) #Animation of graph
        quit_app = rec_voice.mainloop()

    #Function responsible for logging user in or displaying a error message, as well as creating a new account if
    #requested.
    def info(self):
        # If Create Account is pressed - New Account Process
        if self.login_win.get_pressed() == True:
            # Set new variables for new account
            new_username = self.login_win.get_username()
            new_password = self.login_win.get_password()
            new_firstname = self.login_win.get_firstname()
            new_surname = self.login_win.get_surname()
            username = '"' + new_username + '"'
            user_id = self.new_account.select_details("UserID", "users", "Username", username)
            self.start_capture(new_firstname, new_surname, user_id, new_username, new_password)

        # If New Account isn't pressed - User Login Process
        elif self.login_win.get_pressed() == False:
            closed = self.login_win.get_closed()
            if closed == True:
                print("Closing Program")
            elif closed == False:
                print("Successful Login")
                username = self.login_win.get_username()
                username = '"' + username + '"'
                #Gets details from databse to send into the main calling window - Allows the profile and name in top
                #left to be displayed
                userid = self.new_account.select_details("UserID", "users", "Username", username)
                user_firstname = self.new_account.select_details("FirstName", "profiles", "ProfileID", str(userid))
                user_surname = self.new_account.select_details("Surname", "profiles", "ProfileID", str(userid))
                user_username = self.new_account.select_details("Username", "users", "UserID", str(userid))
                user_password = self.new_account.select_details("Password", "users", "UserID", str(userid))
                # Begin to capture
                self.start_capture(user_firstname, user_surname, userid, user_username, user_password)
            else:
                print("Error closing")
        else:
            print("Returning")

#Creates the object of Main
mainclass = Main()
mainclass.info()













# def start_capture(firstname, surname, userid, username, password):
#     rec_voice = AudioGui(firstname, surname, userid, username, password)
#     f = rec_voice.get_f()
#     ani = Animation.FuncAnimation(f, rec_voice.animate, interval=1)
#     quit_app = rec_voice.mainloop()
#
# # Initilise login GUI
# login_win = InterfaceDisplay()
# login_win.mainloop()
#
# new_account = Database()
#
# # If Create Account is pressed - New Account Process
# if login_win.get_pressed() == True:
#     # Set new variables for new account
#     new_username = login_win.get_username()
#     new_password = login_win.get_password()
#     new_firstname = login_win.get_firstname()
#     new_surname = login_win.get_surname()
#
#     # Creates an Account
#     #new_account = Database()
#     #new_account.set_username(new_username)
#     #new_account.set_password(new_password)
#     #new_account.set_firstname(new_firstname)
#     #new_account.set_surname(new_surname)
#     #new_account.order_databsae()
#     #user_check = new_account.check_existing_accounts()
#     #if user_check == True:
#     #    print("Try Again")
#     #elif user_check == False:
#     #    print("Creating New Account")
#     #    #new_account.generate_id()
#     #    new_account.create_account()
#     #    print("Account Added")
#     username = '"'+new_username+'"'
#     user_id = new_account.select_details("UserID", "users", "Username", username)
#     start_capture(new_firstname, new_surname, user_id, new_username, new_password)
#     #else:
#     #    print("Error")
#
#
# # If New Account isn't pressed - User Login Process
# elif login_win.get_pressed() == False:
#     closed = login_win.get_closed()
#     if closed == True:
#         print("Closing Program")
#     elif closed == False:
#         print("Successful Login")
#         #user_firstname = login_win.get_firstname()
#         #user_surname = login_win.get_surname()
#         username = login_win.get_username()
#         username = '"'+username+'"'
#         userid = new_account.select_details("UserID", "users", "Username", username)
#         user_firstname = new_account.select_details("FirstName", "profiles", "ProfileID", str(userid))
#         user_surname = new_account.select_details("Surname", "profiles", "ProfileID", str(userid))
#         user_username = new_account.select_details("Username","users","UserID",str(userid))
#         user_password = new_account.select_details("Password","users","UserID",str(userid))
#         # Begin to capture
#         start_capture(user_firstname,user_surname, userid, user_username, user_password)
#     else:
#         print("Error closing")
# else:
#     print("Returning")







#login_username = login_win.get_username()
    #login_password = login_win.get_password()

    #Get information from Database
    #get_database_info = Database()
    #get_database_info.set_username(login_username)
    #get_database_info.set_userid()

    #user_id = get_database_info.get_userid()

    #get_database_info.set_firstname()
    #get_database_info.set_surname()
    #user_firstname = get_database_info.get_firstname()
    #user_surname = get_database_info.get_surname()

    #Begin to capture
    #start_capture(user_firstname,user_surname)



    # Login Check - If login button is pressed details are checked
    #login_check = LoginProcess()
    #login_check.set_username(login_username)
    #login_check.set_password(login_password)
    #login_check.login_request()
    #login_check.mainloop()


#rec_voice = AudioGui()
#rec_voice.init_graph()
#rec_voice.draw_graph()
#rec_voice.mainloop()


#put stuff below into mainloop so it works please thank you
#old_account = Database(login_username,login_password,"","")
#old_account.check_login()

#login_check.login_request()

#-----