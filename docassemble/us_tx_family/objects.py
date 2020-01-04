"""
objects.py - Objects used in the us-tx-family pacakge.

Copyright (c) 2019 by Thomas J. Daley, J.D. All Rights Reserved.
"""
from decimal import Decimal

from docassemble.base.util import DAList, DAObject, PeriodicValue, word
from docassemble.base.legal import Case

__all__ = ['Job', 'JobList', 'Income', 'IncomeList']

class MyPeriodicValue(PeriodicValue):
    def init(self, *pargs, **kwargs):
        self.exists = True
        super(MyPeriodicValue, self).init(*pargs, **kwargs)


class JobList(DAList):
    def init(self, *pargs, **kwargs):
        self.object_type = Job
        self.complete_attribute = 'complete'
        super(JobList, self).init(*pargs, **kwargs)

    def total(self, desired_period: int = 12):
        """
        Returns the total value in the list, gathering the list items if necessary.

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

    @property
    def count(self) -> int:
        """
        Returns the number of jobs we have defined.
        """
        return len(self.elements)

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
        super(Job, self).init(*pargs, **kwargs)

    def summary(self):
        return self.employer or "**NONE**"

    @property
    def complete(self):
        return self.employer is not None

    def __unicode__(self):
        return self.summary()


class IncomeList(DAList):
    def init(self, *pargs, **kwargs):
        self.object_type = Income
        self.complete_attribute = 'complete'
        super(IncomeList, self).init(*pargs, **kwargs)

    def total(self, desired_period: int = 12):
        """
        Returns the total value in the list, gathering the list items if necessary.

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

    @property
    def count(self) -> int:
        """
        Returns the number of jobs we have defined.
        """
        return len(self.elements)


class Income(DAObject):
    """
    An Income is an income stream other than through employment and
    is NOT subject to payroll taxes nor union dues. It is might be
    subject to income taxes.
    """
    def init(self, *pargs, **kwargs):
        if 'income' not in kwargs:
            self.initializeAttribute('income', MyPeriodicValue)
        super(Income, self).init(*pargs, **kwargs)

    def summary(self):
        return self.description or "**NONE**"

    @property
    def complete(self):
        return self.description is not None

    def __unicode__(self):
        return self.summary()


class TexasFamilyCase(Case):
    """
    Extends docassemble's Case class, primarily to fix
    the bug in case_id_in_caption().
    """
    def init(self, *pargs, **kwargs):
        super(TexasFamilyCase, self).init(*pargs, **kwargs)

    def case_id_in_caption(self, **kwargs):
        if hasattr(self, 'case_id'):
            return word('Cause No.') + " " + self.case_id
        return word('Cause No.')