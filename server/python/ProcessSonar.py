
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

from Helper import Helper


dotenv_path = dirname(__file__)[:-14] + "/server/documents/local/app-env"
load_dotenv(dotenv_path)

class ProcessSonar (object):

    """
    handles all incoming requests
    """

    def __init__(self, group, project):

        """
        init process sonar class and set buffers accordingly
        :param group: group the project belongs to
        :param project: project name
        """

        self.helper = Helper(group, project)

        # check log folders existed, if not, create

        self.helper.checkAllLogs()
        self.helper.checkQProfileLogReq()


    def getcategoryoverview (self):
        issues = self.helper.getIssuesAll()

        if 'err' in issues:
            return issues

        # get all rules associate with quanlity profile
        rules = []

        rules.extend(self.helper.ruleswithdetail)


        # store details

        scores = self.helper.calTotalScoreAllCategory()
        scores_rem = copy.deepcopy(scores)
        scores_checked_Id = set()

        for issue in issues:

            ruleID = issue['rule']

            ruleResult = filter(lambda r: r['key'] == ruleID, rules)

            if len(ruleResult) > 0:

                # deduct score
               self.helper.deductscore(ruleID, scores_checked_Id, issue, scores)



        # cal percentage

        percentage = self.helper.calPercentByScore(scores, scores_rem)

        res = self.helper.jsonify(percentage)

        return res


    def getcategoryissues (self, main, sub):
        return



    def process(self, onlyDup, byAuthor):

        """
        get issues from sonarqube, filter out irrelevant issues, reconstruct the remaining issues
        according to the predefined 5 main categories and subcategories.

        :param onlyDup: decide if only duplication issues are returned
        :return: issues in the selected project
        """


        whichCache = self.helper.LOG_ISSUES_GENERAL_DIR
        if byAuthor:
            whichCache = self.helper.LOG_ISSUES_AUTHOR_DIR
        if onlyDup:
            whichCache = self.helper.LOG_ISSUES_DUPLICATIONS_DIR

        cachedissues = self.checkCached(whichCache)

        if not cachedissues == "NO CACHE":

            return self.helper.jsonify(cachedissues)

        # get all issues that are open
        issues = self.helper.getIssuesAll()

        if 'err' in issues:
            return issues

        # get all rules associate with quanlity profile
        rules = []
        if not onlyDup:
            rules.extend(self.helper.ruleswithdetail)
        else:
            rules.extend(self.helper.getDuplicationsLocal())

            
        # store details
        dup_errmessages = []
        scores = self.helper.calTotalScoreAllCategory()
        scores_rem = copy.deepcopy(scores)
        scores_checked_Id = set()
        for issue in issues:

            ruleID = issue['rule']
            ruleResult = filter(lambda r: r['key'] == ruleID, rules)

            if len(ruleResult) > 0:
                errmessage = self.helper.makeErrMessage(issue,ruleResult)

                # deduct score
                self.helper.deductscore(ruleID, scores_checked_Id, issue, scores)

                # add code
                if ruleID == "common-java:DuplicatedBlocks":
                    dup_errmessages.append(errmessage)
                else:
                    errmessage['code'] = []
                    self.helper.storeCodes(issue, errmessage)
                    self.helper.storeIssue (ruleID, errmessage)

        # if there is duplication issues, store the issues in separate buffer
        if len(dup_errmessages) > 0:
            self.helper.duplicatedBlockHandlerStore(dup_errmessages)

        # cal percentage

        percentage = self.helper.calPercentByScore(scores, scores_rem)
        data = self.helper.dataHandler(percentage, onlyDup)

        if byAuthor:
           data = self.getbyauthor(data)


        # store severity list

        data['severitylist'] = self.helper.getSeverityList()

        # if not only duplication, store the log   

        self.helper.checkAnalysisLog(whichCache,data)
        if byAuthor:
            self.helper.checkAnalysisLog(self.helper.LOG_STATISTICS_AUTHOR_DIR,
                                            self.helper.getNumIssuesAllAuthor(data))


        res = self.helper.jsonify(data)

        return res

    def getbyauthor (self, data):
        """
        re-arrange result by author
        :return: re-arranged issues by author
        """
        errors = data['error']
        res = {}
        for maincategory, possibleissues in errors.iteritems():
            # if code smell or java note
            if type(possibleissues) is list:
                  self.helper.handleAuthorStore(possibleissues, maincategory, "",  res)
                  
            # if other main categories
            else:
           
                for subcategory, issues in possibleissues.iteritems():
                   
                    self.helper.handleAuthorStore(issues['detail'], maincategory, subcategory, res)
        return self.helper.jsonify(res)

    def statistics(self):

        """
        get the statistics of the project
        :return:  statistics in json
        """

        measures = self.helper.getMeasuresReq()
        res = {}
        res ['measures'] = {}
        for measure in measures:
            res['measures'][measure['metric']] = measure['value']

        #store longest methods
        res['measures']['lmethods'] = []
        res['measures']['lmethods'].extend(self.longestmethods())

        #write logs to local
        self.helper.checkAnalysisLog(self.helper.LOG_STATISTICS_GENERAL_DIR,
                                     res)

        return self.helper.jsonify(res)

    def longestmethods (self):

        """
        get the longest methods (at least more than 15 lines of codes)
        :return: top 10 longest methods names that exceed 15 lines of codes
        """

        total_pages = self.helper.\
            getNumOfPagesIssuesReq()  # get total number of pages in response


        issues = self.helper.getIssuesReq(total_pages,
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
            items = self.helper.getSourceReq(sl, el, issue)

            entries[count]['code'] = []
            title = 0

            # strip methond name and store codes

            for item in items:
                mname = ""
                if title == 0:
                    mname = self.helper.stripmethodname(item[1])
                entries[count]['methodname'] = mname
                entries[count]['code'].append(item[1])

            count += 1

         # sort the result by method length
        entries.sort(key=lambda x: x['methodlen'], reverse=False)

        #make res
        res = {}
        res['method'] = []
        res['method'].extend(entries[:10])
        return self.helper.jsonify(res)


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
              + self.helper.GITLAB_GROUP \
              + "/projects?search="\
              + self.helper.PLAIN_PROJECT

        r  = requests.get(URL, headers={'PRIVATE-TOKEN': self.helper.TOKEN})
        projects = r.json()

        # get project id from response
        projectid = -1
        for p in projects:
            if p['path'] ==self.helper.PLAIN_PROJECT \
                    or p['name'] == self.helper.PLAIN_PROJECT:
                projectid = p['id']
                break

        if projectid == -1:
            return []

        # using project id to get commits

        res = {}
        res['authors'] = {}
        dates = {}
        commits = self.helper.getcommits(GITLAB_URL, projectid, self.helper.TOKEN)

        # read in student ids and names from csv

        studentidmaps = self.helper.readStudentInfo()

        # if only statistics is requested, get the statistics using the student id map

        if onlyStat:
            return self.getcommitstatfast(studentidmaps)

        # iterating through all commits and stores relevant information

        for commit in commits:
            # retrieve gitlab id
            authoremail = commit['author_email']
            authorname = self.helper.convertEmailtoGitlabId(authoremail,studentidmaps)

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


        return self.helper.jsonify(res)


    def getcommitstatfast(self, studentidmaps):

        """
        get statistics info of commits
        :param studentidmaps:  store student ids and names
        :return: statistics information of commits
        """

        stats = self.helper.executeShellStats()   # call shell script to get statistics information

        parsed = re.split(r'\n--\n', stats)  # delete empty lines

        res = {}  # result
        res_dates = {}  # store dates correspond to each author
        current_author = ""  # current author
        converted_date = ""  # dates after conversion
        left_bound = self.helper.getDateFromTuple("2099 Dec 31")  # initial left bound
        right_bound = self.helper.getDateFromTuple("1999 Jan 1")  #initial right bound

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
                    current_author = self.helper.convertEmailtoGitlabId(authoremail,studentidmaps)
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
                    numerical_date = self.helper.getDateFromTuple(current_date)
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

        projectdates = self.helper.readProjectDates(self.helper.PLAIN_PROJECT)
        startdate = projectdates['STARTDATE']
        enddate = projectdates['ENDDATE']

        res["bounds"] = {
            "left" : startdate,
            "right" : enddate
        }


        return self.helper.jsonify(res)

    def getproject(self):

        """
        check if project exist in sonar and gitlab
        :return: string contains whether project exists
        """

        res = {}

        found_project = self.helper.getComponentsReq()
        if 'errors' in found_project:
            res['sonar'] = "not found"
        else:
            res['sonar'] = "found"

        GITLAB_URL = "https://coursework.cs.duke.edu/api/v4"
        URL = GITLAB_URL \
              + "/groups/" \
              + self.helper.GITLAB_GROUP \
              + "/projects?search="\
              + self.helper.PLAIN_PROJECT
        r = requests.get(URL, headers={'PRIVATE-TOKEN': self.helper.TOKEN})
        if len(r.json()) == 0:
            res['gitlab'] = "not found"
        else:
            res['gitlab'] = "found"
        return self.helper.jsonify(res)

    def getbydirectory(self):

        """
        return all issues corresponding to authors
        :return: json contains the directories and files and issues in them
        """
        res = json.loads(self.getproject())

        if res['sonar'] == 'not found':
            return json.dumps({})

        res = {}
        path = self.helper.CODES_PATH \
               + "/" \
               + self.helper.GITLAB_GROUP \
               + "/" \
               + self.helper.PLAIN_PROJECT
        for root, subdirs, files in os.walk(path):

            if "/.git/" in root or root[-4:] == ".git":
                continue

            rootshort = re.sub(path, "", root)
            if rootshort == "":
                rootshort = "."
            if rootshort[0] == '/':
                rootshort = rootshort[1:]

            if self.helper.shouldSkipDir(rootshort, ["src"]):
                continue

            res[rootshort] = {}
            res[rootshort]['directories'] = self.helper.getFullPath(rootshort, subdirs)
            res[rootshort]['files'] = self.helper.getFullPath(rootshort, files)


        issues = json.loads(self.process(False, False))

        for category, mainissuelist in issues['error'].items():

           if category == "Duplications":
               continue
           if isinstance(mainissuelist, dict):
               for subcategory, subissuelist in mainissuelist.items():

                   self.helper.makeIssueEntryForDIR(subissuelist['detail'], res)
           else:
               self.helper.makeIssueEntryForDIR(mainissuelist, res)


        return self.helper.jsonify(res)


    def gethistory (self):

        """
        get history of analysis
        :return: history of statistics for each author and the whole project
        """

        res = {}
        res['general'] =self.helper.readLogJSONAll(self.helper.LOG_STATISTICS_GENERAL_DIR)
        res['author'] = self.helper.readLogJSONAll(self.helper.LOG_STATISTICS_AUTHOR_DIR)

        return self.helper.jsonify(res)


    def getcodemaat(self):
        """
        testing method
        :return:
        """
        return self.helper.executeShellRunCodeMaat()


    def checkCached (self, whichCache):
        """
        check whether the cache exists
        :param whichCache:  which cache to check
        :return: cache or no cache
        """
        cachedissues = {}
        mostrecenttime = self.helper.getMostRecentAnalysisDateReq()
        mostrecenttime = self.helper.adjustSonarTime(mostrecenttime)
        self.helper.readLogJSON(whichCache, mostrecenttime + ".json", cachedissues)
        if len(cachedissues) > 0 :
            return cachedissues.values()[0]
        return "NO CACHE"



if __name__ == '__main__':
   # print ProcessSonar("CompSci308_2018Spring", "test-xu").getcategoryoverview()
    #ProcessSonar("CompSci308_2018Spring", "test-xu").statistics()
    print ProcessSonar("CompSci308_2018Spring", "test-xu").longestmethods()