
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
        """
        get all main catgories name
        :return: all main categories name
        """
        res = []
        for i in range(self.getNumMainTitle()):
            res.append(self.getMainTitle(i))
        return res

    def getAllSubTitleOfMain(self, mindex):
        """
        get all sub categories under a main category
        :param mindex: main category index
        :return: get all sub categories under a main category
        """
        res = []
        for i in range(self.getNumSubTitle(mindex)):
            res.append(self.getSubTitle(mindex, i))
        return res

    def getNumMainTitle(self):
        """
        get number of main categories
        :return: number of main categories
        """
        return len(self.title)

    def getNumSubTitle(self, index):
        """
        get number of sub categories under a main category
        :param index: main category index
        :return: number of sub categories under a main category
        """
        return len(self.title[index].values()[0])

    def getMainTitle(self, index):
        """
        get specific main category name
        :param index:index of the category
        :return:category name
        """

        return self.title[index].keys()[0]

    def getSubTitle(self, mindex, sindex):

        """
        get specific sub category name
        :param mindex: main category index
        :param sindex: sub category index
        :return: sub category name
        """

        maincates = self.getMainTitle(mindex)
        return self.title[mindex][maincates][sindex]

    def getDescriptionByIndex(self, mindex, sindex):

        """
        get sub category detailed description
        :param mindex: main category index
        :param sindex: sub category index
        :return: the description
        """
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

    def getNumOfAllRules(self):
        return len(self.rules.keys())

    def getAllRules(self):
        return self.rules.keys()

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