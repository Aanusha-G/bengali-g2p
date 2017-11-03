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

	return syllabify(''.join(word_ipa))
	#return ''.join(word_ipa)


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
		else:
			print "Test failed"


def syllabify(word):
	vowels = ['aa', 'i', 'iy', 'e', 'ei', 'ae', 'o', 'ow', 'ou', 'u', 'uw']
	ph = word.strip('|').split('|')
	syl = []
	v_flag = 0
	c_flag = 0
	l = len(ph) - 1
	for index, i in enumerate(reversed(ph)):
		syl.append(i+'|')
		if i in vowels:
			v_flag = 1
		else:
			if v_flag == 1:
				c_flag = 1
		if v_flag == 1 and c_flag == 1 and index != l:
			v_flag = c_flag = 0
			syl.append('-')
	syl_word = ''.join(list(reversed(syl)))
	return syl_word


run_tests()