
'''
handle categories related functionality
'''

from categories import categories

class CategoriesHelper ():

    def getNumMainTitle(self):
        return len(categories().title)


    def getNumSubTitle(self, index):
        return len(categories().title[index].values())


    def getMainTitle(self, index):
        return categories().title[index].key()


    def getSubTitle(self, mindex, sindex):
        return categories().title[mindex][sindex]


    def getDescriptionByIndex(self, mindex, sindex):
        maintitle = categories().getMainTitle(mindex)
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
            if cates[0] == 0:
                return "communication"
            if cates[0] == 1:
                return "modularity"
            if cates[0] == 2:
                return "flexibility"
            if cates[0] == 3:
                return "javanote"
            if cates[0] == 4:
                return "codesmell"
            if cates[0] == 5:
                return "duplications"
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

