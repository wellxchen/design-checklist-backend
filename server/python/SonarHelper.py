'''
Helper class that handle sonarqube related functionalities

:Authors:
    - Chengkang Xu <cx33@duke.edu>
'''

from DataHelper import DataHelper

import requests

class SonarHelper():

    def activateRule(self, SONAR_URL, QUALITY_PROFILE, ruleID):
        SONAR_LOGIN = os.environ.get("SONAR_LOGIN")
        SONAR_PASSWORD = os.environ.get("SONAR_PASSWORD")
        r = requests.post(SONAR_URL + '/api/qualityprofiles/activate_rule?=',
                          data={'profile_key': QUALITY_PROFILE, 'rule_key': ruleID},
                          auth=(SONAR_LOGIN, SONAR_PASSWORD))


    # adjust number of pages based on number of entries

    def adjustNumOfPages(self,total_number_entries, page_size):
        total_pages = 2
        if total_number_entries > page_size:
            total_pages += total_number_entries / page_size
            if total_number_entries % page_size != 0:
                total_pages += 1
        return total_pages

    # get number of pages for issues

    def getNumOfPagesIssues(self, SONAR_URL, TEST_PROJECT):
        QUERY = '/api/issues/search?ps=500&componentKeys='
        r = requests.get(SONAR_URL + QUERY + TEST_PROJECT)
        total_number_entries = r.json()['total']
        page_size = r.json()['ps']
        total_pages = self.adjustNumOfPages(total_number_entries, page_size)
        return total_pages

    # get number of pages for tree

    def getNumOfPagesTree(self, SONAR_URL, TEST_PROJECT):
        QUERY = '/api/components/tree?ps=500&component='
        r = requests.get(SONAR_URL + QUERY + TEST_PROJECT)
        if 'errors' in r.json():
            return -1
        total_number_entries = r.json()['paging']['total']
        page_size = r.json()['paging']['pageSize']
        total_pages = self.adjustNumOfPages(total_number_entries, page_size)
        return total_pages

    # get all issues or for specific rule

    def getIssues(self, SONAR_URL, TEST_PROJECT, total_pages, rule):
        issues = []
        ruleToCheck = ""
        if len(rule) > 0:
            ruleToCheck += "&rules="
            ruleToCheck += rule
        for i in range(1, total_pages):
            r = requests.get(
                SONAR_URL + '/api/issues/search?ps=500&p=' + str(i) + '&componentKeys=' + TEST_PROJECT + ruleToCheck)
            allissues = r.json()['issues']  # all issues it has
            openissue = filter(lambda r: r['status'] != 'CLOSED', allissues)
            issues.extend(openissue)
        return issues

    # get issues only associates with the rules that are in the categories

    def getIssuesInCategories (self, SONAR_URL, TEST_PROJECT):
        # if project not been analysis return error
        r = requests.get(SONAR_URL + "/api/components/show?component=" + TEST_PROJECT)
        found_project = r.json()
        if 'errors' in found_project:
            return DataHelper().errHandler()

        # get number of pages

        total_pages = self.getNumOfPagesIssues(SONAR_URL, TEST_PROJECT)

        # get all issues that are open
        issues = self.getIssues(SONAR_URL, TEST_PROJECT, total_pages, "")

        return issues

    # get rules associate with a specific quality profile

    def getRules (self, SONAR_URL, QUALITY_PROFILE):

        r = requests.get(SONAR_URL + '/api/rules/search?ps=500&activation=true&qprofile=' + QUALITY_PROFILE)
        return r.json()['rules']

    # get all files or for specific project

    def getFiles(self, SONAR_URL, TEST_PROJECT, total_pages):
        files = []
        for i in range(1, total_pages):
            r = requests.get(
                SONAR_URL + '/api/components/tree??ps=500&p=' + str(i) + '&component=' + TEST_PROJECT)
            allfiles = r.json()['components']
            nondirfiles = filter(lambda r: r['qualifier'] != 'DIR', allfiles)
            files.extend(nondirfiles)
        return files

    # handle duplicated block

    def duplicatedBlockHandlerStore(self, SONAR_URL, dup_errmessages, message, rulesViolated, filesChecked):
            dup_block_id = "common-java:DuplicatedBlocks"
            # out = ""
            for dup_errmessage in dup_errmessages:

                r = requests.get(SONAR_URL + "/api/duplications/show?key=" + dup_errmessage['path'][0])
                items = r.json()
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

                        if entry['loc'] in filesChecked:
                            discard = True
                            break
                        r1 = requests.get(SONAR_URL + "/api/sources/show?from=" + str(entry['startLine']) +
                                          "&to=" + str(entry['endLine']) +
                                          "&key=" + entry['loc'])
                        items = r1.json()["sources"]
                        entry['code'] = []
                        for item in items:
                            entry['code'].append(item[1])
                        single_dup.append(entry)

                    if not discard:
                        dup_errmessage['duplications'].append(single_dup)

                filesChecked.add(dup_errmessage['path'][0])
                if len(dup_errmessage['duplications']) > 0:
                    self.storeIssue(dup_block_id, dup_errmessage, message, rulesViolated)


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

    #get most recent analysis ID

    def getMostRecentAnalysisDate (self, SONAR_URL, TEST_PROJECT):
        r = requests.get(SONAR_URL + '/api/project_analyses/search?project=' +
                         TEST_PROJECT)

        DataHelper().displayData(r.json())
        return r.json()['analyses'][0]['date']