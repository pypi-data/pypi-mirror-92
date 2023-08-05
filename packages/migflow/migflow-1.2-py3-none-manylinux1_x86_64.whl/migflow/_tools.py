import time
import atexit
import gmsh
import signal

gmsh.initialize()
gmsh.option.setNumber("General.Terminal",1)

signal.signal(signal.SIGINT, signal.SIG_DFL)

timers = {}

def timeit(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        tic = time.process_time()
        r = func(*args, **kwargs)
        toc = time.process_time()
        name = func.__name__
        timers[name] = timers.get(name, 0) + toc - tic
        return r
    return wrapper

def timeprint(timers) :
    if len(timers) != 0 :
        print(timers)

atexit.register(timeprint, timers)
