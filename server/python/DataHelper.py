'''
Helper class that handle data structure related functionalities

:Authors:
    - Chengkang Xu <cx33@duke.edu>
'''


import re
from CategoriesHelper import CategoriesHelper



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



    def errHandler(self):
            data = {}
            data['err'] = "project not found"
            data[
                'description'] = "please change the file name and extension for xml.txt to pom.xml and yml.txt to .gitlab-ci.yml"
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

    def shouldSkipDir(self, dir, returndirs):
            for returndir in returndirs:
                if dir == returndir or dir[:4] == "src/":
                    return False
            return True

    def makeIssueEntryForDIR (self, issuelist, TEST_PROJECT, res):
        for issue in issuelist:
            for filepath in issue['path']:
                filepathshort = re.sub(TEST_PROJECT + ":", "", filepath)
                lastslash = filepathshort.rfind("/")
                parentdirectory = filepathshort[:lastslash]
                if parentdirectory not in res or filepathshort not in res[parentdirectory]["files"]:
                    continue
                res[parentdirectory]["files"][filepathshort].append(issue)