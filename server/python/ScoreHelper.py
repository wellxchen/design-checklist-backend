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
            rules.extend(self.ruleswithdetailbycate[mainname][subid])

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
            subcateid = -1
            if len(category.values()) > 0:
                for i in range(0, len(category.values())):
                    subcate = self.title[maincate][i]
                    if i == 0:
                        l[maincate] = []
                    l[maincate].append({subcate, self.calTotalScorePerCategory(maincate, subcateid)})
            else:
                l[maincate] = self.calTotalScorePerCategory(maincate, subcateid)
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
        l = []
        for i in range(0, self.getNumMainTitle()):
            l.append(0)

        for catename, score in scores.iteritems():
            index = self.getCategoryNumberByName(catename)
            l[index] = (score / scores_rem[catename]) * 100.00
        return l
