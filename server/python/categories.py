
class categories ():



    title = [{"Communication" : ["Meaningful names",
                                   "No magic values",
                                   "Readable code",
                                   "Use scope wisely",
                                   "Same level code",
                                   "Concise code",
                                   "No warning"]},
             {"Modularity": ['Data responsibility',
                             'No public instance variables',
                             'No manager classes',
                             'No static variables',
                             'Active classes',
                             'Get method give minimum info',
                             'Get method validate input',
                             'Superclasses are their own class']},
             {"Flexibility": ['General type',
                              'Single Purpose',
                              'Behavior Driven Design',
                              'Polymorphism']},
             {"Java Notes": []},
             {"Code Smells": []},
             {"Duplications": []}]

    def getNumMainTitle(self):
        return len(self.title)

    def getNumSubTitle(self, index):
        return len(self.title[index].values())

    def getMainTitle(self, index):
        return self.title[index].key()

    def getSubTitle(self, mindex, sindex):
        return self.title[mindex][sindex]

    def getDescriptionByIndex(self, mindex, sindex):
        maintitle = self.getMainTitle(mindex)
        return descriptions[maintitle][sindex]

    def getDescriptionByName (self, mname, sindex):
        return descriptions[mname][sindex]


    severitylist = ['fail', 'high', 'medium', 'low', 'info']

    def getSeverityList (self):
        return self.severitylist

    descriptions = {
                "Communication" :
                [
                'Meaningful names: give variables, methods, classes, and packages non-abbreviated, intention-revealing names',
                'No magic values: use constants for all values used multiple times or in program logic',
                'Write readable code instead of comments: use comments only to explain important design decisions or purpose of code, not to restate code logic',
                'Use scope wisely: variables should be declared as close as possible to where they are used',
                'At all points, code should be "at the same level" (try not to mix method calls and low-level if logic in same method)',
                'Code should be "concise" (use booleans wisely, for-each loop where possible, use Java API calls instead of implementing yourself)',
                'Code should contain no warnings from Java compiler or CheckStyle'],

                "Modularity" :
                [
                "Tell, don't ask: classes should be responsible for their own data and delegate to other objects instead of doing it themselves",
                "No public instance variables: keep implementation details of your class hidden from the public interface",
                'No "manager" classes: create several classes that work together distributing intelligence, rather than one "smart" class and a few "dumb" helpers',
                'No static variables: there should be no reason for shared global public state',
                'Active classes: classes should not consist of only get/set methods and, in general, should minimize their use. ',
                'get methods should give away the minimal information possible',
                'set methods should validate data received',
                'Superclasses are their own class: thus should not contain instance variables or methods specific to only some subclasses'],

                "Flexibility" :
                [
                'Declared types should be as general as possible (i.e., ArrayList should never be visible in your public interface)',
                'Single Purpose: keep classes, methods, and variables short and well named by giving them only one purpose',
                'Behavior Driven Design: give each class a purpose by focusing on the behavior (or services) it provides first, its state later',
                'Polymorphism: use subclassing to avoid "case-based code logic" (i.e., conditional chains or case statements on "type" information)'],

                "Duplications" :
                [
                    'DRY: no duplicated code, either exactly (from cutting and pasting), structurally (in flow of control or decisions), or in setup ("boilerplate" code)']
                }


    communication = {
    'squid:S00115', 'squid:S1190', 'squid:S00101', 'squid:S1942', 'squid:S1221', 'squid:S1223', 'squid:S109',
    'squid:S00122', 'squid:S00121', 'squid:S2681','squid:S1941','squid:S881', 'squid:S2114','squid:S2589', 'squid:S2293',
    'squid:S2178', 'squid:S2175', 'squid:S2200', 'squid:S1126', 'squid:S1125', 'squid:S2185', 'squid:S1481',
    'squid:S3923', 'squid:S1656', 'squid:S2959', 'squid:S1604','squid:S1133', 'squid:S00108', 'squid:S2097',
    'squid:S1148', 'squid:S00112', 'squid:S2208', 'squid:UselessImportCheck', 'squid:UselessParenthesesCheck', 'squid:S1199',
    'squid:S1488', 'squid:S1244', 'squid:S135', 'squid:S2692', 'squid:S1710', 'squid:S3358', 'squid:S2147', 'squid:S1170',
    'squid:S2159', 'squid:S1068', 'squid:S2153', 'squid:S1066', ' squid:S1157', 'squid:S2154', 'squid:S1764'
    }
    modularity = {
    'squid:S1258', 'squid:S1450', 'squid:HiddenFieldCheck','squid:S3066', 'squid:ClassVariableVisibilityCheck',
    'squid:S00104', 'squid:S1188', 'squid:S1200', 'squid:S1448','squid:S2390', 'squid:S2209', 'squid:S1444',
    'squid:S2885', 'squid:S2386', 'squid:S2786', 'squid:S1185', 'squid:S2638',
    }
    flexibility = {
    'squid:S1319','squid:S3776', 'squid:S2176', 'squid:MethodCyclomaticComplexity',
        'squid:S138', 'squid:S1067', 'squid:S00107','squid:S1479', 'squid:S1219', 'squid:S1151','squid:S3400'
    }
    javanote = {
    'squid:EmptyFile', 'squid:S2094', 'squid:S2177', 'squid:S1698', 'squid:S1596', 'squid:S1181', 'squid:S2275',
    'squid:S3457', 'squid:S1872', 'squid:S1197', 'squid:S2133', 'squid:S1641', 'squid:S1640', 'squid:S1155', 'squid:S2864',
    'squid:S1158', 'squid:S1168', 'squid:S1166', 'squid:S2131', 'squid:S1643', 'squid:S2975', 'squid:S3631',
    'squid:S1695', 'squid:S1210', 'squid:S2789', 'squid:S2440', 'squid:S1194', 'squid:S2696', 'squid:S2694',
    'squid:S2388', 'squid:S2387', 'squid:S2384', 'squid:S2141', 'squid:S3038', 'squid:S2156', 'squid:S1186',
    'squid:S2129', 'squid:S1150', 'squid:S1165', 'squid:S1160', 'squid:S2972', 'squid:ObjectFinalizeOverridenCallsSuperFinalizeCheck',
    'squid:S1201', 'squid:S1206', 'squid:S2160', 'squid:S1611', 'squid:S1850', 'squid:S1858', 'squid:S1711', 'squid:S3422',
    'squid:S2166', 'squid:S1118', 'squid:CallToDeprecatedMethod', 'squid:UndocumentedApi', 'squid:S1610', 'squid:S2162',
    'squid:S2301', 'squid:S1213'
    }
    codesmell = {

        'squid:S2189', 'squid:S2252', 'squid:S2251', 'squid:S1994', 'squid:S1862', 'squid:S134', 'squid:S1905',
        'squid:ForLoopCounterChangedCheck', 'squid:S1226'
    }
    duplicationsID = {
    'common-java:DuplicatedBlocks','squid:S3047',  'squid:S1939','squid:S1871','squid:S1700','squid:S1192'
    }
    duplications = [
        {'key': 'common-java:DuplicatedBlocks', 'name': 'Source files should not have any duplicated blocks'},
        {'key': 'squid:S3047', 'name': 'Multiple loops over the same set should be combined'},
        {'key': 'squid:S1939', 'name': 'Extensions and implementations should not be redundant'},
        {'key': 'squid:S1871',
         'name': 'Two branches in a conditional structure should not have exactly the same implementation'},
        {'key': 'squid:S1700', 'name': 'A field should not duplicate the name of its containing class'},
        {'key': 'squid:S1192', 'name': 'String literals should not be duplicated'}]

    #id : [main, sub]
    #main : 0 communication, 1 modularity, 2 flexibility, 3 javanote, 4 codesmell, 5 duplications
    rules = {'squid:S1942' : [0,1],
             'squid:S00115' : [0,1],
             'squid:S1223' : [0,1],
             'squid:S1190' : [0,1],
             'squid:S1221' : [0,1],
             'squid:S00101' : [0,1],
             'squid:S109' : [0, 2],
             'squid:S00122': [0, 3],
             'squid:S00121': [0, 3],
             'squid:S2681': [0, 3],
             'squid:S1941' : [0, 4],
             'squid:S881': [0, 5],
             'squid:S2114': [0, 5],
             'squid:S1604': [0, 6],
             'squid:S2175': [0, 6],
             'squid:S1126': [0, 6],
             'squid:S2293': [0, 6],
             'squid:S2200': [0, 6],
             'squid:S2589': [0, 6],
             'squid:S1656': [0, 6],
             'squid:S2178': [0, 6],
             'squid:S2959': [0, 6],
             'squid:S2185': [0, 6],
             'squid:S3923': [0, 6],
             'squid:S1481': [0, 6],
             'squid:S1125': [0, 6],
             'squid:S2147': [0, 7],
             'squid:S1157': [0, 7],
             'squid:UselessParenthesesCheck': [0, 7],
             'squid:S1488': [0, 7],
             'squid:S1764': [0, 7],
             'squid:S00108': [0, 7],
             'squid:S2153': [0, 7],
             'squid:S1170': [0, 7],
             'squid:S1133': [0, 7],
             'squid:S2097': [0, 7],
             'squid:S2154': [0, 7],
             'squid:S1199': [0, 7],
             'squid:UselessImportCheck': [0, 7],
             'squid:S2159': [0, 7],
             'squid:S135': [0, 7],
             'squid:S2692': [0, 7],
             'squid:S1710': [0, 7],
             'squid:S1066': [0, 7],
             'squid:S1068': [0, 7],
             'squid:S00112': [0, 7],
             'squid:S1148': [0, 7],
             'squid:S1244': [0, 7],
             'squid:S3358': [0, 7],
             'squid:S2208': [0, 7],
             'squid:S1450': [1, 1],
             'squid:S1258': [1, 1],
             'squid:HiddenFieldCheck': [1, 1],
             'squid:S3066': [1, 2],
             'squid:ClassVariableVisibilityCheck' : [1, 2],
             'squid:S00104': [1, 3],
             'squid:S1200': [1, 3],
             'squid:S1188': [1, 3],
             'squid:S1448': [1, 3],
             'squid:S2786': [1, 4],
             'squid:S2390': [1, 4],
             'squid:S2386': [1, 4],
             'squid:S2885': [1, 4],
             'squid:S2209': [1, 4],
             'squid:S1444': [1, 4],
             'squid:S1185' : [1, 7],
             'squid:S2638' : [1, 7],
             'squid:S1319' : [2, 1],
             'squid:S138': [2, 2],
             'squid:S1067': [2, 2],
             'squid:MethodCyclomaticComplexity': [2, 2],
             'squid:S00107': [2, 2],
             'squid:S3776': [2, 2],
             'squid:S2176': [2, 2],
             'squid:S3400' : [2, 3],
             'squid:S1479' : [2, 4],
             'squid:S1219' : [2, 4],
             'squid:S1151' : [2, 4],
             'squid:S1181': [3],
             'squid:S2129': [3],
             'squid:S2141': [3],
             'squid:S1872': [3],
             'squid:S1641': [3],
             'squid:S1640': [3],
             'squid:S1643': [3],
             'squid:S1850': [3],
             'squid:S2275': [3],
             'squid:S2864': [3],
             'squid:S1186': [3],
             'squid:S1858': [3],
             'squid:CallToDeprecatedMethod': [3],
             'squid:S1150': [3],
             'squid:EmptyFile': [3],
             'squid:S2694': [3],
             'squid:S1155': [3],
             'squid:S1213': [3],
             'squid:S1210': [3],
             'squid:S1158': [3],
             'squid:S3631': [3],
             'squid:S2789': [3],
             'squid:S3457': [3],
             'squid:S2094': [3],
             'squid:ObjectFinalizeOverridenCallsSuperFinalizeCheck': [3],
             'squid:S2177': [3],
             'squid:S1118': [3],
             'squid:S2133': [3],
             'squid:S2156': [3],
             'squid:S2131': [3],
             'squid:S1194': [3],
             'squid:S1197': [3],
             'squid:S1695': [3],
             'squid:S2975': [3],
             'squid:S2972': [3],
             'squid:S1596': [3],
             'squid:S2696': [3],
             'squid:S1610': [3],
             'squid:S1611': [3],
             'squid:S1698': [3],
             'squid:S1711': [3],
             'squid:S1201': [3],
             'squid:S1168': [3],
             'squid:S2384': [3],
             'squid:S2387': [3],
             'squid:S3038': [3],
             'squid:S1165': [3],
             'squid:S2440': [3],
             'squid:S1206': [3],
             'squid:S1160': [3],
             'squid:S3422': [3],
             'squid:S2388': [3],
             'squid:S2301': [3],
             'squid:S2160': [3],
             'squid:UndocumentedApi': [3],
             'squid:S2162': [3],
             'squid:S1166': [3],
             'squid:S2166': [3],
             'squid:S1994': [4],
             'squid:S1226': [4],
             'squid:S1862': [4],
             'squid:S2252': [4],
             'squid:S2251': [4],
             'squid:S134': [4],
             'squid:S1905': [4],
             'squid:S2189': [4],
             'squid:ForLoopCounterChangedCheck': [4],
             'common-java:DuplicatedBlocks': [5],
             'squid:S3047': [5],
             'squid:S1939': [5],
             'squid:S1871': [5],
             'squid:S1700': [5],
             'squid:S1192': [5]
    }

    def getRuleDetail (self, ruleID):
        if ruleID in self.rules:
            return self.rules[ruleID]
        return []

    def getMainCateNameById(self, ruleID):
        if ruleID in self.rules:
            cates = self.rules[ruleID]
            if cates[0] == 0:
                return "communication"
            if cates[0] == 1:
                return "modularity"
            if cates[0] == 2:
                return "flexibility"
            if cates[0] == 3:
                return "javanote"
            if cates[0] == 4:
                return "codesmell"
            if cates[0] == 5:
                return "duplications"
        return ""

    def getCategoryNumberByName(self, name):
        if name == "communication":
            return 0
        if name ==  "modularity":
            return 1
        if name ==  "flexibility":
            return 2
        if name ==  "javanote":
            return 3
        if name == "codesmell":
            return 4
        if name == "duplications":
            return 5
        return -1

    def allrules (self):
        return self.communication.union(
            self.flexibility.union(
            self.javanote.union(
            self.codesmell.union(
            self.modularity.union(self.duplicationsID)))))

