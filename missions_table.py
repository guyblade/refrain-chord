#!/usr/bin/env python3

import csv
import functools
import re
import common

def ReadMissions():
  dt = common.read_csv("missions.csv")
  for entry in dt:
    entry['Reward'] = re.split(r'\s*,\s*', entry['Reward'])
  return dt

def MissionSortStr(entry):
  name = entry['Mission']
  m = re.match(r'(\w+)\s+Mission\s+(\w)!', name)
  if m:
    return "00 %s %s" % (m.group(1), m.group(2))
  m = re.match(r'Mission\s+(\w)\s+[fF]rom\s+(\w+)', name)
  if m:
    return "01 %s %s" % (m.group(2), m.group(1))
  m = re.match(r'Clear\s+(\d+)\s+Missions!', name)
  if m:
    return "02 %05d" % int(m.group(1))
  m = re.match(r'find (a|\d+|all) treasure', name.lower())
  if m:
    if m.group(1) == 'a':
      i = 1
    elif m.group(1) == 'all':
      i = 99999
    else:
      i = int(m.group(1))
    return "03 %05d" % i
  m = re.match(r'synthesize (an|\d+)', name.lower())
  if m:
    if m.group(1) == 'an':
      i = 1
    else:
      i = int(m.group(1))
    return "04 %05d" % i
  return name

def DrawMissionTable():
  missions = ReadMissions()
  missions.sort(key=MissionSortStr)

  print("<table border='1' width='100%'>")
  print("<tr><th>Mission</th><th>Unlock Requirement</th><th>Clear Condition</th><th>Reward</th></tr>")

  for mission in missions:
    bits = []
    bits.append(mission['Mission'])
    bits.append(mission['Unlock Condition'])
    bits.append(mission['Clear Condition'])
    bits.append("<ul><li>" + "</li><li>".join(mission['Reward']) + "</li></ul>")
    print("<tr><td>" + common.HighlightNames(common.HighlightSkills("</td><td>".join(bits))) + "</td></tr>")

  print("</table>")


def main():
  DrawMissionTable()

if __name__ == "__main__":
  main()
