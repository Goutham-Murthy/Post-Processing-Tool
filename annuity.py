# -*- coding: utf-8 -*-
import math


#annuity factor as defined by VDI 2067
def get_annuity_factor(q,obperiod):
    a = (q-1)/(1-q**(-obperiod))
    return a
    
#For getting the anuuity    
def get_Ank(A0,r,q,obperiod,deperiod):
    a = get_annuity_factor(q,obperiod)
    A = [0] 
    n = int(math.floor(obperiod/deperiod))
    for i in range (1,n+1):
        A.append(A0*(r**(i*deperiod))/(q**(i*deperiod)))
    An = A0
    for i in range (0,n+1):
        An = An + A[i] 
    Rw = A0*r**(n*deperiod)*((n+1)*deperiod-obperiod)/(deperiod*q**obperiod)
    Ank = (An-Rw)*a
    return Ank

def get_b(r,q,obperiod):
    b = (1-(r/q)**obperiod)/(q-r)
    return b