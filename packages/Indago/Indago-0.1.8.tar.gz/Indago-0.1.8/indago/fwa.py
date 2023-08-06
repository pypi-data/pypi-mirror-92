# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 13:43:18 2018

@author: Stefan
"""

# -*- coding: utf-8 -*-

import numpy as np
from .optimizer import Optimizer, CandidateState, OptimizationResults
import random


class FWA(Optimizer):
    """Firework Algorithm class"""

    def __init__(self):
        """Initialization"""
        Optimizer.__init__(self)

        # self.X = None # seems to be obsolete
        self.X0 = None
        self.cX = None
        self.method = 'Vanilla'
        self.params = {}

    def _check_params(self):

        defined_params = list(self.params.keys())
        mandatory_params, optional_params = [], []

        if self.method == 'Vanilla':
            mandatory_params = 'n m1 m2'.split()
            optional_params = ''.split()
        elif self.method == 'Rank':
            mandatory_params = 'n m1 m2'.split()
            optional_params = ''.split()
        else:
            assert False, f'Uknonwn method! {self.method}'

        Optimizer._check_params(self, mandatory_params, optional_params, defined_params)

    def _init_method(self):
        self._init_optimizer()

        self.cX = np.array([CandidateState(self) for p in range(self.params['n'])], dtype=CandidateState)
        
        # Generate initial positions
        for p in range(self.params['n']):
            
            # Random position
            self.cX[p].X = np.random.uniform(self.lb, self.ub, self.dimensions)
            
            # Using specified initial positions
            if self.X0 is not None:
                if p < np.shape(self.X0)[0]:
                    self.cX[p].X = self.X0[p]

        # Evaluate all
        self.collective_evaluation(self.cX)

        # Sort
        self.cX = np.sort(self.cX)
        
        # Initialize the results
        self.results = OptimizationResults(self)
        self.results.cHistory = [np.min(self.cX).copy()]


    def run(self, seed=None):
        Optimizer.run(self, seed=seed)
        self._check_params()
        self._init_method()
        
        n = self.params['n']

        for i in range(self.iterations):

            explosion_sparks = self.explosion()
            mutation_sparks = self.gaussian_mutation()

            #self.__mapping_rule(sparks, self.lb, self.ub, self.dimensions)
            for cS in (explosion_sparks + mutation_sparks):
                
                ilb = cS.X < self.lb
                cS.X[ilb] = self.lb[ilb]
                iub = cS.X > self.ub
                cS.X[iub] = self.ub[iub]

                self.cX = np.append(self.cX, [cS])

            self.collective_evaluation(self.cX)

            self.cX = np.sort(self.cX)[:n]

            # Update history
            self.results.cHistory.append(np.min(self.cX).copy())

            # Stop if fitness threshold achieved
            if np.min(self.cX).f < self.target_fitness:
                break
        
        return np.min(self.cX)
        # self.best = Gbest
        # self._set_Gbest(Gbest)

    def explosion(self):
        eps=0.001
        amp=10
        a=0.01
        b=10
        F = np.array([cP.f for cP in self.cX])
        fmin = np.min(F)
        fmax = np.max(F)
        
        explosion_sparks = []
        for p in range(self.params['n']):
               
            cFw = self.cX[p].copy()
            #print(cFw.X)
            
            if self.method == 'Vanilla':
                # Number of sparks
                n1 = self.params['m1'] * (fmax - cFw.f + eps) / np.sum(fmax - F + eps)
                n1 = self.min_max_round(n1, self.params['m1'] * a, self.params['m2'] * b)
                
                # Amplitude
                A = amp * (cFw.f - fmin + eps) /  (np.sum(F - fmin) + eps)

                for j in range(n1):
                    for k in range(self.dimensions):
                        if (random.choice([True, False])):
                            cFw.X[k] += random.uniform(-A, A)
                    explosion_sparks.append(cFw.copy())
                
            if self.method == 'Rank':
                
                # Number of sparks
                #vn1 = self.params['m1'] * (fmax - cFw.f + eps) / np.sum(fmax - F + eps)
                #vn1 = self.min_max_round(vn1, self.params['m1'] * a, self.params['m2'] * b)
                
                n1 = self.params['m1'] * (self.params['n'] - p)**1 / np.sum(np.arange(self.params['n']+1)**1)
                n1 = random.choice([int(np.floor(n1)), int(np.ceil(n1))])
                #print(self.cX[p].f, vn1, n1)
                
                # Amplitude
                #Ac = amp * (cFw.f - fmin + eps) / (np.sum(F - fmin) + eps)
                    
                #print('n1:', n1, 'A:', A)
                XX = np.array([cP.X for cP in self.cX])
                #print(XX.shape)
                
                # Uniform
                dev = np.std(XX, 0)
                avg_scale = np.average(np.sqrt(np.arange(self.params['n']) + 1))
                scale = np.sqrt(p + 1) / avg_scale
                
                #avg_scale = np.average(np.arange(self.params['n']) + 1)
                #scale = (p + 1) / avg_scale
                
                
                A = np.sqrt(12) / 2 * dev * scale
                A *= 1.5

                
                #cS = cFw.copy()
                for j in range(n1):
                    cFw.X = cFw.X + np.random.uniform(-A, A) * np.random.randint(0, 1, A.size)
                    
                    for k in range(self.dimensions):
                        if (random.choice([True, False])):
                            # Uniform
                            cFw.X[k] += np.random.uniform(-A[k], A[k])
                            # Normal
                            # cFw.X[k] += random.normal(-A[k], A[k])
                    
                    #print(cS.X)
                    explosion_sparks.append(cFw.copy())  

        #print('expl sparks:', len(explosion_sparks))
        #input(' > Press return to continue.')
        return explosion_sparks
    
    """
    def __explosion_operator(self, sparks, fw, function,
                             dimension, m, eps, amp, Ymin, Ymax, a, b):
        
        sparks_num = self.__round(m * (Ymax - function(fw) + eps) /
                                  (sum([Ymax - function(fwk) for fwk in self.X]) + eps), m, a, b)
        print(sparks_num)

        amplitude = amp * (function(fw) - Ymax + eps) / \
            (sum([function(fwk) - Ymax for fwk in self.X]) + eps)

        for j in range(int(sparks_num)):
            sparks.append(np.array(fw))
            for k in range(dimension):
                if (random.choice([True, False])):
                    sparks[-1][k] += random.uniform(-amplitude, amplitude)
    """
    
    def gaussian_mutation(self):
        
        mutation_sparks = []
        for j in range(self.params['m2']):
            cFw = self.cX[np.random.randint(self.params['n'])].copy()
            g = np.random.normal(1, 1)
            for k in range(self.dimensions):
                if(random.choice([True, False])):
                    cFw.X[k] *= g
            mutation_sparks.append(cFw)

        #print('mut sparks:', np.sort([p.f for p in mutation_sparks]))
        #print('mut sparks:', len(mutation_sparks))
        return mutation_sparks
            
    def __mapping_rule(self, sparks, lb, ub, dimension):
        for i in range(len(sparks)):
            for j in range(dimension):
                if(sparks[i].X[j] > ub[j] or sparks[i].X[j] < lb[j]):
                    sparks[i].X[j] = lb[j] + \
                        (sparks[i].X[j] - lb[j]) % (ub[j] - lb[j])

    def __selection(self, sparks, n, function):        

        self.collective_evaluation(sparks)
        self.cX = np.append(self.cX, sparks)


    def min_max_round(self, s, smin, smax):
        return int(np.round(np.min([np.max([s, smin]), smax])))

    def __round(self, s, m, a, b):
        if (s < a * m):
            return round(a * m)
        elif (s > b * m):
            return round(b * m)
        else:
            return round(s)
