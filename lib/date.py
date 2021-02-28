class Date:
    def __init__(self, date):
        self.month = date.split('-')[0]
        self.day = date.split('-')[1]
        self.year = date.split('-')[2]