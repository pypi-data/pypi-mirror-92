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
        self.assertEqual( t0, 0 )
        t1 = t.get_time()
        self.assertLess( t0, t1 )
        t2 = t.stop()
        self.assertLess( t1, t2 )

        t3 = t.get_time()
        self.assertEqual( t2, t3 )
        t.start()
        t4 = t.get_time()
        self.assertLess( t3, t4 )

        t.reset()
        t5 = t.get_time()
        self.assertEqual( t5, 0 )

###################################################################
    def test_watchdogtimer(self):
        def add1( x, y=1 ):
            return x+y
        def add2( x, y=0 ):
            return x+y

        wdt = WatchDogTimer( 0.2, add1, 1 )
        wdt_stop = WatchDogTimer( 0.2, add1, 1 )
        wdt.start()
        wdt_stop.start()
        wdt_stop.stop()

        for i in range(5):
            wdt.feed()
            time.sleep(0.1)
        self.assertFalse( wdt.is_timeout )
        time.sleep(0.2)
        self.assertEqual( wdt.ret, 2 )
        self.assertFalse( wdt_stop.is_timeout )

        wdt = WatchDogTimer( 0.1, add1, x=1 )
        wdt.start()
        wdt.set_callback( add2, 2, y=2 )
        time.sleep(0.1)
        self.assertEqual( wdt.ret, 4 )

###################################################################
    def test_periodic(self):
        def add( x, y=1, sleep=0.1 ):
            time.sleep(sleep)
            return x+y

        prd = Periodic( 0.2, add, 1 )
        prd.start()

        time.sleep( 0.15 )
        self.assertEqual( prd.ret, 2 )
        prd.set_callback( add, 2 )
        time.sleep( 0.15 )
        self.assertEqual( prd.ret, 3 )

        prd.stop()


###################################################################
    def suite():
        suite = unittest.TestSuite()
        suite.addTests(unittest.makeSuite(tests))
        return suite

if( __name__ == '__main__' ):
    unittest.main()
