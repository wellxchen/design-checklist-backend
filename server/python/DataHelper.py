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
        """
        display any json like data in an easy to read format
        :param data: any json like data
        :return: void
        """
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(data)


    def storeIssue(self, ruleID, errmessage):
            """
            store the issue in message buffer
            :param ruleID: rule id
            :param errmessage: error message contains the information to be store
            :return: void
            """

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
            """
            make a json contains error
            :return: json contains error
            """
            data = {}
            data['err'] = "project not found"
            data['description'] = \
                "please change the file name and extension for xml.txt to pom.xml and yml.txt to .gitlab-ci.yml"
            return json.dumps(data)

    def dataHandler(self, percentage, onlyDup):
            """
            make data entries that contains corresponding issues i
            :param percentage: percentages for each category
            :param onlyDup: only need to handle duplciation
            :return: data buffer that contains percentage and issues
            """
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
        """
        extract path and the corresponding issue with it
        :param issuelist: list of issues
        :param res: buffer contains the directory oriented issue list, originall empty
        :return: void
        """
        for issue in issuelist:
            for filepath in issue['path']:
                filepathshort = re.sub(self.TEST_PROJECT + ":", "", filepath)
                lastslash = filepathshort.rfind("/")
                parentdirectory = filepathshort[:lastslash]
                if parentdirectory not in res or filepathshort not in res[parentdirectory]["files"]:
                    continue
                res[parentdirectory]["files"][filepathshort].append(issue)

    def filterRuleFromSonar (self, issue, rules):
        """
        filter rules from sonarqube, keep only the rules that are stored locally
        :param issue:
        :param rules:
        :return:
        """
        ruleID = issue['rule']
        ruleResult = filter(lambda r: r['key'] == ruleID, rules)
        return ruleResult


    def makeTextRange(self, issue):
        """
        get the text range in either textRange or flow in the response from sonaqube
        :param issue: a specfic issue
        :return: the text range
        """

        res = []
        if len(issue['flows']) == 0:
            res.append({'textRange': issue['textRange'], 'msg': ""})
        else:
            for line in issue['flows']:
                res.append(line['locations'][0])
        res.sort(key=lambda x: x['textRange']['startLine'], reverse=False)

        return res

    def makeErrMessage (self, issue, ruleResult):
        """
        extract useful information from issue and make the err message
        :param issue: a specific issue
        :param ruleResult: rule information for the issue
        :return: an entry contains the necessary information
        """
        errmessage = {}
        errmessage['path'] = [issue['component']]
        errmessage['rule'] = ruleResult[0]['name']
        errmessage['message'] = issue['message']
        errmessage['severity'] = self.renameSeverity(issue['severity'])
        errmessage['author'] = issue['author']
        return errmessage




    def handleAuthorStore (self, issues, maincategory, subcategory, res):
        """
        store issues by author
        :param issues: issues under main and sub categories
        :param maincategory: main category currently checking
        :param subcategory: sub category currently checking
        :param res: buffer that contains the author oriented issues
        :return: void
        """
        for issue in issues:
            author = issue['author']
            if author not in res:
                res[author]=self.makeEmptyIssueEntry()
            if subcategory == "":
                res[author][maincategory].append(issue)
            else:
                res[author][maincategory][subcategory].append(issue)




    def makeEmptyIssueEntry (self):
        """
        make an entry that has all the main categories and sub categories name to store issues
        :return: entry that has all the main categories and sub categories name
        """
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


    def getNumIssuesAllAuthor (self, data):
        """
        add the number of issues for each category to the correpsonding author
        :param data: original by author data
        :return: by author number of issues
        """

        res = {}
        for key, val in data.iteritems():
            if type(val) is list:
                res[key] = len(val)
            else:
                res[key] = self.countNumIssuesEachCate(val)
        return res

    def countNumIssuesEachCate(self, data):
        """
        count number of issues each category
        :param data: input JSON contains all issues
        :return: JSON contains number of issues each category
        """
        res = {}
        for key, val in data.iteritems():
            res[key] = len(val)
        return res


    def getFileChecked (self):
        """
        get files that have been checked
        :return: checked files
        """
        return self.fileChecked

    def getRulesViolated(self):
        """
        get rules current project violated
        :return: rules violated
        """
        return self.rulesViolated

    def getMessage(self):
        """
        get the message contains errors and percentages
        :return: message contains errors and percentages
        """
        return self.message