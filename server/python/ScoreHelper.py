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
    def calTotalScorePerCategory(self, SONAR_URL, categoryname):
        rules = self.getRulesByCategoryName(categoryname)


        score = 0.00
        for rule in rules:
            r = requests.get(SONAR_URL + '/api/rules/search?rule_key=' + rule)
            ruleInfo = r.json()['rules'][0]
            ruleseverity = ruleInfo["severity"]
            score += self.getScoreForSeverity(ruleseverity)
        return score

    # calcualte total score for rules under all categories
    def calTotalScoreAllCategory(self):
        l = {}

        for category in self.title:
            maincate = category.keys()[0]
            l[maincate] = self.calTotalScorePerCategory(self.SONAR_URL, maincate)
        return l

    # get score for the category
    def getScoreForSeverity(self, ruleseverity):

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

    #
    def calPercentByScore(self, scores, scores_rem):
        l = []
        for i in range(0, self.getNumMainTitle()):
            l.append(0)

        for catename, score in scores.iteritems():
            index = self.getCategoryNumberByName(catename)
            l[index] = (score / scores_rem[catename]) * 100.00
        return l

    # calcualte percentage for the category (SIMPLY BY NUMBER OF RULES VIOLATED)
    def calPercentByNum(self, category, rules_under_category):
        if len(category) > 0:
            return ((0.0 + len(category) - len(rules_under_category)) / len(category)) * 100.00
        return 100.0