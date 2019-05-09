import subprocess

class Algorithm:
    '''
    class definition for user optimization algorithm
    '''
    def __init__(self, func, params_amount, optimal_value, params_boundries, discrete_params, mode):
        self.func = func
        self.mode = mode
        self.params_amount = params_amount
        self.optimal_value = optimal_value
        self.params_upper_boundries = []
        self.params_lower_boundries = []
        self.set_params_boundries(params_boundries)
        self.discrete_params = discrete_params
    def load_func(self,func_file):
        #TODO gets function definition from file
        pass
    def set_params_boundries(self,params_boundries):
        """
        params: list(tuple(a,b))
        Get superior and inferior boundries for each parameter.
        """
        for i in range(self.params_amount):
            lo,up = params_boundries[i]
            if lo > up:
                raise Exception("Boundries Error [lower_boundry > upper_boundry]")
            self.params_upper_boundries.append(up)
            self.params_lower_boundries.append(lo)
    def build(self, params_boundries, params_types):
        pass
    def evaluate(self, params):
        try:
            response = list(self.run(params).split())
        except:
            raise Exception("Not valid algorithm output, float list response expected...")
        value = []
        for evaluation in response:
            try:
                value.append(float(evaluation))
            except:
                raise Exception("Not valid algorithm output, float list response expected...")
        # print("-")
        return value
        #
        #     value = float(response)
        # 
        # if not self.mode:
        #     return  abs(self.optimal_value - value)
        # else:
        #     return value
    def run(self, params:list):
        response = ""
        str_params = []
        for param in params:
            str_params.append(str(param))
        with subprocess.Popen(self.func + str_params, stdout = subprocess.PIPE) as proc:
            response = proc.stdout.read()
        return response
