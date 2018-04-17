import re
from categories import categories
import json
import requests

import os
from os.path import join, dirname, abspath
from dotenv import load_dotenv
dotenv_path = dirname(__file__)[:-14] + "/server/documents/local/app-env"
load_dotenv(dotenv_path)

import datetime

class utility ():

    def getRootPath(self):

        return abspath(dirname(__file__))[:-14]

    def writeData (self, data):

        with open('data.txt', 'w') as outfile:
            outfile.write(data)

    def displayData(self, data):
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(data)

    def activateRule (self, SONAR_URL, QUALITY_PROFILE, ruleID):
        SONAR_LOGIN = os.environ.get("SONAR_LOGIN")
        SONAR_PASSWORD = os.environ.get("SONAR_PASSWORD")
        r = requests.post(SONAR_URL + '/api/qualityprofiles/activate_rule?=' ,
                          data={'profile_key':QUALITY_PROFILE, 'rule_key' : ruleID},
                          auth=(SONAR_LOGIN, SONAR_PASSWORD))

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

    def makeIssueEntryForDIR (self, issuelist, TEST_PROJECT, res):
        for issue in issuelist:
            for filepath in issue['path']:
                filepathshort = re.sub(TEST_PROJECT + ":", "", filepath)
                lastslash = filepathshort.rfind("/")
                parentdirectory = filepathshort[:lastslash]
                if parentdirectory not in res or filepathshort not in res[parentdirectory]["files"]:
                    continue
                res[parentdirectory]["files"][filepathshort].append(issue)

    def makeMap(self, rules, main, sub):
        res = ""
        for rule in rules:
            if sub > 0:
                res = res + "'" + rule + "' : ['" + main + "'," + str(sub) + "],\n"
            else:
                res = res + "'" + rule + "': ['" + main + "'],\n"

        return res

    #strip method name
    def stripmethodname (self, line):
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


    #strip html code
    def striphtml(self, data):
        p = re.compile(r'<.*?>')
        p = p.sub('', data)
        p = p.replace('&lt;', '<')
        p = p.replace('&gt;', '>')
        p = p.replace('&le;', '<=')
        p = p.replace('&ge;', '>=')
        return p


    #get number of pages for issues

    def getNumOfPagesIssues (self, SONAR_URL, TEST_PROJECT):
        QUERY = '/api/issues/search?ps=500&componentKeys='
        r = requests.get(SONAR_URL + QUERY + TEST_PROJECT)
        total_number_entries = r.json()['total']
        page_size = r.json()['ps']
        total_pages = 2
        if total_number_entries > page_size:
            total_pages += total_number_entries / page_size
            if total_number_entries % page_size != 0:
                total_pages += 1
        return total_pages

    # get number of pages for tree

    def getNumOfPagesTree(self, SONAR_URL, TEST_PROJECT):
        QUERY = '/api/components/tree?ps=500&component='
        r = requests.get(SONAR_URL + QUERY + TEST_PROJECT)
        if 'errors' in r.json():
            return -1
        total_number_entries = r.json()['paging']['total']
        page_size = r.json()['paging']['pageSize']
        total_pages = 2
        if total_number_entries > page_size:
            total_pages += total_number_entries / page_size
            if total_number_entries % page_size != 0:
                total_pages += 1
        return total_pages

    #get all issues or for specific rule

    def getIssues (self, SONAR_URL, TEST_PROJECT, total_pages, rule):
        issues = []
        ruleToCheck = ""
        if len(rule) > 0:
            ruleToCheck += "&rules="
            ruleToCheck += rule
        for i in range(1, total_pages):
            r = requests.get(
                SONAR_URL + '/api/issues/search?ps=500&p=' + str(i) + '&componentKeys=' + TEST_PROJECT + ruleToCheck)
            allissues = r.json()['issues']  # all issues it has
            openissue = filter(lambda r: r['status'] != 'CLOSED', allissues)
            issues.extend(openissue)
        return issues

    # get all files or for specific project

    def getFiles (self, SONAR_URL, TEST_PROJECT, total_pages):
        files = []
        for i in range(1, total_pages):
            r = requests.get(
                SONAR_URL + '/api/components/tree??ps=500&p=' + str(i) + '&component=' + TEST_PROJECT)
            allfiles = r.json()['components']
            nondirfiles = filter(lambda r: r['qualifier'] != 'DIR', allfiles)
            files.extend(nondirfiles)
        return files


    #get all commits
    def getcommits (self, GITLAB_URL, projectid, TOKEN):
        commits = []
        counter = 1
        URL = GITLAB_URL + "/projects/" + str(projectid) + "/repository/commits?ref_name=master&per_page=100&page="
        r = requests.get(URL + str(counter), headers={'PRIVATE-TOKEN': TOKEN})

        while len(r.json()) > 0:
            commits.extend(r.json())
            counter += 1
            r = requests.get(URL + str(counter), headers={'PRIVATE-TOKEN': TOKEN})

        return commits



    #extract gitlabid
    def readStudentInfo (self):
        emails = {}
        netids = {}
        netidindex = 2
        emailindex = 3
        gitlabidindex = 4

        csvpath = dotenv_path = dirname(__file__)[:-14] + '/server/documents/local/308students.csv'
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

    def convertEmailtoGitlabId(self, authoremail, studentidmaps):

        indexofat = authoremail.find("@")
        authorname = authoremail[:indexofat]

        if authorname in studentidmaps["email"]:
            authorname = studentidmaps["email"][authorname]
        elif authorname in studentidmaps["netid"]:
            authorname = studentidmaps["netid"][authorname]
        return  authorname

    #calcualte total score for rules under one category
    def calTotalScorePerCategory (self, SONAR_URL, rules):
        score = 0.00
        for rule in rules:
            r = requests.get(SONAR_URL + '/api/rules/search?rule_key='+rule)
            ruleInfo = r.json()['rules'][0]
            ruleseverity =  ruleInfo["severity"]
            score += self.getScoreForSeverity(ruleseverity)
        return score

    # calcualte total score for rules under all categories
    def calTotalScoreAllCategory (self, SONAR_URL):
        l = {}
        l["communication"] = self.calTotalScorePerCategory(SONAR_URL, categories().communication)
        l["modularity"] = self.calTotalScorePerCategory(SONAR_URL, categories().modularity)
        l["flexibility"] = self.calTotalScorePerCategory(SONAR_URL, categories().flexibility)
        l["codesmell"] = self.calTotalScorePerCategory(SONAR_URL, categories().codesmell)
        l["javanote"] = self.calTotalScorePerCategory(SONAR_URL, categories().javanote)
        l["duplications"] = self.calTotalScorePerCategory(SONAR_URL, categories().duplicationsID)
        return l

    #get score for the category
    def getScoreForSeverity (self, ruleseverity):

        if ruleseverity == "BLOCKER":
            return 100.00
        if ruleseverity == "CRITICAL":
            return 50.00
        if ruleseverity == "MAJOR":
            return 20.00
        if ruleseverity == "MINOR":
            return 10.00
        if ruleseverity == "INFO":
            return 5.00
        return 0.0

    def renameSeverity(self, ruleseverity ):
        if ruleseverity == "BLOCKER":
            return "fail"
        if ruleseverity == "CRITICAL":
            return "high"
        if ruleseverity == "MAJOR":
            return "medium"
        if ruleseverity == "MINOR":
            return "low"
        if ruleseverity == "INFO":
            return "info"
        return ""
    #
    def calPercentByScore (self, scores, scores_rem):
        l = []
        for i in range(0,categories().getNumberOfMainCategories()):
            l.append(0)

        for catename, score in scores.iteritems():
            index = categories().getCategoryNumberByName(catename)
            l[index] = (score / scores_rem[catename]) * 100.00
        return l

    #calcualte percentage for the category (SIMPLY BY NUMBER OF RULES VIOLATED)
    def calPercentByNum (self, category, rules_under_category):
        if len(category) > 0:
                return ((0.0 + len(category) - len(rules_under_category)) / len(category)) * 100.00
        return 100.0

    #get the text range in either textRange or flow

    def makeTextRange (self, issue):
        res = []
        if len(issue['flows']) == 0:
            res.append({'textRange' : issue['textRange'], 'msg' : ""})
        else:
            for line in issue['flows']:
                res.append(line['locations'][0])
        res.sort(key=lambda x: x['textRange']['startLine'], reverse=False)

        return res

    #store the issue in message

    def storeIssue(self, ruleID, errmessage, message, rulesViolated):
        ruleInfo = categories().getRuleDetail(ruleID)
        if len(ruleInfo) == 0:
            return
        mainindex = ruleInfo[0]

        if len(ruleInfo) == 2:
            subindex = ruleInfo[1]
            message[mainindex][subindex - 1].append(errmessage)
        else:
            message[mainindex].append(errmessage)
        if not ruleID in rulesViolated[mainindex]:
            rulesViolated[mainindex].append(ruleID)


    #handle duplicated block

    def duplicatedBlockHandlerStore(self, SONAR_URL, dup_errmessages, message, rulesViolated, filesChecked):
        dup_block_id = "common-java:DuplicatedBlocks"
        #out = ""
        for dup_errmessage in dup_errmessages:

            r = requests.get(SONAR_URL + "/api/duplications/show?key=" + dup_errmessage['path'][0])
            items = r.json()
            duplications = items['duplications']
            files = items['files']
            dup_errmessage['duplications'] = []

            for duplication in duplications:

                blocks = duplication['blocks']
                single_dup = []
                discard = False
                for block in blocks:
                    entry = {}
                    entry['startLine'] = block['from']
                    entry['endLine'] = entry['startLine'] - 1 + block['size']
                    entry['loc'] = files[block['_ref']]['key']

                    if entry['loc'] in filesChecked:
                        discard = True
                        break
                    r1 = requests.get(SONAR_URL + "/api/sources/show?from=" + str(entry['startLine']) +
                                      "&to=" + str(entry['endLine']) +
                                      "&key=" + entry['loc'])
                    items = r1.json()["sources"]
                    entry['code'] = []
                    for item in items:
                        entry['code'].append(item[1])
                    single_dup.append(entry)

                if not discard:
                    dup_errmessage['duplications'].append(single_dup)

            filesChecked.add(dup_errmessage['path'][0])
            if len(dup_errmessage['duplications']) > 0:
                self.storeIssue(dup_block_id, dup_errmessage, message, rulesViolated)


    def errHandler (self):
        data = {}
        data['err'] = "project not found"
        data['description'] = "please change the file name and extension for xml.txt to pom.xml and yml.txt to .gitlab-ci.yml"
        return json.dumps(data)


    def dataHandler(self, message, percentage, onlyDup):

        data = {}
        data['error'] = {}


        data['error']['Duplications'] = {}
        data['error']['Duplications']["category description"] = categories().Duplication_sub[1]
        data['error']['Duplications']["detail"] = message[5]

        if onlyDup:
            return data


        data['error']['Communication'] = {}
        data['error']['Communication']['Meaningful names'] = {}
        data['error']['Communication']['Meaningful names']["category description"] = categories().Communication_sub[1]
        data['error']['Communication']['Meaningful names']["detail"] = message[0][0]

        data['error']['Communication']['No magic values'] = {}
        data['error']['Communication']['No magic values']["category description"] = categories().Communication_sub[2]
        data['error']['Communication']['No magic values']["detail"] = message[0][1]

        data['error']['Communication']['Readable code'] = {}
        data['error']['Communication']['Readable code']["category description"] = categories().Communication_sub[3]
        data['error']['Communication']['Readable code']["detail"] = message[0][2]

        data['error']['Communication']['Use scope wisely'] = {}
        data['error']['Communication']['Use scope wisely']["category description"] = categories().Communication_sub[4]
        data['error']['Communication']['Use scope wisely']["detail"] = message[0][3]

        data['error']['Communication']['Same level code'] = {}
        data['error']['Communication']['Same level code']["category description"] = categories().Communication_sub[5]
        data['error']['Communication']['Same level code']["detail"] = message[0][4]

        data['error']['Communication']['Concise code'] = {}
        data['error']['Communication']['Concise code']["category description"] = categories().Communication_sub[6]
        data['error']['Communication']['Concise code']["detail"] = message[0][5]

        data['error']['Communication']['No warning'] = {}
        data['error']['Communication']['No warning']["category description"] = categories().Communication_sub[7]
        data['error']['Communication']['No warning']["detail"] = message[0][6]

        data['error']['Modularity'] = {}
        data['error']['Modularity']['Data responsibility'] = {}
        data['error']['Modularity']['Data responsibility']["category description"] = categories().Modularity_sub[1]
        data['error']['Modularity']['Data responsibility']["detail"] = message[1][0]

        data['error']['Modularity']['No public instance variables'] = {}
        data['error']['Modularity']['No public instance variables']["category description"] = \
        categories().Modularity_sub[2]
        data['error']['Modularity']['No public instance variables']["detail"] = message[1][1]

        data['error']['Modularity']['No manager classes'] = {}
        data['error']['Modularity']['No manager classes']["category description"] = categories().Modularity_sub[3]
        data['error']['Modularity']['No manager classes']["detail"] = message[1][2]

        data['error']['Modularity']['No static variables'] = {}
        data['error']['Modularity']['No static variables']["category description"] = categories().Modularity_sub[4]
        data['error']['Modularity']['No static variables']["detail"] = message[1][3]

        data['error']['Modularity']['Active classes'] = {}
        data['error']['Modularity']['Active classes']["category description"] = categories().Modularity_sub[5]
        data['error']['Modularity']['Active classes']["detail"] = message[1][4]

        data['error']['Modularity']['Get method give minimum info'] = {}
        data['error']['Modularity']['Get method give minimum info']["category description"] = \
        categories().Modularity_sub[6]
        data['error']['Modularity']['Get method give minimum info']["detail"] = message[1][5]

        data['error']['Modularity']['Get method validate input'] = {}
        data['error']['Modularity']['Get method validate input']["category description"] = categories().Modularity_sub[
                                                                                               7],
        data['error']['Modularity']['Get method validate input']["detail"] = message[1][6]

        data['error']['Modularity']['Superclasses are their own class'] = {}
        data['error']['Modularity']['Superclasses are their own class']["category description"] = \
        categories().Modularity_sub[8]
        data['error']['Modularity']['Superclasses are their own class']["detail"] = message[1][7]

        data['error']['Flexibility'] = {}
        data['error']['Flexibility']['General type'] = {}
        data['error']['Flexibility']['General type']["category description"] = categories().Flexibility_sub[1]
        data['error']['Flexibility']['General type']["detail"] = message[2][0]

        data['error']['Flexibility']['Single Purpose'] = {}
        data['error']['Flexibility']['Single Purpose']["category description"] = categories().Flexibility_sub[2]
        data['error']['Flexibility']['Single Purpose']["detail"] = message[2][1]

        data['error']['Flexibility']['Behavior Driven Design'] = {}
        data['error']['Flexibility']['Behavior Driven Design']["category description"] = categories().Flexibility_sub[3]
        data['error']['Flexibility']['Behavior Driven Design']["detail"] = message[2][2]

        data['error']['Flexibility']['Polymorphism'] = {}
        data['error']['Flexibility']['Polymorphism']["category description"] = categories().Flexibility_sub[4]
        data['error']['Flexibility']['Polymorphism']["detail"] = message[2][3]

        data['error']['Java Notes'] = message[3]
        data['error']['Code Smells'] = message[4]

        data['percentage'] = {}
        data['percentage']['Communication'] = percentage[0]
        data['percentage']['Modularity'] = percentage[1]
        data['percentage']['Flexibility'] = percentage[2]
        data['percentage']['Java Notes'] = percentage[3]
        data['percentage']['Code Smells'] = percentage[4]
        data['percentage']['Duplications'] = percentage[5]
        return data



if __name__ == '__main__':

   utility().readStudentInfo()

