import os
import sys
# import scipy
import time
# import winsound
from algorithm import Algorithm
from harmony_search import HarmonySearch

class ParamsOptimizer:
    def __init__(self, time):
        self.set_user_waiting_time(time)
        self.set_console_methods()
        self.set_all_heuristics()
    def get_amount_evaluations(self):
        #TODO must get time of execution and relate to user's possible
        #waiting time
        pass
    def set_user_waiting_time(self,time):
        self.user_time = time
        pass
    def set_console_methods(self):
        """
        All console methods must be added to dict here
        """
        self.methods = {}
        self.methods['help'] = self.help
        self.methods['q'] = self.q
        self.methods['start'] = self.query_algorithm
        self.methods['load'] = self.load

        self.methods_doc = {}
        self.methods_doc['help'] = "list of commands and short help message"
        self.methods_doc['q'] = "exit program"
        self.methods_doc['start'] = "begin Data Collection and runs Harmony Search algorithm"
        self.methods_doc['load'] = "load data configuration from file\n\
                                -----protocol----\n\
                                line 1: Command\n\
                                line 2: params\n\
                                line 3 to line 2 + k (if there were declared k params): boundries\n\
                                line 3 + k: optimal value (if required)"

    def set_all_heuristics(self):
        self.harmony_search = HarmonySearch(75)
    def run(self):
        """
        run prompt and execute instructions
        """
        self.help()
        while True:
            entry = input(">>> ")
            try:
                self.methods[entry]()
            except Exception as e:
                print("no instruction %s declared" %(e))
    
    ############################## Console Methods ##################################
    def _load(self, file):
        config = open(file, "r")
        try:
            raw = config.readline()
            commad = raw.split()
        except:
            print("error on line 1, check if it was a proper declaration of a command..")
        try:
            params = config.readline().split()
            boundries = []
            j = 0
            for param in params:
                boundry = config.readline()
                if param == "z":
                    boundries.append(self.get_integer_boundry(j, boundry))
                elif param == "r":
                    boundries.append(self.get_float_boundry(j, boundry))
                j+=1
        except:
            print("error on line 2")
        try:
            mode, optimal_value = self.get_optimal_value(config.readline())
        except:
            mode = None
            optimal_value = None
            pass
            # print("error on line 3")
        config.close()
        return self.query_algorithm( commad, raw, params, mode, optimal_value, boundries, True)
    def load(self):
        file = input("config file: ")
        return self._load(file)    
    def play_end_music(self):
        # winsound.Beep(2000,200)
        # winsound.Beep(2500,200)
        # winsound.Beep(3000,300)
        # winsound.Beep(2000,400)
        pass
    def help(self):
        print("\n--------------- Registered Commands -----------------\n")
        for command in self.methods.keys():
            print("command: " + command,end = "  ----   ")
            try:
                print(self.methods_doc[command])
            except:
                print(" -no help message found")
        print("\n")
    def q(self):
        print("Exiting Program, hope you liked it! See ya")
        exit()
    def get_command(self):
        raw = input("\n-Insert the command you use to run your algorithm (no params and full paths required) in a shell as this were it-\n$ ")
        return (raw.split(), raw)
    def get_params_types(self, params = None):
        while True:
            if not params:
                params = str(input("\nInsert for each parameter needed it's type (z means integer, r means real)\n--> ")).split()
            params_types = []
            for param in params:
                if param == "z":
                    params_types.append(True)
                elif param == "r":
                    params_types.append(False)
            if not params:
                confirmation = input("%d parameters have been correctly identified, want to proceed? y|n\n--> " %len(params_types))
                if confirmation != "n":
                    return params_types
            else:
                return params_types
    def get_integer_boundry(self, iparam, boundry = None):
        while True:
            try:
                if not boundry:
                    lo,up = str(input("\n-Insert Lower and Upper search boundries for integer param #%d [example: 0 100]\n-->" %iparam)).split()
                else:
                    lo,up = boundry.split()
            except:
                print("[ERROR] not enough arguments for boundries declaration param $%d, retrying" %iparam)
                continue
            try:
                boundries = (int(lo),int(up))
            except:
                print("[ERROR] at least one of the arguments could'nt be parsed into integer, retrying")
                continue
            return boundries  
    def get_float_boundry(self, iparam, boundry = None):
        while True:
            try:
                if not boundry:
                    lo,up = str(input("\n-Insert Lower and Upper search boundries for real param #%d [example: 1,5 99,9]\n-->" %iparam)).split()
                else:
                    lo,up = boundry.split()
            except:
                print("[ERROR] not enough arguments for boundries declaration param $%d, retrying" %iparam)
                continue
            try:
                boundries = (float(lo),float(up))
            except:
                print("[ERROR] at least one of the arguments could'nt be parsed into float, retrying")
                continue
            return boundries
    def get_optimal_value(self, ov = None):
        while True:
            if not ov:
                val = input("\nInsert optimal value (if none then you should expect minimization)\n--> ")
            else:
                val = ov
            if val == "":
                return (False, None)
            try:
                return (True,float(val))
            except:
                print("[ERROR] optimal value could'nt be parsed into float, try again")
    def query_algorithm(self, command = None, raw = None, params = None, mode = False, optimal_value = "", boundries = [], ovpass = False):
        if not command:
            command, raw = self.get_command()

        print("\n|---------------------------------------|\
               \n|--------Starting Info Gathering--------|\
               \n|---------------------------------------|\n")

        params = self.get_params_types(params = params)
        # boundries = []
        j = 0

        if not boundries:
            for param in params:
                if param:
                    boundries.append(self.get_integer_boundry(j))
                else:
                    boundries.append(self.get_float_boundry(j))
                j+=1

        if not ovpass:
            mode, optimal_value = self.get_optimal_value()
        if not mode:
            message = "*Minimize*"
        else:
            message = str(optimal_value)

        new_alg = Algorithm(command, len(params), optimal_value, boundries, params, mode)
        print("All set up:\n\n\
               algoritm: %s\n\
               amount of params: %d\n\
               optimal value: %s\n" %(raw, len(params),message))
        
        proc = input("Want to proceed? y|n\n-->")
        if proc != "n":
            print("\nStarting Harmony Search\n...\n...")
            try:
                self.harmony_search.build(new_alg)
                a = time.time()
                optimal_set, evaluation = self.harmony_search.run()
                b = time.time()
                print("Harmony Search ended successfully")
                print("[Results]\n\
                    Optimal Params: %s\n\
                    Waiting Time (seconds): %s\n\
                    Evaluation: %s\n" %(str(optimal_set),str(b - a), str(evaluation)))
                self.play_end_music()
            except Exception as e:
                print(e)
        print("Exiting Program, hope you enjoyed our time together!")

# ParamsOptimizer(1)._load("config.txt")
# ParamsOptimizer(2).run()

if __name__ == "__main__":
    po = ParamsOptimizer(0)
    if len(sys.argv) > 2:
        print("usage: python param_optimizer.py [config-file]")
        exit()
    if len(sys.argv) == 2:
        file = sys.argv[1]
        po._load(file)
    else:
        po.run()
