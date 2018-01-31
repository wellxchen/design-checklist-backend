import re

class utility ():
    def makeMap(rules, main, sub):
        res = ""
        for rule in rules:
            if sub > 0:
                res = res + "'" + rule + "' : ['" + main + "'," + str(sub) + "],\n"
            else:
                res = res + "'" + rule + "': ['" + main + "'],\n"

        return res

    def striphtml(self, data):
        p = re.compile(r'<.*?>')
        p = p.sub('', data)
        p = p.replace('&lt;', '<')
        p = p.replace('&gt;', '>')
        p = p.replace('&le;', '<=')
        p = p.replace('&ge;', '>=')
        return p