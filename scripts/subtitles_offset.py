#!/usr/bin/env python
"""Adds an offset to all subtitles in an SRT file.

Example usage:

  ./subtitles_offset.py input_file.srt 2:04
"""

import re
import sys

if len(sys.argv) <= 2:
  print 'Tai shao le!'
  sys.exit()

minutes, seconds = sys.argv[2].split(':')
total_seconds = int(minutes) * 60 + int(seconds)
print 'total_seconds:', total_seconds

def fix_timestamp_line(timestamp_line, offset):
  """Offsets a timestamp line.
  
  :param str timestamp_line: A line, a la "00:01:01,000 --> 00:01:02,000".
  :param int offset: Offset in seconds (positive or negative).
  :return str: The fixed timestamp line, a la "00:01:01,500 --> 00:01:02,500".
  """
  if ' --> ' not in timestamp_line:
    print '*** BAD TIMESTAMP LINE! ***', timestamp_line
    raise Exception()

  parts = timestamp_line.split(' --> ')
  for j in range(len(parts)):
    match = re.match(r'(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+),(?P<milliseconds>\d+)', parts[j])
    if not match:
      print '*** FAILED TO MATCH! ***', parts[j]

    previous_timestamp = (
      int(match.group('hours')) * 3600 +
      int(match.group('minutes')) * 60 +
      int(match.group('seconds'))
    )
    fixed_timestamp = previous_timestamp + offset
    if fixed_timestamp < 0:
      return None

    formatted_timestamp = '%(hours)02d:%(minutes)02d:%(seconds)02d,%(milliseconds)s' % {
      'hours': fixed_timestamp / 3600,
      'minutes': (fixed_timestamp % 3600) / 60,
      'seconds': fixed_timestamp % 60,
      'milliseconds': match.group('milliseconds'),
    }
    # print parts[j], previous_timestamp, ' --> ', fixed_timestamp, formatted_timestamp
    parts[j] = formatted_timestamp

  return ' --> '.join(parts)

# Tuples of timestamp and lines.
subs = []

lines = open(sys.argv[1], 'r').readlines()
ix = 0
while ix < len(lines):
  while ix < len(lines) and not lines[ix].strip():
    ix += 1

  if ix >= len(lines):
    break

  line = lines[ix].strip()
  if not re.match(r'^\d+$', line):
    print '*** BAD PARSE! ***', line
    sys.exit()

  ix += 1
  timestamp_line = lines[ix].strip()
  ix += 1
  ix_start = ix
  while lines[ix].strip():
    ix += 1

  sub_lines = [lines[_].strip() for _ in range(ix_start, ix)]
  print timestamp_line, sub_lines

  fixed_timestamp_line = fix_timestamp_line(timestamp_line, -total_seconds)
  if fixed_timestamp_line is None:
    print '-- Skipped'
    continue

  print 'fixed_timestamp_line:', fixed_timestamp_line
  subs.append((fixed_timestamp_line, sub_lines))

fixed_body = '\n\n'.join([
  '\n'.join([
    str(i + 1),
    subs[i][0],
    '\n'.join(subs[i][1]),
  ])
  for i in range(len(subs))
])

open(re.sub(r'\.srt', '_fixed.srt', sys.argv[1]), 'w').write(fixed_body)
