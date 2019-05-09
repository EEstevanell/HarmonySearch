import sys
import subprocess
import random
import winsound

from grammar import Language

class Bob:
    """
    Our adversary Bob connects to Alice and handles
    all the gaming.
    """
    def __init__(self, alice, runs, tests = False, *languages):
        self.alice = alice
        self.languages = list(languages)
        self.rnd = random.Random()
        self.runs = runs

        if tests:
            self.tests = tests
            self.has_to_save = False
        else: 
            self.tests = {}
            self.has_to_save = True
            for lan in self.languages:
                self.tests[repr(lan)] = []

    def run(self):
        runs = 0
        total_accuracy = 0

        results = []

        for l in self.languages:
            actual_accuracy = 0
            for r in range(self.runs):
                accuracy = self._run_once(l)
                total_accuracy += accuracy
                actual_accuracy += accuracy
                runs += 1
            results.append((l, actual_accuracy/self.runs))
            print("")

        print("----")

        for l,v in results:
            print("%s ==> %.2f %%" % (l, 100 * v))

        finale = "----\nTOTAL: %.2f %% accuracy achieved with %s" % ((100 * total_accuracy / runs), self.alice)
        print(finale)
        
        winsound.MessageBeep()
        return (results,self.tests,finale)

    def _run_once(self, language):
        print("Using language: %s" % repr(language))

        alice = subprocess.Popen(self.alice, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=0)
        print("Connected to Alice")

        right = 0
        N = language.size
        alphabet = language.alphabet

        alice.stdin.write(('%i\n' % N).encode('utf8'))
        alice.stdin.write(('%s\n' % alphabet).encode('utf8'))
        alice.stdin.flush()

        for i in range(N):
            question = alice.stdout.readline().strip().decode('utf8')
            answer = 'yes' if language.test(question) else 'no'

            print("Got: `%s` ==> `%s`" % (question, answer))
            alice.stdin.write(('%s\n' % answer).encode('utf8'))
            alice.stdin.flush()

        for i in range(N):
            length = self.rnd.randint(1, 10)

            if self.rnd.uniform(0, 1) > 0.5:
                question = "".join(self.rnd.choice(alphabet) for i in range(length))
            else:
                question = language.generate(self.rnd, length)
                
            if self.has_to_save:
                self.tests[repr(language)].append((question))
            else:
                question = self.tests[repr(language)][i]

            expected_answer = 'yes' if language.test(question) else 'no'
            alice.stdin.write(('%s\n' % question).encode('utf8'))
            alice.stdin.flush()

            answer = alice.stdout.readline().strip().decode('utf8')

            print("Asked: `%s` ==> `%s` vs `%s`" % (question, answer, expected_answer))

            if answer == expected_answer:
                right += 1

        return right * 1.0 / N

def main():
    a = open("test.txt",mode = 'w')

    results1 = Bob(sys.argv[1:], 5,False,
        Language("Universe", 100, "abc", S="aS bS cS a b c"),
        Language("Even number of a's", 100, "ab", S="aO bE b", O="bO aE a", E="aO bE b"),
        Language("Starts with a", 100, "abc", S="aU a", U="aU bU cU a b c"),
        Language("One A and One B", 100, "abc", S="cS aA bB", A="cA bT b", B="cB aT a", T="cT c"),
        Language("a*b*c*", 100, "abc", S="aA bB cC", A="aA bB cC", B="bB cC", C="cC c"),
        Language("a*|b*|c*", 100, "abc", S="aA bB cC", A="aA a", B="bB b", C="cC c"),
        Language("a+", 100, "abc", S="aS a"),
        Language("(ab*)", 100, "abc", S="aX aB",B="b",X = "bS"),
        Language("No more than two consecutive a's", 100, "abc", S="aA bS cS b c a",A = "aX bS cS a b c", X="bS cS b c"),
    ).run()

    results2 = Bob("python GIG.py", 5,results1[1],
        Language("Universe", 100, "abc", S="aS bS cS a b c"),
        Language("Even number of a's", 100, "ab", S="aO bE b", O="bO aE a", E="aO bE b"),
        Language("Starts with a", 100, "abc", S="aU a", U="aU bU cU a b c"),
        Language("One A and One B", 100, "abc", S="cS aA bB", A="cA bT b", B="cB aT a", T="cT c"),
        Language("a*b*c*", 100, "abc", S="aA bB cC", A="aA bB cC", B="bB cC", C="cC c"),
        Language("a*|b*|c*", 100, "abc", S="aA bB cC", A="aA a", B="bB b", C="cC c"),
        Language("a+", 100, "abc", S="aS a"),
        Language("(ab*)", 100, "abc", S="aX aB",B="b",X = "bS"),
        Language("No more than two consecutive a's", 100, "abc", S="aA bS cS b c a",A = "aX bS cS a b c", X="bS cS b c"),
    ).run()

    results3 = Bob("python GIG-incremental.py", 5,results2[1],
        Language("Universe", 100, "abc", S="aS bS cS a b c"),
        Language("Even number of a's", 100, "ab", S="aO bE b", O="bO aE a", E="aO bE b"),
        Language("Starts with a", 100, "abc", S="aU a", U="aU bU cU a b c"),
        Language("One A and One B", 100, "abc", S="cS aA bB", A="cA bT b", B="cB aT a", T="cT c"),
        Language("a*b*c*", 100, "abc", S="aA bB cC", A="aA bB cC", B="bB cC", C="cC c"),
        Language("a*|b*|c*", 100, "abc", S="aA bB cC", A="aA a", B="bB b", C="cC c"),
        Language("a+", 100, "abc", S="aS a"),
        Language("(ab*)", 100, "abc", S="aX aB",B="b",X = "bS"),
        Language("No more than two consecutive a's", 100, "abc", S="aA bS cS b c a",A = "aX bS cS a b c", X="bS cS b c"),
    ).run()

    for i in range(len(results1[0])):
        l,v = results1[0][i]
        l2,v2 = results2[0][i]
        l3,v3 = results3[0][i]
        print("%s ==> %.2f %% (RPNI) VS (GIG) %s ==> %.2f %% (GIG) VS (GIG-inc)  %s ==> %.2f %%" % (l, 100 * v,l2,100 * v2,l3,100 * v3),file = a)
    
    print(results1[2],file = a)
    print(results2[2],file = a)
    print(results3[2],file = a)
    

if __name__ == '__main__':
    main()