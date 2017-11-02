#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
import os
#dir = os.path.dirname(__file__)
#filename = os.path.join(dir, '/relative/path/to/file/you/want')
#curdir = os.getcwd()
with open("/Users/aanusha/bengali-g2p/character_mappings") as f:
	data = f.readlines()

mappings = {}
for line in data:
	character = line.split(' -> ')[0]
	xipa = line.split(' -> ')[1].strip()
	mappings[character] = xipa


word = unicode('খিচুরি','utf-8')
word_ipa = []
for i in word:
	print i
	word_ipa.append(mappings[i.encode('utf-8')])

print ''.join(word_ipa)
