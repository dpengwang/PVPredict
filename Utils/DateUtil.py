class Date:
    def __init__(self,date):
        self.date =date
        monthToDayMap = {1: 0, 2: 31, 3: 59, 4: 90, 5: 120, 6: 151, 7: 181, 8: 212, 9: 243, 10: 273, 11: 304, 12: 334}
        space = " "
        bar = "-"
        comma = ":"
        date1 = date.split(space)[0].split(bar)
        date2 = date.split(space)[1].split(comma)

        self.date_year = int(date1[0])
        self.date_month = int(date1[1])
        self.date_day = int(date1[2])

        self.date_hour = int(date2[0])
        self.date_minute = int(date2[1])

        self.day_of_year = monthToDayMap[self.date_month] + self.date_day
        self.minute_of_day = self.date_hour * 60 + self.date_minute

    def get_date_year(self):
        return self.date_year

    def get_date_month(self):
        return self.date_month

    def get_date_day(self):
        return self.date_day

    def get_date_hour(self):
        return self.date_hour

    def get_date_minute(self):
        return self.date_minute

    def get_day_of_year(self):
        return self.day_of_year

    def get_minute_of_day(self):
        return self.minute_of_day

test = "2017-07-28 09:45:00"
if __name__ =="__main__":
    date =Date(test)
    print(date.get_date_minute())