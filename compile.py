import sys
from pathlib import Path
import py_compile

if (len(sys.argv) < 2):
    print ("Invalid usage")
    sys.exit()

pyCode2Compile = sys.argv[1]

pyFile = Path(pyCode2Compile)
try:
    pyFileAbsPath = pyFile.resolve(strict=True)
except FileNotFoundError:
    print("File not found! [" + pyCode2Compile + "]")
    sys.exit()
else:
    py_compile.compile(pyFileAbsPath)

