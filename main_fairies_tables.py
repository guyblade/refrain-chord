#!/usr/bin/env python3

import common

def total_skill_cost(skill_info):
  ret = 0
  for s in skill_info['skills']:
    ret += s['cost']
  return ret


def RenderOneFairy(name, skill_info):
  print("<table border='1' width='50%'>")
  print("<tr>")
  print("<td width='50%%'>%s %s</td>" % (common.strong("Name:"), common.ctext(common.purple, name)))
  print("<td width='50%%' style='text-align: right'>%s %s</td>" % (common.strong("FP to Master:"), total_skill_cost(skill_info)))
  print("</tr>")
  print("</table>")

def main():
  names = common.MainFairyNames()
  skills = common.MainFairySkills()

  for name in names:
    RenderOneFairy(name, skills[name])


if __name__ == "__main__":
  main()
