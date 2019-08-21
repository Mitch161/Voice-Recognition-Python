#File for Searching Algorithms that could be used throughout the program
#Date - 08/11/2018
#Mitchell Hardie

#Class used to hold all algorithms that would be used to search for data throught their sets and lists etc
class SearchData:
    def __init__(self, data, username, password):
        #Private Variables
        self.data = data
        self.range_limit = len(data)
        self.length = len(data)-1
        self.user_search = username.lower()
        self.pass_search = password.lower()
        self.found = False

    #Old binary search that was used before that is not broken and dosnt work as well as the other one
    def binary_search(self):
        first = 0
        last = self.length
        #for loop in range(self.range_limit):  # CHANGED FROM A WHILE LOOP TO A FOR LOOP
        while self.found == False:
            midpoint = (first + last) // 2
            if self.data[midpoint]["Username"].lower() == self.user_search:
                print("Found Username")
                if self.data[midpoint]["Password"].lower() == self.pass_search:
                    print("Found Password")
                    self.found = True
                    return self.found
                    break
            #else:
                #if loop >= self.range_limit:
                    #return self.found
                    #break
            else:
                if self.user_search < self.data[midpoint]["Username"].lower():
                    last = midpoint-1
                else:
                    first = midpoint+1
        return self.found

    #Recursion----------------------------------------------------------------------------------------------------------
    #New binary search that uses recursion to look through the nested dictionary and the find the data that the user
    #is looking for
    def binarySearch(self, dict, elem, section):
        def recurse(first, last):
            print("Recursion")
            mid = int((first + last) / 2)
            if first > last:
                return False #base case/stopping condition
            elif (dict[mid][section] < elem):
                return recurse(mid + 1, last)
            elif (dict[mid][section] > elem):
                return recurse(first, mid - 1)
            else:
                return True
        return recurse(0, len(dict) - 1)
    #-----------------------------------------------------------------------------------------------------------------










#test = SearchData("","","")
#dict = {0: {"x":""}, 1: {"x": "aaaaaaaaaaaaaaa"}, 2: {"x": "bbbbbbbbbbbbbbbbbb"}, 3: {"x": "cccccccccccccccccccccccccccc"}, 4: {"x": "ddd"}, 5: {"x": "eeeeeeeeeeeeeeeee"}, 6: {"x": "ffffffffffffffffff"}, 7: {"x": "g"}}
#print(dict)
#print(test.binarySearch(dict,"ddd","x"))

