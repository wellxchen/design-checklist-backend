'''
:Authors:
    - Chengkang Xu <cx33@duke.edu>
'''

class categories (object):

    # title of main categories and sub categories

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


    # list of self defined severities

    severitylist = ['fail', 'high', 'medium', 'low', 'info']


    # descriptions of subcategories

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


    # rules under duplications

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

    rules = {'squid:S1942' : [0,0],
             'squid:S00115' : [0,0],
             'squid:S1223' : [0,0],
             'squid:S1190' : [0,0],
             'squid:S1221' : [0,0],
             'squid:S00101' : [0,0],
             'squid:S109' : [0, 1],
             'squid:S00122': [0, 2],
             'squid:S00121': [0, 2],
             'squid:S2681': [0, 2],
             'squid:S1941' : [0, 3],
             'squid:S881': [0, 4],
             'squid:S2114': [0, 4],
             'squid:S1604': [0, 5],
             'squid:S2175': [0, 5],
             'squid:S1126': [0, 5],
             'squid:S2293': [0, 5],
             'squid:S2200': [0, 5],
             'squid:S2589': [0, 5],
             'squid:S1656': [0, 5],
             'squid:S2178': [0, 5],
             'squid:S2959': [0, 5],
             'squid:S2185': [0, 5],
             'squid:S3923': [0, 5],
             'squid:S1481': [0, 5],
             'squid:S1125': [0, 5],
             'squid:S2147': [0, 6],
             'squid:S1157': [0, 6],
             'squid:UselessParenthesesCheck': [0, 6],
             'squid:S1488': [0, 6],
             'squid:S1764': [0, 6],
             'squid:S00108': [0, 6],
             'squid:S2153': [0, 6],
             'squid:S1170': [0, 6],
             'squid:S1133': [0, 6],
             'squid:S2097': [0, 6],
             'squid:S2154': [0, 6],
             'squid:S1199': [0, 6],
             'squid:UselessImportCheck': [0, 6],
             'squid:S2159': [0, 6],
             'squid:S135': [0, 6],
             'squid:S2692': [0, 6],
             'squid:S1710': [0, 6],
             'squid:S1066': [0, 6],
             'squid:S1068': [0, 6],
             'squid:S00112': [0, 6],
             'squid:S1148': [0, 6],
             'squid:S1244': [0, 6],
             'squid:S3358': [0, 6],
             'squid:S2208': [0, 6],
             'squid:S1450': [1, 0],
             'squid:S1258': [1, 0],
             'squid:HiddenFieldCheck': [1, 0],
             'squid:S3066': [1, 1],
             'squid:ClassVariableVisibilityCheck' : [1, 1],
             'squid:S00104': [1, 2],
             'squid:S1200': [1, 2],
             'squid:S1188': [1, 2],
             'squid:S1448': [1, 2],
             'squid:S2786': [1, 3],
             'squid:S2390': [1, 3],
             'squid:S2386': [1, 3],
             'squid:S2885': [1, 3],
             'squid:S2209': [1, 3],
             'squid:S1444': [1, 3],
             'squid:S1185' : [1, 4],
             'squid:S2638' : [1, 4],
             'squid:S1319' : [2, 0],
             'squid:S138': [2, 1],
             'squid:S1067': [2, 1],
             'squid:MethodCyclomaticComplexity': [2, 1],
             'squid:S00107': [2, 1],
             'squid:S3776': [2, 1],
             'squid:S2176': [2, 1],
             'squid:S3400' : [2, 2],
             'squid:S1479' : [2, 3],
             'squid:S1219' : [2, 3],
             'squid:S1151' : [2, 3],
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

    def __init__(self):
        pass