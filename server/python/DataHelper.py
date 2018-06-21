'''
Helper class that handle data structure related functionalities

:Authors:
    - Chengkang Xu <cx33@duke.edu>
'''


import re
import CategoriesHelper
import ScoreHelper
import SonarHelper


class DataHelper ():

    def __init__(self):
        self.categorieshelper = CategoriesHelper.CategoriesHelper()
        self.scorehelper = ScoreHelper.ScoreHelper()
        self.sonarhelper = SonarHelper.SonarHelper()


    def displayData(self, data):
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(data)

    # store the issue in message

    def storeIssue(self, ruleID, errmessage, message, rulesViolated):
            ruleInfo = self.categorieshelper.getRuleDetail(ruleID)
            if len(ruleInfo) == 0:
                return
            mainindex = ruleInfo[0]

            if len(ruleInfo) == 2:
                subindex = ruleInfo[1]


                message[mainindex][subindex].append(errmessage)
            else:
                message[mainindex].append(errmessage)
            if not ruleID in rulesViolated[mainindex]:
                rulesViolated[mainindex].append(ruleID)




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
            data['error']['Duplications']["category description"] = self.categorieshelper.getDescriptionByName("Duplications", 0)
            data['error']['Duplications']["detail"] = message[5]

            if onlyDup:
                return data

            for mindex in range(0, self.categorieshelper.getNumMainTitle()):
                maintitle = self.categorieshelper.getMainTitle(mindex)
                data['error'][maintitle] = {}
                if mindex >= 3:
                    data['error'][maintitle] = message[mindex]
                    continue
                for sindex in range(0, self.categorieshelper.getNumSubTitle(mindex)):
                    subtitle = self.categorieshelper.getSubTitle(mindex, sindex)
                    data['error'][maintitle][subtitle] = {}
                    data['error'][maintitle][subtitle]['detail'] = message[mindex][sindex]
                    data['error'][maintitle][subtitle]['category description'] = \
                        self.categorieshelper.getDescriptionByIndex(mindex, sindex)

            data['percentage'] = {}
            for i in range(0, self.categorieshelper.getNumMainTitle()):
                data['percentage'][self.categorieshelper.getMainTitle(i)] = percentage[i]

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
        errmessage['severity'] = self.scorehelper.renameSeverity(issue['severity'])
        errmessage['author'] = issue['author']
        return errmessage

    # get and store codes

    def storeCodes(self, SONAR_URL, issue, errmessage):
        if 'textRange' in issue:
            textRange = self.makeTextRange(issue)
            for entry in textRange:
                startLine = entry['textRange']['startLine']
                endLine = entry['textRange']['endLine']

                items = self.sonarhelper.getSource(SONAR_URL, startLine, endLine, issue)

                entry['code'] = []
                for item in items:
                    entry['code'].append(item[1])
                errmessage['code'].append(entry)


    def handleAuthorStore (self, issues, maincategory, subcategory, res):
        for issue in issues:
            author = issue['author']
            if author not in res:
                res[author]=self.makeEmptyIssueEntry()
            if subcategory == "":
                res[author][maincategory].append(issue)
            else:
                res[author][maincategory][subcategory].append(issue)




    def makeEmptyIssueEntry (self):
        entry = {}
        maintitles = self.categorieshelper.getAllMainTitle()
        for i in range(len(maintitles)):
            if i >= 3:
                entry[maintitles[i]] = []
                continue
            entry[maintitles[i]] = {}
            subtitles = self.categorieshelper.getAllSubTitleOfMain(i)
            for subtitle in subtitles:
                entry[maintitles[i]][subtitle] = []
        return entry
