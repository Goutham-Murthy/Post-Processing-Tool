# -*- coding: utf-8 -*-
"""
This module contains the common functions needed to calculate the annuities
of various technologies. The annuities are calaculated according to the equations
given in VDI 2067. This module is to be included in each technology class, for 
example: boiler class, CHP class etc. It contains the following functions:
1) get_annuity_factor : Used to calculate the annuity factor.
2) get_Ank : used to calcualte the capital costs related annuity.
3) get_b : Used to calculate the price- dynamic cash value factor."""

import math

def get_annuity_factor(q,obperiod):
    """Calculates the annuity factor according to equations in VDI 2067.
    
    Args:
    q (float): Interest rate factor.
    obperiod (float): Number of years of the observation period.
    
    Returns:
    a (float): Annuity factor.
    """
    a = (q-1)/(1-q**(-obperiod))
    return a
    
def get_Ank(A0,r,q,obperiod,deperiod):
    """Calculates the annuity of the capital related costs according to VDI 2067
    
    Args:
    A0 (float): Initial investment amount.
    r (float): Price change factor.
    q (float): Interest rate factor.
    obperiod (float): Number of years of the observation period.
    deperiod (float): Number of years of the depreciation period.
    
    Returns:
    Ank (float): Annuity of the capital related costs
    """
    a = get_annuity_factor(q,obperiod)
    A = [0]    
    # n: number of replacements procured within the observation period
    n = int(math.floor(obperiod/deperiod))
    # Cash of the 1st, 2nd.. nth procured replacement are calcualted and stored
    # in a A
    for i in range (1,n+1):
        A.append(A0*(r**(i*deperiod))/(q**(i*deperiod)))
    An = A0
    for i in range (0,n+1):
        An = An + A[i] 
    # Rw is the residual value of the last procurement
    Rw = A0*r**(n*deperiod)*((n+1)*deperiod-obperiod)/(deperiod*q**obperiod)
    Ank = (An-Rw)*a
    return Ank

def get_b(r,q,obperiod):
    """Calculates the price dynamci cash value factor
    
    Args:
    r (float): Price change factor.
    q (float): Interest rate factor.
    obperiod (float): Number of years of the observation period.
    
    Returns:
    b (float): price dynamic cash value factor"""
    b = (1-(r/q)**obperiod)/(q-r)
    return b
