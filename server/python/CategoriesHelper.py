
'''
handle categories related functionality

:Authors:
    - Chengkang Xu <cx33@duke.edu>

'''


import json
from os.path import dirname



class CategoriesHelper (object):
    ROOT = dirname(__file__)[:-14]
    JSON_DIR = ROOT + "/server/json"
    JSON_SEVERITY_DIR = JSON_DIR + "/severity.json"
    JSON_TITLE_DIR = JSON_DIR + "/title.json"
    JSON_DESCRIPTION_DIR = JSON_DIR + "/description.json"
    JSON_DUPLICATION_DIR = JSON_DIR + "/description_duplication.json"
    JSON_RULE_DIR = JSON_DIR + "/rules.json"
    JSON_RULE_WITH_DETAIL_DIR = JSON_DIR + "/rules_detail.json"
    JSON_RULE_WITH_DETAIL_BY_CATE_DIR = JSON_DIR + "/rules_detail_cate.json"
    # title of main categories and sub categories

    with open(JSON_TITLE_DIR) as f:
        data = json.load(f)

    title = data['title']

    # list of self defined severities

    with open(JSON_SEVERITY_DIR) as f:
        data = json.load(f)

    severitylist = data['severitylist']

    # descriptions of subcategories

    with open(JSON_DESCRIPTION_DIR) as f:
        data = json.load(f)
    descriptions = data['description']

    # rules under duplications
    with open(JSON_DUPLICATION_DIR) as f:
        data = json.load(f)
    duplications = data['description']

    # rules with detail by category
    with open(JSON_RULE_WITH_DETAIL_BY_CATE_DIR) as f:
        data = json.load(f)
    ruleswithdetailbycate = data

    # rules with detail
    with open(JSON_RULE_WITH_DETAIL_DIR) as f:
        data = json.load(f)
    ruleswithdetail = data

    # rule mapping
    with open(JSON_RULE_DIR) as f:
        data = json.load(f)
    rules = data['rule']

    # id : [main, sub]
    # main : 0 communication, 1 modularity, 2 flexibility, 3 javanote, 4 codesmell, 5 duplications



    def __init__(self):
        pass
    
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
        get sub category detailed description by main category index
        :param mindex: main category index
        :param sindex: sub category index
        :return: the description
        """
        maincates = self.getMainTitle(mindex)
        return self.descriptions[maincates][sindex]

    def getDescriptionByName(self, mname, sindex):
        """
        get sub category detailed description by main category name
        :param mname: name of the main category
        :param sindex: index of the sub category
        :return: the description
        """
        return self.descriptions[mname][sindex]

    def getSeverityList (self):
        """
        get the severity list
        :return: severity list
        """
        return self.severitylist

    def getRuleDetail(self, ruleID):
        """
        get the detail of the ruleID
        :param ruleID: id of the rule
        :return: main and sub categories of the rule
        """
        if ruleID in self.rules:
            return self.rules[ruleID]
        return []

    def getMainCateNameById(self, ruleID):
        """
        get main category name by id
        :param ruleID: rule id
        :return: main category name
        """
        if ruleID in self.rules:
            cates = self.rules[ruleID]
            return self.getAllMainTitle()[cates[0]]
        return ""

    def getCategoryNumberByName(self, name):
        """
        get main category's index in the buffer by its name
        :param name: name of the main category
        :return: index
        """
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
        """
        get number of all rules
        :return: number of all rules
        """
        return len(self.rules.keys())

    def getAllRules(self):
        """
        get all rules
        :return: get all rules
        """
        return self.rules.keys()

    def getDuplicationsLocal(self):
        """
        get all rules under duplications
        :return: all rules under duplications
        """
        return self.duplications

    def getRulesIDByCategoryName(self, name):
        """
        get rules ID by main category name
        :param name: main category name
        :return: rules under that category
        """
        categorynumber = self.getCategoryNumberByName(name)
        res = []
        for ruleid, cates in self.rules.iteritems():
            if cates[0] == categorynumber:
                res.append(ruleid)
        return res



if __name__ == '__main__':
    print CategoriesHelper().getAllMainTitle()