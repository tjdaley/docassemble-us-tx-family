"""
objects.py - Objects used in the us-tx-family pacakge.

Copyright (c) 2019 by Thomas J. Daley, J.D. All Rights Reserved.
"""
from docassemble.base.util import DAList, DAObject, PeriodicValue, word

__all__ = ['Job', 'JobList', 'Income', 'IncomeList']

class JobList(DAList):
    def init(self, *pargs, **kwargs):
        self.object_type = Job
        self.complete_attribute = 'job_complete'
        self.there_are_any = False
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
            self.initializeAttribute('income', PeriodicValue)
        if 'union_dues' not in kwargs:
            self.initializeAttribute('union_dues', PeriodicValue)
        super(Job, self).init(*pargs, **kwargs)

    def summary(self):
        s = self.employer + ' ' + word('earning') + ' ' + self.income.value + ' ' + word('per') + ' ' + word(self.income.period)
        if self.self_employed:
            return word('Self-employed') + ' ' + word('d/b/a') + ' ' + s
        return s

    @property
    def job_complete(self):
        self.employer
        self.self_employed
        self.income
        self.union_dues

    def __unicode__(self):
        return self.summary()


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
            self.initializeAttribute('income', PeriodicValue)
        if 'is_taxable' not in kwargs:
            self.is_taxable = False
        if 'type' not in kwargs:
            self.type = None
        super(Income, self).init(*pargs, **kwargs)

    def summary(self):
        s = self.description + ' ' + word('earning') + ' ' + self.income.value + ' ' + word('per') + ' ' + word(self.income.period)
        if self.is_taxable:
            return s + " (" + word('taxable') + ")"
        return s

    @property
    def job_complete(self):
        self.description
        self.income
        self.is_taxable
        self.type

    def __unicode__(self):
        return self.summary()


class IncomeList(DAList):
    def init(self, *pargs, **kwargs):
        self.object_type = Income
        self.complete_attribute = 'job_complete'
        super(IncomeList, self).init(*pargs, **kwargs)

