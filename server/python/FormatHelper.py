import re



class FormatHelper ():
    # strip method name
    def stripmethodname(self, line):
        index = line.find('(')

        if line[index - 1] == ' ':
            index -= 2
        else:
            index -= 1
        i = index
        while i >= 0:
            if line[i] == ' ':
                i += 1
                break
            i -= 1
        return line[i + 5:index - 6]

    # strip html code
    def striphtml(self, data):
        p = re.compile(r'<.*?>')
        p = p.sub('', data)
        p = p.replace('&lt;', '<')
        p = p.replace('&gt;', '>')
        p = p.replace('&le;', '<=')
        p = p.replace('&ge;', '>=')
        return p

    def getDateFromTuple(self, tuple):
        return datetime.datetime.strptime(tuple, "%Y %b %d")

    def getFullPath(self, prefix, suffixes):
        res = {}
        for suffix in suffixes:
            if suffix[-4:] == ".git":
                continue
            if prefix == ".":
                res[suffix] = []
                continue
            res[prefix + "/" + suffix] = []
        return res

    def makeMap(self, rules, main, sub):
        res = ""
        for rule in rules:
            if sub > 0:
                res = res + "'" + rule + "' : ['" + main + "'," + str(sub) + "],\n"
            else:
                res = res + "'" + rule + "': ['" + main + "'],\n"

        return res