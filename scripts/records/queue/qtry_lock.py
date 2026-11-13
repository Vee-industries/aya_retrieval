"""Wait for, then hold, the card lock while one qtry.sh try runs (R-229); log to LABEL.log beside it.

Usage: python qtry_lock.py LABEL LR EPOCHS DATA
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
    with open(HERE / f"{sys.argv[1]}.log", "w", encoding="utf-8") as log:
        rc = subprocess.run(
            [BASH, str(HERE / "qtry.sh"), *sys.argv[1:5]],
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
