
def makeMap(rules, main, sub):
    res = ""
    for rule in rules:
        if sub > 0:
            res = res + "'" + rule + "' : ['" +main+ "',"+ str(sub) + "],\n"
        else:
            res = res +  "'" + rule + "': ['" +main+ "'],\n"


    return res


rules = {'squid:S00115', 'squid:S1190', 'squid:S00101', 'squid:S1942', 'squid:S1221', 'squid:S1700', 'squid:S1223'}

print makeMap(rules, "communication", 1)