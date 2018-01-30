import requests
import json
import re

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

            # communication
        self.Communication = {'squid:S00115', 'squid:S1190', 'squid:S1126',
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
        self.Communication_Sub = [
                'Meaningful names: give variables, methods, classes, and packages non-abbreviated, intention-revealing names',
                'No magic values: use constants for all values used multiple times or in program logic',
                'Write readable code instead of comments: use comments only to explain important design decisions or purpose of code, not to restate code logic',
                'Use scope wisely: variables should be declared as close as possible to where they are used',
                'At all points, code should be "at the same level" (try not to mix method calls and low-level if logic in same method)',
                'Code should be "concise" (use booleans wisely, for-each loop where possible, use Java API calls instead of implementing yourself)',
                'Code should contain no warnings from Java compiler or CheckStyle']
            # Modularbility
        self.Modularbility = {'squid:S1258', 'squid:S3066', 'squid:ClassVariableVisibilityCheck',
                             'squid:S00104', 'squid:S1188', 'squid:S2094',
                             'squid:S2177', 'squid:S2440', 'squid:S2209',
                             'squid:S1194', 'squid:S2696', 'squid:S2694',
                             'squid:S2388', 'squid:S2386', 'squid:S2387',
                             'squid:S2384', 'squid:S2141', 'squid:S3038',
                             'squid:S2156'}
        self.Modularbility_sub = [
                "Tell, don't ask: classes should be responsible for their own data and delegate to other objects instead of doing it themselves",
                "No public instance variables: keep implementation details of your class hidden from the public interface",
                'No "manager" classes: create several classes that work together distributing intelligence, rather than one "smart" class and a few "dumb" helpers',
                'No static variables: there should be no reason for shared global public state',
                'Active classes: classes should not consist of only get/set methods and, in general, should minimize their use. ',
                'get methods should give away the minimal information possible',
                'set methods should validate data received',
                'Superclasses are their own class: thus should not contain instance variables or methods specific to only some subclasses']

            # Flexibility
        self.Flexibility = {'common-java:DuplicatedBlocks', 'squid:S3047', 'squid:S3776',
                           'squid:S2176', 'squid:MethodCyclomaticComplexity', 'squid:S138',
                           'squid:S1067', 'squid:S1479', 'squid:S1118',
                           'squid:S00107', 'squid:S3422', 'squid:S2166'}

        self.Flexibility_sub = [
                'DRY: no duplicated code, either exactly (from cutting and pasting), structurally (in flow of control or decisions), or in setup ("boilerplate" code)',
                'Declared types should be as general as possible (i.e., ArrayList should never be visible in your public interface)',
                'Single Purpose: keep classes, methods, and variables short and well named by giving them only one purpose',
                'Behavior Driven Design: give each class a purpose by focusing on the behavior (or services) it provides first, its state later',
                'Polymorphism: use subclassing to avoid "case-based code logic" (i.e., conditional chains or case statements on "type" information)']

            # Java related
        self.JavaNote = {}
            # code smell
        self.CodeSmell = {}


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
                        formattedItem = self.striphtml(formattedItem)
                        errmessage['code'].append(formattedItem)

                if ruleID in self.Communication:
                    self.checkRuleID(0, ruleID, errmessage)
                elif ruleID in self.Modularbility:
                    self.checkRuleID(1, ruleID, errmessage)
                elif ruleID in self.Flexibility:
                    self.checkRuleID(2, ruleID, errmessage)
                elif ruleID in self.JavaNote:
                    self.checkRuleID(3, ruleID, errmessage)
                elif ruleID in self.CodeSmell:
                    self.checkRuleID(4, ruleID, errmessage)


        #cal percentage
        percentageA = self.calpercentage(self.Communication, self.rulesViolated[0])
        percentageB = self.calpercentage(self.Modularbility, self.rulesViolated[1])
        percentageC = self.calpercentage(self.Flexibility, self.rulesViolated[2])
        percentageD = self.calpercentage(self.JavaNote, self.rulesViolated[3])
        percentageE = self.calpercentage(self.CodeSmell, self.rulesViolated[4])



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

