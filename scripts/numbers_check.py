#!/usr/bin/env python
"""Checks the ranges of intervals in some lines.

Example usage:

  ls foo* | ./numbers_check.py

Prints out intervals as:

  Found intervals: [(1, 45), 47, (50, 75)]
"""

import os
import re
import sys

pattern = r'\d+' if len(sys.argv) < 2 else sys.argv[1]

numbers = set()
for line in sys.stdin:
  match = re.search(pattern, line)
  if match:
    numbers.add(int(match.group(0)))

numbers = list(numbers)
numbers.sort()
ix = 0
intervals = []
while ix < len(numbers):
  ix_start = ix
  while ix + 1 < len(numbers) and numbers[ix + 1] == numbers[ix] + 1:
    ix += 1

  intervals.append((numbers[ix_start], numbers[ix] if ix < len(numbers) else numbers[ix - 1]))
  ix += 1

print 'Found intervals:', [
  _ if _[0] < _[1] else _[0]
  for _ in intervals
]
