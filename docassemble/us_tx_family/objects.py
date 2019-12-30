"""
objects.py - Objects used in the us-tx-family pacakge.

Copyright (c) 2019 by Thomas J. Daley, J.D. All Rights Reserved.
"""
from decimal import Decimal

from docassemble.base.util import DAList, DAObject, PeriodicValue, word

__all__ = ['Job', 'JobList', 'Income', 'IncomeList']

class MyPeriodicValue(PeriodicValue):
    def init(self, *pargs, **kwargs):
        self.exists = True
        super(MyPeriodicValue, self).init(*pargs, **kwargs)

class JobList(DAList):
    def init(self, *pargs, **kwargs):
        self.object_type = Job
        self.complete_attribute = 'job_complete'
        super(JobList, self).init(*pargs, **kwargs)


class Job(DAObject):
    """
    A Job is an income stream through employment and is subject to
    payroll taxes and possibley union dues. It is also subject to
    income taxes.
    """
    def init(self, *pargs, **kwargs):
        if 'self_employed' not in kwargs:
            self.self_employed = False
        if 'employer' not in kwargs:
            self.employer = None
        if 'income' not in kwargs:
            self.initializeAttribute('income', MyPeriodicValue)
        if 'union_dues' not in kwargs:
            self.initializeAttribute('union_dues', MyPeriodicValue)
        super(Job, self).init(*pargs, **kwargs)

    def summary(self):
        return self.employer or "**NONE**"

    @property
    def job_complete(self):
        self.employer
        self.self_employed
        self.income
        self.union_dues

    def __unicode__(self):
        return self.summary()


class IncomeList(DAList):
    def init(self, *pargs, **kwargs):
        self.object_type = Income
        self.complete_attribute = 'income_complete'
        super(IncomeList, self).init(*pargs, **kwargs)


class Income(DAObject):
    """
    An Income is an income stream other than through employment and
    is NOT subject to payroll taxes nor union dues. It is might be
    subject to income taxes.
    """
    def init(self, *pargs, **kwargs):
        if 'description' not in kwargs:
            self.description = None
        if 'income' not in kwargs:
            self.initializeAttribute('income', MyPeriodicValue)
        if 'is_taxable' not in kwargs:
            self.is_taxable = False
        if 'type' not in kwargs:
            self.type = None
        super(Income, self).init(*pargs, **kwargs)

    def summary(self):
        return self.description or "**NONE**"

    @property
    def income_complete(self):
        self.description
        self.income
        self.is_taxable
        self.type

    def __unicode__(self):
        return self.summary()
