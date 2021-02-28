class Date:
    def __init__(self, date):
        self.month = date.split('-')[0]
        self.day = date.split('-')[1]
        self.year = date.split('-')[2]

    def __str__(self):
        return "{}-{}-{}".format(self.month, self.day, self.year)