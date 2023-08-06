#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#  This file is part of the `pypath` python module
#
#  Copyright
#  2014-2021
#  EMBL, EMBL-EBI, Uniklinik RWTH Aachen, Heidelberg University
#
#  File author(s): Dénes Türei (turei.denes@gmail.com)
#                  Nicolàs Palacio
#                  Olga Ivanova
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  Website: http://pypath.omnipathdb.org/
#

import pypath.share.curl as curl
import pypath.resources.urls as urls


def abs_interactions():
    """
    TF-target (transcriptional regulation) interactions from the ABS
    database.
    """

    result = []
    url = urls.urls['abs']['url']
    c = curl.Curl(url, silent = False)
    data = c.result
    data = [[x.replace('*', '') for x in xx.split('\t')]
            for xx in data.split('\n')]

    for d in data:

        if len(d) > 2:

            result.append([d[2], d[0]])

    return result
