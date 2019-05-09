from algorithm import Algorithm
import random_variables
import random
import math

class Harmony():
    def __init__(self, notes, mode = False, optimal_v = 0):
        self.notes = notes
        self.mode = mode
        self.optimal_v = optimal_v
        self.evaluation = None
    def evaluate(self, algorithm:Algorithm):
        self.evaluation = algorithm.evaluate(self.notes)
    def compare(self,other):
        count = 0
        for i in range(len(self.evaluation)):
            if self.mode:
                my_value = abs(self.optimal_v - self.evaluation[i])
                other_value = abs(self.optimal_v - other.evaluation[i])
            else:
                my_value = self.evaluation[i]
                other_value = other.evaluation[i]

            if my_value < other_value:
                count += 1
            if my_value > other_value:
                count -= 1
        return count
    def __eq__(self,other):
        return self.compare(other) == 0
    def __gt__(self,other):
        return self.compare(other) < 0

class HarmonySearch():
    """
    Class definition for Harmony Search technique for parameters optimization.

    >>> ``:Params:``\n
    `max_amount_iterations:` max amount of iterations for the search\n
    `harmony_memory_size:` size of harmony memory matrix (amount of harmonies)\n
    `harmony_memory_considering_rate:` probability of improvisation after copying harmonies notes.\n
    `min_par:` min probability of rewrite copied notes.\n
    `max_par:` min probability of rewrite copied notes.\n
    """
    def __init__(self, max_amount_iterations, harmony_memory_size = 50, harmony_memory_considering_rate = 0.99, min_par = 0, max_par = 1, par = 0.5):
        if harmony_memory_size == 0:
            raise Exception("harmony_memory_size must be greater than 0, common sense...")
        if harmony_memory_considering_rate == 0:
            raise Exception("harmony_memory_considering_rate must be greater than 0 in order to get somewhere...")
        if not (0 <= par <= 1):
            raise Exception("PAR parameter must be between 0 and 1")            
        if not (0 <= min_par <= 1):
            raise Exception("min PAR parameter must be between 0 and 1")            
        if not (0 <= max_par <= 1):
            raise Exception("max PAR parameter must be between 0 and 1")
        if min_par > max_par:
            raise Exception("min PAR must be lower or equal to max PAR")

        self.harmony_memory_size = harmony_memory_size
        self.harmony_memory_considering_rate = harmony_memory_considering_rate
        self.max_amount_iterations = max_amount_iterations
        self.algorithm = None
        self.min_par = min_par
        self.max_par = max_par
        self.par = par
    def initialize_harmony_memory(self):
        """
        initial harmony memory will be created randomly picking factible values
        for each note.

        `note`: this may differ in future
        """
        self.harmony_memory = []
        steps = []
        param_val = []
        for iparam in range(len(self.algorithm.params_upper_boundries)):
            lo = self.algorithm.params_lower_boundries[iparam]
            up = self.algorithm.params_upper_boundries[iparam]
            step = float((float(up) - float(lo))/float(self.harmony_memory_size))
            steps.append(step)
            param_val.append(lo)

        for i in range(self.harmony_memory_size):
            new_harmony_notes = []
            for j in range(self.algorithm.params_amount):
                lo = self.algorithm.params_lower_boundries[j]
                up = self.algorithm.params_upper_boundries[j]
                if self.algorithm.discrete_params[j]: #if param is discrete
                    new_harmony_notes.append(random.randint(lo,up))
                else: #if param is continue
                    new_harmony_notes.append(param_val[j])
                    param_val[j] += steps[j]
            self.harmony_memory.append(Harmony(new_harmony_notes, self.algorithm.mode, self.algorithm.optimal_value))
    def get_max_note(self, inote):
        """
        returns max value note at position `inote` of all harmonies.
        """
        max_note = self.algorithm.params_lower_boundries[inote]
        for harmony in self.harmony_memory:
            if harmony.notes[inote] > max_note:
                max_note = harmony.notes[inote]
        return max_note
    def get_min_note(self, inote):
        """
        returns max value note at position `inote` of all harmonies.
        """
        min_note = self.algorithm.params_upper_boundries[inote]
        for harmony in self.harmony_memory:
            if harmony.notes[inote] < min_note:
                min_note = harmony.notes[inote]
        return min_note
    def improvise(self):
        """
        Improvise operation method. Creates a new note based on the
        description of the Harmony Search Algorithm.\n
        `returns`: new harmony
        """
        hmcr = self.harmony_memory_considering_rate
        new_harmony = [0]*self.algorithm.params_amount

        for param in range(self.algorithm.params_amount):
            rd = random.random()
            if rd <= hmcr:#seleccion from memory
                iharmony = random.randint(0,self.harmony_memory_size - 1)
                new_harmony[param] = self.harmony_memory[iharmony].notes[param]
                rd = random.random()
                if rd <= self.par:
                    rd = random.random()
                    if rd < 0.5:
                        rd = random.random()
                        max_n = self.get_max_note(param)
                        if self.algorithm.discrete_params[param]:
                            new_harmony[param] = int(new_harmony[param] + (max_n - new_harmony[param])*rd)
                        else:
                            new_harmony[param] = new_harmony[param] + (max_n - new_harmony[param])*rd
                    else:
                        rd = random.random()
                        min_n = self.get_min_note(param)
                        if self.algorithm.discrete_params[param]:
                            new_harmony[param] = int(new_harmony[param] - (new_harmony[param] - min_n)*rd)
                        else:
                            new_harmony[param] = new_harmony[param] - (new_harmony[param] - min_n)*rd
            else: #selection from possible values
                lo = self.algorithm.params_lower_boundries[param]
                up = self.algorithm.params_upper_boundries[param]
                if self.algorithm.discrete_params[param]:
                    new_harmony[param] = random.randint(lo,up)
                else:
                    new_harmony[param] = random_variables.uniform_distribution(lo,up)

        return Harmony(new_harmony, self.algorithm.mode, self.algorithm.optimal_value)
    def build(self, algorithm:Algorithm):
        self.algorithm = algorithm
    def run(self):
        if self.algorithm == None:
            raise Exception("Algorithm not found, try build method first.")
        self.initialize_harmony_memory()
        for harmony in self.harmony_memory:
            harmony.evaluate(self.algorithm)
        
        for i in range(self.max_amount_iterations):
            self.harmony_memory.sort()#key = lambda harmony: harmony.evaluation)
            new_harmony = self.improvise()
            new_harmony.evaluate(self.algorithm)
            if new_harmony.evaluation < self.harmony_memory[self.harmony_memory_size - 1].evaluation:
                self.harmony_memory[self.harmony_memory_size - 1] = new_harmony

        response = ""
        rs = self.algorithm.evaluate(self.harmony_memory[0].notes)
        for val in rs:
            response += str(val) + " "
        return (self.harmony_memory[0].notes, response)

# test_alg = Algorithm("a*b",4,float("12.34"),[(0,3),(2,8),(1,100),(2,100)],[True,True,False,False])
# a = HarmonySearch(10)
# a.build(test_alg)
# a.run()