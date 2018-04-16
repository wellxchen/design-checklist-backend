import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python'))
from ProcessSonar import ProcessSonar

def show (project):
        return ProcessSonar("", project).process(False)

def getcommit (project):
	group = 'CompSci308_2018Spring'
        return ProcessSonar(group, project).getcommit(False)

def getcommitstat (project):
	group = 'CompSci308_2018Spring'
        return ProcessSonar(group, project).getcommit(True)

if __name__ == '__main__':
	# print show('slogo_team02')
	# print getcommit('slogo_team02')
	print getcommitstat('slogo_team02')
