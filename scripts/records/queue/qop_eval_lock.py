"""Wait for, then hold, the card lock while qop_eval.sh runs (R-253); log to qop_eval.log beside it.

Usage: python qop_eval_lock.py
"""

import errno
import msvcrt
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOCK = r"C:\Users\Gaming\scratch\card.lock"
BASH = r"C:\Program Files\Git\bin\bash.exe"

fd = os.open(LOCK, os.O_RDWR)
os.lseek(fd, 0, os.SEEK_SET)
while True:  # wait for the card if anything holds it
    try:
        msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
        break
    except OSError as e:
        if e.errno != errno.EACCES:
            raise
        time.sleep(30)
try:
    with open(HERE / "qop_eval.log", "w", encoding="utf-8") as log:
        rc = subprocess.run(
            [BASH, str(HERE / "qop_eval.sh"), *sys.argv[1:1]],
            stdout=log,
            stderr=subprocess.STDOUT,
            creationflags=0x00004000,
        ).returncode
    print("exit", rc)
    sys.exit(rc)
finally:
    os.lseek(fd, 0, os.SEEK_SET)
    msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
    os.close(fd)
