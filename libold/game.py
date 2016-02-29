import psutil

class Game(object) :
    def __init__(self,pname):
        for proc in psutil.process_iter():
            if proc.name() == pname:
                self.proc = proc
        self.paused = True
    
    def pause(self):
        if not self.paused :
            self.proc.suspend()
            self.paused = True
            
    def resume(self):
        self.proc.resume()
        self.paused = False