import time
import warnings
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
    def __init__( self, time_sec, callback, *args, **kwargs ):
        Thread.__init__(self)
        self.__lock = Lock()

        self.__time_sec = time_sec
        self.__callback = callback
        self.__args = args
        self.__kwargs = kwargs

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
                    self.__ret = self.__callback( *self.__args, **self.__kwargs  )
                    break

            self.__event.clear()

    def set_callback( self, callback, *args, **kwargs ):
        with self.__lock:
            self.__callback = callback
            self.__args = args
            self.__kwargs = kwargs

    def set_time_sec( seld, time_sec ):
        self.__time_sec = time_sec
        self.feed()

    def feed( self ):
        self.__event.set()

    def start( self, daemon=True ):
        if( not self.__running ):
            self.__running = True
            self.daemon=daemon
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

    @property
    def is_running( self ):
        return self.__is_running


class Periodic(Thread):
    def __init__( self, time_sec, callback, *args, **kwargs ):
        Thread.__init__(self)
        self.__lock = Lock()

        Thread.__init__(self)
        self.__lock = Lock()

        self.__time_sec = time_sec
        self.__callback = callback
        self.__args = args
        self.__kwargs = kwargs

        self.__event = Event()
        self.__running = False
        self.__ret = None

        self.__timer = PerfTimer()

    def run( self ):
        while( self.__running ):
            with self.__lock:
                self.__timer.restart()
                self.__ret = self.__callback( *self.__args, **self.__kwargs  )

            sec = self.__time_sec
            if( self.compensate ):
                sec -= self.__timer.get_time()
            if( sec > 0 ):
                self.__event.wait(timeout=sec)
                self.__event.clear()
            else:
                msg = 'callback takes longer than periodic time.'
                warnings.warn( msg )

    def start( self, daemon=True, compensate=True ):
        self.compensate = compensate
        if( not self.__running ):
            self.__running = True
            self.daemon=daemon
            Thread.start(self)

    def stop( self ):
        if( self.__running ):
            self.__running = False
            self.__event.set()
            self.join()

    def set_callback( self, callback, *args, **kwargs ):
        with self.__lock:
            self.__callback = callback
            self.__args = args
            self.__kwargs = kwargs

    @property
    def ret( self ):
        return self.__ret

    @property
    def is_running( self ):
        return self.__is_running
