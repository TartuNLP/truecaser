#!/usr/bin/env python3

import sys
import re

from learntc import log, tokens

class DefUniqDict(dict):
	def __missing__(self, key):
		return key

class WordFreqTuple():
	def __init__(self, word, freq):
		self.word = word
		self.freq = freq

def loadModel(filename, freqs = False):
	res = DefUniqDict()
	
	with open(filename, 'r') as filehandle:
		for w in filehandle:
			w, f = w.strip().split()
			
			res[w.lower()] = WordFreqTuple(w, int(f))
		
		return res

def isUpper(w):
	return re.search(r'[A-Z]', w) and not re.search(r'[a-z]', w)

def truecase(model, wordlist):
	return [model[w.lower()].word if (w.lower() in model and (i == 0 or isUpper(w) or wordlist[i-1] in ".:;?!")) else w for i, w in enumerate(wordlist)]

def updateToken(line, span, newtoken):
	return line[:span[0]] + newtoken + line[span[1]:]

def processLines(model, fh):
	logFreq = 100000
	i = 0
	for line in fh:
		words, spans = zip(*tokens(line))
		
		tcwords = truecase(model, words)
		
		resline = line.strip()
		for w, s in zip(tcwords, spans):
			resline = updateToken(resline, s, w)
		
		print(resline)
		
		i += 1
		if not i % logFreq:
			log("processed {0} lines".format(i))
	
	if i % logFreq:
		log("processed {0} lines".format(i))

if __name__ == '__main__':
	modelfile = sys.argv[1]
	
	model = loadModel(modelfile)
	
	try:
		filename = sys.argv[2]
	except IndexError:
		filename = '-'
	
	if filename == '-':
		processLines(model, sys.stdin)
	else:
		with open(filename, 'r') as fh:
			processLines(model, fh)
