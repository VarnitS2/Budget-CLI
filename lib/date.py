from datetime import date

class Date:
    def __init__(self, date):
        self.month = int(date.split('/')[0])
        self.day = int(date.split('/')[1])
        self.year = int(date.split('/')[2])

    def __str__(self):
        if (self.month < 10 and self.day < 10):
            toReturn = "0{}/0{}/{}".format(self.month, self.day, self.year)
        elif (self.month < 10):
            toReturn = "0{}/{}/{}".format(self.month, self.day, self.year)
        else:
            toReturn = "{}/{}/{}".format(self.month, self.day, self.year)
        
        return toReturn

    def compare(self, other):
        if other.year > self.year:
            return -1
        elif other.year < self.year:
            return 1
        elif other.month > self.month:
            return -1
        elif other.month < self.month:
            return 1
        elif other.day > self.day:
            return -1
        elif other.day < self.day:
            return 1
        else:
            return 0

    def diffDays(self, other):
        return (date(2000+other.year, other.month, other.day) - date(2000+self.year, self.month, self.day)).days