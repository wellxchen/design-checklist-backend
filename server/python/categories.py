'''
:Authors:
    - Chengkang Xu <cx33@duke.edu>
'''

import json
from os.path import dirname

ROOT = dirname(__file__)[:-14]
JSON_DIR = ROOT + "/server/json"
JSON_TITLE_DIR = JSON_DIR + "/title.json"
JSON_SEVERITY_DIR = JSON_DIR + "/severity.json"
JSON_DESCRIPTION_DIR = JSON_DIR + "/description.json"
JSON_DUPLICATION_DIR = JSON_DIR + "/description_duplication.json"


class categories (object):

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



    #id : [main, sub]
    #main : 0 communication, 1 modularity, 2 flexibility, 3 javanote, 4 codesmell, 5 duplications

    with open(JSON_DIR + "/rule.json") as f:
        data = json.load(f)
    rules = data['rule']

    def __init__(self):
        pass


if __name__ == "__main__":
    print categories.title