import requests
import json
import re

class ProcessSonar (object):

    def __init__(self, arg):

        self.GROUPID = 'duke-compsci308:'
        self.TEST_PROJECT = self.GROUPID + arg
        self.QUALITY_PROFILE = 'AV8XUqRGF03llpuaxc6_'#new quality profile 'AV-ylMj9F03llpuaxc9n'

        self.SONAR_URL = 'http://coursework.cs.duke.edu:9000'

        self.rulesViolated = []
        self.issue = []
        self.message = []

        for i in range(3):
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


    def percentage(self):

        #if project not been analysis return error
        r = requests.get(self.SONAR_URL + "/api/components/show?component=" + self.TEST_PROJECT)
        found_project = r.json()
        if 'errors' in found_project:
            data = {}
            data['err'] = "project not found"
            return json.dumps(data)

        A = {'squid:S00115', 'squid:S1190', 'squid:S1126',
            'squid:S109', 'squid:S00122', 'squid:S00121',
            'squid:S2681', 'squid:S881', 'squid:S2114',
            'squid:S2589', 'squid:S2293', 'squid:S2178',
            'squid:S2175', 'squid:S2200', 'squid:S1192',
            'squid:S1126', 'squid:S1125', 'squid:S2185',
            'squid:S1133', 'squid:S00108', 'squid:S1596',
            'squid:S2097', 'squid:S1148', 'squid:S00112',
            'squid:S2208', 'squid:UselessImportCheck', 'squid:UselessParenthesesCheck',
            'squid:S1197', 'squid:S1199 ', 'squid:S1488',
            'squid:S2189', 'squid:S1244 ', 'squid:S135',
            'squid:S2692', 'squid:S1481', 'squid:S1710',
            'squid:S3358', 'squid:S2147', 'squid:S1170',
            'squid:S2159', 'squid:S1068'}
        B = {'squid:S1258', 'squid:S3066', 'squid:ClassVariableVisibilityCheck',
        	'squid:S00104','squid:S1188', 'squid:S2094',
        	'squid:S2177','squid:S2440', 'squid:S2209',
        	'squid:S1194', 'squid:S2696', 'squid:S2694',
        	'squid:S2388', 'squid:S2386', 'squid:S2387',
        	'squid:S2384', 'squid:S2141', 'squid:S3038',
        	'squid:S2156'}
        C = {'common-java:DuplicatedBlocks', 'squid:S3047', 'squid:S3776',
        	'squid:S2176', 'squid:MethodCyclomaticComplexity', 'squid:S138',
        	'squid:S1067', 'squid:S1479', 'squid:S1118',
        	'squid:S00107', 'squid:S3422', 'squid:S2166'}

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
                    print issue['component']
                    for item in items:
                        formattedItem = item[1].replace('\t', '')
                        formattedItem = self.striphtml(formattedItem)
                        errmessage['code'].append(formattedItem)

                if ruleID in A:
                    self.checkRuleID(0,ruleID, errmessage)
                elif ruleID in B:
                    self.checkRuleID(1,ruleID, errmessage)
                elif ruleID in C:
                    self.checkRuleID(2, ruleID,  errmessage)

        #cal percentage
        percentageA = 100.0
        percentageB = 100.0
        percentageC = 100.0

        if len(A) > 0:
            percentageA = (0.0 + len(A) - len(self.rulesViolated[0])) / len(A) * 100.00
        if len(B) > 0:
            percentageB = (0.0 + len(B) - len(self.rulesViolated[1])) / len(B) * 100.00
        if len(C) > 0:
            percentageC = (0.0 + len(C) - len(self.rulesViolated[2])) / len(C) * 100.00
        data = {}
        data['error'] = {}
        data['error']['Communication'] = self.message[0]
        data['error']['Modularity'] = self.message[1]
        data['error']['Flexibility'] = self.message[2]
        data['percentage'] = {}
        data['percentage']['Communication'] = percentageA
        data['percentage']['Modularity'] = percentageB
        data['percentage']['Flexibility'] = percentageC

        return json.dumps(data)



if __name__ == '__main__':
    ProcessSonar("sonar_test").percentage()

