#Imported Classes
from database import Database
#Creates the Object to database
edit = Database()

#Used for basic constsruction of the database, ensuring that all primary and foreign keys are set in place.
#As well as making sure that the tables are independant and reach the 3SF
#Makes handling the database information much easier and more efficent
def create_relationships():
    edit.delete_column("users","ProfileID")

    edit.delete_column("profiles","History")

    edit.create_primarykey("users","UserID")

    edit.create_primarykey("profiles","ProfileID")

    edit.create_table("usersprofiles", "UserID INT(10) NOT NULL, ProfileID INT(10) NOT NULL, "
                                       "PRIMARY KEY (UserID, ProfileID), "
                                       "FOREIGN KEY (UserID) REFERENCES users(UserID), "
                                       "FOREIGN KEY (ProfileID) REFERENCES profiles(ProfileID)")

    edit.create_table("history", "HistoryID INT(10) NOT NULL, Filename VARCHAR(255), "
                                       "PRIMARY KEY (HistoryID)")

    edit.create_table("profileshistory", "ProfileID INT(10) NOT NULL, HistoryID INT(10) NOT NULL, "
                                       "PRIMARY KEY (ProfileID, HistoryID), "
                                       "FOREIGN KEY (ProfileID) REFERENCES profiles(ProfileID), "
                                         "FOREIGN KEY (HistoryID) REFERENCES history(HistoryID)")

    edit.delete_user("0")











