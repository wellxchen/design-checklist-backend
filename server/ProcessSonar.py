import requests
import json

from categories import categories
from utility import utility

class ProcessSonar (object):

    def __init__(self, arg):

        self.GROUPID = 'duke-compsci308:'
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
                        #formattedItem = item[1].replace('\t', '')
                        #formattedItem = self.striphtml(formattedItem)
                        errmessage['code'].append(item[1])


                self.checkRuleID (ruleID, errmessage)



        #cal percentage
        percentageA = self.calpercentage(categories().communication, self.rulesViolated[0])
        percentageB = self.calpercentage(categories().modularity, self.rulesViolated[1])
        percentageC = self.calpercentage(categories().flexibility, self.rulesViolated[2])
        percentageD = self.calpercentage(categories().javanote, self.rulesViolated[3])
        percentageE = self.calpercentage(categories().codesmell, self.rulesViolated[4])


        data = {}
        data['error'] = {}
        data['error']['Communication'] = {}
        data['error']['Communication']['Meaningful names'] = {}
        data['error']['Communication']['Meaningful names']["category description"] = categories().Communication_Sub[1]
        data['error']['Communication']['Meaningful names']["detail"]  = self.message[0][0]

        data['error']['Communication']['No magic values'] = {}
        data['error']['Communication']['No magic values']["category description"] = categories().Communication_Sub[2]
        data['error']['Communication']['No magic values']["detail"] =  self.message[0][1]

        data['error']['Communication']['Readable code'] = {}
        data['error']['Communication']['Readable code']["category description"] = categories().Communication_Sub[3]
        data['error']['Communication']['Readable code']["detail"] = self.message[0][2]

        data['error']['Communication']['Use scope wisely'] = {}
        data['error']['Communication']['Use scope wisely']["category description"] = categories().Communication_Sub[4]
        data['error']['Communication']['Use scope wisely']["detail"] = self.message[0][3]

        data['error']['Communication']['Same level code'] = {}
        data['error']['Communication']['Same level code']["category description"] = categories().Communication_Sub[5]
        data['error']['Communication']['Same level code']["detail"] = self.message[0][4]

        data['error']['Communication']['Concise code'] = {}
        data['error']['Communication']['Concise code']["category description"] = categories().Communication_Sub[6]
        data['error']['Communication']['Concise code']["message"] = self.message[0][5]

        data['error']['Communication']['No warning'] = {}
        data['error']['Communication']['No warning']["category description"] = categories().Communication_Sub[7]
        data['error']['Communication']['No warning']["message"] = self.message[0][6]

        data['error']['Modularity'] = {}
        data['error']['Modularity']['Data responsibility'] = {}
        data['error']['Modularity']['Data responsibility']["category description"]  = categories().Modularity_sub[1]
        data['error']['Modularity']['Data responsibility']["message"] = self.message[1][0]

        data['error']['Modularity']['No public instance variables'] = {}
        data['error']['Modularity']['No public instance variables']["category description"] = categories().Modularity_sub[2]
        data['error']['Modularity']['No public instance variables']["message"] = self.message[1][1]

        data['error']['Modularity']['No manager classes'] = {}
        data['error']['Modularity']['No manager classes']["category description"] = categories().Modularity_sub[3]
        data['error']['Modularity']['No manager classes']["message"] = self.message[1][2]

        data['error']['Modularity']['No static variables'] = {}
        data['error']['Modularity']['No static variables']["category description"] = categories().Modularity_sub[4]
        data['error']['Modularity']['No static variables']["message"] = self.message[1][3]

        data['error']['Modularity']['Active classes'] = {}
        data['error']['Modularity']['Active classes']["category description"] = categories().Modularity_sub[5]
        data['error']['Modularity']['Active classes']["message"] = self.message[1][4]

        data['error']['Modularity']['Get method give minimum info'] = {}
        data['error']['Modularity']['Get method give minimum info']["category description"] = categories().Modularity_sub[6]
        data['error']['Modularity']['Get method give minimum info']["message"] = self.message[1][5]

        data['error']['Modularity']['Get method validate input'] = {}
        data['error']['Modularity']['Get method validate input']["category description"] = categories().Modularity_sub[7],
        data['error']['Modularity']['Get method validate input']["message"] = self.message[1][6]

        data['error']['Modularity']['Superclasses are their own class'] = {}
        data['error']['Modularity']['Superclasses are their own class']["category description"] = categories().Modularity_sub[8]
        data['error']['Modularity']['Superclasses are their own class']["message"] =  self.message[1][7]

        data['error']['Flexibility'] = {}
        data['error']['Flexibility']['No duplicated code'] = {}
        data['error']['Flexibility']['No duplicated code']["category description"] = categories().Modularity_sub[1]
        data['error']['Flexibility']['No duplicated code']["message"] = self.message[2][0]

        data['error']['Flexibility']['General type'] = {}
        data['error']['Flexibility']['General type']["category description"] = categories().Modularity_sub[2]
        data['error']['Flexibility']['General type']["message"] = self.message[2][1]

        data['error']['Flexibility']['Single Purpose'] = {}
        data['error']['Flexibility']['Single Purpose']["category description"] = categories().Modularity_sub[3]
        data['error']['Flexibility']['Single Purpose']["message"] =  self.message[2][2]

        data['error']['Flexibility']['Behavior Driven Design'] = {}
        data['error']['Flexibility']['Behavior Driven Design']["category description"] = categories().Modularity_sub[4]
        data['error']['Flexibility']['Behavior Driven Design']["message"] = self.message[2][3]

        data['error']['Flexibility']['Polymorphism'] = {}
        data['error']['Flexibility']['Polymorphism']["category description"] = categories().Modularity_sub[5]
        data['error']['Flexibility']['Polymorphism']["message"] = self.message[2][4]

        data['error']['Java Note'] = self.message[3]
        data['error']['Code Smell'] = self.message[4]
        data['percentage'] = {}
        data['percentage']['Communication'] = percentageA
        data['percentage']['Modularity'] = percentageB
        data['percentage']['Flexibility'] = percentageC
        data['percentage']['Java Note'] = percentageD
        data['percentage']['Code Smell'] = percentageE

        res = json.dumps(data,
                 indent=4, separators=(',', ': '))
        print res
        return res



if __name__ == '__main__':
     ProcessSonar("test").process()

