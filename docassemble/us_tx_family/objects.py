"""
objects.py - Objects used in the us-tx-family pacakge.

Copyright (c) 2019 by Thomas J. Daley, J.D. All Rights Reserved.
"""
from decimal import Decimal
from docassemble.base.logger import logmessage
from docassemble.base.util import Address, DAList, DAObject, Individual, \
    PeriodicValue, Person, word

__all__ = ['Attorney', 'AttorneyList',
           'Income', 'IncomeList',
           'Job', 'JobList',
           'LawFirm',
           'RepresentedParty',
           'RepresentedPartyList',
           'MyPeriodicValue']


class Attorney(Individual):
    def init(self, *pargs, **kwargs):
        if 'address' not in kwargs:
            self.initializeAttribute('address', Address)
        if 'firm' not in kwargs:
            self.initializeAttribute('firm', LawFirm)
        if 'client' not in kwargs:
            self.initializeAttribute('client', Individual)
        if 'bar_number' not in kwargs:
            self.initializeAttribute('bar_number', str)
            self.bar_number = ''
        return super().init(*pargs, **kwargs)


class AttorneyList(DAList):
    def init(self, *pargs, **kwargs):
        self.object_type = Attorney
        return super().init(*pargs, **kwargs)

    def contains(self, attorney):
        for atty in self.elements:
            if atty.bar_number == attorney.bar_number:
                return True
        return False


class Income(DAObject):
    """
    An Income is an income stream other than through employment and
    is NOT subject to payroll taxes nor union dues. It is might be
    subject to income taxes.
    """
    def init(self, *pargs, **kwargs):
        if 'income' not in kwargs:
            self.initializeAttribute('income', MyPeriodicValue)
        return super().init(*pargs, **kwargs)

    def summary(self):
        return self.description or "**NONE**"

    @property
    def complete(self):
        return self.description is not None

    def __unicode__(self):
        return self.summary()


class IncomeList(DAList):
    def init(self, *pargs, **kwargs):
        self.object_type = Income
        self.complete_attribute = 'complete'
        return super().init(*pargs, **kwargs)

    def total(self, desired_period: int = 12):
        """
        Returns the total value in the list, gathering the list items if
        necessary.

        Args:
            desired_period (int): 1=Annually, 12=Monthly, etc. Default=12.
        Returns:
            (Decimal): Total gross income per desired_period.
        """
        self._trigger_gather()
        result = Decimal(0)
        for item in self.elements:
            result += item.income.amount(desired_period)
        return(Decimal(result))


class Job(DAObject):
    """
    A Job is an income stream through employment and is subject to
    payroll taxes and possibley union dues. It is also subject to
    income taxes.
    """
    def init(self, *pargs, **kwargs):
        if 'income' not in kwargs:
            self.initializeAttribute('income', MyPeriodicValue)
        if 'union_dues' not in kwargs:
            self.initializeAttribute('union_dues', MyPeriodicValue)
        return super().init(*pargs, **kwargs)

    def summary(self):
        return self.employer or "**NONE**"

    @property
    def complete(self):
        return self.employer is not None

    def __unicode__(self):
        return self.summary()


class JobList(DAList):
    def init(self, *pargs, **kwargs):
        self.object_type = Job
        self.complete_attribute = 'complete'
        return super().init(*pargs, **kwargs)

    def total(self, desired_period: int = 12):
        """
        Returns the total value in the list, gathering the list items if
        necessary.

        Args:
            desired_period (int): 1=Annually, 12=Monthly, etc. Default=12.
        Returns:
            (Decimal): Total gross income per desired_period.
        """
        self._trigger_gather()
        result = Decimal(0)
        for item in self.elements:
            result += item.income.amount(desired_period)
        return(Decimal(result))


class LawFirm(Person):
    def init(self, *pargs, **kwargs):
        return super().init(*pargs, **kwargs)


class RepresentedParty(Individual):
    def init(self, *pargs, **kwargs):
        if 'attorney' not in kwargs:
            self.initializeAttribute('attorney', Attorney)
        return super().init(*pargs, **kwargs)

    def service_name(self):
        if getattr(self, 'attorney', None) is not None:
            return self.attorney.name
        return f"{self.name}, pro se"

    def service_method(self):
        if getattr(self, 'attorney', None) is not None:
            return f"Electronic service to {self.attorney.email}"
        if getattr(self, 'email', None) is not None:
            return f"Electronic service to {self.email}"
        return f"USPS Certified mail to {self.address}, Item #_______________"


class RepresentedPartyList(DAList):
    def init(self, *pargs, **kwargs):
        self.object_type = RepresentedParty
        return super().init(*pargs, **kwargs)


class MyPeriodicValue(PeriodicValue):
    def init(self, *pargs, **kwargs):
        self.exists = True
        return super().init(*pargs, **kwargs)
