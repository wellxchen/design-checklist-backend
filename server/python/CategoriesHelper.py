
'''
handle categories related functionality

:Authors:
    - Chengkang Xu <cx33@duke.edu>

'''

from  categories import categories

class CategoriesHelper (categories):


    def __init__(self):
        super(CategoriesHelper, self).__init__()
    
    def getAllMainTitle(self):
        res = []
        for i in range(self.getNumMainTitle()):
            res.append(self.getMainTitle(i))
        return res

    def getAllSubTitleOfMain(self, mindex):
        res = []
        for i in range(self.getNumSubTitle(mindex)):
            res.append(self.getSubTitle(mindex, i))
        return res

    def getNumMainTitle(self):
        return len(self.title)

    def getNumSubTitle(self, index):

        return len(self.title[index].values()[0])

    def getMainTitle(self, index):
        return self.title[index].keys()[0]

    def getSubTitle(self, mindex, sindex):

        maincates = self.getMainTitle(mindex)
        return self.title[mindex][maincates][sindex]

    def getDescriptionByIndex(self, mindex, sindex):
        maincates = self.getMainTitle(mindex)
        return self.descriptions[maincates][sindex]

    def getDescriptionByName(self, mname, sindex):
        return self.descriptions[mname][sindex]

    def getSeverityList (self):
        return self.severitylist

    def getRuleDetail(self, ruleID):
        if ruleID in self.rules:
            return self.rules[ruleID]
        return []

    def getMainCateNameById(self, ruleID):
        if ruleID in self.rules:
            cates = self.rules[ruleID]
            return self.getAllMainTitle()[cates[0]]
        return ""

    def getCategoryNumberByName(self, name):

        if name == "Communication":
            return 0
        if name == "Modularity":
            return 1
        if name == "Flexibility":
            return 2
        if name == "Java Notes":
            return 3
        if name == "Code Smells":
            return 4
        if name == "Duplications":
            return 5
        return -1

    def allrules(self):
        return len(self.rules.keys())

    def getDuplicationsLocal(self):
        return self.duplications

    def getRulesByCategoryName(self, name):
        categorynumber = self.getCategoryNumberByName(name)
        res = []
        for ruleid, cates in self.rules.iteritems():
            if cates[0] == categorynumber:
                res.append(ruleid)
        return res


if __name__ == '__main__':
    print CategoriesHelper().getAllMainTitle()