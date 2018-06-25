from GitlabHelper import GitlabHelper
from SonarHelper import SonarHelper

class Helper (SonarHelper, GitlabHelper):
    def __init__(self, group, project):
        super(Helper, self).__init__(group,project)


