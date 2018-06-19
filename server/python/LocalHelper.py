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
import subprocess

ROOT = dirname(__file__)[:-14]
dotenv_path = ROOT + "/server/documents/local/app-env"
load_dotenv(dotenv_path)

from SonarHelper import  SonarHelper
from DataHelper import DataHelper
from FormatHelper import  FormatHelper

class LocalHelper ():

    def __init__(self, group, project):
        self.SONAR_GROUP = 'duke-compsci308:'
        if project is None:
            project = ""
        self.ROOT_PATH = self.getRootPath()
        self.GITLAB_GROUP = group
        self.PLAIN_PROJECT = project
        self.TEST_PROJECT = self.SONAR_GROUP + project
        self.QUALITY_PROFILE = 'AV-ylMj9F03llpuaxc9n'
        self.SONAR_URL = 'http://coursework.cs.duke.edu:9000'
        self.TOKEN = os.environ.get("GITLAB_TOKEN")
        self.CACHE_PATH = self.ROOT_PATH + "/cache"
        self.CODES_PATH = self.CACHE_PATH + "/codes"
        self.LOGS_PATH = self.CACHE_PATH + "/logs"
        self.SHELL_PATH = self.ROOT_PATH + "/server/shell"
        self.LOG_DIR = self.LOGS_PATH + "/" + self.GITLAB_GROUP + "/" + self.PLAIN_PROJECT
        self.LOG_ISSUES = self.LOG_DIR + "/issues"
        self.LOG_STATISTICS = self.LOG_DIR + "/statistics"


    def readProjectDates (self, project):
        '''
        read start dates and end dates of project
        :param project: the name the project
        :return: return the start and end dates
        '''
        config = configparser.ConfigParser()
        config.read(ROOT + "/server/documents/config.ini")
        res = {}
        self.storeSingleConfigDate(res, config, "ENDDATE", project)
        self.storeSingleConfigDate(res, config, "STARTDATE", project)

        return res


    def storeSingleConfigDate (self, res, config, key, project):
        '''
        Store single configuration date in to res buffer
        :param res:  buffer to hold the result
        :param config: original configuration
        :param key: key in the configuration
        :param project: projects
        :return: void
        '''
        res[key] = {}
        for k,v in config[key].items():
            if k in project:
                res[key][k] = v
                return

    def getRootPath(self):
        '''
        get the root
        :return: root  path
        '''
        return abspath(dirname(__file__))[:-14]

    def writeLog (self, logname, data):
        '''
        write log file
        :param logname: name of file store the log
        :param data: data to be stored
        '''
        with open(logname, 'w') as outfile:
            outfile.write(data)

    def writeLogJSON (self, logname, data):
        '''
        write JSON log file
        :param logname: name of JSON file store the log
        :param data: data to be stored
        '''
        with open(logname, 'w') as outfile:
            json.dump(data,outfile)

    def handleLogJSON (self, WHICHLOG, data):
        '''
        check if the log extisted, if so do nothing, if not caching
        :param WHICHLOG: which log to be written
        :param data: data to be stored
        '''
        analysisTime = SonarHelper().getMostRecentAnalysisDate(self.SONAR_URL, self.TEST_PROJECT)
        analysisTime = FormatHelper().adjustSonarTime(analysisTime)
        existed = self.executeShellCheckDIR(WHICHLOG, analysisTime)
        if "no" in existed:
            self.writeLogJSON(WHICHLOG + "/" + analysisTime + ".json", data)


    #extract gitlabid
    def readStudentInfo (self):

        '''
        read student info from csv file and store into the buffer
        :return: email and netids
        '''
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

    def executeShellLog(self):
        '''
        execute shell script that check log folder existence
        :return: output from terminal
        '''
        return subprocess.check_output([self.SHELL_PATH + '/logs.sh',
                                        self.GITLAB_GROUP,
                                        self.PLAIN_PROJECT,
                                        self.ROOT_PATH])

    def executeShellCode(self):
        '''
        execute shell script that cache gitlab codes
        :return: output from terminal
        '''
        return subprocess.check_output([self.SHELL_PATH + '/codes.sh',
                                        self.TOKEN,
                                        self.GITLAB_GROUP,
                                        self.PLAIN_PROJECT,
                                        self.ROOT_PATH])

    def executeShellStats(self):

        '''
        execute shell scripts that extract stat information
        :return: stat information
        '''
        return subprocess.check_output([self.SHELL_PATH + '/stats.sh',
                                        self.TOKEN,
                                        self.GITLAB_GROUP,
                                        self.PLAIN_PROJECT,
                                        self.ROOT_PATH])

    def executeShellCheckDIR(self, WHICHLOG, ANALYSISID):
        '''
            execute shell script that check log file existence
            :return: whether it exists
        '''
        return subprocess.check_output([self.SHELL_PATH + '/checkdir.sh',
                                        WHICHLOG,
                                        ANALYSISID])


