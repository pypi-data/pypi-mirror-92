#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import time

from WDT import *

class tests( unittest.TestCase ):
###################################################################
    @classmethod
    def setUpClass(cls): # it is called before test starting
        pass

    @classmethod
    def tearDownClass(cls): # it is called before test ending
        pass

    def setUp(self): # it is called before each test
        pass

    def tearDown(self): # it is called after each test
        pass

###################################################################
    def test_perftimer(self):
        t = PerfTimer()
        t0 = t.get_time()
        t.start()
        self.assertTrue( t0 == 0 )
        t1 = t.get_time()
        self.assertTrue( t0 < t1 )
        t2 = t.stop()
        self.assertTrue( t1 < t2 )

        t3 = t.get_time()
        self.assertTrue( t2 == t3 )
        t.start()
        t4 = t.get_time()
        self.assertTrue( t3 < t4 )

        t.reset()
        t5 = t.get_time()
        self.assertTrue( t5 == 0 )

    def test_watchdogtimer(self):
        def add1( x ):
            return x+1
        def add2( x ):
            return x+2

        wdt = WatchDogTimer( add1, {'x':1}, 0.2 )
        wdt_stop = WatchDogTimer( add1, {'x':1}, 0.2 )
        wdt.start()
        wdt_stop.start()
        wdt_stop.stop()

        for i in range(5):
            wdt.feed()
            time.sleep(0.1)
        self.assertFalse( wdt.is_timeout )
        time.sleep(0.2)
        self.assertTrue( wdt.ret == 2 )
        self.assertFalse( wdt_stop.is_timeout )

        wdt = WatchDogTimer( add1, {'x':1}, 0.1 )
        wdt.start()
        wdt.set_callback( add2, {'x':2} )
        time.sleep(0.1)
        self.assertTrue( wdt.ret == 4 )


###################################################################
    def suite():
        suite = unittest.TestSuite()
        suite.addTests(unittest.makeSuite(tests))
        return suite

if( __name__ == '__main__' ):
    unittest.main()
