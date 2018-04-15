import requests
import json

from categories import categories
from utility import utility
import os
from os.path import join, dirname
from dotenv import load_dotenv

import copy

import subprocess
import re


dotenv_path = join(dirname(__file__), './documents/local/app-env')
load_dotenv(dotenv_path)

class ProcessSonar (object):

    def __init__(self, group, project):

        self.GROUPID = 'duke-compsci308:'
        if project is None:
            project = ""
        self.GITLABGROUP = group
        self.PLAIN_PROJECT = project
        self.TEST_PROJECT = self.GROUPID + project
        self.QUALITY_PROFILE = 'AV-ylMj9F03llpuaxc9n'
        self.SONAR_URL = 'http://coursework.cs.duke.edu:9000'
        self.TOKEN = os.environ.get("GITLAB_TOKEN")

        self.fileChecked = set()
        self.rulesViolated = []
        self.message = []

        for i in range(6):
            self.rulesViolated.append([])
            self.message.append([])
            k = 0
            if i == 0: #communication
                k = len(categories().Communication_sub) - 1
            if i == 1: #modularity
                k = len(categories().Modularity_sub) - 1
            if i == 2: #flexibility
                k = len(categories().Flexibility_sub) - 1
            for j in range(k):
                self.message[i].append([])


    def process(self, onlyDup):

        #if project not been analysis return error
        r = requests.get(self.SONAR_URL + "/api/components/show?component=" + self.TEST_PROJECT)
        found_project = r.json()
        if 'errors' in found_project:
            return utility().errHandler()

        #get number of pages

        total_pages = utility().getNumOfPagesIssues(self.SONAR_URL, self.TEST_PROJECT)

        #get all issues that are open
        issues = utility().getIssues (self.SONAR_URL, self.TEST_PROJECT, total_pages, "")

        #get all rules associate with quanlity profile
        rules = []
        if not onlyDup:
            r = requests.get(
            self.SONAR_URL + '/api/rules/search?ps=500&activation=true&qprofile=' + self.QUALITY_PROFILE)
            rules.extend(r.json()['rules'])
        else:
            rules.extend(categories().duplications)
        #store details
        dup_errmessages = []
        scores = utility().calTotalScoreAllCategory(self.SONAR_URL)
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
                errmessage['severity'] = utility().renameSeverity(issue['severity'])

                #deduct score
                maincategoryname = categories().getMainCateNameById(ruleID)
                if len(maincategoryname) > 0 and ruleID not in scores_checked_Id:
                    scores[maincategoryname] -= utility().getScoreForSeverity(issue['severity'])
                    scores_checked_Id.add(ruleID)

                #add code
                if ruleID == "common-java:DuplicatedBlocks":
                    dup_errmessages.append(errmessage)
                else:
                    errmessage['code'] = []
                    if 'textRange' in issue:
                        textRange = utility().makeTextRange(issue)
                        for entry in textRange:
                            startLine = entry['textRange']['startLine']
                            endLine = entry['textRange']['endLine']
                            r = requests.get(self.SONAR_URL + "/api/sources/show?from=" + str(startLine) +
                                     "&to=" + str(endLine) +
                                     "&key=" + issue['component'])
                            items = r.json()["sources"]

                            entry['code'] = []
                            for item in items:
                                entry['code'].append(item[1])
                            errmessage['code'].append(entry)
                    utility().storeIssue (ruleID, errmessage, self.message, self.rulesViolated)

        if len(dup_errmessages) > 0:
            utility().duplicatedBlockHandlerStore(self.SONAR_URL,
                                                  dup_errmessages,
                                                  self.message,
                                                  self.rulesViolated,
                                                  self.fileChecked)
        # cal percentage

        percentage = utility().calPercentByScore(scores, scores_rem)

        data = utility().dataHandler(self.message, percentage, onlyDup)

        data['severitylist'] = ['fail', 'high', 'medium', 'low', 'info']


        res = json.dumps(data, indent=4, separators=(',', ': '))

        return res

    def statistics(self):

        #http://coursework.cs.duke.edu:9000/api/measures/component?componentKey=duke-compsci308:test&metricKeys=lines

        functions = "functions,"
        classes = "classes,"
        directories = "directories,"
        comment_lines = "comment_lines,"
        comment_lines_density = "comment_lines_density,"
        ncloc = "ncloc"

        r = requests.get(
            self.SONAR_URL + '/api/measures/component?componentKey=' +
            self.TEST_PROJECT + "&metricKeys="  + functions +
            classes + directories + comment_lines + comment_lines_density + ncloc)
        measures = r.json()['component']['measures']
        res = {}
        res ['measures'] = {}
        for measure in measures:
            res['measures'][measure['metric']] = measure['value']

        res['measures']['lmethods'] = []
        res['measures']['lmethods'].extend(self.longestmethods())

        return json.dumps(res)

    def longestmethods (self):

        total_pages = utility().getNumOfPagesIssues(self.SONAR_URL, self.TEST_PROJECT)
        issues = utility().getIssues(self.SONAR_URL, self.TEST_PROJECT, total_pages, "squid:S138") #array

        entries = []

        count = 0

        for issue in issues:
            entries.append({})
            entries[count]['methodlen'] = int(issue['message'].split()[3])
            entries[count]['startline'] = issue['line']
            entries[count]['path'] = issue['component']

            r = requests.get(self.SONAR_URL + "/api/sources/show?from=" + str(issue['textRange']['startLine']) +
                             "&to=" + str(issue['textRange']['endLine']) +
                             "&key=" + issue['component'])
            items = r.json()["sources"]

            entries[count]['code'] = []
            title = 0
            for item in items:
                mname = ""
                if title == 0:
                    mname = utility().stripmethodname(item[1])
                entries[count]['methodname'] = mname
                entries[count]['code'].append(item[1])

            count += 1
        entries.sort(key=lambda x: x['methodlen'], reverse=False)
        return entries[:10]


    def getcommitsonar (self):

        total_pages = utility().getNumOfPagesTree(self.SONAR_URL, self.TEST_PROJECT)
        if total_pages == -1:
            return {}
        files = utility().getFiles(self.SONAR_URL, self.TEST_PROJECT, total_pages)

        commitIds = {}
        authors = {}
        totalnumofcommits = 0
        for file in files:
            r = requests.get(self.SONAR_URL + '/api/sources/scm?key='+ file['key'])
            commits = r.json()['scm']
            for commit in commits:
                newcommit = False
                author = commit[1]
                date = commit[2]
                commitId = commit[3]
                if commitId not in commitIds:
                    commitIds[commitId] = {}
                    commitIds[commitId]['files'] = []
                    commitIds[commitId]['date'] = date
                    newcommit = True
                if file['key'] not in commitIds[commitId]['files']:
                    commitIds[commitId]['files'].append(file['key'])
                if newcommit == True:
                    totalnumofcommits += 1
                    if author not in authors:
                        authors[author] = []
                    authors[author].append(commitId)

        res = {}
        res['authors'] = {}
        for author in authors:
            res['authors'][author] = {}
            res['authors'][author]['commitlist'] = []
            res['authors'][author]['commitdates'] = []
            dates = {}
            for commitId in authors[author]:
                commit = commitIds[commitId]
                entry = {}
                entry['commitId'] = commitId
                entry['files'] = commit['files']
                entry['date'] = commit['date']
                d = commit['date'][:10]
                if d not in dates:
                    dates[d] = 1
                else:
                    dates[d] += 1
                res['authors'][author]['commitlist'].append(entry)
            ls = sorted(dates.iterkeys())
            for l in ls:
                entry = {}
                entry[l] = dates[l]
                res['authors'][author]['commitdates'].append(entry)

            res['authors'][author]['commitlist'].sort(key=lambda x: x['date'], reverse=False)
            numofcommits = len(res['authors'][author]['commitlist'])
            res['authors'][author]['numofcommits'] = numofcommits
            res['authors'][author]['percentageofcommits'] = 100.00 * numofcommits / totalnumofcommits


        return json.dumps(res)


    def getcommit (self, onlyStat):

        GITLAB_URL = "https://coursework.cs.duke.edu/api/v4"
        URL = GITLAB_URL +"/groups/" + self.GITLABGROUP + "/projects?search=" + self.PLAIN_PROJECT

        r  = requests.get(URL, headers={'PRIVATE-TOKEN': self.TOKEN})
        projects = r.json()
        projectid = -1
        for p in projects:
            if p['name'] ==self.PLAIN_PROJECT:
                projectid = p['id']
                break
        if projectid == -1:
            return []

        res = {}
        res['authors'] = {}
        dates = {}
        commits = utility().getcommits(GITLAB_URL, projectid, self.TOKEN)

        studentidmaps = utility().readStudentInfo()

        if onlyStat:
            return self.getcommitstatfast(studentidmaps)

        for commit in commits:
            # retrieve gitlab id
            authoremail = commit['author_email']
            authorname = utility().convertEmailtoGitlabId(authoremail,studentidmaps)

            #get other info

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

            #handle date

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

        for author in res['authors']:
            res['authors'][author]['commitdates'].sort(key=lambda x: x.keys(), reverse=False)
            res['authors'][author]['commitlist'].sort(key=lambda x: x['date'], reverse=False)
            numofcommits = len(res['authors'][author]['commitlist'])
            res['authors'][author]['numofcommits'] = numofcommits
            res['authors'][author]['percentageofcommits'] = 100.00 * numofcommits / totalnumofcommits

        return json.dumps(res)


    def getcommitstatfast(self, studentidmaps):
        stats = subprocess.check_output(['./stats.sh', self.TOKEN, self.GITLABGROUP, self.PLAIN_PROJECT])
        parsed = re.split(r'\n--\n', stats)

        res = {}
        res_dates = {}
        current_author = ""
        converted_date = ""
        left_bound = utility().getDateFromTuple("2099 Dec 31")
        right_bound = utility().getDateFromTuple("1999 Jan 1")
        for p in parsed:
            lines = p.split("\n")
            for line in lines:

                if "Author:" in line:
                    authorline = line.split()
                    authoremail = authorline[-1]
                    authoremail = authoremail[1:-1]
                    current_author = utility().convertEmailtoGitlabId(authoremail,studentidmaps)
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
                    numerical_date = utility().getDateFromTuple(current_date)
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

        res["bounds"] = {
            "left" : left_bound.strftime('%Y/%m/%d'),
            "right" : right_bound.strftime('%Y/%m/%d')
        }

        return json.dumps(res)

    def getproject(self):

        res = {}
        r = requests.get(self.SONAR_URL + "/api/components/show?component=" + self.TEST_PROJECT)
        found_project = r.json()
        if 'errors' in found_project:
            res['sonar'] = "not found"
        else:
            res['sonar'] = "found"
       
        GITLAB_URL = "https://coursework.cs.duke.edu/api/v4"
        URL = GITLAB_URL + "/groups/" + self.GITLABGROUP + "/projects?search=" + self.PLAIN_PROJECT
        r = requests.get(URL, headers={'PRIVATE-TOKEN': self.TOKEN})
        if len(r.json()) == 0:
            res['gitlab'] = "not found"
        else:
            res['gitlab'] = "found"
        return json.dumps(res)

    def getalldirectory(self):
        #TODO
        res = {}
        res['root'] = {}
        return res



if __name__ == '__main__':


    #ProcessSonar("sonar_test").getcommit("CompSci308_2018Spring", "slogo_team02",True)
    print ProcessSonar("CompSci308_2018Spring", "slogo_team02").getproject()


    '''
        
    '''