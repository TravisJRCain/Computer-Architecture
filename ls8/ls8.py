#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
program = None

if len(sys.argv) > 1:
    program = sys.argv[1]

cpu.load(program)
cpu.run()