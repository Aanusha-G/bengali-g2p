#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import regex
#dir = os.path.dirname(__file__)
#filename = os.path.join(dir, '/relative/path/to/file/you/want')
#curdir = os.getcwd()
with open("/Users/aanusha/bengali-g2p/character_mappings") as f:
	data = f.readlines()


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
		(r'^[a-z]{1,3}\|\KAX\|(?=[a-z]{1,3}\|)', r'ao|'),
		# XX|j|aal| -> ae|
		(r'XX\|j\|aal\|', r'ae|'),
		# Word-final h is always followed by ow|
		(u'h\|AX\|$', u'h|ow|'),
		# Word-final schwas -> ow| for conjugate clusters
		(r'XX\|\w{1,3}\|\KAX\|$', r'ow|'),
		# Other word-final schwas are deleted
		(u'AX\|$', u''),
		# AX|cons|AX|$ -> ao|cons|
		(r'AX\|([a-z]{1,3}\|$)', r'ow|\1'),
		# Alternating schwas -> ow| (after full vowel)
		(r'ao\|\w{1,3}\|\KAX\|', r'ow|'),
		# Alternating schwas -> ow| (after implied schwa)
		(r'AX\|\w{1,3}\|\KAX\|', r'ow|'),
		# "swa" -> sh|
		(u'sx\|XX\|(?:b|m)\|', u'sh|'),
		# sx+cons -> s|
		(r'sx\|XX\|', r's|'),
		# ligature vowel + y -> ow|
		(r'(?:(?:aa|i|u|e|ow|oi|ou|)l\|)\Ky\|', r'ow|'),
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
		(r'(?:(?:aa|ae|ao|i|u|e|ow|oi|ou)l?)\K\|NX\|', r'n|'),
		# Remove vowel ligature symbols
		(r'(?:aa|ae|ao|i|u|e|ow|oi|ou)\Kl', r'')
	]
	print "phoneme_string before schwa_deletion", phoneme_string

	for old, new in replacements: 
		phoneme_string = regex.sub(old, new, phoneme_string)
	print "phoneme_string after schwa_deletion" , phoneme_string
	return syllabify(phoneme_string)


def syllabify(word):
	vowels = ['aa', 'ae', 'ao', 'ow', 'ou', 'i', 'e', 'oi', 'u', 'AX']
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
	# Fix s|-td|ao|b|XX|-ddh|ow|
	syl_word = ''.join(list(reversed(syl)))
	# If first syllable has no vowel, remove last syllable marker
	first_syll = syl_word.split('-')[0]
	print first_syll
	if regex.search(r'(aa|ae|ao|i|e|u|o|oi|ou)', first_syll) == None:
		syl_word = regex.sub(r'-', r'', syl_word, 1)

	#syl_word = regex.sub(r'^((?!aa|ae|ao|i|e|u|o|oi|ou)\w{1,3}\|)(?R)?-', r'\1', syl_word)
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