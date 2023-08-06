import time
from threading import Thread, Event,Lock

class PerfTimer:
    def __init__( self ):
        self.reset()

    def start( self ):
        self.__start_time = time.perf_counter()

    def stop( self ):
        self.__sec += time.perf_counter() - self.__start_time
        self.__start_time = None
        return self.get_time()

    def reset( self ):
        self.__start_time = None
        self.__sec = 0

    def restart( self ):
        self.reset()
        self.start()

    def get_time( self ):
        s = self.__sec
        if( self.__start_time is not None ):
            s += time.perf_counter() - self.__start_time
        return s

class WatchDogTimer(Thread):
    def __init__( self, callback, args_dict={}, time_sec=1, daemon=True ):
        Thread.__init__(self)
        self.daemon=daemon

        self.__lock = Lock()

        self.__args_dict = args_dict
        self.__callback=callback
        self.__time_sec = time_sec

        self.__event = Event()
        self.__running = False
        self.__ret = None
        self.__is_timeout = False

    def run( self ):
        while( self.__running ):
            if( not self.__event.wait(timeout=self.__time_sec) ):
                # timeout
                with self.__lock:
                    self.__is_timeout = True
                    self.__ret = self.__callback( **self.__args_dict )
                    break

            self.__event.clear()

    def set_callback( self, callback=None, args_dict=None ):
        with self.__lock:
            if( callback is not None ):
                self.__callback = callback
            if( args_dict is not None ):
                self.__args_dict = args_dict

    def set_time_sec( seld, time_sec ):
        self.__time_sec = time_sec
        self.feed()

    def feed( self ):
        self.__event.set()

    def start( self ):
        if( not self.__running ):
            self.__running = True
            Thread.start(self)

    def stop( self ):
        if( self.__running ):
            self.__running = False
            self.__event.set()
            self.join()

    @property
    def ret( self ):
        return self.__ret

    @property
    def is_timeout( self ):
        return self.__is_timeout
