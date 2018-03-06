import requests
import json

from categories import categories
from utility import utility
import gitlab

class ProcessSonar (object):

    def __init__(self, arg):

        self.GROUPID = 'duke-compsci308:'
        if arg is None:
            arg = ""
        self.TEST_PROJECT = self.GROUPID + arg
        self.QUALITY_PROFILE = 'AV-ylMj9F03llpuaxc9n'
        self.SONAR_URL = 'http://coursework.cs.duke.edu:9000'

        self.fileChecked = set()
        self.rulesViolated = []
        self.message = []

        for i in range(6):
            self.rulesViolated.append([])
            self.message.append([])
            k = 0
            if i == 0: #communication
                k = 7
            if i == 1: #modularity
                k = 8
            if i == 2: #flexibility
                k = 4
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
        for issue in issues:

            ruleID = issue['rule']
            ruleResult = filter(lambda r: r['key'] == ruleID, rules)  #rulename = ruleResult[0]['name']

            if len(ruleResult) > 0:

                errmessage = {}
                errmessage['path'] = [issue['component']]
                errmessage['rule'] = ruleResult[0]['name']
                errmessage['message'] = issue['message']
                errmessage['severity'] = issue['severity']
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
        percentage = []
        percentage.append(utility().calPercentage(categories().communication, self.rulesViolated[0]))
        percentage.append(utility().calPercentage(categories().modularity, self.rulesViolated[1]))
        percentage.append(utility().calPercentage(categories().flexibility, self.rulesViolated[2]))
        percentage.append(utility().calPercentage(categories().javanote, self.rulesViolated[3]))
        percentage.append(utility().calPercentage(categories().codesmell, self.rulesViolated[4]))
        percentage.append(utility().calPercentage(categories().duplicationsID, self.rulesViolated[5]))


        data = utility().dataHandler(self.message, percentage, onlyDup)
        #utility().displayData(data)
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


    def getcommit (self):

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


    def getcommitv2 (self,group, project):

        GITLAB_URL = "https://coursework.cs.duke.edu/api/v4"
        URL = GITLAB_URL +"/groups/" + group + "/projects?search=" + project

        r  = requests.get(URL, headers={'PRIVATE-TOKEN': 'e1Wh-viL3xFYskHgirxR'})
        projects = r.json()
        projectid = -1
        for p in projects:
            if p['name'] ==project:
                projectid = p['id']
                break
        if projectid == -1:
            return []

        res = {}
        res['authors'] = {}
        dates = {}


        commits = utility().getcommits(GITLAB_URL, projectid)

        for commit in commits:
            authorname = commit['author_name']
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
            res['authors'][author]['commitlist'].sort(key=lambda x: x['date'], reverse=False)
            numofcommits = len(res['authors'][author]['commitlist'])
            res['authors'][author]['numofcommits'] = numofcommits
            res['authors'][author]['percentageofcommits'] = 100.00 * numofcommits / totalnumofcommits

        utility().displayData(res)

    def getrules (self, main, sub):
        #TODO
        res = ""
        return res


if __name__ == '__main__':
    #ProcessSonar("test").getcommit()
    data = ProcessSonar("test").getcommitv2("CompSci308_2017Fall", "sonar_test")


    '''
        
    '''