#! /usr/bin/python3 -OOt

import sys
import subprocess

command = sys.argv[1]
filename = sys.argv[2].replace("\ "," ")

#subprocess.run(["/usr/bin/notify-send", "--icon=error", filename])
#subprocess.run(["mcomix", command])
subprocess.run([command, filename])

