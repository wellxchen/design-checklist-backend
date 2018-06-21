'''
Helper class that handle data structure related functionalities

:Authors:
    - Chengkang Xu <cx33@duke.edu>
'''


import re
from CategoriesHelper import CategoriesHelper
from SonarHelper import  SonarHelper



class DataHelper ():
    def displayData(self, data):
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(data)

    # store the issue in message

    def storeIssue(self, ruleID, errmessage, message, rulesViolated):
            ruleInfo = CategoriesHelper().getRuleDetail(ruleID)
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

    # store codes
    def storeCodes(self, SONAR_URL, issue, errmessage):
        if 'textRange' in issue:
            textRange = self.makeTextRange(issue)
            for entry in textRange:
                startLine = entry['textRange']['startLine']
                endLine = entry['textRange']['endLine']

                items = SonarHelper().getSource(SONAR_URL, startLine, endLine, issue)

                entry['code'] = []
                for item in items:
                    entry['code'].append(item[1])
                errmessage['code'].append(entry)




    def errHandler(self):
            data = {}
            data['err'] = "project not found"
            data['description'] = \
                "please change the file name and extension for xml.txt to pom.xml and yml.txt to .gitlab-ci.yml"
            return json.dumps(data)

    def dataHandler(self, message, percentage, onlyDup):

            data = {}
            data['error'] = {}
            data['error']['Duplications'] = {}
            data['error']['Duplications']["category description"] = CategoriesHelper().getDescriptionByName("Duplications", 0)
            data['error']['Duplications']["detail"] = message[5]

            if onlyDup:
                return data

            for mindex in range(0, CategoriesHelper().getNumMainTitle()):
                maintitle =CategoriesHelper().getMainTitle(mindex)
                data['error'][maintitle] = {}
                if mindex >= 3:
                    data['error'][maintitle] = message[mindex]
                    continue
                for sindex in range(0, CategoriesHelper().getNumSubTitle(mindex)):
                    subtitle = CategoriesHelper().getSubTitle(mindex, sindex)
                    data['error'][maintitle][subtitle] = {}
                    data['error'][maintitle][subtitle]['detail'] = message[mindex][sindex]
                    data['error'][maintitle][subtitle]['category description'] = CategoriesHelper().getDescriptionByIndex(
                        mindex, sindex)

            data['percentage'] = {}
            for i in range(0, CategoriesHelper().getNumTitle()):
                data['percentage'][CategoriesHelper().getTitle(i)] = percentage[i]

            return data



    def makeIssueEntryForDIR (self, issuelist, TEST_PROJECT, res):
        for issue in issuelist:
            for filepath in issue['path']:
                filepathshort = re.sub(TEST_PROJECT + ":", "", filepath)
                lastslash = filepathshort.rfind("/")
                parentdirectory = filepathshort[:lastslash]
                if parentdirectory not in res or filepathshort not in res[parentdirectory]["files"]:
                    continue
                res[parentdirectory]["files"][filepathshort].append(issue)

    def filterRuleFromSonar (self, issue, rules):
        ruleID = issue['rule']
        ruleResult = filter(lambda r: r['key'] == ruleID, rules)
        return ruleResult

    # get the text range in either textRange or flow

    def makeTextRange(self, issue):

        res = []
        if len(issue['flows']) == 0:
            res.append({'textRange': issue['textRange'], 'msg': ""})
        else:
            for line in issue['flows']:
                res.append(line['locations'][0])
        res.sort(key=lambda x: x['textRange']['startLine'], reverse=False)

        return res

    # extract useful information from issue and make the err message
    def makeErrMessage (self, issue, ruleResult):
        errmessage = {}
        errmessage['path'] = [issue['component']]
        errmessage['rule'] = ruleResult[0]['name']
        errmessage['message'] = issue['message']
        errmessage['severity'] = ScoreHelper().renameSeverity(issue['severity'])
        return errmessage