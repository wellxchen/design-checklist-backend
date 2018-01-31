
def makeMap(rules, main, sub):
    res = ""
    for rule in rules:
        if sub > 0:
            res = res + "'" + rule + "' : ['" +main+ "',"+ str(sub) + "],\n"
        else:
            res = res +  "'" + rule + "': ['" +main+ "'],\n"


    return res


rules = {'squid:S2189', 'squid:S2252', 'squid:S2251', 'squid:S1994', 'squid:S1862', 'squid:S134', 'squid:S1905', 'squid:ForLoopCounterChangedCheck', 'squid:IndentationCheck', 'squid:S1226'}

print makeMap(rules, "codesmell", 0)