
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

        self.localhepler = LocalHelper(group, project)  # stores and handles all local related functions
        self.fileChecked = set()  # whether files are checked
        self.rulesViolated = []  # store rules violated
        self.message = []  # store details of issues

        # initiate buffers
        for i in range(6):
            self.rulesViolated.append([])
            self.message.append([])
            k = 0

            if i < 3:
                k = CategoriesHelper().getNumSubTitle(i)

            for j in range(k):
                self.message[i].append([])

        # check log folders existed, if not, create

        self.localhepler.executeShellLog()
        self.localhepler.executeShellCode()


    def process(self, onlyDup):

        """
        get issues from sonarqube, filter out irrelevant issues, reconstruct the remaining issues
        according to the predefined 5 main categories and subcategories.

        :param onlyDup: decide if only duplication issues are returned
        :return: issues in the selected project
        """

        # get all issues that are open
        issues = SonarHelper().getIssuesAll(self.localhepler.SONAR_URL,
                                                     self.localhepler.TEST_PROJECT)

        if 'err' in issues:
            return issues

        # get all rules associate with quanlity profile
        rules = []
        if not onlyDup:
            rules.extend(SonarHelper().getRules(self.localhepler.SONAR_URL,
                                                self.localhepler.QUALITY_PROFILE))
        else:
            rules.extend(CategoriesHelper().getDuplications())
            
        # store details
        dup_errmessages = []
        scores = ScoreHelper().calTotalScoreAllCategory(self.localhepler.SONAR_URL)
        scores_rem = copy.deepcopy(scores)
        scores_checked_Id = set()
        for issue in issues:

            ruleID = issue['rule']
            ruleResult = filter(lambda r: r['key'] == ruleID, rules)

            if len(ruleResult) > 0:
                errmessage = DataHelper().makeErrMessage(issue,ruleResult)
                
                # deduct score
                maincategoryname = CategoriesHelper().getMainCateNameById(ruleID)
                if len(maincategoryname) > 0 and ruleID not in scores_checked_Id:
                    scores[maincategoryname] -= ScoreHelper().getScoreForSeverity(issue['severity'])
                    scores_checked_Id.add(ruleID)

                # add code
                if ruleID == "common-java:DuplicatedBlocks":
                    dup_errmessages.append(errmessage)
                else:
                    errmessage['code'] = []
                    DataHelper().storeCodes(SONAR_URL, issue, errmessage)
                    DataHelper().storeIssue (ruleID, errmessage, self.message, self.rulesViolated)

        # if there is duplication issues, store the issues in separate buffer
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

        measures = SonarHelper().getMeasures(SONAR_URL, TEST_PROJECT)
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

            sl = issue['textRange']['startLine']
            el =  issue['textRange']['endLine']
            items = SonarHelper().getSource(SONAR_URL, sl, el, issue)

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

        # using project id to get commits

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

        stats = self.localhepler.executeShellStats()   # call shell script to get statistics information

        parsed = re.split(r'\n--\n', stats)  # delete empty lines

        res = {}  # result
        res_dates = {}  # store dates correspond to each author
        current_author = ""  # current author
        converted_date = ""  # dates after conversion
        left_bound = FormatHelper().getDateFromTuple("2099 Dec 31")  # initial left bound
        right_bound = FormatHelper().getDateFromTuple("1999 Jan 1")  #initial right bound

        # start to iterating through parsed statistics
        for p in parsed:
            lines = p.split("\n")

            #  iterating each line
            for line in lines:

                # if keyword author is found in the line, store the author information
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

        """
        check if project exist in sonar and gitlab
        :return: string contains whether project exists
        """

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

    def getbydirectory(self):

        """
        return all issues corresponding to authors
        :return: json contains the directories and files and issues in them
        """
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

            if self.localhepler.shouldSkipDir(rootshort, ["src"]):
                continue

            res[rootshort] = {}
            res[rootshort]['directories'] = FormatHelper().getFullPath(rootshort, subdirs)
            res[rootshort]['files'] = FormatHelper().getFullPath(rootshort, files)


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

        """
        get history of analysis
        :return: history
        """

        # iterating through log directory
        resdict = {}
        for filename in os.listdir(self.localhepler.LOG_STATISTICS):
            # if file end with json, open the file and add it to the buffer
            if filename.endswith(".json"):
                with open(self.localhepler.LOG_STATISTICS + "/" + filename, 'r') as f:
                    data = json.load(f)
                    resdict[filename] = data
        res = []  # store the result

        # sort the result by analysis date
        for key in sorted(resdict.iterkeys()):
            entry = {key:resdict[key]}
            res.append(entry)

        return json.dumps(res)

    def getbyauthor (self, onlyDup):
        
        """
        get issues by authors
        :param onlyDup: if only returns issues regarding duplication
        :return: json contains authors and issues in their codes
        """

        # get all issues that are open
        issues = SonarHelper().getIssuesAll(self.localhepler.SONAR_URL,
                                                     self.localhepler.TEST_PROJECT)
        if 'err' in issues:
            return issues

        rules = SonarHelper().getRules(self.localhepler.SONAR_URL,
                                       self.localhepler.QUALITY_PROFILE)

        res = {}
        for issue in issues:
            ruleResult = DataHelper().filterRuleFromSonar(issue, rules)
            if len(ruleResult) > 0:
                author = issue['author']
                if author not in res:
                    res[author] = {}








if __name__ == '__main__':

    ProcessSonar("CompSci308_2018Spring", "test-xu").getbyauthor()

