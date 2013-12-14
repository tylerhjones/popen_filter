import time
import subprocess

print time.time()
subprocess.Popen(['sleep', '1000'])
print time.time()