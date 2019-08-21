#Imported Modules
import mysql.connector
from searching_algorithms import SearchData

#Connection to database that allows the program to communicate with program ------------------------------
mydb_admin = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="computing_nea_2000",
    database="assetsdb",
    auth_plugin="mysql_native_password"
)
#Would be changed to user account connection rather than admin root connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="computing_nea_2000",
    database="assetsdb",
    auth_plugin="mysql_native_password"
)
mycursor = mydb.cursor(buffered=True)
#--------------------------------------------------------------------------------------------------------
#Main calling class within this file - Is responsible for handling all requests, pulls, pushes and updates to the
#database. Acts as the calling hub for any program that wishes to do anything with the database
class Database:
    def __init__(self):
        #Private Variables
        self.mycursor = mydb.cursor()
        self.userid = 0
        self.username = ""
        self.password = ""
        self.profileid = 0
        self.firstname = ""
        self.surname = ""
        self.tablename = ""
        self.target = ""
        self.ordered_names = []
        self.ordered_passwords = []
        self.ordered_userIDs = []
        self.ordered_dictionary = {}

    #SQL Functions - responsible for executing the correct and right commands - Each perform their own role
    def create_primarykey(self, tablename, columnname):
        sql = "ALTER TABLE "+tablename+" ADD PRIMARY KEY("+columnname+")"
        mycursor.execute(sql)
        mydb.commit()
        print("Primary key created as ", columnname)

    def create_foreignkey(self, tablename, columnname, reftable, refcolumn):
        sql = "ALTER TABLE "+tablename+" ADD FOREIGN KEY ("+columnname+") REFERENCES "+reftable+"("+refcolumn+")"
        mycursor.execute(sql)
        mydb.commit()
        print("Foreign key created as", columnname)

    def create_table(self, tablename, expression):
        sql = "CREATE TABLE "+tablename+" ("+expression+")"
        mycursor.execute(sql)
        mydb.commit()
        print("Table ",tablename, " created")

    def select_details(self, column, table, column2, username):
        sql = 'SELECT '+column+' FROM '+table+' WHERE '+column2+'='+username
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        myresult = myresult[0][0]
        return myresult

    def delete_column(self, tablename, columnname):
        sql = "ALTER TABLE "+tablename+" DROP COLUMN "+columnname
        mycursor.execute(sql)
        mydb.commit()
        print("Column ", columnname, " has been deleted from database")

    def delete_user(self, userid):
        sql = "DELETE FROM users WHERE UserID="+userid
        mycursor.execute(sql)
        mydb.commit()
        print("User has been deleted from database")

    def insert_history_into_table(self, user_id, filename):
        sql = "INSERT INTO history (HistoryID, Filename) VALUES (%s, %s)"
        user_input = (user_id,filename)
        mycursor.execute(sql, user_input)
        mydb.commit()
        print("Values inserted into History table")

    def update_user_info(self):
        sqlU = "UPDATE users SET Username=%s, Password=%s WHERE UserID=%s"
        user_detailsU = (self.username, self.password, self.userid)
        mycursor.execute(sqlU, user_detailsU)
        mydb.commit()
        print("user table updated")
        sqlP = "UPDATE profiles SET Firstname=%s, Surname=%s WHERE ProfileID=%s"
        user_detailsP = (self.firstname, self.surname, self.profileid)
        mycursor.execute(sqlP, user_detailsP)
        mydb.commit()
        print("profile table updated")

    #create history file for all user data----------------------------------------------------------------------------
    def write_binaryfile(self, input_info, file_path):
        buffer = bytes(input_info)
        with open(file_path, 'bw') as f:
            f.write(buffer)
    def read_binaryfile(self, file_path):
        lst = []
        with open(file_path, 'br') as f:
            buffer = f.read()
        for line in buffer:
            lst[line] = buffer
        print(lst)
        return lst
    #-----------------------------------------------------------------------------------------------------------------

    def order_databsae(self):
        sql = "SELECT UserID, Username, Password FROM users ORDER BY Username"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        # Add items in database into a list
        for pos in range(len(myresult)):
            data1 = myresult[pos][0]
            data2 = myresult[pos][1]
            data3 = myresult[pos][2]
            self.ordered_dictionary[pos] = {"UserID": data1, "Username": data2, "Password": data3}

    def username_search(self):
        binarysearch_user = SearchData(self.ordered_dictionary, self.username, self.password)
        found_username = binarysearch_user.binarySearch(self.ordered_dictionary, self.username,"Username")
        if found_username == True:
            return True
        elif found_username == False:
            return False
        else:
            print("Error")
            return False

    def search_database(self):
        binarysearch_user = SearchData(self.ordered_dictionary, self.username, self.password)
        found_username = binarysearch_user.binarySearch(self.ordered_dictionary, self.username,"Username")
        found_password = binarysearch_user.binarySearch(self.ordered_dictionary, self.password,"Password")
        if found_username == True:
            if found_password == True:
                print("Logging In...")
                return True
            elif found_password == False:
                print("Incorrect Login Details")
                return False
            else:
                print("Error")
        elif found_username == False:
            print("Incorrect Details")
            return False
        else:
            print("Error")
            return False

    def check_login(self):
        sql_username_search = "SELECT users, Username FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = 'assetsdb' AND column_name = 'UserID'"
        sql_password_search = "SELECT users, Password FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = 'assetsdb' AND column_name = 'UserID'"
        username_result = mycursor.execute(sql_username_search)
        password_result = mycursor.execute(sql_password_search)
        if username_result == self.username and password_result == self.password:
            print("Logging In...")
        elif username_result == self.username and password_result != self.password:
            print("Password Is Incorrect!")
        elif username_result != self.username and password_result == self.password:
            print("Username is Incorrect!")
        else:
            print("Wrong Account Information!")

    def check_existing_accounts(self):
        found = False
        database_search = SearchData(self.ordered_dictionary, self.username, self.password)
        found_user = database_search.binarySearch(self.ordered_dictionary, self.username, "Username")
        #found_user = database_search.binary_search()
        if found_user == True:
            print("Account Already Exists - Please Enter New Details")
            found = True
            return found
        else:
            print("Account is Available")
            return found

    #Getters and Setters
    def generate_id(self):
        mycursor.execute("SELECT * FROM users")
        number_of_users = mycursor.rowcount
        self.userid = number_of_users+1
        self.profileid = number_of_users+1
    def set_userid(self):
        sql_userid_search = "SELECT UserID, Username FROM users"
        mycursor.execute(sql_userid_search)
        userid_result = mycursor.fetchall()
        for x in range(len(userid_result)):
            if userid_result[x][1] == self.username:
                self.userid = userid_result[x][0]
    def get_userid(self):
        return self.userid
    def get_profileid(self):
        return self.profileid

    def set_userid_file(self, userid):
        self.userid = userid
    def set_profileid_file(self, profileid):
        self.profileid = profileid

    def set_username(self,username):
        self.username = username
    def get_username(self):
        return self.username
    def set_password(self,password):
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

    def get_database_fn(self):
        sql_userid_search = "SELECT ProfileID, FirstName FROM profiles"
        mycursor.execute(sql_userid_search)
        firstname_result = mycursor.fetchall()
        for x in range(len(firstname_result)):
            if firstname_result[x][0] == self.userid:
                self.firstname = firstname_result[x][1]
    def get_database_sn(self):
        sql_userid_search = "SELECT ProfileID, Surname FROM profiles"
        mycursor.execute(sql_userid_search)
        surname_result = mycursor.fetchall()
        for x in range(len(surname_result)):
           if surname_result[x][0] == self.userid:
               self.surname = surname_result[x][1]

    #Hashing algorithm ------------------------------------------------------------------------------------------
    #Ensures that all users in the database have a unique address and ID so they can all be uniquely identified
    def insert_into_table(self, address):
        check = True
        while check == True:
            try:
                sqlFormula = "INSERT INTO users (UserID, Username, Password) VALUES (%s, %s, %s)"
                user = (address, self.username, self.password)
                self.mycursor.execute(sqlFormula, user)
                mydb.commit()
                sqlFormula = "INSERT INTO profiles (ProfileID, FirstName, Surname) VALUES (%s, %s, %s)"
                user = (address, self.firstname, self.surname)
                self.mycursor.execute(sqlFormula, user)
                mydb.commit()
                check = False
            except:
                #Very basic system where by the address is incremented by one everytime if the user cannot be entered
                #into database due to conflicting addresses
                #Stops collision erros
                address += 1

    def generate_key(self,username,firstname,surname):
        #Create hash key
        key = 0
        user_info = username+firstname+surname #Combine the firstname and surname together before loop
        for c in user_info:
            key = key + ord(c)
        return key

    def create_account(self):
        #Initiate Hashing Algorithm Key
        key = self.generate_key(self.username,self.firstname,self.surname)
        address = key // 100
        #Insert information into tables within database, pass address through
        self.insert_into_table(address)
    #--------------------------------------------------------------------------------------------------------------


















#mycursor = mydb.cursor()

#mycursor.execute("CREATE TABLE neurallink (AudioID INTEGER(10), WordID INTEGER(10))")
#mycursor.execute("SHOW TABLES")

#sqlFormula = "INSERT INTO users (UserID, Username, Password, ProfileID) VALUES (%s, %s, %s, %s)"
#user1 = (2, "test", "test", 2)
#mycursor.execute(sqlFormula, user1)
#mydb.commit()

#for db in mycursor:
#    print(db)
#mycursor.execute("SELECT * FROM users")
#for tb in mycursor:
#    print(tb)