"""Raup's model"""

# Author: Koji Noshita <noshita@morphometrics.jp>
# License: ISC

import numpy as np
import sympy as sym

from ..base import GeneratingCurveModel, SimulatorMixin, EqnsMixin

class RaupModelSimulator(GeneratingCurveModel, SimulatorMixin):
    def __init__(self, W = 10**0.2, T = 1.5, D = 0.1, S = 1, r0 = 1):
        self.W = W
        self.T = T
        self.D = D
        self.S = S
        self.r0 = r0
        
    def _generate_generating_spiral(self, theta: float, **params):
        
        W = params.get("W") if params.get("W") else self.W
        T = params.get("T") if params.get("T") else self.T
        D = params.get("D") if params.get("D") else self.D
        r0 = params.get("r0") if params.get("r0") else self.r0
        
        w = r0*W**(theta/(2*np.pi))
        px = w * (2*D/(1 - D) + 1 )*np.cos(theta)
        py = w * (2*D/(1 - D) + 1 )*np.sin(theta)
        pz = w * 2*T*(D/(1 - D) + 1)
        
        return px, py, pz
    
    def compute_generating_spiral(self, theta: float, **params):
        return self._generate_generating_spiral(theta, **params)
            
    def compute(self, theta: float, phi: float, **params):
        """
        
        """

        W = params.get("W") if params.get("W") else self.W
        T = params.get("T") if params.get("T") else self.T
        D = params.get("D") if params.get("D") else self.D
        S = params.get("S") if params.get("S") else self.S
        r0 = params.get("r0") if params.get("r0") else self.r0

        w = r0*W**(theta/(2*np.pi))
        
        X = w * (2*D/(1 - D) + 1 + np.cos(phi))*np.cos(theta)
        Y = w * (2*D/(1 - D) + 1 + np.cos(phi))*np.sin(theta)
        Z = w * (2*T*(D/(1 - D) + 1) + np.sin(phi)/S)
        
        return X, Y, Z

class RaupModelEqns(GeneratingCurveModel, EqnsMixin):
    def __init__(self, 
                 W = sym.Symbol("W"), T = sym.Symbol("T"), D = sym.Symbol("D"), S = sym.Symbol("S"), 
                 r0 = sym.Symbol("r_0"), theta = sym.Symbol("theta"), phi = sym.Symbol("phi")):
        self.W = W
        self.T = T
        self.D = D
        self.S = S
        self.r0 = r0
        self.theta = theta
        self.phi = phi
        
        self.__definition = self._define(W = self.W, T = self.T , D = self.D, S = self.S,
                                          r0 = self.r0, theta = self.theta, phi = self.phi)
        
    def _generate_generating_spiral(self, **params):
        W = params.get("W") if params.get("W") else self.W
        T = params.get("T") if params.get("T") else self.T
        D = params.get("D") if params.get("D") else self.D
        r0 = params.get("r0") if params.get("r0") else self.r0
        theta = params.get("theta") if params.get("theta") else self.theta
        
        w = W**(theta/(2*sym.pi))
        denom = -1+D
        eqns = sym.Matrix([
            -((1+D)*r0*w*sym.cos(theta))/denom,
            -((1+D)*r0*w*sym.sin(theta))/denom,
            (2*r0*T*w)/denom
        ])
        return eqns
    
    def calculate_generating_spiral(self, **params):
        """
        Args:
        """
        return self._generate_generating_spiral(**params)
    
    @property
    def definition(self):
        return self.__definition
    
    def _define(self, **params):
        W = params.get("W") if params.get("W") else self.W
        T = params.get("T") if params.get("T") else self.T
        D = params.get("D") if params.get("D") else self.D
        S = params.get("S") if params.get("S") else self.S
        r0 = params.get("r0") if params.get("r0") else self.r0
        theta = params.get("theta") if params.get("theta") else self.theta
        phi = params.get("phi") if params.get("phi") else self.phi
        
        definition = r0 * W**(theta/(2*sym.pi)) * sym.Matrix(
            [
                [sym.cos(theta), -sym.sin(theta), 0], 
                [sym.sin(theta), sym.cos(theta), 0], 
                [0, 0, 1]
            ]) * (sym.Matrix([ sym.cos(phi), 0, (1/S)*sym.sin(phi)]) 
                  + sym.Matrix([2*D/(1-D)+1, 0, 2*T*(D/(1-D)+1)]))
        return definition
    
    def solve(self, **params):

        sol = self._define(**params)

        return sol
    
    def to_tex(self, simplified = False):
        """
        
        """
        return sym.latex(self.calculate())  