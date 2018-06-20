
"""
:Authors:
    - Chengkang Xu <cx33@duke.edu>
"""


import requests
import json


import copy
import re
import os
from os.path import dirname
from dotenv import load_dotenv

from LocalHelper import LocalHelper
from ScoreHelper import ScoreHelper
from GitlabHelper import GitlabHelper
from SonarHelper import SonarHelper
from FormatHelper import FormatHelper
from DataHelper import  DataHelper
from CategoriesHelper import CategoriesHelper


dotenv_path = dirname(__file__)[:-14] + "/server/documents/local/app-env"
load_dotenv(dotenv_path)

class ProcessSonar (object):

    """
    handles all incoming requests
    """

    def __init__(self, group, project):

        """
        init process sonar class and set buffers accordingly
        :param group:
        :param project:
        """

        self.localhepler = LocalHelper(group, project) #stores and handles all local related functions
        self.fileChecked = set() #whether files are checked
        self.rulesViolated = [] #store rules violated
        self.message = [] #store details of issues

        #initiate buffers
        for i in range(6):
            self.rulesViolated.append([])
            self.message.append([])
            k = 0

            if i < 3:
                k = CategoriesHelper().getNumSubTitle(i)

            for j in range(k):
                self.message[i].append([])

        #check log folders existed, if not, create

        self.localhepler.executeShellLog()
        self.localhepler.executeShellCode()


    def process(self, onlyDup):

        """
        get issues from sonarqube, filter out irrelevant issues, reconstruct the remaining issues
        according to the predefined 5 main categories and subcategories.

        :param onlyDup: decide if only duplication issues are returned
        :return: issues in the selected project
        """

        #if project not been analysis return error
        r = requests.get( self.localhepler.SONAR_URL + "/api/components/show?component=" +  self.localhepler.TEST_PROJECT)
        found_project = r.json()
        if 'errors' in found_project:
            return DataHelper().errHandler()

        #get number of pages

        total_pages = SonarHelper().getNumOfPagesIssues( self.localhepler.SONAR_URL,
                                                         self.localhepler.TEST_PROJECT)

        #get all issues that are open
        issues = SonarHelper().getIssues (self.localhepler.SONAR_URL,
                                          self.localhepler.TEST_PROJECT,
                                          total_pages, "")

        #get all rules associate with quanlity profile
        rules = []
        if not onlyDup:
            r = requests.get(
            self.localhepler.SONAR_URL +
            '/api/rules/search?ps=500&activation=true&qprofile=' +
            self.localhepler.QUALITY_PROFILE)
            rules.extend(r.json()['rules'])
        else:
            rules.extend(CategoriesHelper().getDuplications())
        #store details
        dup_errmessages = []
        scores = ScoreHelper().calTotalScoreAllCategory(self.localhepler.SONAR_URL)
        scores_rem = copy.deepcopy(scores)
        scores_checked_Id = set()
        for issue in issues:

            ruleID = issue['rule']
            ruleResult = filter(lambda r: r['key'] == ruleID, rules)

            if len(ruleResult) > 0:
                errmessage = {}
                errmessage['path'] = [issue['component']]
                errmessage['rule'] = ruleResult[0]['name']
                errmessage['message'] = issue['message']
                errmessage['severity'] = ScoreHelper().renameSeverity(issue['severity'])

                #deduct score
                maincategoryname = CategoriesHelper().getMainCateNameById(ruleID)
                if len(maincategoryname) > 0 and ruleID not in scores_checked_Id:
                    scores[maincategoryname] -= ScoreHelper().getScoreForSeverity(issue['severity'])
                    scores_checked_Id.add(ruleID)

                #add code
                if ruleID == "common-java:DuplicatedBlocks":
                    dup_errmessages.append(errmessage)
                else:
                    errmessage['code'] = []
                    if 'textRange' in issue:
                        textRange = SonarHelper().makeTextRange(issue)
                        for entry in textRange:
                            startLine = entry['textRange']['startLine']
                            endLine = entry['textRange']['endLine']
                            r = requests.get(self.localhepler.SONAR_URL + "/api/sources/show?from=" + str(startLine) +
                                     "&to=" + str(endLine) +
                                     "&key=" + issue['component'])
                            items = r.json()["sources"]

                            entry['code'] = []
                            for item in items:
                                entry['code'].append(item[1])
                            errmessage['code'].append(entry)
                    DataHelper().storeIssue (ruleID, errmessage, self.message, self.rulesViolated)

        #if there is duplication issues, store the issues in separate buffer
        if len(dup_errmessages) > 0:
            SonarHelper().duplicatedBlockHandlerStore(self.localhepler.SONAR_URL,
                                                  dup_errmessages,
                                                  self.message,
                                                  self.rulesViolated,
                                                  self.fileChecked)
        # cal percentage

        percentage = ScoreHelper().calPercentByScore(scores, scores_rem)
        data = DataHelper().dataHandler(self.message, percentage, onlyDup)

        # store severity list

        data['severitylist'] = CategoriesHelper().getSeverityList()

        res = json.dumps(data, indent=4, separators=(',', ': '))

        # if not only duplication, store the log

        if not onlyDup:
            self.localhepler.writeLog(self.localhepler.LOG_ISSUES, res)

        return res

    def statistics(self):

        """
        get the statistics of the project
        :return:  statistics in json
        """

        functions = "functions," #keyword for number of functions
        classes = "classes," #keyword for number of classes
        directories = "directories," #keyword for number of directories
        comment_lines = "comment_lines," #keyword for number of comments
        comment_lines_density = "comment_lines_density," #keyword for density of comments
        ncloc = "ncloc" #keyword for number of lines in total

        #query sonarqube to get the statistics

        r = requests.get(
            self.localhepler.SONAR_URL + '/api/measures/component?componentKey=' +
            self.localhepler.TEST_PROJECT + "&metricKeys="  + functions +
            classes + directories + comment_lines + comment_lines_density + ncloc)
        measures = r.json()['component']['measures']
        res = {}
        res ['measures'] = {}
        for measure in measures:
            res['measures'][measure['metric']] = measure['value']

        #store longest methods
        res['measures']['lmethods'] = []
        res['measures']['lmethods'].extend(self.longestmethods())

        #write logs to local
        self.localhepler.handleLogJSON(self.localhepler.LOG_STATISTICS, res)

        return json.dumps(res)

    def longestmethods (self):

        """
        get the longest methods (at least more than 15 lines of codes)
        :return: top 10 longest methods names that exceed 15 lines of codes
        """

        total_pages = SonarHelper().\
            getNumOfPagesIssues(self.localhepler.SONAR_URL,
                                self.localhepler.TEST_PROJECT)  # get total number of pages in response


        issues = SonarHelper().getIssues(self.localhepler.SONAR_URL,
                                         self.localhepler.TEST_PROJECT,
                                         total_pages,
                                         "squid:S138")  # get issues with method too long

        entries = []  # store result

        count = 0  # number of entries

        # start to iterating issues and store relevant fields

        for issue in issues:
            entries.append({})
            entries[count]['methodlen'] = int(issue['message'].split()[3])
            entries[count]['startline'] = issue['line']
            entries[count]['path'] = issue['component']

            # get codes from sonar

            r = requests.get(self.localhepler.SONAR_URL
                             + "/api/sources/show?from="
                             + str(issue['textRange']['startLine'])
                             + "&to=" + str(issue['textRange']['endLine'])
                             + "&key=" + issue['component'])
            items = r.json()["sources"]

            entries[count]['code'] = []
            title = 0

            # strip methond name and store codes

            for item in items:
                mname = ""
                if title == 0:
                    mname = FormatHelper().stripmethodname(item[1])
                entries[count]['methodname'] = mname
                entries[count]['code'].append(item[1])

            count += 1

         # sort the result by method length
        entries.sort(key=lambda x: x['methodlen'], reverse=False)
        return entries[:10]


    def getcommit (self, onlyStat):

        """
        get commit information/statistics from gitlab
        :param onlyStat: whether only statistics is returned
        :return: information about commits or statistics about commits
        """

        # request gitlab for projects information based on group

        GITLAB_URL = "https://coursework.cs.duke.edu/api/v4"
        URL = GITLAB_URL \
              +"/groups/" \
              + self.localhepler.GITLAB_GROUP \
              + "/projects?search="\
              + self.localhepler.PLAIN_PROJECT

        r  = requests.get(URL, headers={'PRIVATE-TOKEN': self.localhepler.TOKEN})
        projects = r.json()

        # get project id from response
        projectid = -1
        for p in projects:
            if p['path'] ==self.localhepler.PLAIN_PROJECT \
                    or p['name'] == self.localhepler.PLAIN_PROJECT:
                projectid = p['id']
                break

        if projectid == -1:
            return []

        # using projectid to get commits

        res = {}
        res['authors'] = {}
        dates = {}
        commits = GitlabHelper().getcommits(GITLAB_URL, projectid, self.localhepler.TOKEN)

        # read in student ids and names from csv

        studentidmaps = self.localhepler.readStudentInfo()

        # if only statistics is requested, get the statistics using the student id map

        if onlyStat:
            return self.getcommitstatfast(studentidmaps)

        # iterating through all commits and stores relevant information

        for commit in commits:
            # retrieve gitlab id
            authoremail = commit['author_email']
            authorname = GitlabHelper().convertEmailtoGitlabId(authoremail,studentidmaps)

            # get other info

            commitdate = commit['committed_date']
            commitid = commit['id']

            if authorname not in res['authors']:
                res['authors'][authorname] = {}
                res['authors'][authorname]['commitlist'] = []
                res['authors'][authorname]['commitdates'] = []
                dates[authorname] = {}
            entry = {}
            entry['commitId'] = commitid
            entry['date'] = commitdate
            entry['files'] = []
            res['authors'][authorname]['commitlist'].append(entry)

            # handle date

            shortdate = commitdate[:10]
            curnumdates = len(res['authors'][authorname]['commitdates'])
            if shortdate not in dates[authorname]:
                dates[authorname][shortdate] = curnumdates
            datesindex = dates[authorname][shortdate]
            if datesindex == curnumdates:
                entry = {}
                entry[shortdate] = 1
                res['authors'][authorname]['commitdates'].append(entry)
            else:
                res['authors'][authorname]['commitdates'][datesindex][shortdate] += 1

        totalnumofcommits = len(commits)

        # sort commitsdates, lists and store other information
        for author in res['authors']:
            res['authors'][author]['commitdates'].sort(key=lambda x: x.keys(), reverse=False)
            res['authors'][author]['commitlist'].sort(key=lambda x: x['date'], reverse=False)
            numofcommits = len(res['authors'][author]['commitlist'])
            res['authors'][author]['numofcommits'] = numofcommits
            res['authors'][author]['percentageofcommits'] = 100.00 * numofcommits / totalnumofcommits


        return json.dumps(res)


    def getcommitstatfast(self, studentidmaps):

        """
        get statistics info of commits
        :param studentidmaps:  store student ids and names
        :return: statistics information of commits
        """

        # call shell script to get statistics information

        stats = self.localhepler.executeShellStats()

        parsed = re.split(r'\n--\n', stats)

        res = {}
        res_dates = {}
        current_author = ""
        converted_date = ""
        left_bound = FormatHelper().getDateFromTuple("2099 Dec 31")
        right_bound = FormatHelper().getDateFromTuple("1999 Jan 1")
        for p in parsed:
            lines = p.split("\n")
            for line in lines:

                if "Author:" in line:
                    authorline = line.split()
                    authoremail = authorline[-1]
                    authoremail = authoremail[1:-1]
                    current_author = GitlabHelper().convertEmailtoGitlabId(authoremail,studentidmaps)
                    if current_author not in res:
                        res[current_author] = {}
                        res[current_author]["dates"] = {}
                        res[current_author]["total"] = {}
                        res[current_author]["total"]["files changed"] = 0
                        res[current_author]["total"]["insertions"] = 0
                        res[current_author]["total"]["deletions"] = 0
                        res_dates[current_author] = []
                elif "Date:" in line:
                    #check bounds
                    dateline = line.split()
                    current_date = dateline[5] + " " + dateline[2] + " " + dateline[3]
                    numerical_date = FormatHelper().getDateFromTuple(current_date)
                    if numerical_date > right_bound:
                        right_bound = numerical_date
                    elif numerical_date < left_bound:
                        left_bound = numerical_date
                    converted_date = numerical_date.strftime('%Y/%m/%d')
                    #modify res
                    if converted_date not in res_dates[current_author]:
                        res_dates[current_author].append(converted_date)
                        inentry = {}
                        inentry["files changed"] = 0
                        inentry["insertions"] = 0
                        inentry["deletions"] = 0
                        res[current_author]["dates"][converted_date] = inentry
                elif "file changed," in line or "files changed," in line:
                    statsline = line.split(", ")
                    for stat in statsline:

                        key = ""
                        if "files changed" in stat or 'file changed' in stat:
                            key = "files changed"
                        elif "insertions" in stat or "insertion" in stat:
                            key = "insertions"
                        elif "deletions" in stat or "deletion" in stat:
                            key = "deletions"

                        statdata = stat.split()

                        res[current_author]["dates"][converted_date][key] += int(statdata[0])
                        res[current_author]["total"][key] += int(statdata[0])

        for authorname, v in res_dates.items():
            res[authorname]["sorteddates"] = []
            res[authorname]["sorteddates"].extend(res_dates[authorname])

        projectdates = self.localhepler.readProjectDates(self.localhepler.PLAIN_PROJECT)
        startdate = projectdates['STARTDATE']
        enddate = projectdates['ENDDATE']

        res["bounds"] = {
            "left" : startdate,
            "right" : enddate
        }

        DataHelper().displayData(res)
        return json.dumps(res)

    def getproject(self):

        res = {}
        r = requests.get(self.localhepler.SONAR_URL
                         + "/api/components/show?component="
                         + self.localhepler.TEST_PROJECT)
        found_project = r.json()
        if 'errors' in found_project:
            res['sonar'] = "not found"
        else:
            res['sonar'] = "found"

        GITLAB_URL = "https://coursework.cs.duke.edu/api/v4"
        URL = GITLAB_URL \
              + "/groups/" \
              + self.localhepler.GITLAB_GROUP \
              + "/projects?search="\
              + self.localhepler.PLAIN_PROJECT
        r = requests.get(URL, headers={'PRIVATE-TOKEN': self.localhepler.TOKEN})
        if len(r.json()) == 0:
            res['gitlab'] = "not found"
        else:
            res['gitlab'] = "found"
        return json.dumps(res)

    def getalldirectory(self): #delete packages that do not have any .java

        res = json.loads(self.getproject())

        if res['sonar'] == 'not found':
            return json.dumps({})

        res = {}
        path = self.localhepler.CODES_PATH \
               + "/" \
               + self.localhepler.GITLAB_GROUP \
               + "/" \
               + self.localhepler.PLAIN_PROJECT
        for root, subdirs, files in os.walk(path):

            if "/.git/" in root or root[-4:] == ".git":
                continue

            rootshort = re.sub(path, "", root)
            if rootshort == "":
                rootshort = "."
            if rootshort[0] == '/':
                rootshort = rootshort[1:]

            if DataHelper().shouldSkipDir(rootshort, ["src"]):
                continue

            res[rootshort] = {}
            res[rootshort]['directories'] = FormatHelper().getFullPath(rootshort, subdirs)
            res[rootshort]['files'] = FormatHelper().getFullPath(rootshort, files)

        #utility().displayData(res)
        issues = json.loads(self.process(False))

        for category, mainissuelist in issues['error'].items():

           if category == "Duplications":
               continue
           if isinstance(mainissuelist, dict):
               for subcategory, subissuelist in mainissuelist.items():

                   DataHelper().makeIssueEntryForDIR(subissuelist['detail'],
                                                     self.localhepler.TEST_PROJECT,
                                                     res)
           else:
               DataHelper().makeIssueEntryForDIR(mainissuelist,
                                                 self.localhepler.TEST_PROJECT,
                                                 res)

        return json.dumps(res)


    def getHistory (self):

        resdict = {}
        for filename in os.listdir(self.localhepler.LOG_STATISTICS):
            if filename.endswith(".json"):
                with open(self.localhepler.LOG_STATISTICS + "/" + filename, 'r') as f:
                    data = json.load(f)
                    resdict[filename] = data
        res = []
        for key in sorted(resdict.iterkeys()):
            entry = {key:resdict[key]}
            res.append(entry)

        DataHelper().displayData(res)
        return json.dumps(res)





if __name__ == '__main__':

    ProcessSonar("CompSci308_2018Spring", "test-xu").getHistory()

