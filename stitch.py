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

	print "phone_seq after schwa_deletion = ", phoneme_seq
	phoneme_string = '|'.join(phoneme_seq)+'|'
	print "phoneme_string before schwa_deletion", phoneme_string
	# Delete schwa before halant
	phoneme_string = re.sub(u'AX\|XX\|',u'XX|', phoneme_string)
	# Delete schwa followed by vowel ligatures
	phoneme_string = re.sub(u'AX\|(?=(?:aa|i|u|e|ow|oi|ou|)l\|)', u'', phoneme_string)
	# Word-final h is always followed by ow|
	phoneme_string = re.sub(u'h\|AX\|$', u'h|ow|', phoneme_string)
	# Word-final schwas -> ow| for conjugate clusters
	phoneme_string = re.sub(r'(XX\|\w{1,3}\|)\KAX\|$', u'ow|', phoneme_string)
	# Other word-final schwas are deleted
	phoneme_string = re.sub(u'AX\|$', u'', phoneme_string)
	# "swa" -> sh|
	phoneme_string = re.sub(u'sx\|XX\|(?:b|m)\|', u'sh|', phoneme_string)
	# Convert all remaining shwas to ao|
	phoneme_string = re.sub(u'AX\|', u'ao|', phoneme_string)
	# Remove all remaining halants
	# phoneme_string = re.sub(u'XX\|', u'', phoneme_string)
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
	ph = replace_ligatures(ph)
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

def replace_ligatures(phonemes_list):
	lig_vowels = ['aal', 'il', 'el', 'oil', 'owl', 'oul', 'ul']
	for index,phoneme in enumerate(phonemes_list):
		if phoneme in lig_vowels:
			phonemes_list[index] = phoneme.strip('l')
	return(phonemes_list)

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

run_tests()