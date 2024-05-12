#!/usr/bin/env python3

import csv
import functools
import re

def red():
  return 'color:rgb(209,72,65);'

def green():
  return 'color:rgb(65,168,95);'

def orange():
  return 'color:rgb(243,121,52);'

def gold():
  return 'color:rgb(194,144,62);'

def light_blue():
  return 'color:rgb(102,127,178);'

def purple():
  return 'color:rgb(147,101,184);'

def strong(txt):
  return "<strong>%s</strong>" % (txt,)

def ctext(func, txt):
  return "<span style='%s'>%s</span>" % (func(), txt)

def read_csv(file_name, cols=None):
  ret = []
  with open(file_name, newline="") as f:
    red = csv.reader(f)
    header = next(red)

    for row in red:
      if not re.match(".+", row[0]):
        continue
      rdata = {}
      for i, col in enumerate(row):
        if not header[i]:
          continue
        if cols is not None and i not in cols:
          continue
        rdata[header[i]] = col
      ret.append(rdata)

  return ret

def ReadFairySkills(filename):
  data = read_csv(filename, set([i for i in range(0, 5)]))
  ordered_fairies = []
  ret = {}
  for entry in data:
    name = entry['Fairy']
    if name not in ret:
      ret[name] = {'name': name, 'skills': []}
      ordered_fairies.append(name)
    ret[name]['skills'].append({
      'name': entry['Ability'],
      'page': entry['Page'],
      'cost': (0 if entry['Cost'] == '-' else int(entry['Cost'])),
      'unlock': entry['Unlock Requirement'],
    });
  return ret, ordered_fairies

@functools.cache
def _ReadMainFairies():
  return ReadFairySkills("mainfairies.csv")

def MainFairyNames():
  return _ReadMainFairies()[1]

def MainFairySkills():
  return _ReadMainFairies()[0]

@functools.cache
def _ReadSubFairy():
  return ReadFairySkills("subfairies.csv")

def SubFairyNames():
  return _ReadSubFairy()[1]

def SubFairySkills():
  return _ReadSubFairy()[0]


@functools.cache
def GetDistinctSkills():
  m = MainFairySkills()
  s = SubFairySkills()
  ret = set()
  for pile in [m, s]:
    for _, entry in pile.items():
      for row in entry['skills']:
        ret.add(row['name'])
  # print("Distinct Skills:\n %r" % ret)
  return ret


@functools.cache
def GetNames():
  base = set(["Fang", "Apollonius", "Pippin", "Rinne",
              "Sherman", "Harley", "Fleur", "Galdo", "Tiara",
              "Marianna", "Ethel", "Ibfreet", "Noie",
             ])

  for name in MainFairyNames():
    base.add(name)
  for name in SubFairyNames():
    base.add(name)

  return base

def CleanLiteral(txt):
  return re.sub(r'(\+|\:|\.)', r'\\\1', txt)

def HighlightAnyWord(input, color, string_list):
  return re.sub(r'\b(' + '|'.join(string_list) + r')\b', ctext(color, r'\1'), input)

def HighlightQuotedWords(input, color, string_list):
  regexp = r'"(' + '|'.join(CleanLiteral(x) for x in string_list) + r')"'
  # print("%r" % regexp)
  return re.sub(regexp, ctext(color, r'\1'), input)

def HighlightNames(input):
  return HighlightAnyWord(input, purple, GetNames())

def HighlightSkills(input):
  return HighlightQuotedWords(input, light_blue, GetDistinctSkills())

