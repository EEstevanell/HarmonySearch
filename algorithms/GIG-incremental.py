import sys
from grammar import *
import re

class Individual:
    total_amount = 1
    total_generations = 1

    @staticmethod
    def reset():
        Individual.total_amount = 1
        Individual.total_generations = 1

    @staticmethod
    def new_generation():
        Individual.total_generations+=1
        pass
    def clone(self):
        return Individual(self.chromosomes.copy(),ev = self.evaluation,copy = self.id)
    def __init__(self,chromosomes,ev = 0,copy = 0):
        self.chromosomes = chromosomes
        self.evaluation = ev
        self.ng_accepted = 0
        self.copy = copy
        self.mutated = False
        self.generation = Individual.total_generations
        self.id = Individual.total_amount
        Individual.total_amount += 1
    def __str__(self):
        return str(self.id)
    def __repr__(self):  
        ret = "Individual(%d)" % self.id + " - gen(%d)" % self.generation
        if self.copy > 0:
            ret += "-gen(%d)" % self.generation
        if self.mutated:
            ret += "-mutated"
        return ret

class MCA:
    def clone(self):
        m = MCA(self.E)
        m.Q = self.Q
        for ic in range(len(self.E)):
            for r in range(self.Q):
                if r == 0:
                    m.f[ic][r] = self.f[ic][r].copy()
                else:
                    m.f[ic].append(self.f[ic][r].copy())
        m.F = self.F.copy()
        return m
    def __init__(self,vocabulary,samples = []):
        self.initial = 0
        self.Q = 0
        self.E = vocabulary
        self.f = []
        self.F = []
        for char in self.E:
            self.f.append([])
        self.add_state()

        for sample in samples:
            self.insert(sample)
        pass
    def insert(self,sample,state = 0):
        if not sample:
            self.F[state] = 1
            return

        ichar = self.E.find(sample[0])
        self.f[ichar][state].add(self.Q)
        self.add_state()
        return self.insert(sample[1:],self.Q - 1)
    def add_state(self):
        self.Q += 1
        for column in self.f:
            column.append(set())
        self.F += [0]
        pass
    def transform(self,partition,amount_of_partitions):
        sets = []
        for i in range(amount_of_partitions):
            sets.append(set())
        for chro in range(len(partition)):
            sets[partition[chro]].add(chro)
        for part in sets:
            if len(part) > 1:
                self.add_state()
                for state in part:
                    if self.F[state] == 1:
                        self.F[self.Q - 1] = 1
                    for ichar in range(len(self.E)):
                        for x in self.f[ichar][state].copy():
                            self.f[ichar][self.Q - 1].add(x) 
                        incterct = self.f[ichar][state].intersection(part)
                        if incterct:
                            for st in incterct:
                                self.f[ichar][self.Q - 1].remove(st)
                            self.f[ichar][self.Q - 1].add(self.Q - 1)
                for icolumn in range(len(self.E)):
                    for state in range(self.Q - 1):
                        incterct = self.f[icolumn][state].intersection(part)
                        if incterct:
                            for st in incterct:
                                self.f[icolumn][state].remove(st)
                            self.f[icolumn][state].add(self.Q - 1)
        pass
    def test(self,w,state = 0):
        if not w:
            return True if self.F[state] == 1 else False

        ichar = self.E.find(w[0])
        for st in self.f[ichar][state]:
            if self.test(w[1:],st):
                return True
        return False
    def __repr__(self):
        return "MCA(Q = %d)" % self.Q

class Alice:
    def __init__(self, mutation_rate = 0.01, crossover_rate = 0.2, max_generations = 50, total_population = 100):
        self.alphabet = 'abc'
        self.init_mutation_rate = float(mutation_rate)
        self.crossover_rate = float(crossover_rate)
        self.max_evaluation_amount = int(max_generations)
        self.total_population = int(total_population)
        self.samples = {}
        self.ps_samples = []
        self.ng_samples = set()
        self.previous_questions = []
        self.pendient_questions = []
        self.limit = 0
        self.amount_ps = 0
        self.amount_ns = 0
        self.mca = MCA(self.alphabet)
        pass
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
    def extreme_left_partition(self,partition):
        list_chro = []
        for ichro in range(len(partition)):
            if list_chro.count(partition[ichro]) == 0:
                list_chro.append(partition[ichro])
            partition[ichro] = list_chro.index(partition[ichro])
        return partition      
    def structural_crossover(self,population):
        amount = int(len(population) * self.crossover_rate)
        amount += 1 if amount % 2 == 1 else 0
        children = []
        Individual.new_generation()
        while amount:
            ff = False
            mf = False
            ifather = random.randint(0,len(population)-1)
            father = population[ifather]
            if ifather == 0:
                imother = random.randint(1,len(population)-1)
                mother = population[imother]
                population.remove(mother)
            else:
                population.remove(father)
                imother = random.randint(0,len(population)-1)
                mother = population[imother]
                if imother != 0:
                    population.remove(mother)
            
            amount_blocks_father = max(father.chromosomes) + 1
            amount_blocks_mother = max(mother.chromosomes) + 1

            selected_father_block = random.randint(0,amount_blocks_father)
            selected_mother_block = random.randint(0,amount_blocks_mother)

            male_child_chro =  father.chromosomes.copy()
            female_child_chro = mother.chromosomes.copy()
            
            for chro in range(len(female_child_chro)):
                if father.chromosomes[chro] == selected_father_block:
                    female_child_chro[chro] = selected_mother_block
                if mother.chromosomes[chro] == selected_mother_block:
                    male_child_chro[chro] = selected_father_block
            
            male_child = Individual(self.extreme_left_partition(male_child_chro))
            female_child = Individual(self.extreme_left_partition(female_child_chro))

            self.fittness_function(male_child)
            self.fittness_function(female_child)

            children.append(male_child)
            children.append(female_child)
            amount-=2

        population += children
        return population
    def structural_mutation(self,population):
        amount = int(len(population)*self.mutation_rate)
        amount = 1 if amount == 0 else amount
        while amount:
            individual = random.choice(population).clone()
            selected_chromosome = random.randint(0,len(individual.chromosomes) - 1)
            before_block = individual.chromosomes[selected_chromosome]
            selected_block = random.randint(0,max(individual.chromosomes)+1)
            individual.chromosomes[selected_chromosome] = selected_block
            individual.mutated = True
            individual.chromosomes = self.extreme_left_partition(individual.chromosomes)
            amount -= 1
        return population
    def fittness_function(self,individual):
        temp_mca = self.mca.clone()
        amount_sets = len(set(individual.chromosomes))
        new_Q = max(individual.chromosomes) + 1
        temp_mca.transform(individual.chromosomes,new_Q)

        for ng_sample in self.ng_samples:
            if temp_mca.test(ng_sample):
                individual.ng_accepted += 1
        
        individual.evaluation = self.mca.Q + individual.ng_accepted if individual.ng_accepted > 0 else amount_sets
        self.total_evaluation += individual.evaluation
        pass
    def select_fittests(self,population):
        selected = []
        amount = random.randint(2,len(population))
        average_ev = self.total_evaluation / len(population)

        sel_pos = []
        total = 0
        for individual in population:
            chance = average_ev - individual.evaluation + 1
            if chance >= 0:
                sel_pos.append([individual,chance])
                total += chance
        sel_pos.sort(key=lambda x: x[1],reverse=True)
        while amount:
            rnd = random.randint(0,int(total))
            for tup in sel_pos:
                if rnd > tup[1]:
                    rnd -= tup[1]
                else:
                    new = tup[0]
                    if tup[0] in selected:
                        new = tup[0].clone()
                    selected.append(new)
                    break
            amount -= 1
        population = selected
        return population
    def select_individual(self):
        
        pass
    def generate_population(self,population_size):
        amount_random = population_size
        for i in range(amount_random):
            ''' temp = 0
            chromosomes = []
            for state in range(self.mca.Q):
                chromosome = random.randint(0,temp)
                chromosomes.append(chromosome)
                temp += 1 if chromosome == temp else 0
            self.population.append(Individual(chromosomes)) '''
            initial_chro = list(range(self.mca.Q))
            self.population.append(Individual(initial_chro))
        pass
    def adapt_population(self):
        for individual in self.population:
            chromosomes = []
            temp = max(individual.chromosomes)+1
            for state in range(self.mca.Q - len(individual.chromosomes)):
                chromosome = random.randint(0,temp)
                chromosomes.append(chromosome)
            individual.chromosomes += chromosomes
        pass
    def GIG(self,population = []):
        self.population = population if population else []
        self.current_generation = 0
        self.total_evaluation = 0
        self.mutation_rate = self.init_mutation_rate * self.mca.Q
        if not population:
            self.generate_population(self.total_population)
        else:
            self.adapt_population()

        for individual in self.population:
            self.fittness_function(individual)

        self.population.sort(key = lambda x: x.evaluation)
        max_generations = self.max_evaluation_amount
        while max_generations > 0:
            if self.population[0].evaluation < self.mca.Q - 20 and self.population[0].ng_accepted < 4:
                break
            self.select_fittests(self.population)
            self.structural_crossover(self.population)
            self.structural_mutation(self.population)       
            self.population.sort(key = lambda x: x.evaluation)
            max_generations -= 1
        return self.population[0]
    def ready(self):
        sample = self.ps_samples.pop(0)
        self.mca.insert(sample)
        self.solution = self.GIG()
        self.solution_DFA = self.mca.clone()
        self.solution_DFA.transform(self.solution.chromosomes,max(self.solution.chromosomes)+1)
        # print("\nrunning:-------------------------------------------------------------------------------------------|")
        # print("_")
        # print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
        while self.ps_samples:
            sample = self.ps_samples.pop(0)
            if not self.solution_DFA.test(sample):
                self.mca.insert(sample)
                self.solution = self.GIG(self.population)
                # print("_")
                self.solution_DFA = self.mca.clone()
                self.solution_DFA.transform(self.solution.chromosomes,max(self.solution.chromosomes)+1)
        # print("\nfinished!\n")
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
        self.samples[question] = response
        if response:
            self.amount_ps += 1
            self.ps_samples.append(question)
        else:
            self.amount_ns += 1
            self.ng_samples.add(question)
        pass 
    def answer(self, i, question):
        return self.solution_DFA.test(question)
    def run(self, language):
        # Read the size of the language
        self.N = 100
        # Read the alfabet
        # self.alphabet = ['a','b','c']
        # Call init
        # self.__init__()
        self.bob = Bob(language)

        for i in range(self.N):
            # Build a random string of symbols
            question = self.ask(i)

            # Print and store the response
            # print("asking: %s" %question)
            # print(question)
            # sys.stdout.flush()

            answer = self.bob.check(question)

            # # Check the answer is OK
            # assert answer in ['yes', 'no']

            # Call learn
            self.learn(i, question, answer)

        # print("\n analizing...")
        self.ready()

        # Asnwer the N responses
        accepted = 0
        for i in range(self.N):
            question = self.bob.generate_q()

            # Is Bob cheating ?
            assert all(symbol in self.alphabet for symbol in question)

            # Compute the answer
            answer = self.answer(i, question)
            
            correct = answer == self.bob.should_be
            # print("question: %s --> response: %s %s" %(question,str(answer),str(correct)))
            accepted += 1 if correct else 0

        Individual.reset()
        return accepted
            # Print
            # print('yes' if answer else 'no')
            # sys.stdout.flush()#Python

            #print('vs yes' if self.bob.should_be else 'vs no')

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

def score(*args):
    resuts = [get_mean_score( 2, RegularGrammar(S="aS bS cS a b c"), *args),
              get_mean_score( 2, RegularGrammar(S="aO bE b", O="bO aE a", E="aO bE b"), *args),
              get_mean_score( 2, RegularGrammar(S="aU a", U="aU bU cU a b c"), *args),
              get_mean_score( 2, RegularGrammar(S="aA bS cS b c a",A = "aX bS cS a b c", X="bS cS b c"), *args),
              get_mean_score( 2, RegularGrammar(S="aS a"), *args)]
    return resuts

def get_mean_score(alices_amount, regular_grammar, *args,):
    val = 0
    for i in range(alices_amount):
        val += Alice(*args).run(regular_grammar)
    return float(val/alices_amount)
def get_best_score(*args):
    best = 0
    for run in score(*args):
        if run > best:
            best = run
    return best
def get_dominancy_score(*args):
    pass

# score( 0.01, 0.1, 10, 100)
# score( 0.1, 0.9, 10, 100)
# score( 0.01, 0.1, 10, 100)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: ./GIG-incremental.py <mutation rate/r> <crossover rate/r> <generations amount/z> <population size/z>")
        # print("usage: ./GIG-incremental.py -d")
        exit()

    if len(sys.argv) < 5:
        print("usage: ./GIG-incremental.py <mutation rate/r> <crossover rate/r> <generations amount/z> <population size/z>")
        # print("usage: ./GIG-incremental.py -d")
        exit()

    response = ""
    for sc in score(*sys.argv[1:]):
        response += str(sc) + " "

    print(response)
    
        
    

