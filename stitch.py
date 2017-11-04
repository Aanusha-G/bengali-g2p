#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
#dir = os.path.dirname(__file__)
#filename = os.path.join(dir, '/relative/path/to/file/you/want')
#curdir = os.getcwd()
with open("/Users/aanusha/bengali-g2p/character_mappings") as f:
	data = f.readlines()

def is_first_vowel(vin, word):
	vowels = ['aa', 'ao', 'i', 'e', 'oi', 'ae', 'o', 'ow', 'ou',
			  'u', 'uw', 'aal', 'il', 'el', 'ul', 'owl', 'oul',
			  'oil', 'AX']
	for index,i in enumerate(word): 
		if i in vowels: 
			first_vow_index = index
			break
	if vin == first_vow_index: 
		return 1
	else: 
		return 0

def g2p(word):
	del_list = ['aal', 'il', 'el', 'ae', 'ao', 'oil', 'owl', 'oul', 'ul', 'XX']
	mappings = {}
	for line in data:
		character = line.split(' -> ')[0]
		xipa = line.split(' -> ')[1].strip()
		mappings[character] = xipa

	#test_word = unicode('খিচুরি','utf-8')
	map_xipa = []
	for i in word:
		map_xipa.append(mappings[i.encode('utf-8')].strip('|').split('|'))
	phoneme_seq = [item for sublist in map_xipa for item in sublist]
	phoneme_string = '|'.join(phoneme_seq)+'|'

	replacements = [
		# Delete schwa before halant
		(u'AX\|XX\|', u'XX|'),
		# Delete schwa followed by vowel ligatures
		(u'AX\|(?=(?:aa|i|u|e|ow|oi|ou|)l\|)', u''),
		# Retain all first syllable schwas (between non-archiphonemes) - this rule might be redundant: check
		(r'(^[a-z]{1,3}\|)AX\|(?=[a-z]{1,3}\|)', r'\1ao|'),
		# XX|j|aal| -> ae|
		(r'XX\|j\|aal\|', r'ae|'),
		# Word-final h is always followed by ow|
		(u'h\|AX\|$', u'h|ow|'),
		# Word-final schwas -> ow| for conjugate clusters
		(r'(XX\|\w{1,3}\|)AX\|$', r'\1ow|'),
		# Other word-final schwas are deleted
		(u'AX\|$', u''),
		# Alternating schwas -> ow| (after full vowel)
		(r'(ao\|\w{1,3}\|)AX\|', r'\1ow|'),
		# Alternating schwas -> ow| (after implied schwa)
		(r'(AX\|\w{1,3}\|)AX\|', r'\1ow|'),
		# "swa" -> sh|
		(u'sx\|XX\|(?:b|m)\|', u'sh|'),
		# sx+cons -> s|
		(r'sx\|XX\|', r's|'),
		# ligature vowel + y -> ow|
		(r'((?:aa|i|u|e|ow|oi|ou|)l\|)y\|', r'\1ow|'),
		# plosive + j phola -> geminate
		(r'(p|t|k|b|d|g)\|XX\|j\|', r'\1|\1|'),
		# Handle -tam
		(r'AX\|(?=td\|aal\|m\|)', r''),
		# Convert all remaining shwas to ao|
		# Might want to apply this rule in a separate step after conjugate clusters are sorted out
		# Or after common morphemes like -tam are sorted out
		(u'AX\|', u'ao|'),
		# Remove all remaining halants
		(u'XX\|', u''),
		# Nasalise vowels
		(r'((?:aa|ae|ao|i|u|e|ow|oi|ou)l?)\|NX\|', r'\1n|'),
		# Remove vowel ligature symbols
		(r'(aa|ae|ao|i|u|e|ow|oi|ou)l', r'\1')
	]
	print "phoneme_string before schwa_deletion", phoneme_string

	for old, new in replacements: 
		phoneme_string = re.sub(old, new, phoneme_string)
	print "phoneme_string after schwa_deletion" , phoneme_string
	return syllabify(phoneme_string)

def cons_clusters(phoneme_seq):
	clust = []
	temp = []
	lig_vowels = ['aal', 'il', 'el', 'oil', 'owl', 'oul', 'ul']
	for index,phoneme in enumerate(phoneme_seq):
		if phoneme not in lig_vowels and phoneme_seq[index+1] == 'AX' and phoneme_seq[index+2] in lig_vowels:
			clust.append(phoneme_seq[index:(index+2)])
	print clust


def syllabify(word):
	vowels = ['aa', 'i', 'e', 'ei', 'ae', 'ao', 'ow', 'ou', 'u', 'AX', 'OW']
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


def run_tests():
	with open("/Users/aanusha/bengali-g2p/test_bangla") as f:
		testdata = f.readlines()
	test_pairs = {}
	for line in testdata:
		word = line.split(' ')[0]
		pron = line.split(' ')[1].strip()
		test_pairs[word] = pron
	tot_tests = len(test_pairs)
	c = 0
	for i in test_pairs.keys():
		g2p_output = g2p(unicode(i,'utf-8'))
		print "Expected: ", test_pairs[i], "\nG2P: ", g2p_output
		if test_pairs[i] == g2p_output:
			print "pass!"
			c+=1
		else:
			print "Test failed"
		print '________________'
	print c, " out of ", tot_tests, " passed "
run_tests()