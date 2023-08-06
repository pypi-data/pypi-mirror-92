#! /usr/bin/python
# coding: utf-8
# Prerequisite: sudo easy_install regex
import regex
import sys
import collections
sys.setdefaultencoding('utf-8')
import codecs

test = False

"""
Regex series:

Unhandled cases:
भेदन (भिद् ल्युट्)
"""

lines = []
if (test):
  test_lines = u"""
अ पु. संस्कृत वर्णमाला का प्रथम वर्ण [विशेषतया तीन दिन
तक चलने वाले सोम-याग (त्रिरात्र) के प्रथम दिन आज्य
इति”, पञ्च. ब्रा. 2०.14.3।
अंश पु.1 अ. भाग (देवों, पितरों एवं मनुष्यों के लिए नियत)
ऋ.वे. 1०.31.3; अ.वे. 11.1.5;1 ब. पशु-भाग, बौ.श्रौ.सू.
का नाम, ऋ. प्रा. 17.4; निदा.सू. 1०5.2०।
""".split("\n")
  lines = test_lines
else:
  f = codecs.open('vedic-rituals-hi.txt', encoding='utf-8')
  lines = f.readlines()
  # lines = sys.stdin.readlines()
  # lines = [line.decode('utf-8') for line in sys.stdin]

full_text = "".join(lines)
# print(full_text)
full_text = regex.sub(r'^(\S+)\s+(पु[ .])', '####\g<1>####\g<1> \g<2>', full_text, flags=regex.UNICODE|regex.MULTILINE)
full_text = regex.sub(r'^(\S+?)\s+(वि[ .])', '####\g<1>####\g<1> \g<2>', full_text, flags=regex.UNICODE)
full_text = regex.sub(r'^(\S+?)\s+(न[ .])', '####\g<1>####\g<1> \g<2>', full_text, flags=regex.UNICODE|regex.MULTILINE)
full_text = regex.sub(r'^(\S+?)\s+(क्रि\.वि[ .])', '####\g<1>####\g<1> \g<2>', full_text, flags=regex.UNICODE|regex.MULTILINE)
full_text = regex.sub(r'^(\S+?)\s+(स्त्री[ .])', '####\g<1>####\g<1> \g<2>', full_text, flags=regex.UNICODE|regex.MULTILINE)
print(full_text)

