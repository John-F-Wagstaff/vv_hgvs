# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

from nose.plugins.attrib import attr

from hgvs.exceptions import HGVSUnsupportedNormalizationError
import hgvs.dataproviders.uta
import hgvs.variantmapper
import hgvs.parser
import hgvs.normalizer

hdp = hgvs.dataproviders.uta.connect()


@attr(tags=["normalization"])
class Test_HGVSNormalizer(unittest.TestCase):
    """Tests for normalizer"""

    def setUp(self):
        self.hp = hgvs.parser.Parser()
        self.norm   = hgvs.normalizer.Normalizer(hdp)
        self.norm5  = hgvs.normalizer.Normalizer(hdp, direction=5)
        self.normf  = hgvs.normalizer.Normalizer(hdp, direction=3, fill=False)
        self.normc  = hgvs.normalizer.Normalizer(hdp, direction=3, cross=False)
        self.norm5c = hgvs.normalizer.Normalizer(hdp, direction=5, cross=False)

    def test_c_normalizer(self):
        """Test normalizer for variant type c."""
        #3' shuffling
        self.assertEqual( str(self.norm.normalize(self.hp.parse_hgvs_variant('NM_001166478.1:c.31del')))  ,'NM_001166478.1:c.35delT')
        self.assertEqual( str(self.norm.normalize(self.hp.parse_hgvs_variant('NM_001166478.1:c.35_36insT')))  ,'NM_001166478.1:c.35dupT')
        self.assertEqual( str(self.norm.normalize(self.hp.parse_hgvs_variant('NM_001166478.1:c.36_37insTC')))  ,'NM_001166478.1:c.36_37dupCT')
        self.assertEqual( str(self.norm.normalize(self.hp.parse_hgvs_variant('NM_001166478.1:c.35_36dup')))  ,'NM_001166478.1:c.36_37dupCT')
        self.assertEqual( str(self.norm.normalize(self.hp.parse_hgvs_variant('NM_001166478.1:c.2_7delinsTTTAGA')))  ,'NM_001166478.1:c.3_4delGAinsTT')
        self.assertEqual( str(self.norm.normalize(self.hp.parse_hgvs_variant('NM_001166478.1:c.30_31insT')))  ,'NM_001166478.1:c.35dupT')
        self.assertEqual( str(self.norm.normalize(self.hp.parse_hgvs_variant('NM_001166478.1:c.59delG')))  ,'NM_001166478.1:c.61delG')
        
        #5' shuffling
        self.assertEqual( str(self.norm5.normalize(self.hp.parse_hgvs_variant('NM_001166478.1:c.34del')))  ,'NM_001166478.1:c.31delT')
        self.assertEqual( str(self.norm5.normalize(self.hp.parse_hgvs_variant('NM_001166478.1:c.35_36insT')))  ,'NM_001166478.1:c.31dupT')
        self.assertEqual( str(self.norm5.normalize(self.hp.parse_hgvs_variant('NM_001166478.1:c.36_37insTC')))  ,'NM_001166478.1:c.35_36dupTC')
        self.assertEqual( str(self.norm5.normalize(self.hp.parse_hgvs_variant('NM_001166478.1:c.35_36dup')))  ,'NM_001166478.1:c.35_36dupTC')
        self.assertEqual( str(self.norm5.normalize(self.hp.parse_hgvs_variant('NM_001166478.1:c.2_7delinsTTTAGA')))  ,'NM_001166478.1:c.3_4delGAinsTT')
        self.assertEqual( str(self.norm5.normalize(self.hp.parse_hgvs_variant('NM_001166478.1:c.30_31insT')))  ,'NM_001166478.1:c.31dupT')
        self.assertEqual( str(self.norm5.normalize(self.hp.parse_hgvs_variant('NM_001166478.1:c.61delG')))  ,'NM_001166478.1:c.59delG')
        
        #No fill
        self.assertEqual( str(self.normf.normalize(self.hp.parse_hgvs_variant('NM_001166478.1:c.31del')))  ,'NM_001166478.1:c.35del')
        self.assertEqual( str(self.normf.normalize(self.hp.parse_hgvs_variant('NM_001166478.1:c.35_36insT')))  ,'NM_001166478.1:c.35dup')
        self.assertEqual( str(self.normf.normalize(self.hp.parse_hgvs_variant('NM_001166478.1:c.36_37insTC')))  ,'NM_001166478.1:c.36_37dup')
        self.assertEqual( str(self.normf.normalize(self.hp.parse_hgvs_variant('NM_001166478.1:c.35_36dup')))  ,'NM_001166478.1:c.36_37dup')
        self.assertEqual( str(self.normf.normalize(self.hp.parse_hgvs_variant('NM_001166478.1:c.2_7delinsTTTAGA')))  ,'NM_001166478.1:c.3_4delinsTT')
        self.assertEqual( str(self.normf.normalize(self.hp.parse_hgvs_variant('NM_001166478.1:c.30_31insT')))  ,'NM_001166478.1:c.35dup')
        
        #Around exon-intron boundary
        self.assertEqual( str(self.normc.normalize(self.hp.parse_hgvs_variant('NM_001166478.1:c.59delG')))  ,'NM_001166478.1:c.60delG')
        self.assertEqual( str(self.norm5c.normalize(self.hp.parse_hgvs_variant('NM_001166478.1:c.61delG')))  ,'NM_001166478.1:c.61delG')
        self.assertRaises(HGVSUnsupportedNormalizationError, self.normc.normalize, self.hp.parse_hgvs_variant('NM_001166478.1:c.59_61del'))
    





if __name__ == '__main__':
    unittest.main()

## <LICENSE>
## Copyright 2015 HGVS Contributors (https://bitbucket.org/biocommons/hgvs)
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
## </LICENSE>
