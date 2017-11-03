#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
import os
#dir = os.path.dirname(__file__)
#filename = os.path.join(dir, '/relative/path/to/file/you/want')
#curdir = os.getcwd()
with open("/Users/aanusha/bengali-g2p/character_mappings") as f:
	data = f.readlines()

def g2p(word):
	mappings = {}
	for line in data:
		character = line.split(' -> ')[0]
		xipa = line.split(' -> ')[1].strip()
		mappings[character] = xipa


	test_word = unicode('খিচুরি','utf-8')
	word_ipa = []
	for i in word:
		word_ipa.append(mappings[i.encode('utf-8')])

	return ''.join(word_ipa)


def run_tests():
	with open("/Users/aanusha/bengali-g2p/test_bangla") as f:
		testdata = f.readlines()
	test_pairs = {}
	for line in testdata:
		word = line.split(' ')[0]
		pron = line.split(' ')[1].strip()
		test_pairs[word] = pron
	for i in test_pairs.keys():
		g2p_output = g2p(unicode(i,'utf-8'))
		print "Expected: ", test_pairs[i], "\nG2P: ", g2p_output
		if test_pairs[i] == g2p_output:
			print "pass!"


run_tests()