import re
from categories import categories
import json
import requests

class utility ():

    def activateRule (self, SONAR_URL, QUALITY_PROFILE, ruleID):

        r = requests.post(SONAR_URL + '/api/qualityprofiles/activate_rule?=' ,
                          data={'profile_key':QUALITY_PROFILE, 'rule_key' : ruleID},
                          auth=('rcd', 'wzuA3F4g27'))

    def makeMap(self, rules, main, sub):
        res = ""
        for rule in rules:
            if sub > 0:
                res = res + "'" + rule + "' : ['" + main + "'," + str(sub) + "],\n"
            else:
                res = res + "'" + rule + "': ['" + main + "'],\n"

        return res

    def striphtml(self, data):
        p = re.compile(r'<.*?>')
        p = p.sub('', data)
        p = p.replace('&lt;', '<')
        p = p.replace('&gt;', '>')
        p = p.replace('&le;', '<=')
        p = p.replace('&ge;', '>=')
        return p

    #get number of pages

    def getNumOfPages (self, SONAR_URL, TEST_PROJECT):
        r = requests.get(
            SONAR_URL + '/api/issues/search?ps=500&componentKeys=' + TEST_PROJECT)
        total_number_issues = r.json()['total']
        page_size = r.json()['ps']
        total_pages = 2
        if total_number_issues > page_size:
            total_pages += total_number_issues / page_size
            if total_number_issues % page_size != 0:
                total_pages += 1
        return total_pages

    #get all issues

    def getIssues (self, SONAR_URL, TEST_PROJECT, total_pages):
        issues = []
        for i in range(1, total_pages):
            r = requests.get(
                SONAR_URL + '/api/issues/search?ps=500&p=' + str(i) + '&componentKeys=' + TEST_PROJECT)
            allissues = r.json()['issues']  # all issues it has
            openissue = filter(lambda r: r['status'] != 'CLOSED', allissues)
            issues.extend(openissue)
        return issues

    #calcualte percentage for the category

    def calPercentage (self, category, rules_under_category):
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

    def duplicatedBlockHandlerStore(self, SONAR_URL, dup_errmessages, message, rulesViolated):
        dup_block_id = "common-java:DuplicatedBlocks"
        for dup_errmessage in dup_errmessages:
            r = requests.get(SONAR_URL + "/api/duplications/show?key=" + dup_errmessage['path'][0])
            items = r.json()
            duplications = items['duplications']
            files = items['files']
            dup_errmessage['duplications'] = []
            for duplication in duplications:
                blocks = duplication['blocks']
                single_dup = []
                for block in blocks:
                    entry = {}
                    entry['startLine'] = block['from']
                    entry['endLine'] = entry['startLine'] - 1 + block['size']
                    entry['loc'] = files[block['_ref']]['key']
                    r1 = requests.get(SONAR_URL + "/api/sources/show?from=" + str(entry['startLine']) +
                                      "&to=" + str(entry['endLine']) +
                                      "&key=" + entry['loc'])
                    items = r1.json()["sources"]
                    entry['code'] = []
                    for item in items:
                        entry['code'].append(item[1])
                    single_dup.append(entry)
                dup_errmessage['duplications'].append(single_dup)
            self.storeIssue(dup_block_id, dup_errmessage, message, rulesViolated)

    def errHandler (self):
        data = {}
        data['err'] = "project not found"
        data['description'] = "please change the file name and extension for xml.txt to pom.xml and yml.txt to .gitlab-ci.yml"
        return json.dumps(data)

    def dataHandler(self, message, percentage, onlyDup):

        data = {}
        data['error'] = {}

        data['error']['Flexibility'] = {}
        data['error']['Flexibility']['No duplicated code'] = {}
        data['error']['Flexibility']['No duplicated code']["category description"] = categories().Flexibility_sub[1]
        data['error']['Flexibility']['No duplicated code']["detail"] = message[2][0]

        if onlyDup:
            return data


        data['error']['Communication'] = {}
        data['error']['Communication']['Meaningful names'] = {}
        data['error']['Communication']['Meaningful names']["category description"] = categories().Communication_Sub[1]
        data['error']['Communication']['Meaningful names']["detail"] = message[0][0]

        data['error']['Communication']['No magic values'] = {}
        data['error']['Communication']['No magic values']["category description"] = categories().Communication_Sub[2]
        data['error']['Communication']['No magic values']["detail"] = message[0][1]

        data['error']['Communication']['Readable code'] = {}
        data['error']['Communication']['Readable code']["category description"] = categories().Communication_Sub[3]
        data['error']['Communication']['Readable code']["detail"] = message[0][2]

        data['error']['Communication']['Use scope wisely'] = {}
        data['error']['Communication']['Use scope wisely']["category description"] = categories().Communication_Sub[4]
        data['error']['Communication']['Use scope wisely']["detail"] = message[0][3]

        data['error']['Communication']['Same level code'] = {}
        data['error']['Communication']['Same level code']["category description"] = categories().Communication_Sub[5]
        data['error']['Communication']['Same level code']["detail"] = message[0][4]

        data['error']['Communication']['Concise code'] = {}
        data['error']['Communication']['Concise code']["category description"] = categories().Communication_Sub[6]
        data['error']['Communication']['Concise code']["detail"] = message[0][5]

        data['error']['Communication']['No warning'] = {}
        data['error']['Communication']['No warning']["category description"] = categories().Communication_Sub[7]
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

        data['error']['Flexibility']['General type'] = {}
        data['error']['Flexibility']['General type']["category description"] = categories().Flexibility_sub[2]
        data['error']['Flexibility']['General type']["detail"] = message[2][1]

        data['error']['Flexibility']['Single Purpose'] = {}
        data['error']['Flexibility']['Single Purpose']["category description"] = categories().Flexibility_sub[3]
        data['error']['Flexibility']['Single Purpose']["detail"] = message[2][2]

        data['error']['Flexibility']['Behavior Driven Design'] = {}
        data['error']['Flexibility']['Behavior Driven Design']["category description"] = categories().Flexibility_sub[4]
        data['error']['Flexibility']['Behavior Driven Design']["detail"] = message[2][3]

        data['error']['Flexibility']['Polymorphism'] = {}
        data['error']['Flexibility']['Polymorphism']["category description"] = categories().Flexibility_sub[5]
        data['error']['Flexibility']['Polymorphism']["detail"] = message[2][4]

        data['error']['Java Notes'] = message[3]
        data['error']['Code Smells'] = message[4]
        data['error']['Duplications'] = message[5]
        data['percentage'] = {}
        data['percentage']['Communication'] = percentage[0]
        data['percentage']['Modularity'] = percentage[1]
        data['percentage']['Flexibility'] = percentage[2]
        data['percentage']['Java Notes'] = percentage[3]
        data['percentage']['Code Smells'] = percentage[4]
        data['percentage']['Duplications'] = percentage[5]
        return data