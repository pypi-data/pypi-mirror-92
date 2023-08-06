WDT
===

Watch Dog Timer and Timer for python

`Github <https://github.com/mastnk/WDT/>`__
`PyPI <https://pypi.org/project/WDT/>`__

Instalation
-----------

``% pip install WDT``

*class* WatchDogTimer
---------------------

The WatchDogTimer is used to invoke a callback function when the timeout
happens. After starting the WatchDogTimer, the application need "feed"
the WatchDogTimer periodically if you want to prevent to invoke the
callback.

If you do not "feed", the callback function would be invoked after the
setting time from the last "feed".

Methods
~~~~~~~

-  **init**\ ( self, callback, args\_dict={}, time\_sec=1, daemon=True )

   **callback**: a function or a functor,

   **args\_dict**: an arguemnts of the function in the dictionary
   format,

   **time\_sec**: a setting time,

   **daemon**: If it is true, the thread is daemonized.

-  start( self ) -> None

   Start the WatchDogTimer.

-  stop( self ) -> None

   Stop the WatchDogTimer. The callback function is not invoked.

-  feed( self ) -> None

   Feed to the WatchDogTimer.

-  set\_callback( self, callback=None, args\_dict=None ) -> None

   Change the *callback* and the *args\_dict* if they are not None.

-  set\_time\_sec( self, time\_sec ) -> None

   Change the *time\_sec*.

Variables
~~~~~~~~~

-  ret

   It holds a retun velue of the callback function. If the callback
   function is not invoked, it is *None*.

-  is\_timeout

   It is boolean which represents the WatchDogTimer is timeout or not.

*class* PerfTimer
-----------------

It is a timer to measure the time with time.perf\_counter.

Methods
~~~~~~~

-  **init**\ ( self )

   The constructor

-  start( self ) -> None

   Start the timer.

-  stop( self ) -> float

   Stop the timer. It return the time in seconds.

-  reset( self )

   It reset the accumulate time to zero.

-  restart( self )

   Reset and start.

-  get\_time( self ) -> float

   Return the time.

Sample code
-----------

.. code:: python

    from WDT import *

    import time

    def callback_func1( x ):
        y = x+1
        print( 'func1: ', x, '->', y )
        return y

    pt0 = PerfTimer()
    pt1 = PerfTimer()

    # the callback is not invoked because wdt is feed before timeout
    pt0.start()
    pt1.start()
    print( 'Sample1' )
    wdt = WatchDogTimer( callback_func1, {'x':1}, 0.2 )
    wdt.start()
    for i in range(5):
        wdt.feed()
        time.sleep(0.1)
    wdt.stop()
    pt0.stop()
    pt1.stop()
    print( pt0.get_time(), pt1.get_time() )

    # invoke callback after some seconds
    pt0.restart()
    pt1.start()
    print( 'Sample2' )
    wdt = WatchDogTimer( callback_func1, {'x':1}, 0.2 )
    wdt.start()
    time.sleep(0.3)
    pt0.stop()
    pt1.stop()
    print( pt0.get_time(), pt1.get_time() )

    ###
    pt0.restart()
    pt1.start()
    print( 'Sample3' )
    wdt = WatchDogTimer( callback_func1, {'x':1}, 0.2 )
    wdt.start()
    for i in range(5):
        wdt.feed()
        wdt.set_callback( None, {'x':i} )
        time.sleep(0.1)
    time.sleep(0.3)
    pt0.stop()
    pt1.stop()
    print( pt0.get_time(), pt1.get_time() )


