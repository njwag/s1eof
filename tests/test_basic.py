import unittest
import tempfile
import utils.utils as utils
import os
from datetime import datetime
from os.path import join

class s1eoftest(unittest.TestCase):
    
    def setUp(self):
        """Runs before each test."""
        self.download_dates = [['1A',datetime(2015, 12, 31, 0, 0),datetime(2016, 1, 2, 0, 0)]]
        self.start = '2016-01-01'
        self.end = '2016-01-01'
        self.existing = [['1A',
                           datetime(2019, 12, 26, 0, 0),
                           datetime(2019, 12, 28, 0, 0)],
                          ['1B',
                           datetime(2017, 6, 4, 0, 0),
                           datetime(2017, 6, 6, 0, 0)]]
        self.url = ['https://scihub.copernicus.eu/gnss/search?q=(platformname:Sentinel-1 AND producttype:AUX_POEORB AND platformserialidentifier:1A AND beginposition:[2015-12-31T00:00:00.000Z TO 2015-12-31T23:59:59.000Z] AND endposition:[2016-01-02T00:00:00.000Z TO 2016-01-02T23:59:59.000Z])']
        self.url_dr = 'https://scihub.copernicus.eu/gnss/search?q=(platformname:Sentinel-1 AND producttype:AUX_POEORB AND beginposition:[2015-12-31T00:00:00.000Z TO 2015-12-31T23:59:59.000Z] AND endposition:[2016-01-02T00:00:00.000Z TO 2016-01-02T23:59:59.000Z])&rows=100'
        self.orbits = [['S1A_OPER_AUX_POEORB_OPOD_20210310T034742_V20151231T225943_20160102T005943.EOF',"https://scihub.copernicus.eu/gnss/odata/v1/Products('a764fd8f-7012-4d8f-9643-298ce806ff8b')/$value"]]

    def test_check_existing(self):
     """Test that file names are read correctly"""    
     with tempfile.TemporaryDirectory() as temp_dir:
         zipfile = tempfile.NamedTemporaryFile(dir=temp_dir)
         safefile = tempfile.NamedTemporaryFile(dir=temp_dir)
         zipname = join(temp_dir,'S1A_IW_SLC__1SDV_20191227T121253_20191227T121320_030534_037F23_5899.zip')
         safename = join(temp_dir,'S1B_IW_SLC__1SDV_20170605T120333_20170605T120354_005915_00A5F6_834E.SAFE')
         os.rename(zipfile.name,zipname)
         os.rename(safefile.name,safename)
         self.assertCountEqual(utils.check_existing(temp_dir), self.existing, "error check_existing")

    def test_get_urls(self):
        self.assertEqual(utils.get_urls(self.download_dates), self.url, "error get_urls")
        
    def test_get_urls_daterange(self):
        self.assertEqual(utils.get_urls_daterange(self.start,self.end), self.url_dr, "error get_urls_daterange")

    def test_get_orbits(self):
        self.assertEqual(utils.get_orbits(self.url), self.orbits, "error get_orbits")
        
    def test_get_orbits_daterange(self):
        self.assertEqual(utils.get_orbits(self.url_dr,daterange=True), self.orbits, "error get_orbits daterange")

if __name__ == '__main__':
    suite = unittest.makeSuite(s1eoftest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    
