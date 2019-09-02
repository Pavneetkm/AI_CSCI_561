from __future__ import print_function
from copy import deepcopy

f = open('input.txt', 'r')
N = f.readline()
N = ''.join(c for c in N if c not in '\n ''')
N = int(N)
Q = []
for i in range(N):
    q = f.readline()
    q = ''.join(c for c in q if c not in '\n ''')
    Q.append(q)
KBBB = f.readline()
KBBB = ''.join(c for c in KBBB if c not in '\n ''')
KBBB = int(KBBB)
kb = []

for i in range(KBBB):
    k = f.readline()
    k = ''.join(c for c in k if c not in '\n ''')
    kb.append(k)
class Node:
    def __init__(self, info):
        self.info = info
        self.left = None
        self.right = None
        self.level = None

    def __str__(self):
        return str(self.info)

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def top(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

    def get(self):
        return self.items

def brac(st, lent):
    st = list(st)

    for i in range(lent - 1):
        if st[i] == "(" and st[i + 1] == "(":
            st[i] = "( "
            st = "".join(st)
            l = len(st)
            st = brac(st, l)
        if st[i] == ")" and st[i + 1] == ")":
            st[i + 1] = " )"
            st = "".join(st)
            l = len(st)
            st = brac(st, l)
    st = "".join(st)
    return st

def op_space(st):
    if "|" in st:
        st=st.replace("|"," | ")
    return st

def final_spaces(st, le):
    st = list(st)
    for i in range(len(st)):
        if st[i] == "(" and st[i + 1].isalpha():
            for j in range(len(st)):
                if i + j < le:
                    if st[i + j] == ")":
                        st = "".join(st)
                        if "(" in st[i + 1:i + j]:
                            a = st[i + 1:i + j].count("(")
                            b = st[i + 1:i + j].count(")")
                            if a != b:
                                continue
                            else:
                                if "|" in st[i + 1:i + j]:
                                    st = list(st)
                                    st[i] = "( "
                                    if st[i + j - 1] != " ":
                                        st[i + j] = " )"
                                    break
                                if "`" in st[i + 1:i + j]:
                                    st = list(st)
                                    st[i] = "( "
                                    if st[i + j - 1] != " ":
                                        st[i + j] = " )"
                                    break
                                break
                                st = list(st)
                        else:
                            if "|" in st[i + 1:i + j]:
                                st = list(st)
                                st[i] = "( "
                                if st[i + j - 1] != " ":
                                    st[i + j] = " )"
                                break
                            if "`" in st[i + 1:i + j]:
                                st = list(st)
                                st[i] = "( "
                                if st[i + j - 1] != " ":
                                    st[i + j] = " )"
                                break
                            break
                            st = list(st)
        st = "".join(st)
        st = list(st)
    st = "".join(st)
    return st

def special_space(st, le):
    st = list(st)
    for i in range(le):
        if st[i] == "(" and st[i] in ["`", "|"]:
            for j in range(le):
                if i + j < len(st):
                    if st[i + j] == ")":
                        st = "".join(st)
                        if st[i + 4:i + j].isalpha():
                            st = list(st)
                            st[i + j] = " )"
                            break
                        break
        if st[i] == ")" and i  <= le:
            if st[i] in ["`", "|"]:
                for j in range(le):
                    if i + j < len(st):
                        if st[i + j] == ")":
                            st = "".join(st)
                            if st[i + 2:i + j].isalpha():
                                st = list(st)
                                st[i + j] = " )"
                                break
                            break
    st = "".join(st)
    return st

def notvar(st):
    q = st.count("~")
    for i in range(q):
        if "~" in st:
            st = st.replace("~","`", 1)
    st = "".join(st)
    return st

class BinaryTree:
    def __init__(self, rootObj):
        self.key = rootObj
        self.leftChild = None
        self.rightChild = None
        self.parent = None

    def insertRight(self, parent, newNode):
        tree = BinaryTree(newNode)
        tree.parent = parent
        if self.rightChild == None:
            self.rightChild = tree
        else:
            tree.rightChild = self.rightChild
            self.rightChild = tree

    def insertLeft(self, parent, newNode):
        tree = BinaryTree(newNode)
        tree.parent = parent
        if self.leftChild == None:
            self.leftChild = tree
        else:
            tree.leftChild = self.leftChild
            self.leftChild = tree

    def getRightChild(self):
        return self.rightChild

    def getLeftChild(self):
        return self.leftChild

    def setRootVal(self, obj):
        self.key = obj

    def getRootVal(self):
        return self.key

    def postorder(self):
        if self.leftChild:
            self.getLeftChild().postorder()
        if self.rightChild:
            self.getRightChild().postorder()

    def inorder(self):
        if self.leftChild:
            self.leftChild.inorder()
        if self.rightChild:
            self.rightChild.inorder()

def inorder(tree):
    if tree != None:
        inorder(tree.getLeftChild())
        inorder(tree.getRightChild())

def buildParseTree(fpexp):
    fplist = fpexp.split()
    pStack = Stack()
    eTree = BinaryTree('root')
    pStack.push(eTree)
    currentTree = eTree
    for i in fplist:
        if i == '(':
            currentTree.insertLeft(currentTree, 'LLL')
            pStack.push(currentTree)
            currentTree = currentTree.getLeftChild()
        elif i not in [')',"|", "`"]:
            currentTree.setRootVal(i)
            parent = pStack.pop()
            currentTree = parent
        elif i in [ "|", "`"]:
            currentTree.setRootVal(i)
            currentTree.insertRight(currentTree, 'RRR')
            pStack.push(currentTree)
            currentTree = currentTree.getRightChild()
        elif i == ')':
            currentTree = pStack.pop()
        else:
            raise ValueError
    return eTree

def fix_negation(tr):
    if tr != None:
        if tr.getRootVal() == "`":
            if tr.getLeftChild() != None:
                if tr.getLeftChild().getRootVal().isalnum() and tr.getRightChild() != None:
                    tr.leftChild = tr.getRightChild()
                    tr.rightChild = None
    if tr.getLeftChild() != None:
        tr.leftChild = fix_negation(tr.getLeftChild())
    if tr.getRightChild() != None:
        tr.rightChild = fix_negation(tr.getRightChild())
    return tr

def standardize(tr, a):
    standard = a
    if tr:
        if tr.getRootVal() not in ["|","`"]:
            p1 = tr.getRootVal().find("(")
            p2 = tr.getRootVal().find(")")
            while True:
                va = tr.getRootVal()
                if va[p1 + 1].islower():
                    va = va[:p2] + str(a) + va[p2:]
                    c = va.find(",")
                    if c == -1:
                        break
                    store = p1
                    for i in range(c, p2):
                        if va[i] == ",":
                            if va[store:i].islower():
                                store = i
                                va = va[:i] + str(a) + va[i:]
                break
            tr.setRootVal(va)
            return tr
    if tr.leftChild != None:
        tr.leftChild = standardize(tr.leftChild, a)
    if tr.rightChild != None:
        tr.rightChild = standardize(tr.rightChild, a)
    return tr

t = []
ntree = []
tre = []
for i in range(len(kb)):
    a = notvar(kb[i])
    s = brac(a, len(a))
    ss = op_space(s)
    t1 = final_spaces(ss, len(ss))
    t.append(special_space(t1, len(t1)))
    tre = buildParseTree(t[i])
    tre = fix_negation(tre)
    tre = standardize(tre, i + 1)
    ntree.append(tre)

newkb = []

def nkb(tr):
    if tr.getRootVal() != "&":
        newkb.append(tr)

def merge_negation(tr):
    if tr.getRootVal() == "`":
        if tr.getLeftChild() != None:
            a = tr.getLeftChild().getRootVal()
            a = a[:0] + "~" + a[0:]
            tr.setRootVal(a)
            tr.leftChild = None
    else:
        if tr.leftChild != None:
            tr.leftChild = merge_negation(tr.getLeftChild())
        if tr.rightChild != None:
            tr.rightChild = merge_negation(tr.getRightChild())
    return tr

for i in range(len(ntree)):
    nkb(ntree[i])

for i in range(len(newkb)):
    newkb[i] = merge_negation(newkb[i])

the_kb = []
def to_list(tr, l):
    if tr.getRootVal() == "|":
        if tr.getLeftChild() != None:
            if tr.getLeftChild().getRootVal() != "|":
                l.append(tr.getLeftChild().getRootVal())
            else:
                tr.leftChild = to_list(tr.getLeftChild(), l)
        if tr.getRightChild() != None:
            if tr.getRightChild().getRootVal() != "|":
                l.append(tr.getRightChild().getRootVal())
            else:
                tr.rightChild = to_list(tr.getRightChild(), l)
    else:
        l.append(tr.getRootVal())

    return l

for i in range(len(newkb)):
    l = []
    the_kb.append(to_list(newkb[i], l))

def unify_var(var, x):
    if var[0] in theta:
        return unify(theta[var[0]], x)
    elif x[0] in theta:
        return unify(var, theta[x[0]])
    else:
        theta[var[0]] = x[0]
        return theta

def unify(x, y):
    if x == y:
        return theta
    elif x[0][0].islower() and len(x) == 1:
        K = unify_var(x, y)
        return K
    elif y[0][0].islower() and len(y) == 1:
        return unify_var(y, x)
    elif len(x) > 1 and len(y) > 1 and type(x) == list and type(y) == list:
        X = x[0]
        Y = y[0]
        x.pop(0)
        y.pop(0)
        z = unify([X], [Y])
        return unify(x, y)
    else:
        return None

def check_clause(c1, c2):
    c1len = len(c1)
    c2len = len(c2)
    for i in range(c1len):
        for j in range(c2len):
            o1 = c1[i].find("(")
            o2 = c2[j].find("(")
            if o1 != o2:
                if o1 > o2:
                    if c1[i][1:o1] == c2[j][0:o2]:
                        return 1
                if o1 < o2:
                    if c1[i][0:o1] == c2[j][1:o2]:
                        return 1
    return 0

def unite(c1, c2, s1, s2):
    uni = []
    for i in range(len(c1)):
        if c1[i] != s1:
            uni.append(c1[i])
    for j in range(len(c2)):
        if c2[j] != s2:
            uni.append(c2[j])
    return uni

def substitution(uni, theta):
    for i in range(len(uni)):
        a = uni[i]
        o = a.find("(")
        c = a.find(")")
        if "," in a[o + 1:c]:
            p = a[o + 1:c].split(",")
            for j in range(len(p)):
                if theta is not None:
                    if p[j] in theta:
                        p[j] = theta[p[j]]
            p = ",".join(p)
        else:
            p = a[o + 1:c]
            if theta is not None:
                if p in theta:
                    p = theta[p]
            p = "".join(p)
        a = a[:o + 1] + p + a[c:]
        uni[i] = a
    return uni

standard = KBBB

def standardized(uni1, standard):
    flag = 0
    for i in range(len(uni1)):
        o = uni1[i].find("(")
        c = uni1[i].find(")")
        if o and c == -1:
            return uni1
        for j in range(o, c):
            flag = 0
            if uni1[i][j] == ",":
                flag = 2
                if uni1[i][o + 1].islower():
                    uni1[i] = list(uni1[i])
                    uni1[i][o + 2] = str(standard)
                    uni1[i] = "".join(uni1[i])
                    o = j
                    flag = 1
                if flag == 2:
                    o = j
        if uni1[i][o + 1].islower():
            uni1[i] = list(uni1[i])
            uni1[i][o + 2] = str(standard)
            uni1[i] = "".join(uni1[i])
            flag = 1
    if flag == 1:
        standard = standard + 1
    return uni1

def check_diff(m, the_kb):
    r = deepcopy(m)
    for i in range(len(r)):
        if r[i][0] == "~":
            r[i] = r[i][1:]
        else:
            r[i] = r[i][:0] + "~" + r[i][0:]
    for i in range(len(r)):
        for j in range(len(the_kb)):
            if r[i] in the_kb[j][0]:
                return 1
    return 0


def resolve(c1, c2, theta):
    o1 = len(c1)
    o2 = len(c2)
    temp_kb = []
    for i in range(o2):
        for j in range(o1):
            s1 = c1[j]
            s2 = c2[i]
            p1 = []
            p2 = []
            os1 = s1.find("(")
            os2 = s2.find("(")
            if s1[0:os1] == s2[1:os2] or s1[1:os1] == s2[0:os2]:
                cs1 = s1.find(")")
                cs2 = s2.find(")")
                if "," in s1[os1 + 1:cs1]:
                    p1 = s1[os1 + 1:cs1].split(",")
                else:
                    p1.append(s1[os1 + 1:cs1])
                if "," in s2[os2 + 1:cs2]:
                    p2 = s2[os2 + 1:cs2].split(",")
                else:
                    p2.append(s2[os2 + 1:cs2])
                S = unify(p1, p2)
                if S == None:
                    return -1
                uni = unite(c1, c2, s1, s2)
                if uni == []:
                    tempkb = [[]]
                    return tempkb
                uni1 = substitution(uni, theta)
                element = standardized(uni1, standard)
                temp_kb.append(element)
    return temp_kb

def resolution(kb, q):
    KB = []
    if q[0] == "~":
        q = q[1:]
    else:
        q = q[:0] + "~" + q[0:]
    KB.append([q])
    kk = 0
    global theta
    theta = {}
    for i in range(50000):
        if len(KB) <= kk:
            return 0
        nq = KB[kk]
        kk = kk + 1
        length = len(kb)
        for j in range(length):
            a = kb[j]
            c = check_clause(a, nq)
            if c == 1:
                r = resolve(a, nq, theta)
                if r == [[]]:
                    return 1
                if r != -1:
                    for k in range(len(r)):
                        if check_diff(r[k], the_kb) == 1:
                            return 1
                        if (r[k] not in kb) and (r[k] not in KB):
                            KB.append(r[k])
    return 0

answer = []
for i in range(len(Q)):
    res = resolution(the_kb, Q[i])
    if res == 1:
        answer.append("TRUE")
        the_kb.append([Q[i]])
    else:
        answer.append("FALSE")

f = open("output.txt", 'w')
for j in range(len(answer)):
    f.write(answer[j])
    f.write("\n")
f.close()