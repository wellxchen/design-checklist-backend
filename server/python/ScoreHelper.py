'''
Helper class that handle score related functionalities

:Authors:
    - Chengkang Xu <cx33@duke.edu>
'''

import requests


from CategoriesHelper import CategoriesHelper
from LocalHelper import LocalHelper


class ScoreHelper( LocalHelper, CategoriesHelper):

    def __init__(self, group, project):
        super(ScoreHelper, self).__init__(group, project)


    # calcualte total score for rules under one category
    def calTotalScorePerCategory(self, mainname, subid):

        """
        calculate the total score for the main category
        :param categoryname: category name
        :return: total scores of the category
        """
        rules = []


        if (subid == -1) :
            rules.extend(self.ruleswithdetailbycate[mainname])
        else :
            rules.extend(self.ruleswithdetailbycate[mainname][subid].values()[0])

        score = 0.00

        for rule in rules:

            ruleseverity = rule["severity"]
            score += self.getScoreForSeverity(ruleseverity)
        return score


    def calTotalScoreAllCategory(self):
        """
        calcualte total score for rules under all categories
        :return: scores for all categories
        """
        l = {}

        for category in self.title:
            curmaincate = category.keys()
            maincate = curmaincate[0]
            nosub = -1
            subcategories = category.values()[0]
            if len(subcategories) > 0:
                for i in range(0, len(subcategories)):
                    subcate = subcategories[i]
                    if i == 0:
                        l[maincate] = []
                    l[maincate].append({subcate: self.calTotalScorePerCategory(maincate, i)})
            else:
                l[maincate] = self.calTotalScorePerCategory(maincate, nosub)
        return l



    def getScoreForSeverity(self, ruleseverity):

        """
        convert sonar severity to weights
        :param ruleseverity: sonar severity
        :return: weights
        """
        if ruleseverity == "BLOCKER":
            return 100.00
        if ruleseverity == "CRITICAL":
            return 50.00
        if ruleseverity == "MAJOR":
            return 20.00
        if ruleseverity == "MINOR":
            return 10.00
        if ruleseverity == "INFO":
            return 5.00
        return 0.0

    def renameSeverity(self, ruleseverity):
        """
        convert sonar severity to self defined severity
        :param ruleseverity: sonar severity
        :return: self defined severity
        """
        if ruleseverity == "BLOCKER":
            return "fail"
        if ruleseverity == "CRITICAL":
            return "high"
        if ruleseverity == "MAJOR":
            return "medium"
        if ruleseverity == "MINOR":
            return "low"
        if ruleseverity == "INFO":
            return "info"
        return ""


    def calPercentByScore(self, scores, scores_rem):
        """
        calculate percentage of correctness based on weighted scores
        :param scores: score buffer that stores scores
        :param scores_rem: total score under that main category
        :return: buffer that contains scores
        """
        l = {}


        for catename, score in scores.iteritems():
            total_score = 0.0
            rem_score = 0.0
            l[catename] = {}
            l[catename]['percentage'] = 1
            if type(score) == list:

                l[catename]['subcategory'] = []
                index = 0
                for subentry in score:
                    subcatename = subentry.keys()[0]
                    subcatescore = subentry.values()[0]
                    subcatescore_rem = scores_rem[catename][index].values()[0]
                    total_score += subcatescore
                    rem_score += subcatescore_rem
                    l[catename]['subcategory'].append({subcatename : (subcatescore / subcatescore_rem) * 100.00})
                    index += 1
            else:
                total_score = score
                rem_score = scores_rem[catename]
            l[catename]['percentage'] = (total_score / rem_score) * 100.00
        return l


    def deductscore (self, ruleID, scores_checked_Id, issue, scores):
        maincategoryname = self.getMainCateNameByRuleId(ruleID)
        subcategoryid = self.getSubCatedIdByRuleId(ruleID)
        if len(maincategoryname) > 0 and ruleID not in scores_checked_Id:
            deductscore = self.getScoreForSeverity(issue['severity'])
            if subcategoryid == -1:
                scores[maincategoryname] -= deductscore
            else:
                newscore = scores[maincategoryname][subcategoryid].values()[0] - deductscore
                subcatename = self.getSubCateShortDesc(maincategoryname, subcategoryid)
                scores[maincategoryname][subcategoryid][subcatename] = newscore
            scores_checked_Id.add(ruleID)
