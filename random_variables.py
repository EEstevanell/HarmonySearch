import random

def uniform_distribution(a,b):
    rd = random.random()
    return a + rd*(b - a) 