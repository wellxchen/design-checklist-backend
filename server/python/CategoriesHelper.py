
'''
handle categories related functionality

:Authors:
    - Chengkang Xu <cx33@duke.edu>

'''

from categories import categories


class CategoriesHelper ():

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
        return len(categories().title)

    def getNumSubTitle(self, index):

        return len(categories().title[index].values()[0])

    def getMainTitle(self, index):
        return categories().title[index].keys()[0]

    def getSubTitle(self, mindex, sindex):

        maintitle = self.getMainTitle(mindex)
        return categories().title[mindex][maintitle][sindex]

    def getDescriptionByIndex(self, mindex, sindex):
        maintitle = self.getMainTitle(mindex)
        return categories().descriptions[maintitle][sindex]

    def getDescriptionByName(self, mname, sindex):
        return categories().descriptions[mname][sindex]

    def getSeverityList (self):
        return categories().severitylist

    def getRuleDetail(self, ruleID):
        if ruleID in categories().rules:
            return categories().rules[ruleID]
        return []

    def getMainCateNameById(self, ruleID):
        if ruleID in categories.rules:
            cates = categories.rules[ruleID]
            return self.getAllMainTitle()[cates[0]]
        return ""

    def getCategoryNumberByName(self, name):

        if name == "communication":
            return 0
        if name == "modularity":
            return 1
        if name == "flexibility":
            return 2
        if name == "javanote":
            return 3
        if name == "codesmell":
            return 4
        if name == "duplications":
            return 5
        return -1

    def allrules(self):
        return categories().communication.union(
            categories().flexibility.union(
                categories().javanote.union(
                    categories().codesmell.union(
                        categories().modularity.union(categories().duplicationsID)))))

    def getDuplications(self):
        return categories().duplications


if __name__ == '__main__':
    print CategoriesHelper().getAllMainTitle()