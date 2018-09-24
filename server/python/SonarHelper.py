'''
Helper class that handle sonarqube related functionalities

:Authors:
    - Chengkang Xu <cx33@duke.edu>
'''

from DataHelper import DataHelper
import requests

class SonarHelper(DataHelper):

    def __init__(self, group, project):
        super(SonarHelper, self).__init__(group,project)



    def activateRuleReq(self,  ruleID):
        """
        activate a single rule in a quality profile on sonarqube
        :param QUALITY_PROFILE:  quality profile to be changed
        :param ruleID: rule to be activated
        :return: void
        """

        SONAR_LOGIN = os.environ.get("SONAR_LOGIN")
        SONAR_PASSWORD = os.environ.get("SONAR_PASSWORD")
        r = requests.post(SONAR_URL + '/api/qualityprofiles/activate_rule?=',
                          data={'profile_key': self.QUALITY_PROFILE, 'rule_key': ruleID},
                          auth=(SONAR_LOGIN, SONAR_PASSWORD))


    def adjustNumOfPages(self,total_number_entries, page_size):
        """
        adjust number of pages based on number of entries
        :param total_number_entries: total number of entries
        :param page_size: number of entries on each page
        :return: adjusted number of pages
        """
        total_pages = 2
        if total_number_entries > page_size:
            total_pages += total_number_entries / page_size
            if total_number_entries % page_size != 0:
                total_pages += 1
        return total_pages


    def getNumOfPagesIssuesReq(self):
        """
        get number of pages for issues
        :return:  number of pages for issues
        """

        QUERY = '/api/issues/search?ps=500&componentKeys='
        r = requests.get(self.SONAR_URL
                         + QUERY
                         + self.TEST_PROJECT)
        total_number_entries = r.json()['total']
        page_size = r.json()['ps']
        total_pages = self.adjustNumOfPages(total_number_entries, page_size)
        return total_pages



    def getNumOfPagesTreeReq(self):
        """
        get number of pages for tree
        :return: number of pages for tree
        """

        QUERY = '/api/components/tree?ps=500&component='
        r = requests.get(self.SONAR_URL
                         + QUERY
                         + self.TEST_PROJECT)
        if 'errors' in r.json():
            return -1
        total_number_entries = r.json()['paging']['total']
        page_size = r.json()['paging']['pageSize']
        total_pages = self.adjustNumOfPages(total_number_entries, page_size)
        return total_pages


    def getIssuesReq(self, total_pages, rule):

        """
        get all issues or for specific rule or all rules
        :param total_pages: total number of pages
        :param rule: spefic rule, if empty, all rules will be checked
        :return: all issues associate with the rule
        """

        issues = []
        ruleToCheck = ""
        if len(rule) > 0:
            ruleToCheck += "&rules="
            ruleToCheck += rule
        for i in range(1, total_pages):
            r = requests.get(self.SONAR_URL
                             + '/api/issues/search?ps=500&p='
                             + str(i)
                             + '&componentKeys='
                             + self.TEST_PROJECT
                             + ruleToCheck)
            allissues = r.json()['issues']  # all issues it has
            openissue = filter(lambda r: r['status'] != 'CLOSED', allissues)
            issues.extend(openissue)
        return issues

    def getIssuesAll (self):

        """
        get all issues
        :return: all issues
        """

        # if project not been analysis return error
        found_project = self.getComponentsReq()
        if 'errors' in found_project:
            return self.errHandler()

        # get number of pages
        total_pages = self.getNumOfPagesIssuesReq()

        # get all issues that are open
        issues = self.getIssuesReq(total_pages, "")

        return issues


    def getRulesReq (self):
        """
        get rules associate with a specific quality profile
        :return: rules asscoiate with the q profile
        """

        r = requests.get(self.SONAR_URL
                         + '/api/rules/search?ps=500&activation=true&qprofile='
                         + self.QUALITY_PROFILE)
        return r.json()['rules']


    def getFilesReq(self, total_pages):

        """
        get all files or for specific project
        :param total_pages: total number of pages
        :return: list of files for that project
        """

        files = []
        for i in range(1, total_pages):
            r = requests.get(self.SONAR_URL
                             + '/api/components/tree??ps=500&p='
                             + str(i)
                             + '&component='
                             + self.TEST_PROJECT)
            allfiles = r.json()['components']
            nondirfiles = filter(lambda r: r['qualifier'] != 'DIR', allfiles)
            files.extend(nondirfiles)
        return files


    def duplicatedBlockHandlerStore(self, dup_errmessages):

        """
        store the details of each duplication error in to the message buffer
        :param dup_errmessages: duplication err message that contains the duplicatin info
        :return: void
        """

        dup_block_id = "common-java:DuplicatedBlocks"

        for dup_errmessage in dup_errmessages:

            items = self.getDuplicationsReq(dup_errmessage)
            duplications = items['duplications']
            files = items['files']
            dup_errmessage['duplications'] = []

            for duplication in duplications:

                blocks = duplication['blocks']
                single_dup = []
                discard = False
                for block in blocks:
                    entry = {}
                    entry['startLine'] = block['from']
                    entry['endLine'] = entry['startLine'] - 1 + block['size']
                    entry['loc'] = files[block['_ref']]['key']

                    if entry['loc'] in self.fileChecked:
                        discard = True
                        break

                    items = self.getSourceReq(entry['startLine'], entry['endLine'], entry['loc'])
                    entry['code'] = []
                    for item in items:
                        entry['code'].append(item[1])
                    single_dup.append(entry)

                if not discard:
                    dup_errmessage['duplications'].append(single_dup)

            self.fileChecked.add(dup_errmessage['path'][0])
            if len(dup_errmessage['duplications']) > 0:
                self.storeIssue(dup_block_id, dup_errmessage)



    def getMostRecentAnalysisDateReq (self):

        """
        get most recent analysis date
        :return: most recent analysis date
        """

        r = requests.get(self.SONAR_URL
                         + '/api/project_analyses/search?project='
                         + self.TEST_PROJECT)

        return r.json()['analyses'][0]['date']


    def getSourceReq (self, startLine, endLine, issue):

        """
        get source code from start to end
        :param startLine: start line of the code
        :param endLine:  end line of the code
        :param issue: the specific issue
        :return: the source code
        """

        if 'component' in issue:
            issue = issue['component']
        r = requests.get(self.SONAR_URL
                         + "/api/sources/show?from="
                         + str(startLine)
                         + "&to="
                         + str(endLine)
                         + "&key="
                         + issue)
        return r.json()["sources"]



    def getMeasuresReq (self):

        """
        get measurements of the project
        :return: measurements in json
        """

        functions = "functions,"  # keyword for number of functions
        classes = "classes,"  # keyword for number of classes
        directories = "directories,"  # keyword for number of directories
        comment_lines = "comment_lines,"  # keyword for number of comments
        comment_lines_density = "comment_lines_density,"  # keyword for density of comments
        ncloc = "ncloc"  # keyword for number of lines in total

        # query sonarqube to get the statistics

        r = requests.get(
            self.SONAR_URL + '/api/measures/component?componentKey=' +
            self.TEST_PROJECT + "&metricKeys=" + functions +
            classes + directories + comment_lines + comment_lines_density + ncloc)

        return r.json()['component']['measures']



    def getComponentsReq (self):

        """
        get components of the project
        :return:  components of the project
        """

        r = requests.get(self.SONAR_URL
                       + "/api/components/show?component="
                       + self.TEST_PROJECT)
        return r.json()


    def checkAnalysisLog(self,  WHICHLOG, data):
        """
        check if analysis log already existed
        :param WHICHLOG: which log to be checked
        :param data: data to be stored
        :return: void
        """
        analysisTime = self.getMostRecentAnalysisDateReq()
        self.dateLogJSON(analysisTime, WHICHLOG, data)


    def getSingleRuleReq(self, rule):
        """
        get information for a single rule
        :param rule: rule id
        :return: rule information
        """
        r = requests.get(self.SONAR_URL + '/api/rules/search?rule_key=' + rule)
        ruleInfo = r.json()['rules'][0]
        return ruleInfo


    def getDuplicationsReq(self, dup_errmessage):
        """
        get the duplications blocks from sonarqube
        :param dup_errmessage:
        :return: duplications
        """
        r = requests.get(self.SONAR_URL + "/api/duplications/show?key=" + dup_errmessage['path'][0])
        return r.json()


    def storeCodes(self, issue, errmessage):
        """
        get and store source codes of the issue
        :param issue: specific issue
        :param errmessage: buffer contains the code
        :return:
        """
        if 'textRange' in issue:
            textRange = self.makeTextRange(issue)
            for entry in textRange:
                startLine = entry['textRange']['startLine']
                endLine = entry['textRange']['endLine']

                items = self.getSourceReq(startLine, endLine, issue)

                entry['code'] = []
                for item in items:
                    entry['code'].append(item[1])
                errmessage['code'].append(entry)


    def checkQProfileLogReq(self):

        """
        check if quality profile has been updated, if so, update the cache and display the difference
        :return: void
        """

        r = requests.get(self.SONAR_URL
                         + "/api/qualityprofiles/changelog?profileKey="
                         + self.QUALITY_PROFILE)
        r = r.json()['events']
        mostrecentupdatetime = self.adjustSonarTime(r[0]['date'])
        
        existed = self.executeShellCheckDIR(self.LOG_QPROFILE_KEY_DIR,
                                            mostrecentupdatetime +  ".json")

        if "no" in existed:
            data = self.getRulesReq()
            res = []
            map(lambda e : res.append({"key" : e['key'],
                                       "name": e['name']}),
                data)
            difference = filter(lambda e: e['key'] not in self.rules.keys(), res)

            self.displayData(difference)

            self.writeLogJSON(self.LOG_QPROFILE_KEY_DIR
                              + "/"
                              + mostrecentupdatetime
                              + ".json",
                              res)

    def getRuleDetailByCategoryReq (self, categoryname):
        """
        get all detailed rule under certain category
        :param categoryname:
        :return:
        """
        rules = self.getRulesIDByCategoryName(categoryname)
        res = []
        for rule in rules:
            r = requests.get(self.SONAR_URL + '/api/rules/search?rule_key=' + rule)
            ruleInfo = r.json()['rules'][0]
            res.append(ruleInfo)
        return res

    def getAllRulesWithDetailByCateReq (self):
        """
        get all detailed rules under all category
        :return:
        """
        l = {}

        for category in self.title:
            maincate = category.keys()[0]
            l[maincate] = self.getRuleDetailByCategoryReq(maincate)

        return l






if __name__ == '__main__':

    o=SonarHelper("CompSci308_2018Spring", "test-xu")
    #o.writeLogJSON(o.JSON_RULE_WITH_DETAIL_DIR, o.getRulesReq())
    #print o.getMostRecentAnalysisDateReq()