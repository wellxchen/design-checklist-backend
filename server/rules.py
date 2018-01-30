
class categories ():

    Communication_Sub = [
                'Meaningful names: give variables, methods, classes, and packages non-abbreviated, intention-revealing names',
                'No magic values: use constants for all values used multiple times or in program logic',
                'Write readable code instead of comments: use comments only to explain important design decisions or purpose of code, not to restate code logic',
                'Use scope wisely: variables should be declared as close as possible to where they are used',
                'At all points, code should be "at the same level" (try not to mix method calls and low-level if logic in same method)',
                'Code should be "concise" (use booleans wisely, for-each loop where possible, use Java API calls instead of implementing yourself)',
                'Code should contain no warnings from Java compiler or CheckStyle']

    Modularbility_sub = [
                "Tell, don't ask: classes should be responsible for their own data and delegate to other objects instead of doing it themselves",
                "No public instance variables: keep implementation details of your class hidden from the public interface",
                'No "manager" classes: create several classes that work together distributing intelligence, rather than one "smart" class and a few "dumb" helpers',
                'No static variables: there should be no reason for shared global public state',
                'Active classes: classes should not consist of only get/set methods and, in general, should minimize their use. ',
                'get methods should give away the minimal information possible',
                'set methods should validate data received',
                'Superclasses are their own class: thus should not contain instance variables or methods specific to only some subclasses']

    Flexibility_sub = [
                'DRY: no duplicated code, either exactly (from cutting and pasting), structurally (in flow of control or decisions), or in setup ("boilerplate" code)',
                'Declared types should be as general as possible (i.e., ArrayList should never be visible in your public interface)',
                'Single Purpose: keep classes, methods, and variables short and well named by giving them only one purpose',
                'Behavior Driven Design: give each class a purpose by focusing on the behavior (or services) it provides first, its state later',
                'Polymorphism: use subclassing to avoid "case-based code logic" (i.e., conditional chains or case statements on "type" information)']



    rules = {'squid:S1942' : ['communication',1],
'squid:S00115' : ['communication',1],
'squid:S1223' : ['communication',1],
'squid:S1190' : ['communication',1],
'squid:S1221' : ['communication',1],
'squid:S00101' : ['communication',1],
'squid:S1700' : ['communication',1],
'squid:S109' : ['communication', 2],
'squid:S00122': ['communicaion', 3],
'squid:S00121': ['communicaion', 3],
'squid:S2681': ['communicaion', 3],
'squid:S1941' : ['communicaion', 4],

    }

    def getRules (self, rule):
        return self.rules[rule]