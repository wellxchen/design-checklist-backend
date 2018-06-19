

'''
Helper class that handle local storage
'''

import re
import json
import requests

import os
from os.path import join, dirname, abspath
from dotenv import load_dotenv

import datetime
import configparser

ROOT = dirname(__file__)[:-14]
dotenv_path = ROOT + "/server/documents/local/app-env"
load_dotenv(dotenv_path)

class LocalHelper ():


    def readProjectDates (self, project):
        config = configparser.ConfigParser()
        config.read(ROOT + "/server/documents/config.ini")
        res = {}
        self.storeSingleConfigDate(res, config, "ENDDATE", project)
        self.storeSingleConfigDate(res, config, "STARTDATE", project)

        return res

    def storeSingleConfigDate (self, res, config, key, project):
        res[key] = {}
        for k,v in config[key].items():
            if k in project:
                res[key][k] = v
                return

    def getRootPath(self):

        return abspath(dirname(__file__))[:-14]

    def writeLog (self, logname, data):
        with open(logname, 'w') as outfile:
            outfile.write(data)


    #extract gitlabid
    def readStudentInfo (self):
        emails = {}
        netids = {}
        netidindex = 2
        emailindex = 3
        gitlabidindex = 4

        csvpath = dirname(__file__)[:-14] + '/server/documents/local/308students.csv'
        import csv
        with open(csvpath, 'rb') as csvfile:
            spamreader = csv.reader(csvfile)

            for row in spamreader:
                emails[row[emailindex]] =row [gitlabidindex]
                netids[row[netidindex]] = row [gitlabidindex]
        res = {}
        res["email"] = emails
        res["netid"] = netids
        return res





