"""
Helper class that handle format related functionalities

:Authors:
    - Chengkang Xu <cx33@duke.edu>
"""

import re
import datetime


class FormatHelper (object):

    HourDifference = -4  # sonarqube time is * hours faster than actual time


    def __init__(self, **kwargs):
        pass

    def adjustSonarTime (self, SonarTime):

        """
        adjust the time stampe from sonar to more readable format
        :param SonarTime: time stamp from sonar
        :return: readable time stamp
        """
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

        # store the result

        l = [self.addPrefixToDate(Year),
             self.addPrefixToDate(Month),
             self.addPrefixToDate(Day),
             self.addPrefixToDate(Hour),
             self.addPrefixToDate(Minuate),
             self.addPrefixToDate(Second)]

        return '-'.join(l)


    def addPrefixToDate(self, any):
        """
        add 0 to any number less than 10 in date
        :param any: any time
        :return: 0 added time
        """
        strAny = str(any)
        if any < 10:
            strAny = '0' + strAny
        return strAny

    def checkRunYear (self, year):
        """
        check if it is run year
        :param year: any year
        :return:  whether it is run year
        """
        if (year % 4 == 0 and not year % 100 == 0) or (year % 400 == 0):
            return True
        return False

    def stripmethodname(self, line):
        """
        strip method name from sonarqube
        :param line: a line of code contains the method name
        :return: return only the name
        """
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


    def striphtml(self, data):
        """
        strip html code
        :param data: code from sonarqube
        :return: cleaner version of the code
        """
        p = re.compile(r'<.*?>')
        p = p.sub('', data)
        p = p.replace('&lt;', '<')
        p = p.replace('&gt;', '>')
        p = p.replace('&le;', '<=')
        p = p.replace('&ge;', '>=')
        return p

    def getDateFromTuple(self, tuple):
        """
        convert the date to specific format
        :param tuple: date
        :return: self defined date
        """
        return datetime.datetime.strptime(tuple, "%Y %b %d")

    def getFullPath(self, prefix, suffixes):
        """
        given prefix and suffix of the directories, combine them to full path
        :param prefix: root directory
        :param suffixes: file
        :return: full path
        """
        res = {}
        for suffix in suffixes:
            # ignore .git file
            if suffix[-4:] == ".git":
                continue
            if prefix == ".":
                res[suffix] = []
                continue
            res[prefix + "/" + suffix] = []
        return res

    def makeMap(self, rules, main, sub):
        """
        add main categories, sub categories to rules for export
        :param rules: rules under the main and the sub
        :param main: main category
        :param sub: sub category
        :return: rule mapping ready for export
        """
        res = ""
        for rule in rules:
            if sub > 0:
                res = res + "'" + rule + "' : ['" + main + "'," + str(sub) + "],\n"
            else:
                res = res + "'" + rule + "': ['" + main + "'],\n"

        return res



if __name__ == '__main__':
    print (FormatHelper().adjustSonarTime('2018-06-19T18:39:32+0000'))