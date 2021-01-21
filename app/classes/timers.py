from threading import Timer

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

class NoEventTimer(object):
    def __init__(self, offTime):
        self.offTime = offTime
        self.enabled = False
        self._timer = None
    
    def start(self, offFunction):
        if not self.enabled:
            #print('start off timer')
            self._timer= Timer(self.offTime, offFunction)
            self._timer.start()
            self.enabled = True

    def cancel(self):
        if self.enabled:
            #print('cancel off timer')
            self._timer.cancel()
            self.enabled = False