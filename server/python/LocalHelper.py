"""
Helper class that handle local storage

:Authors:
    - Chengkang Xu <cx33@duke.edu>
"""

import json


import os
from os.path import dirname, abspath
from dotenv import load_dotenv
import os.path

import configparser
import subprocess

ROOT = dirname(__file__)[:-14]
dotenv_path = ROOT + "/server/documents/local/app-env"
load_dotenv(dotenv_path)

from FormatHelper import FormatHelper



class LocalHelper (FormatHelper):

    def __init__(self, group, project):

        super(LocalHelper, self).__init__()

        self.SONAR_GROUP = group + ":"
        if project is None:
            project = ""
        self.ROOT_PATH = self.getRootPath()
        self.GITLAB_GROUP = group
        self.PLAIN_PROJECT = project
        self.YEAR = group.split("_")[1][:4]
        self.SEMESTER = group.split("_")[1][4:]
        self.TEST_PROJECT = self.SONAR_GROUP + project
        self.QUALITY_PROFILE = 'AV-ylMj9F03llpuaxc9n'
        self.SONAR_URL = 'http://coursework.cs.duke.edu:9000'
        self.TOKEN = os.environ.get("GITLAB_TOKEN")
        self.CACHE_PATH = self.ROOT_PATH + "/cache"
        self.CODES_PATH = self.CACHE_PATH + "/codes"
        self.LOGS_PATH = self.CACHE_PATH + "/logs"
        self.SERVER_PATH = self.ROOT_PATH + "/server"
        self.SHELL_PATH = self.SERVER_PATH + "/shell"
        self.LOG_QPROFILE_DIR = self.LOGS_PATH + "/qprofile"
        self.LOG_QPROFILE_KEY_DIR = self.LOG_QPROFILE_DIR + "/" + self.QUALITY_PROFILE
        self.LOG_DIR = self.LOGS_PATH + "/" + self.GITLAB_GROUP + "/" + self.PLAIN_PROJECT
        self.LOG_ISSUES_DIR = self.LOG_DIR + "/issues"
        self.LOG_ISSUES_GENERAL_DIR = self.LOG_ISSUES_DIR + "/general"
        self.LOG_ISSUES_AUTHOR_DIR = self.LOG_ISSUES_DIR + "/author"
        self.LOG_ISSUES_DUPLICATIONS_DIR = self.LOG_ISSUES_DIR + "/duplications"
        self.LOG_ISSUES_CODE_DIR = self.LOG_ISSUES_DIR + "/code"
        self.LOG_STATISTICS_DIR = self.LOG_DIR + "/statistics"
        self.LOG_STATISTICS_GENERAL_DIR = self.LOG_STATISTICS_DIR + "/general"
        self.LOG_STATISTICS_AUTHOR_DIR = self.LOG_STATISTICS_DIR + "/author"
        self.DEPENDENCY_DIR = self.SERVER_PATH + "/dependencies"
        self.ROSTER_PATH = dirname(__file__)[:-14] + '/server/documents/local/rosters/cs308/308_student_data_'
        self.ROSTER_PATH += (self.YEAR + self.SEMESTER + ".csv")




    def readProjectDates (self, project):
        """
        read start dates and end dates of project
        :param project: the name the project
        :return: return the start and end dates
        """
        config = configparser.ConfigParser()
        config.read(ROOT + "/server/documents/config.ini")
        res = {}
        self.storeSingleConfigDate(res, config, "ENDDATE", project)
        self.storeSingleConfigDate(res, config, "STARTDATE", project)

        return res


    def storeSingleConfigDate (self, res, config, key, project):
        """
        Store single configuration date in to res buffer
        :param res:  buffer to hold the result
        :param config: original configuration
        :param key: key in the configuration
        :param project: projects
        :return: void
        """
        res[key] = {}
        for k,v in config[key].items():
            if k in project:
                res[key][k] = v
                return




    def readLogJSON(self, logname, filename, resdict):
        """
        read in data from a single JSON log file
        :param logname: name of log directory to read in
        :param filename: specific log file to read in
        :param resdict: buffer to store the data
        :return: void
        """
        path = logname + "/" + filename
        if not os.path.exists(path) :
            return
        with open(path, 'r') as f:
            data = json.load(f)
            resdict[filename[:-5]] = data

    def readLogJSONAll(self, logname):
        """
        read in all log under a specfic directory
        :param logname: name of log to read in
        :return: JSON contains all log files content
        """
        # iterating through log directory
        resdict = {}
        for filename in os.listdir(logname):
            # if file end with json, open the file and add it to the buffer
            if filename.endswith(".json"):
                self.readLogJSON(logname, filename, resdict)
        res = []  # store the result

        # sort the result by analysis date
        for key in sorted(resdict.iterkeys()):
            entry = {key: resdict[key]}
            res.append(entry)
        return res

    def writeLog (self, logname, data):
        """
        write log file
        :param logname: name of file store the log
        :param data: data to be stored
        """
        with open(logname, 'w') as outfile:
            outfile.write(data)

    def writeLogJSON (self, logname, data):
        """
        write JSON log file
        :param logname: name of JSON file store the log
        :param data: data to be stored
        """
        with open(logname, 'w') as outfile:
            json.dump(data,outfile)



    def dateLogJSON (self, analysisTime, WHICHLOG, data):
        """
        check if the log extisted by checking the last analysis time, if so do nothing, if not caching
        :param analysisTime: last analysis time
        :param WHICHLOG: which log to be written
        :param data: data to be stored
        """

        analysisTime = self.adjustSonarTime(analysisTime)
        existed = self.executeShellCheckDIR(WHICHLOG, analysisTime)
        if "no" in existed:
            self.writeLogJSON(WHICHLOG + "/" + analysisTime + ".json", data)


    #extract gitlabid
    def readStudentInfo (self):

        """
        read student info from csv file and store into the buffer
        :return: email and netids
        """
        emails = {}
        netids = {}
        netidindex = 2
        emailindex = 3
        gitlabidindex = 4

        import csv
        with open(self.ROSTER_PATH, 'rb') as csvfile:
            spamreader = csv.reader(csvfile)

            for row in spamreader:
                emails[row[emailindex]] =row [gitlabidindex]
                netids[row[netidindex]] = row [gitlabidindex]
        res = {}
        res["email"] = emails
        res["netid"] = netids
        return res



    def shouldSkipDir(self, dir, returndirs):
        """
        iterating through all directories to check if dir should be skipped
        :param dir: target dir
        :param returndirs: all directories
        :return: whether it should skip the dir
        """
        for returndir in returndirs:
            if dir == returndir or dir[:4] == "src/":
                return False
        return True



    def getRootPath(self):
        """
        get the root
        :return: root  path
        """
        return abspath(dirname(__file__))[:-14]

    def getSONAR_URL (self):
        """
        return SONAR URL
        :return: SONAR_URL
        """
        return self.SONAR_URL


    def getQUALITY_PROFILE(self):
        """
        return quality profile currently using
        :return: QUALITY_PROFILE
        """
        return self.QUALITY_PROFILE

    def getTEST_PROJECT(self):

        """
        return project currently checking
        :return: TEST_PROJECT
        """
        return self.TEST_PROJECT


    def checkAllLogs(self):
        """
        check all logs existence
        :return:
        """
        self.executeShellLog()
        self.executeShellCode()

    def executeShellLog(self):
        """
        execute shell script that check log folder existence
        :return: output from terminal
        """

        return subprocess.check_output([self.SHELL_PATH + '/logs.sh',
                                        self.GITLAB_GROUP,
                                        self.PLAIN_PROJECT,
                                        self.ROOT_PATH])

    def executeShellCode(self):
        """
        execute shell script that cache gitlab codes
        :return: output from terminal
        """
        return subprocess.check_output([self.SHELL_PATH + '/codes.sh',
                                        self.TOKEN,
                                        self.GITLAB_GROUP,
                                        self.PLAIN_PROJECT,
                                        self.ROOT_PATH])


    def executeShellStats(self):
        """
        execute shell scripts that extract stat information
        :return: stat information
        """
        return subprocess.check_output([self.SHELL_PATH + '/stats.sh',
                                        self.TOKEN,
                                        self.GITLAB_GROUP,
                                        self.PLAIN_PROJECT,
                                        self.ROOT_PATH])

    def executeShellCheckDIR(self, WHICHLOG, ANALYSISID):
        """
        execute shell script that check log file existence
        :return: whether it exists
        """
        return subprocess.check_output([self.SHELL_PATH + '/checkdir.sh',
                                        WHICHLOG,
                                        ANALYSISID])

    def executeShellRunCodeMaat(self):
        """
        execute shell script to get result from code-maat
        :return: code-maate related output
        """

        return subprocess.check_output([self.SHELL_PATH + '/code_maat.sh',
                                        self.DEPENDENCY_DIR,
                                        self.CODES_PATH,
                                        self.LOGS_PATH,
                                        self.GITLAB_GROUP,
                                        self.PLAIN_PROJECT,
                                        self.ROOT_PATH])

    def executeShellStatsAdditional(self):
        """
        additional stat in project
        :return: additional stats
        """
        return subprocess.check_output([self.SHELL_PATH + '/stats_additional.sh',
                                        self.TOKEN,
                                        self.GITLAB_GROUP,
                                        self.PLAIN_PROJECT,
                                        self.ROOT_PATH])




    def executeShellContributionByFile (self, file, start, end):
        """
        get contribution by file
        :param file: path
        :param start:  start line
        :param end: end line
        :return: contributions
        """
        return subprocess.check_output([self.SHELL_PATH + '/contribution_file.sh',
                                        self.TOKEN,
                                        self.GITLAB_GROUP,
                                        self.PLAIN_PROJECT,
                                        self.ROOT_PATH,
                                        file,
                                        str(start),
                                        str(end)])



if __name__  == "__main__":
    subprocess.call(['java', '-jar', '/Users/wellxchen/Desktop/xray/org.malnatij.SVPlugin_1.0.4.1.jar'])

#    java -jar code-maat-1.1-SNAPSHOT-standalone.jar -l logfile.log -c git -a summary
# chmod a+x