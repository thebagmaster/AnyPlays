import psutil

PROCNAME = "Fallout3.exe"
for proc in psutil.process_iter():
    if proc.name() == PROCNAME:
        proc.resume()