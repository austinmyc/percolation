from percolation import *
from tqdm import tqdm

class Exp:
    def __init__(self, n, trials):
        self.n=n
        self.trials=trials
        self.res=[-1]*trials
    
    def run(self):
        for r in tqdm(range(self.trials)):
            P=Percolation_exp(self.n)
            self.res[r]=P.exp()
    
        
        


