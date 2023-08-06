# -*- coding: utf-8 -*-

import numpy as np
from .optimizer import Optimizer, CandidateState, OptimizationResults 
from scipy.special import gamma

"""
Jain, M., Singh, V., & Rani, A. (2019). A novel nature-inspired algorithm for 
optimization: Squirrel search algorithm. Swarm and evolutionary computation, 
44, 148-175.
"""


class FlyingSquirrel(CandidateState):
    """SSA agent class"""
    
    def __init__(self, optimizer: Optimizer):
        CandidateState.__init__(self, optimizer)


class SSA(Optimizer):
    """Squirrel Search Algorithm class"""

    def __init__(self):
        """Initialization"""
        
        Optimizer.__init__(self)

        self.X = None
        self.X0 = None
        self.method = 'Vanilla'
        self.swarm_size = None
        self.params = {}
        
        # Default params
        self.Pdp = 0.1 # predator_presence_probability
        self.Gc = 1.9 # gliding_constant
        self.dg_lim = [0.5, 1.11] # gliding_distance_limits (for random dg)

    def _check_params(self):

        defined_params = list(self.params.keys())
        mandatory_params, optional_params = [], []

        if self.method == 'Vanilla':
            mandatory_params = 'acorn_tree_attraction'.split()
            optional_params = 'predator_presence_probability gliding_constant \
                                gliding_distance_limits'.split()

        Optimizer._check_params(self, mandatory_params, optional_params, defined_params)
        
    def _init_method(self):
        
        self._init_optimizer()
        
        # Bounds for position and velocity
        self.lb = np.array(self.lb)
        self.ub = np.array(self.ub)

        # Generate a swarm of FS
        self.cS = np.array([FlyingSquirrel(self) for c in range(self.swarm_size)], \
                            dtype=FlyingSquirrel)
        
        # Generate initial positions
        for p in range(self.swarm_size):            
            # Random position
            self.cS[p].X = np.random.uniform(self.lb, self.ub)           
            # Using specified particles initial positions
            if self.X0 is not None:
                if p < np.shape(self.X0)[0]:
                    self.cS[p].X = self.X0[p]                                          
            # Evaluate one by one
            #self.cS[p].evaluate()   
        # Evaluate
        self.collective_evaluation(self.cS)
        
        # Find the overall best, i.e. FSht (hickory nut tree)
        self.best = np.sort(self.cS)[0]
            
        # Update history
        self.results = OptimizationResults(self)
        self.results.cHistory = [self.best]
        
    def run(self, seed=None):
        
        Optimizer.run(self, seed=seed)
        self._check_params()
        self._init_method()
      
        # Load params
        if 'acorn_tree_attraction' in self.params.keys():
            # part of FSnt moving to FSat
            # ATA=0 (all move to FSht) - emphasize local search
            # ATA=1 (all move to FSat's) - emphasize global search
            self.ATA = self.params['acorn_tree_attraction']
        if 'predator_presence_probability' in self.params.keys():
            self.Pdp = self.params['predator_presence_probability']
        if 'gliding_constant' in self.params.keys():
            self.Gc = self.params['gliding_constant']
        if 'gliding_distance_limits' in self.params.keys():
            self.dg_lim = self.params['gliding_distance_limits']
            
        def Levy():
            ra, rb = np.random.normal(0, 1), np.random.normal(0, 1)
            beta = 1.5
            sigma = ((gamma(1 + beta) * np.sin(np.pi * beta / 2)) / \
                     gamma((1 + beta) / 2) * beta * 2**((beta - 1)/2)) **(1 / beta)
            return 0.01 * (ra * sigma) / (np.abs(rb)**(1 / beta))

        for i in range(self.iterations):
            
            # Categorizing FS's
            FSht = np.sort(self.cS)[0] # best FS (hickory nut trees)
            FSat = np.sort(self.cS)[1:4] # good FS (acorn trees)
            FSnt = np.sort(self.cS)[5:] # bad FS (normal trees)
            
            """
            # Moving FSnt - cascading strategy
            # move principally to FSat; 
            # with probability = (1-Pdp)*Pdp = 0.09 move to Fsht
            for fs in FSnt:
                if np.random.rand() >= self.Pdp: # move towards FSat
                    dg = np.random.uniform(self.dg_lim[0], self.dg_lim[1])
                    fs.X = fs.X + dg * self.Gc * \
                            (np.random.choice(FSat).X - fs.X)
                elif np.random.rand() >= self.Pdp: # move towards FSht
                    dg = np.random.uniform(self.dg_lim[0], self.dg_lim[1])
                    fs.X = fs.X + dg * self.Gc * (FSht.X - fs.X)
                else: # not moving, i.e. respawning randomly
                    fs.X = np.random.uniform(self.lb, self.ub)
            """
            
            # Moving FSnt
            Nnt2at = int(np.size(FSnt) * self.ATA) # attracted to acorn trees
            np.random.shuffle(FSnt)
            for fs in FSnt[:Nnt2at]:
                if np.random.rand() >= self.Pdp: # move towards FSat
                    dg = np.random.uniform(self.dg_lim[0], self.dg_lim[1])
                    fs.X = fs.X + dg * self.Gc * \
                            (np.random.choice(FSat).X - fs.X)
                else: # not moving, i.e. respawning randomly
                    fs.X = np.random.uniform(self.lb, self.ub)
            for fs in FSnt[Nnt2at:]:
                if np.random.rand() >= self.Pdp: # move towards FSht
                    dg = np.random.uniform(self.dg_lim[0], self.dg_lim[1])
                    fs.X = fs.X + dg * self.Gc * (FSht.X - fs.X)
                else: # not moving, i.e. respawning randomly
                    fs.X = np.random.uniform(self.lb, self.ub)
            
            # Moving FSat
            for fs in FSat:
                if np.random.rand() >= self.Pdp: # move towards FSht
                    dg = np.random.uniform(self.dg_lim[0], self.dg_lim[1])
                    fs.X = fs.X + dg * self.Gc * (FSht.X - fs.X)
                else: # not moving, i.e. respawning randomly
                    fs.X = np.random.uniform(self.lb, self.ub)
            
            # Seasonal constants (for FSat)
            Sc = np.empty(3)
            for i, fs in enumerate(FSat):
                Sc[i] = np.sqrt(np.sum((fs.X - FSht.X)**2))
                
            # Minimum value of seasonal constant
            Scmin = 1e-6 / (365**(i / (self.iterations / 2.5))) # this is some black magic shit
            
            # Random-Levy relocation at the end of winter season
            if (Sc < Scmin).all():
                for fs in FSnt:
                    fs.X = self.lb + Levy() * (self.ub - self.lb)
            
            for cP in self.cS:
                # Correct position to the bounds
                cP.X = np.clip(cP.X, self.lb, self.ub)       

            # # Evaluate swarm, one by one
            # for cP in self.cS:
            #     cP.evaluate()
                
            # Evaluate swarm
            self.collective_evaluation(self.cS)
            
            # Update the overall best
            self.best = np.min(self.cS)
             
            # Update history
            self.results.cHistory.append(self.best.copy())

            if self.verbose:
                print(i, self.best.f)
                
            # Stop if fitness threshold achieved
            if self.best.f < self.target_fitness:
                break

        return self.best