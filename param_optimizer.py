import os
import scipy
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

        self.methods_doc = {}
        self.methods_doc['help'] = "list of commands and short help message"
        self.methods_doc['q'] = "exit program"
        self.methods_doc['start'] = "begin Data Collection and runs Harmony Search algorithm"

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
    def get_params_types(self):
        while True:
            params = str(input("\nInsert for each parameter needed it's type (z means integer, r means real)\n--> ")).split()
            params_types = []
            for param in params:
                if param == "z":
                    params_types.append(True)
                elif param == "r":
                    params_types.append(False)
            confirmation = input("%d parameters have been correctly identified, want to proceed? y|n\n--> " %len(params_types))
            if confirmation != "n":
                return params_types
    def get_integer_boundry(self, iparam):
        while True:
            try:
                lo,up = str(input("\n-Insert Lower and Upper search boundries for integer param #%d [example: 0 100]\n-->" %iparam)).split()
            except:
                print("[ERROR] not enough arguments for boundries declaration param $%d, retrying" %iparam)
                continue
            try:
                boundries = (int(lo),int(up))
            except:
                print("[ERROR] at least one of the arguments could'nt be parsed into integer, retrying")
                continue
            return boundries  
    def get_float_boundry(self, iparam):
        while True:
            try:
                lo,up = str(input("\n-Insert Lower and Upper search boundries for real param #%d [example: 1,5 99,9]\n-->" %iparam)).split()
            except:
                print("[ERROR] not enough arguments for boundries declaration param $%d, retrying" %iparam)
                continue
            try:
                boundries = (float(lo),float(up))
            except:
                print("[ERROR] at least one of the arguments could'nt be parsed into float, retrying")
                continue
            return boundries
    def get_optimal_value(self):
        while True:
            val = input("\nInsert optimal value (if none then you should expect minimization)\n--> ")
            if val == "":
                return (False, 0)
            try:
                return (True,float(val))
            except:
                print("[ERROR] optimal value could'nt be parsed into float, try again")
    def query_algorithm(self):
        command, raw = self.get_command()

        print("\n|---------------------------------------|\
               \n|--------Starting Info Gathering--------|\
               \n|---------------------------------------|\n")

        params = self.get_params_types()
        boundries = []
        j = 0

        for param in params:
            if param:
                boundries.append(self.get_integer_boundry(j))
            else:
                boundries.append(self.get_float_boundry(j))
            j+=1

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

# ParamsOptimizer(1).play_end_music()
ParamsOptimizer(2).run()