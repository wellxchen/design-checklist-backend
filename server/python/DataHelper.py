'''
Helper class that handle data structure related functionalities

:Authors:
    - Chengkang Xu <cx33@duke.edu>
'''


import re
from ScoreHelper import ScoreHelper



class DataHelper (ScoreHelper):

    def __init__(self, group, project):

        super(DataHelper, self).__init__(group, project)

        self.fileChecked = set()  # whether files are checked
        self.rulesViolated = []  # store rules violated
        self.message = []  # store details of issues

        # initiate buffers
        for i in range(self.getNumMainTitle()):
            self.rulesViolated.append([])
            self.message.append([])
            k = 0

            if i < 3:
                k = self.getNumSubTitle(i)

            for j in range(k):
                self.message[i].append([])


    def displayData(self, data):
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(data)

    # store the issue in message

    def storeIssue(self, ruleID, errmessage):

            ruleInfo = self.getRuleDetail(ruleID)
            if len(ruleInfo) == 0:
                return
            mainindex = ruleInfo[0]

            if len(ruleInfo) == 2:
                subindex = ruleInfo[1]


                self.message[mainindex][subindex].append(errmessage)
            else:
                self.message[mainindex].append(errmessage)
            if not ruleID in self.rulesViolated[mainindex]:
                self.rulesViolated[mainindex].append(ruleID)




    def errHandler(self):
            data = {}
            data['err'] = "project not found"
            data['description'] = \
                "please change the file name and extension for xml.txt to pom.xml and yml.txt to .gitlab-ci.yml"
            return json.dumps(data)

    def dataHandler(self, percentage, onlyDup):

            data = {}
            data['error'] = {}
            data['error']['Duplications'] = {}
            data['error']['Duplications']["category description"] = self.getDescriptionByName("Duplications", 0)
            data['error']['Duplications']["detail"] = self.message[5]

            if onlyDup:
                return data

            for mindex in range(0, self.getNumMainTitle()):
                maintitle = self.getMainTitle(mindex)
                data['error'][maintitle] = {}
                if mindex >= 3:
                    data['error'][maintitle] = self.message[mindex]
                    continue
                for sindex in range(0, self.getNumSubTitle(mindex)):
                    subtitle = self.getSubTitle(mindex, sindex)
                    data['error'][maintitle][subtitle] = {}
                    data['error'][maintitle][subtitle]['detail'] = self.message[mindex][sindex]
                    data['error'][maintitle][subtitle]['category description'] = \
                        self.getDescriptionByIndex(mindex, sindex)

            data['percentage'] = {}
            for i in range(0, self.getNumMainTitle()):
                data['percentage'][self.getMainTitle(i)] = percentage[i]

            return data



    def makeIssueEntryForDIR (self, issuelist,  res):
        for issue in issuelist:
            for filepath in issue['path']:
                filepathshort = re.sub(self.TEST_PROJECT + ":", "", filepath)
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
        errmessage['severity'] = self.renameSeverity(issue['severity'])
        errmessage['author'] = issue['author']
        return errmessage




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
        maintitles = self.getAllMainTitle()
        for i in range(len(maintitles)):
            if i >= 3:
                entry[maintitles[i]] = []
                continue
            entry[maintitles[i]] = {}
            subtitles = self.getAllSubTitleOfMain(i)
            for subtitle in subtitles:
                entry[maintitles[i]][subtitle] = []
        return entry



    def getFileChecked (self):
        return self.fileChecked

    def getRulesViolated(self):
        return self.rulesViolated

    def getMessage(self):
        return self.message