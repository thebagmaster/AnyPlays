import psutil

PROCNAME = "DARKSOULS.exe"
for proc in psutil.process_iter():
    if proc.name() == PROCNAME:
        proc.suspend()
