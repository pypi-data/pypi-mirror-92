#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#
#  This file is part of the `pypath` python module
#
#  Copyright (c) 2014-2015 - EMBL-EBI
#
#  File author(s): Dénes Türei (denes@ebi.ac.uk)
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  Website: http://www.ebi.ac.uk/~denes
#

#
# Thanks for https://github.com/tanghaibao/goatools,
# I learned many ideas used for this module from there!
# However I needed something different, so I wrote an
# almost new one, copying only some at points from goatools.
#

import sys

try:
    import fisher
except:
    sys.stdout.write('\t:: No module `fisher` available.\n')

import statsmodels.stats.multitest as smm
from collections import OrderedDict


class Enrichment(object):
    def __init__(self, set_count, pop_count, set_size, pop_size, data):
        for k, v in locals().iteritems():
            setattr(self, k, v)
        self.pvalue = fisher.pvalue_population(set_count, set_size, pop_count,
                                               pop_size).right_tail

    def significant(self, level=0.05):
        return self.pvalue <= level


class EnrichmentSet(object):
    def __init__(self, data, pop_size, correction_method='hommel', alpha=0.05):
        '''
        @data : dict
        This is a dict with unique labels as keys, lists/tuples as
        values, having set_count, pop_count, set_size as their first 
        3 elements, and nothing or anything behind that.
        E.g. {'Microtubule assembly': (45, 89, 367, ...), ...}
        '''
        for k, v in locals().iteritems():
            setattr(self, k, v)
        self.enrichments = OrderedDict(
            sorted(
                [(name, Enrichment(
                    vals[0], vals[1], vals[2], self.pop_size, data=vals[3:]))
                 for name, vals in data.iteritems()],
                key=lambda x: x[0]))
        self.correction(method=correction_method, alpha=alpha)

    def correction(self, method='hommel', alpha=None):
        if alpha is None:
            alpha = self.alpha
        pvals_corr = smm.multipletests(
            [enr.pvalue for enr in self.enrichments.values()],
            alpha=alpha,
            method=method)[1]
        for i, k in zip(xrange(len(pvals_corr)), self.enrichments.keys()):
            setattr(self.enrichments[k], 'pval_adj', pvals_corr[i])

    def toplist(self,
                length=None,
                alpha=None,
                significant=True,
                min_set_size=0,
                filtr=lambda x: True):
        if alpha is None:
            alpha = self.alpha
        # siglen = len([1 for e in self.enrichments.values() if e.pval_adj <= alpha])
        # length = siglen if length is None else min(length, siglen) if significant else length
        return OrderedDict(
            sorted(
                [(k, e) for k, e in self.enrichments.iteritems()
                 if (not significant or e.pval_adj <= alpha) and e.set_size >
                 min_set_size and filtr((k, e))],
                key=lambda x: x[1].pval_adj)[:length])

    def top_names(self,
                  length=None,
                  significant=True,
                  alpha=0.05,
                  min_set_size=0,
                  filtr=lambda x: True,
                  **kwargs):
        args = get_args(locals())
        return [t.data[0] for t in self.toplist(**args).values()]

    def top_ids(self,
                length=None,
                significant=True,
                alpha=0.05,
                min_set_size=0,
                filtr=lambda x: True,
                **kwargs):
        args = get_args(locals())
        return self.toplist(**args).keys()
