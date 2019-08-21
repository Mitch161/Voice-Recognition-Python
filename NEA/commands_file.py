#Imported Modules
import os
import subprocess
import webbrowser
from googlesearch import search

#Main class responsible for ensuring that the correct commands execute and then return the correct result from the user
class Commands():
    def __init__(self):
        self.open_webpage = None
        self.path = "/home/mitchell/Documents/"
        self.tmp_path = ""
        self.found_file = False

    def command_picker(self, command, action, query, filepath, prev_path):
        if command == "open":
            self.command_open(action)
        elif command == "close":
            self.command_close()
        elif command == "exit":
            self.command_exit()
        elif command == "use":
            self.command_use(action)
        elif command == "search":
            self.command_search(query, filepath, prev_path)
        elif command == "play":
            self.command_play(query)
        elif command == "history":
            self.command_history()
        elif command == "profile":
            self.command_profile()
        elif command == "logout":
            self.command_logout()
        else:
            print("Error within command picker")

    def command_open(self, action):
        print("you are in open")
        try:
            #os.system(action)
            name = webbrowser.get().name
            browser = subprocess.Popen([name, 'https://www.'+action+'.com'])
            self.open_webpage = browser
        except:
            print("failed")

    def command_close(self):
        print("You are in close")
        self.open_webpage.terminate()

    def command_exit(self):
        exit_called = True
        return exit_called

    def command_use(self, query):
        name = webbrowser.get().name
        action = search(query, tld='com', num=1, stop=1, pause=2)
        for j in action:
            action = j
        subprocess.Popen([name, action])

    #Recursive algorithm-----------------------------------------------------------------------------------------------
    #Used to recursivly call through the computer direcotry till a file is found, return true and then end
    def command_search(self, filename, filepath, prev_path):
        contents = os.listdir(filepath)
        for amount in contents:
            if amount == filename:
                print("File found")
                return True #base case/stopping condition
            else:
                print("Not right file")
        for find in contents:
            try:
                next_path = (filepath+find+"/")
                print(next_path)
                os.listdir((next_path))
                filepath = self.command_search(filename, next_path, filepath)
            except:
                print("This is a file not a folder")
        print("returing...")
        return prev_path #base case/ stopping condition
    #------------------------------------------------------------------------------------------------------------------

    def command_play(self, query):
        name = webbrowser.get().name
        action = search(query, tld='com', num=1, stop=1, pause=2)
        for j in action:
            action = j
        subprocess.Popen([name, action])

    def command_history(self):
        file = "/home/mitchell/Documents/speech_data_files/history_folder/history.txt"
        lst = []
        with open(file, 'br') as f:
            buffer = f.read()
        for line in buffer:
            lst[line] = buffer
        print(lst)
        return lst

    def command_profile(self):
        profile_called = True
        return profile_called

    def command_logout(self):
        logout_called = True
        return logout_called