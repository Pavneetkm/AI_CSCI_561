from __future__ import print_function
import numpy as np


class Main:
    def __init__(self):
        self.pospredicate = []
        self.predicateneg = []


varx = []
vary = []
issolvable = False
presentsolution = False
dictpredicate = {}
knowledgeb = []
resolutionsolving = []
knowledgebasenone = 0
rightanswer = False
answer = False
dict = []


def startsolving(info, N):
    global dictpredicate
    global knowledgeb
    global resolutionsolving
    global knowledgebasenone
    global rightanswer
    global answer

    blocks = info.split('|')

    for data in blocks:
        data = data.rstrip(' ')
        data = data.lstrip(' ')
        newdata = data.lstrip('~')
        data_new = newdata.split('(')
        sdata = data.split('(')
        newdata = data_new[0]
        data = sdata[0]

        if not dictpredicate.has_key(newdata):
            dictpredicate[newdata] = Main()

            if data != newdata:
                str = dictpredicate.get(newdata)
                str.predicateneg.append(N)
                dictpredicate[newdata] = str

        if not dictpredicate.has_key(newdata):
            dictpredicate[newdata] = Main()

            if data == newdata:
                str = dictpredicate.get(data)
                str.pospredicate.append(N)
                dictpredicate[data] = str

        else:

            if data != newdata:
                str = dictpredicate.get(newdata)
                str.predicateneg.append(N)
                dictpredicate[newdata] = str

            if data==newdata:
                str = dictpredicate.get(data)
                str.pospredicate.append(N)
                dictpredicate[data] = str


def evaluation(info):
    global dictpredicate
    global knowledgeb
    global resolutionsolving
    global knowledgebasenone
    global rightanswer
    global answer

    info = info.strip('\n')
    data = info.strip('')
    newdata = info.lstrip('~')

    while newdata == data:
        newdata = '~' + newdata
    value = answerstandard(newdata, len(knowledgeb))

    knowledgeb.append(value)

    already = np.zeros(len(knowledgeb), dtype=bool)
    i = len(knowledgeb) - 1

    x = knowledgeb[i]
    ans = binary(x, already)
    return ans


def getupdate(newdata):
    newdata = newdata.strip(' ')
    data = newdata.split('(')
    return data[0]


def binary(x, already):
    global dictpredicate
    global knowledgeb
    global resolutionsolving
    global knowledgebasenone
    global rightanswer
    global answer

    while rightanswer == True:
        return answer

    newx = x.split('|')

    for data in newx:
        data = data.strip(' ')
        newdata = data.lstrip('~')

        if newdata != data:
            functioninfo = getupdate(newdata)

            if dictpredicate.has_key(functioninfo):

                info = dictpredicate.get(functioninfo)

                abc = info.pospredicate
                for clause in abc:
                    if already[clause] == True:
                        continue
                    already[clause] = True
                    combination = allinone(clause, x, already)

                    if combination[0] == True:
                        if combination[1] == '':
                            rightanswer = True
                            answer = True
                            return True

                        resolutionsolving.append(knowledgeb)

                        if binary(combination[1], already):
                            return True
                    already[clause] = False

        else:

            functioninfo = getupdate(newdata)
            if dictpredicate.has_key(functioninfo):
                info = dictpredicate.get(functioninfo)
                ghi = info.predicateneg
                for clause in ghi:
                    if already[clause] == True:
                        continue
                    already[clause] = True
                    combination = allinone(clause, x, already)
                    if combination[0] == True:
                        if combination[1] == '':
                            rightanswer = True
                            answer = True
                            return True

                        resolutionsolving.append(knowledgeb)
                        if binary(combination[1], already):
                            return True
                    already[clause] = False
    return False


def find_functions(data):
    data = data.strip(' ')
    blocks = data.split('|')
    finddict = []
    for str in blocks:
        values = getupdate(str)
        finddict.append(values)
    return finddict


def negative(function):
    new = function.lstrip('~')
    while new == function:
        a = '~'
        string = a + function
        return string
    return new


def allinone(clause_no, clause, visited):
    global dictpredicate
    global knowledgeb
    global resolutionsolving
    global knowledgebasenone
    global rightanswer
    global answer

    data1 = knowledgeb[clause_no]

    info1 = find_functions(data1)
    info2 = find_functions(clause)

    for info in info2:

        index2 = info2.index(info)
        newinfo = negative(info2[index2])

        while newinfo in info1:

            index1 = info1.index(newinfo)
            result = changedata(data1, clause, index1, index2)

            if result[0] != False:
                return (True, result[1])

            else:
                return (False, " ")


def changedata(info1, info2, index1, index2):
    global dictpredicate
    global knowledgeb
    global resolutionsolving
    global knowledgebasenone
    global rightanswer
    global answer

    query1 = info1.strip(' ')
    p1 = query1.split('|')


    query2 = info2.strip(' ')
    p2 = query2.split('|')

    result = unification(p1[index1], p2[index2])

    if result[0] == False:
        return ('False', " ")

    finalstr = ' '

    if result[1] == True:
        finalstr = getupdate(p1[index1])
        finalstr = finalstr.lstrip('~')
    newstring = ''
    counter = 0

    for part in p1:
        newstr = getupdate(part)
        final = newstr.lstrip('~')

        if counter == index1:
            counter = counter + 1
            continue

        counter = counter + 1

        a = newstr
        b = '('
        newstring = newstring + a + b

        blocks = collectarguments(part)
        count = 0
        for data in blocks:
            if result[2].has_key(data):
                v = result[2][data]
                blocks[count] = v
            count = count + 1

        c = ",".join(blocks)
        d = ")|"
        newstring = newstring + c + d

    counter = 0
    for part in p2:
        newstr = getupdate(part)
        final = newstr.lstrip('~')

        if counter == index2:
            counter = counter + 1
            continue
        counter = counter + 1

        a = newstr
        b = '('
        newstring = newstring + a + b
        blocks = collectarguments(part)
        count = 0
        for data in blocks:
            if result[2].has_key(data):
                v = result[2][data]
                blocks[count] = v
            count = count + 1

        c = ",".join(blocks)
        d = ")|"
        newstring = newstring + c + d
    newstring = newstring.rstrip('|')

    newstring = similarity(newstring)
    return (True, newstring)


def similarity(query):
    global dictpredicate
    global knowledgeb
    global resolutionsolving
    global knowledgebasenone
    global rightanswer
    global answer
    global dict

    fns = find_functions(query)
    blocks = query.split('|')

    for i in range(0, len(fns)):
        for j in range(i + 1, len(fns)):
            if fns[i] == fns[j]:
                flag = True
                args1 = collectarguments(blocks[i])
                args2 = collectarguments(blocks[j])
                for k in range(0, len(args1)):
                    if args1[k] != args2[k]:
                        flag = False
                        break
                if flag == True:
                    dict.append(i)

    checkforcondition(dict, blocks, query)

    n_query = ''
    abc = "|".join(blocks)
    n_query = n_query + abc
    return n_query


def checkforcondition(dict, blocks, query):
    if len(dict) != 0:
        dict.sort(reverse=True)

        for x in dict:
            blocks.pop(x)
    else:
        return query


def deletedata(s1, s2):
    function1 = getupdate(s1)
    function2 = getupdate(s2)
    if function1 != function2:
        return True
    else:
        return False


def collectarguments(data):
    data = data.strip(' ')
    data = data.rstrip('\n')
    data = data.strip(')')
    query = data.split('(')
    abc = query[1]
    argument = abc.split(',')
    return argument


def varibleq(query):
    query = query.strip(' ')
    if not query[0].isupper():
        return True
    else:
        return False
    return True


def unification(s1, s2):
    s1 = s1.strip(' ')
    s2 = s2.strip(' ')
    p1 = collectarguments(s1)
    p2 = collectarguments(s2)
    dictionary = {}

    if len(p1) == len(p2):
        for i in range(len(p1)):
            if (not varibleq(p2[i])) and varibleq(p1[i]):
                dictionary[p1[i]] = p2[i]
            elif varibleq(p2[i]) and (not varibleq(p1[i])):
                dictionary[p2[i]] = p1[i]

            elif varibleq(p2[i]) and varibleq(p1[i]):
                dictionary[p1[i]] = p2[i]

            else:
                if p1[i] != p2[i]:
                    return (False, False, dictionary)
    else:
        print('-------404-------')

    return (True, deletedata(s1, s2), dictionary)


def removeall(solution):
    global knowledgeb
    global resolutionsolving
    global rightanswer
    rightanswer = False
    resolutionsolving[:] = []
    knowledgeb.pop()


def answerstandard(given, i):
    global dictpredicate
    global knowledgeb
    global resolutionsolving
    global knowledgebasenone
    global rightanswer
    global answer

    blocks = given.split('|')
    result1 = ''
    for div in blocks:
        full = getupdate(div)
        result1 = result1 + full + '('
        arguments = collectarguments(div)
        for p in arguments:
            if varibleq(p):
                p = p + str(i)
            result1 = result1 + p + ','
        result1 = result1.rstrip(',')
        result1 = result1 + ')'
        result1 = result1 + '|'

    result1 = result1.rstrip('|')
    return result1


def printoutput(solution):
    fout = open('output.txt', 'w')
    final = ''

    for s in solution:
        abc = str(s).upper()
        a = '\n'
        final = final + abc + a
    fout.write(final)
    fout.close


if __name__ == '__main__':
    given = []
    solution = []

    with open("input.txt", 'r') as funct:
        number = funct.readline()
        num = number.rstrip()
        N = (int)(num)

        for i in range(0, N):
            querynum = funct.readline()
            value = querynum.rstrip()
            given.append(value)

        linekb = funct.readline()
        kb_no = linekb.rstrip()

        knowledgebasenone = (int)(kb_no)

        for i in range(0, knowledgebasenone):
            base = funct.readline()
            value = base.strip(' ')
            value = answerstandard(value, i)
            knowledgeb.append(value)

            startsolving(value, i)

    for i in range(0, N):
        solution.append(evaluation(given[i]))
        removeall(solution)

    printoutput(solution)
