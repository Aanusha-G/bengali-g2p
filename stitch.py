#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
g2p.py
~~~~~~~~~~

This script converts Bengali graphemes to romanised phonemes (xipa) and then to their pronunciation (IPA
and ZXSAMPA).

Functions
    (1) g2p: convert Bengali graphemes to xipa phonemes
    (2) syllabify : Syllabifies generated xipa
    (3) xipa2ipa: Converts xipa phonemes to IPA transcription
    (4) xipa2xsampa: Converst xipa to XSAMPA
    (5) run_tests: Runs unit tests from test_bangla file

Aanusha Ghosh (aanusha.ghosh@gmail.com)

Created: 2017-11-03
Last updated: 2017-11-05 Aanusha Ghosh


'''
import os
import regex
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--interactive', action="store_true", help="read tokens from standard input")
parser.add_argument("-f", "--file", dest = 'filepath', help="path to file containing tokens in Bengali")
parser.add_argument("-t", "--run-tests", dest = 'tests', action = "store_true", help="Specify whether unit tests should be run. This is set to true by default if input file is not specified.")
parser.add_argument("--ipa", action="store_true", help="return IPA transcriptions" )
parser.add_argument("--xsampa", action="store_true", help="return XSAMPA transcriptions. If neither --ipa nor --xsampa flags are specified, xipa transcriptions are returned by default")
args = parser.parse_args()


def g2p(word):
	character_mappings = os.path.join(os.getcwd(), 'character_mappings')
	with open(character_mappings) as f:
		data = f.readlines()
	del_list = ['aal', 'il', 'el', 'ae', 'ao', 'oil', 'owl', 'oul', 'ul', 'XX']
	mappings = {}
	for line in data:
		character = line.split(' -> ')[0]
		xipa = line.split(' -> ')[1].strip()
		mappings[character] = xipa

	map_xipa = []
	for i in word:
		map_xipa.append(mappings[i.encode('utf-8')].strip('|').split('|'))
	phoneme_seq = [item for sublist in map_xipa for item in sublist]
	phoneme_string = '|'.join(phoneme_seq)+'|'

	replacements = [
		# Fix putkis
		(r'j\|OO\|', r'y|'),
		(r'b\|OO\|', r'r|'),
		(r'dr\|OO\|', r'rr|'),
		(r'drh\|OO\|', r'rr|'),
		# Delete schwa before halant
		(r'AX\|XX\|', r'XX|'),
		# Delete schwa followed by vowel ligatures
		(r'AX\|(?=(?:aa|i|u|e|ow|oi|ou|)l\|)', r''),
		# Retain all first syllable schwas (between non-archiphonemes) - this rule might be redundant: check
		(r'^[a-z]{1,3}\|\KAX\|(?=[a-z]{1,3}\|)', r'ao|'),
		# XX|j|aal| -> ae|
		(r'XX\|j\|aal\|', r'ae|'),
		# Word-final h is always followed by ow|
		(r'h\|AX\|$', r'h|ow|'),
		# Word-final schwas -> ow| for conjugate clusters
		(r'XX\|\w{1,3}\|\KAX\|$', r'ow|'),
		# Other word-final schwas are deleted
		(r'AX\|$', r''),
		# AX|cons|AX|$ -> ao|cons|
		(r'AX\|([a-z]{1,3}\|$)', r'ow|\1'),
		# Alternating schwas -> ow| (after full vowel)
		(r'ao\|\w{1,3}\|\KAX\|', r'ow|'),
		# Alternating schwas -> ow| (after implied schwa)
		(r'AX\|\w{1,3}\|\KAX\|', r'ow|'),
		# "swa" -> sh|
		(r'sx\|XX\|(?:b|m)\|', r'sh|'),
		# sx+ other cons (plosives, liquids) -> s|
		(r'sx\|XX\|', r's|'),
		# all other sx (not part of conjugate clusters) -> sh|
		(r'sx\|', r'sh|'),
		# বিশ্ব, বিদ্বান cons + b| (word-finally and syllable finally)= geminate
		# TODO: Make this rule syllable-sensitive
		(r'(\w{1,3}\|)XX\|b\|', r'\1\1'),
		# ligature vowel + y -> ow|
		(r'(?:(?:aa|i|u|e|ow|oi|ou|)l\|)\Ky\|', r'ow|'),
		# plosive + j phola -> geminate
		# This rule should only apply NON-word-intially
		(r'(?<!^)((?:p|td?|k|b|dd?|g)h?)\|XX\|j\|', r'\1|\1|'),
		# Clean up aspirated geminates from above step (bh|bh| -> b|bh|)
		(r'((\w{1,2})h)\|\1\|', r'\2|\1|'),
		# Handle -tam
		(r'AX\|(?=td\|aal\|m\|)', r''),
		# Convert all remaining shwas to ao|
		# Might want to apply this rule in a separate step after conjugate clusters are sorted out
		# Or after common morphemes like -tam are sorted out
		(r'AX\|', r'ao|'),
		# Remove all remaining halants
		(r'XX\|', r''),
		# Nasalise vowels
		(r'(?:(?:aa|ae|ao|i|u|e|ow|oi|ou)l?)\K\|NX\|', r'n|'),
		# Remove vowel ligature symbols
		(r'(?:aa|ae|ao|i|u|e|ow|oi|ou)\Kl', r''),
		# ao| or ow| + y| = oy|
		(r'(ao|ow)\|y\|',r'oy|')
	]
	#print "phoneme_string before schwa_deletion", phoneme_string

	for old, new in replacements: 
		phoneme_string = regex.sub(old, new, phoneme_string)
	#print "phoneme_string after schwa_deletion" , phoneme_string
	return syllabify(phoneme_string)


def syllabify(word):
	vowels = ['aa', 'ae', 'ao', 'ow', 'ou', 'i', 'e', 'oi', 'u', 'oy', 'AX']
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
	# If first syllable has no vowel, remove first syllable marker
	first_syll = syl_word.split('-')[0]
	#print first_syll
	if regex.search(r'(aa|ae|ao|i|e|u|o|oi|ou)', first_syll) == None:
		syl_word = regex.sub(r'-', r'', syl_word, 1)

	return syl_word


def run_tests():
	test_bangla = os.path.join(os.getcwd(), "test_bangla")
	with open(test_bangla) as f:
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
		#print "Expected: ", test_pairs[i], "\nG2P: ", g2p_output
		if test_pairs[i] == g2p_output:
			#print "pass!"
			c+=1
		else:
			print "Expected: ", test_pairs[i], "\nG2P: ", g2p_output
			print "Test failed"
			print '________________'
	print c, " out of ", tot_tests, " passed "
	
def run_file(filepath):
	with open(filepath, 'r') as f:
		tokens_list = f.readlines()
	prons_dict = {}
	for token in tokens_list:
		token = token.strip()
		g2p_output = g2p(unicode(token,'utf-8'))
		prons_dict[token] = g2p_output
	for i in prons_dict: 
		print i, 't', prons_dict[i], '\n'

def run_interactive():
	import sys
	while True:
		try:
			token = raw_input('Token: ')
			if token == "stop":
				break
			g2p_output = g2p(unicode(token.strip(),'utf-8'))
			print "phoneme: ", g2p_output
		except KeyboardInterrupt:
			sys.exit()			


if args.tests or (not args.filepath and not args.interactive):
	run_tests()
if args.filepath:
	print "Processing tokens from your file"
elif args.interactive:
	run_interactive()
