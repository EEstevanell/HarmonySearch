import random
import sys
import numpy as np
from grammar import *

def RPNI(MPT):
    m = MPT.clone()
    order = MPT.preorder()
    listp = order.copy()
    listp.pop(0)
    q = listp.pop(0)
    result = []
    itera = 0
    while (listp):
        m.order = order
        for i in range(len(order)):
            p = order[i]
            ip = order.index(p)
            iq = order.index(q)
            if (ip < iq):
                result = MoorePrefixTree.det_merge(m,p,q)
                if (MoorePrefixTree.equal(result,m) == False):
                    m = result
                    break
            else:
                break              
        for state in m.merges:
            order.remove(state)
            if(state != q and state != 0):
                listp.remove(state)
            pass
        if(listp):
            q = listp.pop(0)
        m.garbage += m.merges
        itera+=1
    return m

vocabulary = ['a','b','c']

class MoorePrefixTree():
    def check_sample(self,sample):
        state = 0
        for ichar in range(len(sample)):
            char = sample[ichar]
            i = 0
            for i in range(len(self.E)):
                if (char == self.E[i]):
                    break
            if (ichar == len(sample) - 1):
                r = True if self.F[state] == 1 else False
                return r
            if (self.f[i][state]):
                state = self.f[i][state][0]
            else:
                r = True if self.negative_count > self.positive_count else False
                return r          
    def preorder(self,begining = 0):
        list1 = []
        state = begining
        list1.append(state)
        for char in range(len(self.E)):
            if (self.f[char][state]):
                list1 += self.preorder(self.f[char][state][0])        
        return list1
    def clone(self):
        """
        creates a shallow copy of the Moore Prefix Tree
        """
        Mc = MoorePrefixTree(self.E)
        Mc.Q = self.Q
        for i in range(len(self.E)):
            Mc.f[i].pop()
        
        Mc.F = []
        for i in range(self.Q):
            Mc.F.append(self.F[i])
        
        j = 0 
        for column in self.f:
            for i in range(self.Q):
                Mc.f[j].append(self.f[j][i].copy())
            j+=1
        
        for item in self.garbage:
            Mc.garbage.append(item)
        return Mc
    def add_state(self):
        """
        add a new row to the transition function matrix and add a new item in the
        return function (initialized in 0, the insert function handles the value 
        of the return function).
        """
        self.Q+=1
        self.F.append(0)
        for column in self.f:
            column.append([])
        return
    def remove_state(self,state):
        """
        use it!
        """
        self.Q -= 1
        for column in self.f:
            column.pop(state)
            for i in range(self.Q-1):
                for j in range(len(column[i])):
                    if(column[i][j] == state):
                        column[i].pop(j)
                    else:
                        if(column[i][j] > state):
                            column[i][j] -= 1
                
        self.F.pop(state)
        return
    def insert(self,sample,state = 0,position = 0):
        """
        sample: tuple of 2 elements, sample[0] represents a string while sample[1] represents a boolean.
        state:(default = 0) current state of the Moore Machine where is ocurring insertion
        position:(default = 0) current position of the sample' string, represents a char
        add new values to transition function matrix and creates required states calling add_state
        """
        if (position == len(sample[0])):
            self.F[state] = 1 if sample[1] else 2
            return

        string = sample[0]
        char = string[position]
        index_char = self.E.index(char)
        
        if (self.f[index_char][state]):
            state = self.f[index_char][state][0]
            position+=1
            return self.insert(sample,state,position)
        else:
            new_state = self.Q
            self.f[index_char][state].append(new_state)
            self.add_state()
            position+=1
            return self.insert(sample,new_state,position)
        return
    def __init__(self,vocabulary,samples = [],):
        """
        samples: list of tuples of 2 elements each, the first represents a string and the second a boolean.
        creates a 6-tuple [ Q, E, B, f, initial, F] that represents a Moore Prefix Tree given a set of samples\n
        Q:-> set of states\n
        E:-> in-alphabet\n
        B:-> out-alphabet\n
        f:-> transition function\n
        initial:-> initial state (always equals 0)\n
        F:-> return function\n
        """
        self.initial = 0
        self.Q = 0
        self.E = vocabulary
        self.B = (0,1,2)
        self.f = []
        self.F = []
        self.merges = []
        self.garbage = []
        self.order = []
        self.negative_count = 0
        self.positive_count = 0

        for char in self.E:
            self.f.append([])
        self.add_state()

        for sample in samples:
            self.insert(sample)
        return
    @staticmethod
    def equal(M1,M2):
        if (M1.Q != M2.Q):
            return False

        for c in range(len(M1.f)):
            for r in range(M1.Q):
                if(len(M1.f[c][r]) == len(M2.f[c][r])):
                    for s in range(len(M1.f[c][r])):
                        if(M1.f[c][r][s] != M2.f[c][r][s]):
                            return False
                else:
                    return False

        for i in range(len(M1.F)):
            if (M1.F[i] != M2.F[i]):
                return False
        return True
    @staticmethod
    def merge_tree(M,p,q):  
        """
        merge_tree -> list(iterable)
        """
        list1 = []
        list2 = [(p,q)]
        while (list2):
            tup = list2.pop(0)
            list1 = list1 + [tup] if list1.count(tup) == 0 else list1
            for char in range(len(M.E)):
                if (M.f[char][tup[0]] and M.f[char][tup[1]]):
                    new_tup = (M.f[char][tup[0]][0],M.f[char][tup[1]][0])
                    list2 = list2 + [new_tup] if list2.count(new_tup) == 0 else list2
        return list1
    @staticmethod
    def merge(M,p,q):
        """
        merge -> MoorePrefixTree(object)
        M : Moore Machine where
        p : nodo q del arbol que va a participar en el merge (gana referencias)
        q : nodo q del arbol que va a participar en el merge (pierde referencias)
        p << q (lexicographically)
        """
        if (M.F[p] + M.F[q] == 3):
            return M
        M.F[p] = M.F[q] if M.F[p] == 0 else M.F[p]
        M.F[q] = 0

        for column in M.f:
            for r in column:
                if (r.count(q)>0):
                    r.remove(q)
                    if (r.count(p) == 0):
                        r.append(p)
            for ref in column[q]:
                if (column[p].count(ref) == 0):
                    column[p].append(ref)
                    column[q].remove(ref)
                else:
                    column[q].remove(ref)
        #M.remove_state(q)
        return M
    @staticmethod
    def det_merge(M,p,q):
        """
        det_merge -> MoorePrefixTree(object).
        Returns a DFA if the merge was satisfactory (if all non deterministic cases where resolved)
        else returns M.
        M: Moore Prefix tree where the merge is going to happend
        p: state of M (p << q)(lexicografically)
        q: state of M (p << q)(lexicografically)
        """
        merge = []
        M.merges = []

        for state in range(M.Q):
            merge.append(state)

        Mc = M.clone()
        list1 = [(p,q)]
        while (list1):
            tup = list1.pop(0)
            M1 = Mc.clone()
            if (M.order.index(tup[0]) < M.order.index(tup[1])):
                MoorePrefixTree.merge(M1,tup[0],tup[1])
            merge[tup[1]] = tup[0];
            if MoorePrefixTree.equal(M1,Mc):
                return M
            else:
                for char in range(len(M.E)):
                    if (Mc.f[char][tup[0]] and Mc.f[char][tup[1]]):
                        list1.append((merge[Mc.f[char][tup[0]][0]],merge[Mc.f[char][tup[1]][0]]))  
                Mc = M1

        i = len(merge) - 1
        merge.reverse();
        for state in merge:
            if(state != i):                
                #Mc.remove_state(i)
                Mc.merges.append(i)
            i-=1
        
        return Mc
    @staticmethod
    def consistent(MPT,samples):
        """
        consistent -> bool
        return True if the samples where consistent in the Moore Tree (each positive sample was
        recogniced and each negative sample was rejected).
        Requirements:
        MPT: Moore Prefix Tree.
        samples: list of samples formed by two elements, the first one is the sample's string and the second the identifier of recognition.
        """
        for sample_c in samples:
            state = 0;
            sample = sample_c[0];
            recogniced = 1 if sample_c[1] == True else 2;
            for ichar in range(len(sample)):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
                i = 0;
                char = sample[ichar];
                for i in range(len(MPT.E)):
                    if (MPT.E[i] == char):
                        break
                if (MPT.f[i][state]):
                    state = MPT.f[i][state][0]
                else:
                    return False

                if (ichar == len(sample)-1):
                    if (MPT.F[state] != recogniced):
                        return False                        
        return True;

class Alice:
    def get_limit_query(self):
        for k in range(30):
            if (self.N >= len(self.alphabet)**k):
                pass
            else:
                self.limit = k-1
                return
    def build_query_set_k(self,limit,symbols = [],i = 0):
        if (i == limit):
            self.pendient_questions.append("".join(symbols))
            return
        if (i == 0):
            symbols= [0 for k in range(limit)]

        for char in self.alphabet:
            symbols[i] = char
            i+=1
            self.build_query_set_k(limit,symbols,i)
            i-=1
        pass
    def init(self):
        for char in self.alphabet:
            vocabulary.append(char)  
        self.MPT = MoorePrefixTree(self.alphabet)
        self.pendient_questions = []
        self.first = True
        self.limit = 0
        pass
    def ready(self):
        self.MPT = RPNI(self.MPT)
        b = MoorePrefixTree.consistent(self.MPT,self.sample_set)
        if (b == False):
            print("Not consistent merges, aborting")
        pass
    def ask(self, i):
        if (self.pendient_questions):
            return self.pendient_questions.pop(0)
        else:
            if self.limit > 10:
                self.limit = 1
            self.limit += 1
            self.build_query_set_k(self.limit)
            if (self.pendient_questions):
                return self.pendient_questions.pop(0)
    def learn(self, i, question, response):
        sample = [question,response]
        self.sample_set.append(sample)
        self.MPT.insert(sample)
        pass
    def answer(self, i, question):
        return self.MPT.check_sample(question)
    def run(self, language):
        self.sample_set = []
        # Read the size of the language
        self.N = 100
        # Read the alfabet
        self.alphabet = "abc"
        # Call init
        self.init()
        self.bob = Bob(language)

        for i in range(self.N):
            # Build a random string of symbols
            question = self.ask(i)

            # Print and store the response
            # print(question)
            # sys.stdout.flush()

            answer = self.bob.check(question)

            # Check the answer is OK
            # assert answer in ['yes', 'no']

            # Call learn
            self.learn(i, question, answer)

        self.ready()

        # Asnwer the N responses
        accepted = 0
        for i in range(self.N):
            question = self.bob.generate_q()

            # Is Bob cheating ?
            assert all(symbol in self.alphabet for symbol in question)

            # Compute the answer
            answer = self.answer(i, question)

            accepted += 1 if answer == self.bob.should_be else 0

        return accepted
            # Print
            # print('yes' if answer else 'no')
            # sys.stdout.flush()#Python

class Bob():
    def check(self,w):
        response = self.rg.test(w)
        # print("--> %s \n" % response)
        return response
    def __init__(self, language:RegularGrammar):
        self.rg = language
        # self.rg = RegularGrammar(S="aA bB cC", A="aA bB cC", B="bB cC", C="cC c")
        pass
    def generate_q(self):
        lpength = random.randint(1, 10)
        symbols = [random.choice(['a','b','c']) for k in range(lpength)]
        ch = "".join(symbols)
        self.should_be = True if self.rg.test(ch) else False
        # print(ch + " \n")
        return ch

# a = Alice()
# a.run()

def score(*args):
    resuts = [Alice(*args).run(RegularGrammar(S="aS bS cS a b c")),
              Alice(*args).run(RegularGrammar(S="aO bE b", O="bO aE a", E="aO bE b")),
              Alice(*args).run(RegularGrammar(S="aU a", U="aU bU cU a b c")),
              Alice(*args).run(RegularGrammar(S="aA bS cS b c a",A = "aX bS cS a b c", X="bS cS b c")),
              Alice(*args).run(RegularGrammar(S="aS a"))]
    return resuts
def get_mean_score(*args):
    scores = score(*args)
    return sum(scores)/len(scores)
def get_best_score(*args):
    best = 0
    for run in score(*args):
        if run > best:
            best = run
    return best
def get_dominancy_score(*args):
    pass


if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     print("usage: ./GIG-incremental.py <mutation rate/r> <crossover rate/r> <generations amount/z> <population size/z>")
    #     print("usage: ./GIG-incremental.py -d")
    #     exit()
    
    # if sys.argv[1] == "-d" and len(sys.argv) < 3:
    #     default = True
    #     print(get_mean_score())

    # if len(sys.argv) < 5:
    #     print("usage: ./GIG-incremental.py <mutation rate/r> <crossover rate/r> <generations amount/z> <population size/z>")
    #     print("usage: ./GIG-incremental.py -d")
    #     exit()
    print(get_mean_score())
    