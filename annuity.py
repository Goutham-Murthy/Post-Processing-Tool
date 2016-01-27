# -*- coding: utf-8 -*-
""" Module contains the Annuity class. It consists of common functions and
variables needed to calculate the annuities of various technologies. The
annuities are calculated according to the equations given in VDI 2067.
"""
import math
import abc


class Annuity(object):
    def __init__(self, deperiod, effop, fwins, finst, obperiod=10, q=1.07,
                 r=1.03, gas_price=0.067, electricity_price=0.26):
        """

        :rtype: object: Annuity class containing annuity related parameters and variables
        """
        self.deperiod = deperiod
        self.effop = effop
        self.fwins = fwins
        self.finst = finst
        self.obperiod = obperiod
        self.q = q
        self.r = r
        # Gas price is 0.067 Euros/kWh.
        # [Eurostat. nrg_pc_205. Accessed: 2015-02-11.]
        self.gas_price = gas_price
        self.electricity_price = electricity_price
        self.b = self.get_b(self.r)
        self.bv = self.b
        self.bb = self.get_b(1.02)
        self.bi = self.b
        self.be = self.b
        self.a = (self.q-1)/(1-self.q**(-self.obperiod))
        # Initialising other variables to -1
        self.A0 = 0
        self.Ank = 0
        self.Anv = 0
        self.Anb = 0
        self.Ans = 0
        self.Ane = 0

    def set_Ank(self):
        """Calculates the annuity of the capital related costs according to VDI 2067

        Args:
            A0 (float)          : Initial investment amount.
            r (float)           : Price change factor.
            q (float)           : Interest rate factor.
            obperiod (float)    : Number of years of the observation period.
            deperiod (float)    : Number of years of the depreciation period.

        Returns:
            Ank (float): Annuity of the capital related costs
        """
        A = [0]
        # n: number of replacements procured within the observation period
        n = int(math.floor(self.obperiod/self.deperiod))
        # Cash of the 1st, 2nd.. nth procured replacement are calcualted and
        # stored in a A
        for i in range(1, n+1):
            A.append(self.A0 * (self.r**(i * self.deperiod)) /
                     (self.q**(i*self.deperiod)))
        An = self.A0
        for i in range(0, n+1):
            An = An + A[i]
        # Rw is the residual value of the last procurement
        Rw = self.A0 * self.r**(n * self.deperiod) * \
            ((n + 1) * self.deperiod - self.obperiod)/(self.deperiod *
                                                       self.q**self.obperiod)
        self.Ank = (An - Rw)*self.a
        return

    def get_b(self, r):
        """Calculates the price dynamci cash value factor

        Args:
            r (float)           : Price change factor.

        Returns:
            b (float): price dynamic cash value factor"""
        b = (1-(r/self.q)**self.obperiod)/(self.q-r)
        return b

    @abc.abstractmethod
    def set_annuity(self):
        pass
