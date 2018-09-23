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
    def calTotalScorePerCategory(self, categoryname):

        """
        calculate the total score for the main category
        :param categoryname: category name
        :return: total scores of the category
        """
        rules = self.ruleswithdetailbycate[categoryname]

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
            maincate = category.keys()[0]
            l[maincate] = self.calTotalScorePerCategory(maincate)
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
