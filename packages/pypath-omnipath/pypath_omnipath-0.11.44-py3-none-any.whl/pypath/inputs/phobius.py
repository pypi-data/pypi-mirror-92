#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#  This file is part of the `pypath` python module
#  Helps to translate from the mouse data to human data
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

import re
import collections

import pypath.share.curl as curl
import pypath.resources.urls as urls


def phobius_annotations():
    
    rewrongtab = re.compile(r'(\t[A-Z\d]+_[A-Z]+)\t([A-Z]+)\s+(\d)')
    
    PhobiusAnnotation = collections.namedtuple(
        'PhobiusAnnotation',
        [
            'tm_helices',
            'signal_peptide',
            'cytoplasmic',
            'non_cytoplasmic',
        ]
    )
    
    url = urls.urls['phobius']['url']
    
    c = curl.Curl(url, silent = False, large = True)
    
    _ = next(c.result)
    
    result = collections.defaultdict(set)
    
    for line in c.result:
        
        line = rewrongtab.sub(r'\1\2\t\3', line)
        line = line.strip().split('\t')
        
        result[line[1]].add(
            PhobiusAnnotation(
                tm_helices = int(line[3]),
                signal_peptide = line[4] == 'Y',
                cytoplasmic = line[5].count('i'),
                non_cytoplasmic = line[5].count('o'),
            )
        )
    
    return dict(result)
