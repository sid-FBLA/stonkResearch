#Defining our core company class
class Company:
    #Creating an init method
    def __init__(self, ticker):
        #Initalizing attributes
        self.ticker = ticker
        #Importing method to add attribute
        from getFilings import getDirectCIK
        self.directCIK = self.getDirectCIK()
        #Importing method to add attribute
        from getFilings import getCIK
        self.cik = self.getCIK()


