
'''
Helper class that handle gitlab related functionalities

:Authors:
    - Chengkang Xu <cx33@duke.edu>
'''


import json
import requests

import os
from os.path import join, dirname, abspath
from dotenv import load_dotenv


ROOT = dirname(__file__)[:-14]
dotenv_path = ROOT + "/server/documents/local/app-env"
load_dotenv(dotenv_path)

class GitlabHelper (object):

    def __init__(self):
        pass

    def getGitlabInfoAllPages (self, URL, TOKEN):
        """
        get information from gitlab include all pages
        :param URL: gitlab url
        :param TOKEN: token to login to gitlab
        :return: return all corresponding info
        """
        result = []
        counter = 1
        r = requests.get(URL + str(counter), headers={'PRIVATE-TOKEN': TOKEN})

        while len(r.json()) > 0:
            result.extend(r.json())
            counter += 1
            r = requests.get(URL + str(counter), headers={'PRIVATE-TOKEN': TOKEN})
        return result


    def getcommits(self, GITLAB_URL, projectid, TOKEN):
        """
        get all commits for a specific project
        :param GITLAB_URL: gitlab url
        :param projectid:
        :param TOKEN: token to login to gitlab
        :return: return commits for a specfic project
        """

        URL = GITLAB_URL + "/projects/" + str(projectid) + "/repository/commits?ref_name=master&per_page=100&page="

        return self.getGitlabInfoAllPages(URL, TOKEN)

    def getGitlabIssuesByState (self, GITLAB_URL, projectid, TOKEN, state):
        """
        get issues in gitlab
        :param GITLAB_URL: gitlab url
        :param state: open or close
        :return: return issues in gitlab by state
        """

        URL = GITLAB_URL + "/projects/" + str(projectid) + "/repository/issues?state=" + state

        return self.getGitlabInfoAllPages(URL, TOKEN)

    def  getGitlabProjectIDByName (self, GITLAB_GROUP, PLAIN_PROJECT, TOKEN):

        """
        get gitlab project id by project name
        :param GITLAB_GROUP: gitlab group
        :param PLAIN_PROJECT: name input
        :param TOKEN: token to login to gitlab
        :return: project id
        """

        GITLAB_URL = "https://coursework.cs.duke.edu/api/v4"
        URL = GITLAB_URL \
              +"/groups/" \
              + GITLAB_GROUP \
              + "/projects?search="\
              + PLAIN_PROJECT

        r  = requests.get(URL, headers={'PRIVATE-TOKEN': TOKEN})
        projects = r.json()

        # get project id from response
        projectid = -1
        for p in projects:
            if p['path'] == PLAIN_PROJECT \
                    or p['name'] == PLAIN_PROJECT:
                projectid = p['id']
                break
        return projectid

    def convertEmailtoGitlabId(self, authoremail, studentidmaps):

        indexofat = authoremail.find("@")
        authorname = authoremail[:indexofat]

        if authorname in studentidmaps["email"]:
            authorname = studentidmaps["email"][authorname]
        elif authorname in studentidmaps["netid"]:
            authorname = studentidmaps["netid"][authorname]
        return authorname