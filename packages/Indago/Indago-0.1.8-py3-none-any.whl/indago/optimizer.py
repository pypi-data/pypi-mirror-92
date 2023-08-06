# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import time
import multiprocessing
import string

class Optimizer:
    """Base class for all optimization methods."""

    def __init__(self):
        """Initialization"""

        self.dimensions = None
        self.evaluation_function = None
        self.number_of_processes = 1
        
        self.objectives = 1
        self.objective_weights = None
        self.objective_labels = None
        self.constraints = 0
        self.constraint_labels = None
        
        self.iterations = None
        self.target_fitness = -np.inf
        
        self.lb = None
        self.ub = None
        self.verbose = None
        self.report = {}

        self.forward_unique_str = False
        self._unique_str_list = []
        
    def _init_optimizer(self):
        
        assert not isinstance(self.objectives, np.unsignedinteger), \
            "optimizer.objectives should be positive integer"
        assert self.objectives > 0, "optimizer.objectives should be positive integer"
        
        assert not isinstance(self.constraints, np.unsignedinteger), \
            "optimizer.constraints should be unsigned integer"
        
        if self.objective_weights is None:
            self.objective_weights = np.ones(self.objectives) / self.objectives   
        else:
            assert len(self.objective_weights) == self.objectives, \
                "optimizer.objective_weights list should contain number of elements equal to optimizer.objectives"
        
        if self.objective_labels is None:
            self.objective_labels = [f'o_{o}' for o in range(self.objectives)]   
        else:
            assert len(self.objective_labels) == self.objectives, \
                "optimizer.objective_labels list should contain number of strings equal to optimizer.objectives"
            
        if self.constraint_labels is None:
            self.constraint_labels = [f'c_{c}' for c in range(self.constraints)]   
        else:
            assert len(self.constraint_labels) == self.constraints, \
                "optimizer.constraint_labels list should contain number of strings equal to optimizer.constraints"
            
        self.ET = None

        assert isinstance(self.number_of_processes, int) or self.number_of_processes == 'maximum', \
            "optimizer.number_of_processes should be integer or \'maximum\'"
        if self.number_of_processes == 'maximum':
            self.number_of_processes = multiprocessing.cpu_count()
        if self.number_of_processes > 1:
            self.log(f'Preparing a multiprocess pool for {self.number_of_processes} processes.')
            self.pool = multiprocessing.Pool(self.number_of_processes)


    def _check_params(self, mandatory_params, optional_params, defined_params):
        for param in mandatory_params:
            assert param in defined_params, f'Error: Missing parameter {param}'

        for param in defined_params:
            if param not in mandatory_params and param not in optional_params:
                print(f'Warning: Excessive parameter {param}')

    def title(self, msg, line_length=60):
        t = '-' * line_length
        t += '\n' + msg.center(line_length) + '\n'
        t += '-' * line_length
        print(t)

    def log(self, msg, indent=0):
        print(' ' * indent + msg)
        
    def tic(self):
        self._time1 = time.time()

    def toc(self, msg='', silent=False):

        s = time.time() - self._time1
        
        if not silent:
            if msg == '':
                msg = 'Elapsed time:'

            if s < 1:
                dur = f'{s*1e3:.3f} milliseconds.'
            else:
                dur = f'{s:.3f} seconds.'
            self.log(f'{msg} {dur}')
            
        return s


    def _gen_unique_str(self):
        while True:
            _s = ''.join(np.random.choice([c for c in string.ascii_lowercase]) for i in range(16))
            if _s not in self._unique_str_list:
                self._unique_str_list.append(_s)
                return _s


    def run(self, seed=None):
        if None:
            np.random.seed() # Possibe fix for some seed issues in parallel execution
        else:
            np.random.seed(seed)



    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)

    def _multiprocess_evaluate(self, candidates):

        if self.forward_unique_str:
            result = self.pool.starmap(self.evaluation_function, [tuple([c.X, self._gen_unique_str()]) for c in candidates])
        else:
            result = self.pool.map(self.evaluation_function, [c.X for c in candidates])

        if self.objectives == 1 and self.constraints == 0:
            # Fast evaluation
            for p in range(len(candidates)):
                candidates[p].f = result[p]
                candidates[p].O[0] = result[p]
        else:
            # Full evaluation
            for p in range(len(candidates)):
                for io in range(self.objectives):
                    candidates[p].O[io] = result[p][io]
                candidates[p].f = np.dot(candidates[p].O, self.objective_weights)
                for ic in range(self.constraints):
                    candidates[p].C[ic] = result[p][self.objectives + ic]

        return candidates

    def collective_evaluation(self, candidates):

        if self.number_of_processes > 1:
            self._multiprocess_evaluate(candidates)
        else:
            if self.forward_unique_str:
                for p in range(len(candidates)):
                    candidates[p].evaluate(self._gen_unique_str())
            else:
                for p in range(len(candidates)):
                    candidates[p].evaluate()

    def multiprocess_evaluate_test(self, number_of_candidates, seed=None):
        # Function for testing purpose only - remove it!

        self._init_optimizer()
        if None:
            np.random.seed() # Possibe fix for some seed issues in parallel execution
        else:
            np.random.seed(seed)

        candidates = np.array([CandidateState(self) for c in range(number_of_candidates)], dtype=CandidateState)

        for p in range(number_of_candidates):
            candidates[p].X = np.random.uniform(self.lb, self.ub)

        self.collective_evaluation(candidates)

        return candidates



class CandidateState:
    """Candidate solution for optimization problem"""

    
    def __init__(self, optimizer: Optimizer):
        self._optimizer = optimizer
        self.X = np.zeros(optimizer.dimensions)
        self.O = np.zeros(optimizer.objectives) * np.nan
        self.C = np.zeros(optimizer.constraints) * np.nan
        self.f = np.nan
                    
        # Evaluation
        if self._optimizer.objectives == 1 and self._optimizer.constraints == 0:
            self._evaluate = self._eval_fast
        else:
            self._evaluate = self._eval_full
        
        # Comparison operators
        if self._optimizer.objectives == 1 and self._optimizer.constraints == 0:
            self._eq_fn = CandidateState._eq_fast
            self._lt_fn = CandidateState._lt_fast 
            #self.__gt__ = self._gt_fast
        else:
            self._eq_fn = CandidateState._eq_full
            self._lt_fn = CandidateState._lt_full 
            #self.__gt__ = self._gt_full
        
        
    def copy(self):
        
        cP = CandidateState(self._optimizer)        
        # Real copy for ndarrays
        cP.X = np.copy(self.X)
        cP.O = np.copy(self.O)
        cP.C = np.copy(self.C)
        cP.f = self.f
        return cP
    
    def __str__(self): 
        nch = np.max([np.size(self.X), np.size(self.O), np.size(self.C)]) 
        nch = np.min([8, nch])
        #print(nch)
        s = '-' * (12 * nch + nch + 20)
        
        for i in range(int(np.ceil(np.size(self.X)/nch))):
            if i == 0:
                s += '\n' + 'X: '.rjust(20)
            else:
                s += '\n' + ' ' * 20
            s += ' '.join([f'{x:12.5e}' for x in self.X[i*nch:(i+1)*nch]])
        
        """
        s += '\n' + 'Objectives: '.rjust(20) + ' '.join([f'{o:12.5e}' for o in self.O]) + \
             '\n' + 'Constraints: '.rjust(20) + ' '.join([f'{c:12.5e}' for c in self.C]) + \
        """
        alllbl = self._optimizer.objective_labels + self._optimizer.constraint_labels
        lblchr = np.max([len(lbl) for lbl in alllbl]) + 3
        for o, olbl in zip(self.O, self._optimizer.objective_labels):
            s += '\n' + f'{olbl}: '.rjust(lblchr) + f'{o:12.5e}' 
        for c, clbl in zip(self.C, self._optimizer.constraint_labels):
            s += '\n' + f'{clbl}: '.rjust(lblchr) + f'{c:12.5e}' 
        s += '\n' + 'Fitness: '.rjust(lblchr) + f'{self.f:12.5e}' + \
             '\n' + '-' * (12 * nch + nch + 20)
        return s
    
    # Equality operator
    def __eq__(self, other): 
        return self._eq_fn(self, other) 
    
    @staticmethod
    def _eq_fast(a, b): 
        return a.f == b.f

    @staticmethod
    def _eq_full(a, b):
        return np.sum(np.abs(a.X - b.X)) + np.sum(np.abs(a.O - b.O)) + np.sum(np.abs(a.C - b.C)) == 0.0

    # Inequality operator
    def __ne__(self, other):
        return self.f != other.f
        #return not self.__eq__(other)
    
    # Less-then operator
    def __lt__(self, other):
        return self._lt_fn(self, other)    

    def evaluate(self, s=None):
        return self._evaluate(s)

    @staticmethod
    def _lt_fast(a, b): 
        #print('_lt_fast')
        return a.f < b.f   
    
    @staticmethod     
    def _lt_full(a, b):  
        #print("_lt_full")               
        if np.sum(a.C > 0) == 0 and np.sum(b.C > 0) == 0: 
            # Both are feasible
            # Better candidate is the one with smaller fitness
            return a.f < b.f
        
        elif np.sum(a.C > 0) == np.sum(b.C > 0): 
            # Both are unfeasible and break same number of constraints
            # Better candidate is the one with smaller sum of constraint values
            return np.sum(a.C) < np.sum(b.C)
        
        else:
            # The number of unsatisfied constraints is not the same
            # Better candidate is the one which breaks fewer constraints
            return np.sum(a.C > 0) < np.sum(b.C > 0)
       
    
    def __gt__(self, other):
        #print('__gt__')
        #return self.f > other.f
        return not (self._lt_fn(self, other) or self._eq_fn(self, other))
    """
    def _gt_fast(self, other):
        return self.f > other.f
    def _gt_full(self, other): 
        return not (self.__eq__(other) or self.__lt__(other))
    """    
    
    def __le__(self, other):
        #print('__le__')
        #return self.f <= other.f
        return self._lt_fn(self, other) or self.__eq__(other)
    
    def __ge__(self, other):
        #print('__ge__')
        #return self.f >= other.f
        return self.__gt__(other) or self.__eq__(other)
    
    
    def set_X(self, X: np.ndarray):
        assert np.size(self.X) == np.size(X), 'Unexpected size of optimization vector X'
        self.X = X
        
    def _eval_full(self, s=None):
        
        #print('_eval_full')
        #print(self.X.shape)
        if s is None:
            oc = self._optimizer.evaluation_function(self.X)
        else:
            oc = self._optimizer.evaluation_function(self.X, s)
        #print(f'{self.X=}')
        #print(f'{oc=}')

        for io in range(self._optimizer.objectives):
            self.O[io] = oc[io]
        
        self.f = np.dot(self.O, self._optimizer.objective_weights)
        
        for ic in range(self._optimizer.constraints):
            self.C[ic] = oc[self._optimizer.objectives + ic]

        #print('_eval_full', self.X[:5], self.f)
        return self.O, self.C, self.f
        
    def _eval_fast(self, s=None):

        if s is None:
            f = self._optimizer.evaluation_function(self.X)
        else:
            f = self._optimizer.evaluation_function(self.X, s)

        self.f = f
        self.O[0] = f 
        #print('_eval_fast', self.f, type(self.f))
        #input(' >> Press return to continue.')
        return self.O, self.C, self.f

class OptimizationRecord(CandidateState):
    
    def __init__(self, optimizer: Optimizer):
        super(OptimizationRecord, self).__init__(optimizer)        
        self.evaluation = None

class OptimizationResults:
    """Data holder for optimization results."""
    
    def __init__(self, optimizer: Optimizer):
        
        self.optimizer = optimizer
        self.cHistory = []
        
    def plot_convergence(self, axes=None):
        
        if axes is None:
            fig = plt.figure(constrained_layout=True)
            spec = gridspec.GridSpec(ncols=1, nrows=2, figure=fig)
            axo = fig.add_subplot(spec[0])
            axc = fig.add_subplot(spec[1], sharex=axo)
        else:
            axo, axc = axes
        
        for io in range(self.optimizer.objectives):
            O = np.array([cB.O[io] for cB in self.cHistory])
            axo.plot(np.arange(np.size(O)), O, label=self.optimizer.objective_labels[io], lw=1)
            
        F = np.array([cB.f for cB in self.cHistory])
        axo.plot(np.arange(np.size(F)), F, label='f', lw=2, ls='-', c='b')
         
        axo.legend()
        
        for ic in range(self.optimizer.constraints):
            C = np.array([cB.C[ic] for cB in self.cHistory])
            I = np.arange(np.size(C))
            axc.plot(I, C, label=self.optimizer.constraint_labels[ic], lw=1)
            
            I = I[C > 0]
            C = C[C > 0]
            
            nc = np.sum(C>0)
            axc.plot(I[:nc], C[:nc], c='r', ls='-', lw=2)
            if nc == 1:
                axc.plot(I[:nc], C[:nc],'ro')
                
            
        axc.legend()
        
        axo.set_ylabel('Objectives')
        axc.set_xlabel('Iterations')
        axc.set_ylabel('Constraints')
        #ax.set_yscale('log')
        
        