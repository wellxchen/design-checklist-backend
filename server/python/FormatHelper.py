'''
Helper class that handle format related functionalities
'''

import re
import datetime


class FormatHelper ():

    HourDifference = -4 #sonarqube time is * hours faster than actual time

    def adjustSonarTime (self, SonarTime):
        SonarTime = SonarTime[:-5]
        Year = int(SonarTime[:4])
        Month = int(SonarTime[5:7])
        Day = int(SonarTime[8:10])
        Second = int(SonarTime[-2:])
        Minuate = int(SonarTime[-5:-3])
        Hour = int(SonarTime[-8:-6]) + FormatHelper.HourDifference
        isRunYear = self.checkRunYear(Year)
        if Hour > 23:
            Hour -= 24
            Day += 1
            if Month == 2:
                if Day > 29 and isRunYear:
                    Month += 1
                    Day -= 29
                if Day > 28 and not isRunYear:
                    Month += 1
                    Day -= 28

            elif Month == 1 or Month == 3 or Month == 5 or Month == 7 or Month == 8:
                if Day > 31:
                    Month += 1
                    Day -= 31
            else:
                if Day > 30:
                    Month += 1
                    Day -= 30

            if Month > 12:
                Month -= 12
                Year += 1


        l = [self.addPrefixToDate(Year),
             self.addPrefixToDate(Month),
             self.addPrefixToDate(Day),
             self.addPrefixToDate(Hour),
             self.addPrefixToDate(Minuate),
             self.addPrefixToDate(Second)]

        return '-'.join(l)


    def addPrefixToDate(self, any):
        strAny = str(any)
        if any < 10:
            strAny = '0' + strAny
        return strAny

    def checkRunYear (self, year):
        if (year % 4 == 0 and not year % 100 == 0) or (year % 400 == 0):
            return True
        return False



    # strip method name
    def stripmethodname(self, line):
        index = line.find('(')

        if line[index - 1] == ' ':
            index -= 2
        else:
            index -= 1
        i = index
        while i >= 0:
            if line[i] == ' ':
                i += 1
                break
            i -= 1
        return line[i + 5:index - 6]

    # strip html code
    def striphtml(self, data):
        p = re.compile(r'<.*?>')
        p = p.sub('', data)
        p = p.replace('&lt;', '<')
        p = p.replace('&gt;', '>')
        p = p.replace('&le;', '<=')
        p = p.replace('&ge;', '>=')
        return p

    def getDateFromTuple(self, tuple):
        return datetime.datetime.strptime(tuple, "%Y %b %d")

    def getFullPath(self, prefix, suffixes):
        res = {}
        for suffix in suffixes:
            if suffix[-4:] == ".git":
                continue
            if prefix == ".":
                res[suffix] = []
                continue
            res[prefix + "/" + suffix] = []
        return res

    def makeMap(self, rules, main, sub):
        res = ""
        for rule in rules:
            if sub > 0:
                res = res + "'" + rule + "' : ['" + main + "'," + str(sub) + "],\n"
            else:
                res = res + "'" + rule + "': ['" + main + "'],\n"

        return res

if __name__ == '__main__':
    print FormatHelper().adjustSonarTime('2018-06-19T18:39:32+0000')