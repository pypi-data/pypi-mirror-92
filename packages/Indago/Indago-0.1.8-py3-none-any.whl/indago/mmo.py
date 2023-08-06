# -*- coding: utf-8 -*-

import numpy as np
from .optimizer import Optimizer, CandidateState, OptimizationResults 
import copy
import random
from scipy.interpolate import interp1d # need this for akb_model


class Particle(CandidateState):
    """PSO Particle class"""
    
    def __init__(self, optimizer: Optimizer):
        CandidateState.__init__(self, optimizer)        
        self.V = np.zeros([optimizer.dimensions]) * np.nan


class MMO(Optimizer):
    """Mutualistic Multi-Optimization class"""

    def __init__(self):
        """Initialization"""
        Optimizer.__init__(self)

        self.X0 = None
        self.params = {}
        
        self.PSOmethod = 'Vanilla'
        self.swarm_size = None
        
        self.FWAmethod = 'Vanilla'       
        self.cX = None # FWA


    def _check_params(self):
        defined_params = list(self.params.keys())
        mandatory_params, optional_params = [], []

        if self.PSOmethod == 'Vanilla':
            mandatory_params += 'inertia cognitive_rate social_rate'.split()
            optional_params += 'akb_model akb_fun_start akb_fun_stop'.split()
        elif self.PSOmethod == 'TVAC':
            mandatory_params += 'inertia'.split()
            optional_params += 'akb_model akb_fun_start akb_fun_stop'.split()
        else:
            assert False, f'Uknonwn PSO method! {self.PSOmethod}'

        if self.FWAmethod == 'Vanilla':
            mandatory_params += 'n m1 m2'.split()
            optional_params += ''.split()
        elif self.FWAmethod == 'Rank':
            mandatory_params += 'n m1 m2'.split()
            optional_params += ''.split()
        else:
            assert False, f'Uknonwn FWA method! {self.FWAmethod}'

        Optimizer._check_params(self, mandatory_params, optional_params, defined_params)

        """ Anakatabatic Inertia a.k.a. Polynomial PFIDI """
        if self.params['inertia'] == 'anakatabatic':
            assert ('akb_fun_start' in defined_params \
                    and 'akb_fun_stop' in defined_params) \
                    or 'akb_model' in defined_params, \
                    'Error: Anakatabatic inertia requires either akb_model parameter or akb_fun_start and akb_fun_stop parameters'
                    
            if 'akb_model' in defined_params:

                if self.params['akb_model'] in ['FlyingStork', 'MessyTie', 'RightwardPeaks', 'OrigamiSnake']:   # w-list-based named akb_models                
                    if self.params['akb_model'] == 'FlyingStork':
                        w_start = [-0.86, 0.24, -1.10, 0.75, 0.72]
                        w_stop = [-0.81, -0.35, -0.26, 0.64, 0.60]
                        splinetype = 'linear'
                        if self.PSOmethod != 'Vanilla':
                            print('Warning: akb_model \'FlyingStork\' was designed for Vanilla PSO')                    
                    elif self.params['akb_model'] == 'MessyTie':
                        w_start = [-0.62, 0.18, 0.65, 0.32, 0.77]
                        w_stop = [0.36, 0.73, -0.62, 0.40, 1.09]
                        splinetype = 'linear'
                        if self.PSOmethod != 'Vanilla':
                            print('Warning: akb_model \'MessyTie\' was designed for Vanilla PSO')   
                    elif self.params['akb_model'] == 'RightwardPeaks':
                        w_start = [-1.79, -0.33, 2.00, -0.67, 1.30]
                        w_stop = [-0.91, -0.88, -0.84, 0.67, -0.36]
                        splinetype = 'linear'
                        if self.PSOmethod != 'TVAC':
                            print('Warning: akb_model \'RightwardPeaks\' was designed for TVAC PSO')
                    elif self.params['akb_model'] == 'OrigamiSnake':
                        w_start = [-1.36, 2.00, 1.00, -0.60, 1.22]
                        w_stop = [0.30, 1.03, -0.21, 0.40, 0.06]
                        splinetype = 'linear'
                        if self.PSOmethod != 'TVAC':
                            print('Warning: akb_model \'OrigamiSnake\' was designed for TVAC PSO')                      # code shared for all w-list-based named akb_models
                    Th = np.linspace(np.pi/4, 5*np.pi/4, 5)
                    self.params['akb_fun_start'] = \
                                        interp1d(Th, w_start, kind=splinetype)
                    self.params['akb_fun_stop'] = \
                                        interp1d(Th, w_stop, kind=splinetype) 
                else:
                    if self.params['akb_model'] != 'Languid':
                        print('Warning: Unknown akb_model. Defaulting to \'Languid\'')
                        self.params['akb_model'] = 'Languid'
                if self.params['akb_model'] == 'Languid':
                    def akb_fun_languid(Th):
                        w = (0.72 + 0.05) * np.ones_like(Th)
                        for i, th in enumerate(Th):
                            if th < 4*np.pi/4: 
                                w[i] = 0
                        return w
                    self.params['akb_fun_start'] = akb_fun_languid
                    self.params['akb_fun_stop'] = akb_fun_languid 
                
        
    def _init_method(self):
        self._init_optimizer()
        self.lb = np.array(self.lb)
        self.ub = np.array(self.ub)
        
        """ Initialize PSO """
        # Bounds for velocity
        self.v_max = 0.2 * (self.ub - self.lb)

        # Generate a swarm
        self.cS = np.array([Particle(self) for c in range(self.swarm_size)], dtype=Particle)
        
        # Prepare arrays
        self.dF = np.empty([self.swarm_size]) * np.nan

        # Generate initial positions
        for p in range(self.swarm_size):
            
            # Random position
            self.cS[p].X = np.random.uniform(self.lb, self.ub)
            
            # Using specified particles initial positions
            if self.X0 is not None:
                if p < np.shape(self.X0)[0]:
                    self.cS[p].X = self.X0[p]
                    
            # Generate velocity
            self.cS[p].V = np.random.uniform(-self.v_max, self.v_max)

            # No fitness change at the start
            self.dF[p] = 0.0

        # Evaluate
        self.collective_evaluation(self.cS)
        
        # Use initial particles as best ones
        self.cB = np.array([cP.copy() for cP in self.cS], dtype=CandidateState)
        
        # Update the overall best
        self.p_best = np.argmin(self.cB)
            
        # Update history
        self.results = OptimizationResults(self)
        self.results.cHistory = [self.cB[self.p_best].copy()]
        
        self.BI = np.zeros(self.swarm_size, dtype=int)
        self.TOPO = np.zeros([self.swarm_size, self.swarm_size], dtype=np.bool)

        self.reinitialize_topology()
        self.find_neighbourhood_best()
        
        self.ET = np.zeros([self.iterations])
        
        """ Initialize FWA """
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
        # self.results = OptimizationResults(self) # already initiated by PSO
        if np.min(self.cX).f < self.results.cHistory[0].f:
            self.results.cHistory[0] = np.min(self.cX).copy()

    
    def reinitialize_topology(self, k=3):
        self.TOPO[:, :] = False
        for p in range(self.swarm_size):
            links = np.random.randint(self.swarm_size, size=k)
            self.TOPO[p, links] = True
            self.TOPO[p, p] = True


    def find_neighbourhood_best(self):
        for p in range(self.swarm_size):
            links = np.where(self.TOPO[p, :])[0]
            #best = np.argmin(self.BF[links])
            p_best = np.argmin(self.cB[links])
            p_best = links[p_best]
            self.BI[p] = p_best


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
            
            if self.FWAmethod == 'Vanilla':
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
                
            if self.FWAmethod == 'Rank':
                
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

        return explosion_sparks
    
    
    def gaussian_mutation(self):
        mutation_sparks = []
        for j in range(self.params['m2']):
            cFw = self.cX[np.random.randint(self.params['n'])].copy()
            g = np.random.normal(1, 1)
            for k in range(self.dimensions):
                if(random.choice([True, False])):
                    cFw.X[k] *= g
            mutation_sparks.append(cFw)
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


    def run(self, seed=None):
        Optimizer.run(self, seed=seed)
        self._check_params()
        self._init_method()

        """ Prepare PSO """
        if self.verbose:
            if self.params['inertia'] == 'anakatabatic':
                self.report['theta'] = np.empty([self.swarm_size,
                                                 self.iterations])

        if 'inertia' in self.params.keys():
            w = self.params['inertia']
        if 'cognitive_rate' in self.params.keys():
            c1 = self.params['cognitive_rate']
        if 'cognitive_rate' in self.params.keys():
            c2 = self.params['social_rate']

        """ Prepare FWA """
        n = self.params['n']
        
        """ Main run loop """
        for i in range(self.iterations):
            
            """ PSO iteration """
            R1 = np.random.uniform(0, 1, [self.swarm_size, self.dimensions])
            R2 = np.random.uniform(0, 1, [self.swarm_size, self.dimensions])

            if self.params['inertia'] == 'LDIW':
                w = 1.0 - (1.0 - 0.4) * i / self.iterations

            if self.PSOmethod == 'TVAC':
                c1 = 2.5 - (2.5 - 0.5) * i / self.iterations
                c2 = 0.5 + (2.5 - 0.5) * i / self.iterations

            if self.params['inertia'] == 'anakatabatic':

                theta = np.arctan2(self.dF, np.min(self.dF))
                theta[theta < 0] = theta[theta < 0] + 2 * np.pi  # 3rd quadrant
                # fix for atan2(0,0)=0
                theta0 = theta < 1e-300
                theta[theta0] = np.pi / 4 + \
                    np.random.rand(np.sum(theta0)) * np.pi
                w_start = self.params['akb_fun_start'](theta)
                w_stop = self.params['akb_fun_stop'](theta)
                #print(w_start)
                w = w_start * (1 - i / self.iterations) \
                    + w_stop * (i / self.iterations)

                if self.verbose:
                    self.report['theta'][:, i] = theta
            
            w = w * np.ones(self.swarm_size) # ensure w is a vector
            
            # Calculate new velocity and new position
            
            for p, cP in enumerate(self.cS):

                self.cS[p].V = w[p] * self.cS[p].V + \
                               c1 * R1[p, :] * (self.cB[p].X - self.cS[p].X) + \
                               c2 * R2[p, :] * (self.cB[self.BI[p]].X - self.cS[p].X)
                        
                self.cS[p].X = self.cS[p].X + self.cS[p].V  
                
                # Correct position to the bounds
                cP.X = np.clip(cP.X, self.lb, self.ub)       
                
            # Get old fitness
            f_old = np.array([cP.f for cP in self.cS])

            # Evaluate swarm
            self.collective_evaluation(self.cS)

            for p, cP in enumerate(self.cS):
                # Calculate dF
                self.dF[p] = cP.f - f_old[p]
                
            for p, cP in enumerate(self.cS):
                # Update personal best
                if cP <= self.cB[p]:
                    self.cB[p] = cP.copy()  
            
            # Update the overall best
            self.p_best = np.argmin(self.cB)
                        
            # Update history
            self.results.cHistory.append(self.cB[self.p_best].copy())
            if self.verbose:
                print(i, self.cB[self.p_best].f)
            
            # Stop if fitness threshold achieved
            if self.cB[self.p_best].f < self.target_fitness:
                break
            
            # Update swarm topology
            if np.max(self.dF) >= 0.0:
                self.reinitialize_topology()
                
            # Find best particles in neighbourhood 
            self.find_neighbourhood_best()
            
            """ FWA iteration """
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
            if np.min(self.cX).f < self.results.cHistory[-1].f:
                self.results.cHistory.append(np.min(self.cX).copy())

            # Stop if fitness threshold achieved
            if np.min(self.cX).f < self.target_fitness:
                break
            
            """ Methods cooperating """
            if np.min(self.cX).f < self.cB[self.p_best].f: # FWAbest < PSObest
                PSOworst = np.max(self.cB)
                PSOworst.X = np.min(self.cX).X
                PSOworst.f = np.min(self.cX).f
                PSOworst.dF = 0.0
                self.find_neighbourhood_best()
                #print('FWA updated PSO')
            else: # PSObest < FWAbest
                FWAworst = np.max(self.cX)
                FWAworst.X = self.cB[self.p_best].X
                FWAworst.f = self.cB[self.p_best].f
                #print('PSO updated FWA')
        
        if self.cB[self.p_best].f < np.min(self.cX).f:
            return self.cB[self.p_best] # PSO reports best
        else:
            return np.min(self.cX) # FWA reports best
    
