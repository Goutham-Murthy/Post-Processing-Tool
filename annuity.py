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
        Annuity class for finding the annuity of the various technologies according to VDI 2067.

         Contains common functions and variables needed for calculation of the annuities. set_annuity is an abstract
         method which is implemented in the child classes and is different for each technology.

        :param deperiod: (float)Number of years of the depreciation period [years]
        :param effop: (float)Effort for operation [hours/annum]
        :param fwins: (float)Effort for annual maintenance and inspection as percentage of initial investment [%]
        :param finst: (float)Effort for annual repairs as percentage of initial investment [%]
        :param obperiod: (float)Number of years of the observation period [years]
        :param q: (float)Interest-rate factor [-]
        :param r: (float)Price change factor [-]
        :param gas_price: (float)Price of gas per kWh [Euro/kWh]
        :param electricity_price: (float)Price of electricity per kWh imported from grid [Euro/kWh]
        :return: none
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

    def set_ank(self):
        """
        Calculates the annuity of the capital related costs according to VDI 2067

        :param: none
        :return: none
        """
        a = [0]
        # n: number of replacements procured within the observation period
        n = int(math.floor(self.obperiod/self.deperiod))
        # Cash of the 1st, 2nd.. nth procured replacement are calculated and
        # stored in a A
        for i in range(1, n+1):
            a.append(self.A0 * (self.r**(i * self.deperiod)) /
                     (self.q**(i*self.deperiod)))
        an = self.A0
        for i in range(0, n+1):
            an += a[i]
        # Rw is the residual value of the last procurement
        rw = self.A0 * self.r**(n * self.deperiod) * \
            ((n + 1) * self.deperiod - self.obperiod)/(self.deperiod *
                                                       self.q**self.obperiod)
        self.Ank = (an - rw)*self.a
        return

    def get_b(self, r):
        """
        Calculates the price dynamic cash value factor

        :param r: (float)Price change factor [-]
        :return: b: (float)Price dynamic cash value factor [-]
        """
        b = (1-(r/self.q)**self.obperiod)/(self.q-r)
        return b

    @abc.abstractmethod
    def set_annuity(self):
        """
        Abstract class to be implemented in the child classes

        :return: none
        """
        pass
