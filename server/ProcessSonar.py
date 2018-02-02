import requests
import json

from categories import categories
from utility import utility

class ProcessSonar (object):

    def __init__(self, arg):

        self.GROUPID = 'duke-compsci308:'
        if arg is None:
            arg = ""
        self.TEST_PROJECT = self.GROUPID + arg
        self.QUALITY_PROFILE = 'AV-ylMj9F03llpuaxc9n'

        self.SONAR_URL = 'http://coursework.cs.duke.edu:9000'

        self.rulesViolated = []
        self.message = []

        for i in range(5):
            self.rulesViolated.append([])
            self.message.append([])
            k = 0
            if i == 0:
                k = 7
            if i == 1:
                k = 8
            if i == 2:
                k = 5
            for j in range(k):
                self.message[i].append([])

    def checkRuleID(self, ruleID, errmessage):
        ruleInfo = categories().getRuleDetail(ruleID)

        if len(ruleInfo) == 0:
            return
        mainindex = ruleInfo[0]

        if len(ruleInfo) == 2:
            subindex = ruleInfo[1]

            self.message[mainindex][subindex - 1].append(errmessage)
        else:
            self.message[mainindex].append(errmessage)

        if not ruleID in self.rulesViolated[mainindex]:
            self.rulesViolated[mainindex].append(ruleID)

    def calpercentage (self, category, rules_under_category):
        if len(category) > 0:
                return (0.0 + len(category) - len(rules_under_category)) / len(category) * 100.00
        return 100.0

    def process(self):

        #if project not been analysis return error
        r = requests.get(self.SONAR_URL + "/api/components/show?component=" + self.TEST_PROJECT)
        found_project = r.json()
        if 'errors' in found_project:
            return utility().errHandler()

        #get number of pages
        r = requests.get(
            self.SONAR_URL + '/api/issues/search?ps=500&componentKeys=' + self.TEST_PROJECT)
        total_number_issues = r.json()['total']
        page_size = r.json()['ps']
        total_pages = 2
        if total_number_issues > page_size:
            total_pages += total_number_issues / page_size
            if total_number_issues % page_size != 0:
                total_pages += 1

        #get all issues that are open
        issues = []

        for i in range (1, total_pages):
            r = requests.get(
                self.SONAR_URL + '/api/issues/search?ps=500&p=' + str(i) +  '&componentKeys=' + self.TEST_PROJECT)

            allissues = r.json()['issues']  # all issues it has
            openissue = filter(lambda r: r['status'] != 'CLOSED', allissues)
            issues.extend(openissue)

        #get all rules associate with quanlity profile
        r = requests.get(
            self.SONAR_URL + '/api/rules/search?ps=500&activation=true&qprofile=' + self.QUALITY_PROFILE)
        rules = r.json()['rules']

        #store details
        for issue in issues:
            ruleID = issue['rule']
            ruleResult = filter(lambda r: r['key'] == ruleID, rules)  #rulename = ruleResult[0]['name']
            if len(ruleResult) > 0:

                errmessage = {}
                errmessage['path'] = issue['component']
                errmessage['rule'] = ruleResult[0]['name']
                errmessage['message'] = issue['message']
                errmessage['textRange'] = {}
                if 'textRange' in issue:
                    errmessage['textRange'] = issue['textRange']
                    startLine = issue['textRange']['startLine']
                    endLine = issue['textRange']['endLine']
                    r = requests.get(self.SONAR_URL + "/api/sources/show?from=" + str(startLine) +
                                     "&to=" + str(endLine) +
                                     "&key=" + issue['component'])
                    items = r.json()["sources"]
                    errmessage['code'] = []

                    for item in items:
                        #formattedItem = item[1].replace('\t', '')
                        #formattedItem = self.striphtml(formattedItem)
                        errmessage['code'].append(item[1])


                self.checkRuleID (ruleID, errmessage)

        #cal percentage
        percentage = []
        percentage.append(self.calpercentage(categories().communication, self.rulesViolated[0]))
        percentage.append(self.calpercentage(categories().modularity, self.rulesViolated[1]))
        percentage.append(self.calpercentage(categories().flexibility, self.rulesViolated[2]))
        percentage.append(self.calpercentage(categories().javanote, self.rulesViolated[3]))
        percentage.append(self.calpercentage(categories().codesmell, self.rulesViolated[4]))

        data = utility().dataHandler(self.message, percentage)
        print data
        res = json.dumps(data, indent=4, separators=(',', ': '))


        return res

    def statistics(self):
        #TODO
        res = ""
        return res

    def getrules (self, main, sub):
        #TODO
        res = ""
        return res


if __name__ == '__main__':
     ProcessSonar("test").process()

