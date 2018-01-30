import requests
import json
import re
from rules import categories

class ProcessSonar (object):

    def __init__(self, arg):

        self.GROUPID = 'duke-compsci308:'
        self.TEST_PROJECT = self.GROUPID + arg
        self.QUALITY_PROFILE = 'AV-ylMj9F03llpuaxc9n'

        self.SONAR_URL = 'http://coursework.cs.duke.edu:9000'

        self.rulesViolated = []
        self.issue = []
        self.message = []

        for i in range(5):
            self.rulesViolated.append([])
            self.issue.append([])
            self.message.append([])





    def checkRuleID(self,  index, ruleID,  errmessage):

        self.issue[index].append(ruleID)
        self.message[index].append(errmessage)
        if not ruleID in self.rulesViolated[index]:
            self.rulesViolated[index].append(ruleID)


    def striphtml(self, data):
        p = re.compile(r'<.*?>')
        p = p.sub('', data)
        p = p.replace('&lt;', '<')
        p = p.replace('&gt;', '>')
        p = p.replace('&le;', '<=')
        p = p.replace('&ge;', '>=')
        return p

    def calpercentage (self, category, rules_under_category):
        if len(category) > 0:
                return (0.0 + len(category) - len(rules_under_category)) / len(category) * 100.00
        return 100.0

    def process(self):

        #if project not been analysis return error
        r = requests.get(self.SONAR_URL + "/api/components/show?component=" + self.TEST_PROJECT)
        found_project = r.json()
        if 'errors' in found_project:
            data = {}
            data['err'] = "project not found"
            return json.dumps(data)



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
                        formattedItem = item[1].replace('\t', '')
                        #formattedItem = self.striphtml(formattedItem)
                        errmessage['code'].append(formattedItem)

                if ruleID in categories.Communication:
                    self.checkRuleID(0, ruleID, errmessage)
                elif ruleID in categories.Modularbility:
                    self.checkRuleID(1, ruleID, errmessage)
                elif ruleID in categories.Flexibility:
                    self.checkRuleID(2, ruleID, errmessage)
                elif ruleID in categories.JavaNote:
                    self.checkRuleID(3, ruleID, errmessage)
                elif ruleID in categories.CodeSmell:
                    self.checkRuleID(4, ruleID, errmessage)


        #cal percentage
        percentageA = self.calpercentage(categories.Communication, self.rulesViolated[0])
        percentageB = self.calpercentage(categories.Modularbility, self.rulesViolated[1])
        percentageC = self.calpercentage(categories.Flexibility, self.rulesViolated[2])
        percentageD = self.calpercentage(categories.JavaNote, self.rulesViolated[3])
        percentageE = self.calpercentage(categories.CodeSmell, self.rulesViolated[4])



        data = {}
        data['error'] = {}
        data['error']['Communication'] = self.message[0]
        data['error']['Modularity'] = self.message[1]
        data['error']['Flexibility'] = self.message[2]
        data['error']['Java Note'] = self.message[3]
        data['error']['Code Smell'] = self.message[4]
        data['percentage'] = {}
        data['percentage']['Communication'] = percentageA
        data['percentage']['Modularity'] = percentageB
        data['percentage']['Flexibility'] = percentageC
        data['percentage']['Java Note'] = percentageD
        data['percentage']['Code Smell'] = percentageE

        return json.dumps(data)



if __name__ == '__main__':
    ProcessSonar("sonar_test").percentage()

