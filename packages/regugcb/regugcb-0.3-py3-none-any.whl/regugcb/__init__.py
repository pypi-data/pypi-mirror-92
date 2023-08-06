# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 09:53:54 2021

@author: franc
"""


from __future__ import division

import scipy.signal as ssi
from scipy.signal.ltisys import TransferFunction as TransFun
from numpy import polymul,polyadd
import numpy as np
import scipy.interpolate as sinterpo




def apply_tf(time,u,k=1,c1=0,c2=0,theta=0):
    tf = ssi.TransferFunction([k],[np.abs(c2),np.abs(c1),1])
    _,yp,_ = ssi.lsim(tf,u,time)
    if(np.abs(theta)>0):
        fct_interp = sinterpo.interp1d(time,yp,fill_value="extrapolate")
        yp = fct_interp(time-np.abs(theta))
    return yp



def lsimd(tf,u,time,theta=0):
    a,yp,c = ssi.lsim(tf,u,time)
    if(np.abs(theta)>0):
        fct_interp = sinterpo.interp1d(time,yp,fill_value="extrapolate")
        yp = fct_interp(time-np.abs(theta))
    return a,yp,c



class ltimul(TransFun):
    
    def __neg__(self):
        return ltimul(-self.num,self.den)

    def __floordiv__(self,other):
        # can't make sense of integer division right now
        return NotImplemented

    def __mul__(self,other):
        if type(other) in [int, float]:
            return ltimul(self.num*other,self.den)
        elif type(other) in [TransFun, ltimul]:
            numer = polymul(self.num,other.num)
            denom = polymul(self.den,other.den)
            return ltimul(numer,denom)

    def __truediv__(self,other):
        if type(other) in [int, float]:
            return ltimul(self.num,self.den*other)
        if type(other) in [TransFun, ltimul]:
            numer = polymul(self.num,other.den)
            denom = polymul(self.den,other.num)
            return ltimul(numer,denom)

    def __rtruediv__(self,other):
        if type(other) in [int, float]:
            return ltimul(other*self.den,self.num)
        if type(other) in [TransFun, ltimul]:
            numer = polymul(self.den,other.num)
            denom = polymul(self.num,other.den)
            return ltimul(numer,denom)

    def __add__(self,other):
        if type(other) in [int, float]:
            return ltimul(polyadd(self.num,self.den*other),self.den)
        if type(other) in [TransFun, type(self)]:
            numer = polyadd(polymul(self.num,other.den),polymul(self.den,other.num))
            denom = polymul(self.den,other.den)
            return ltimul(numer,denom)

    def __sub__(self,other):
        if type(other) in [int, float]:
            return ltimul(polyadd(self.num,-self.den*other),self.den)
        if type(other) in [TransFun, type(self)]:
            numer = polyadd(polymul(self.num,other.den),-polymul(self.den,other.num))
            denom = polymul(self.den,other.den)
            return ltimul(numer,denom)

    def __rsub__(self,other):
        if type(other) in [int, float]:
            return ltimul(polyadd(-self.num,self.den*other),self.den)
        if type(other) in [TransFun, type(self)]:
            numer = polyadd(polymul(other.num,self.den),-polymul(other.den,self.num))
            denom = polymul(self.den,other.den)
            return ltimul(numer,denom)

    def tf(self):
        return ssi.TransferFunction(self._num,self._den)

    # sheer laziness: symmetric behaviour for commutative operators
    __rmul__ = __mul__
    __radd__ = __add__
    


