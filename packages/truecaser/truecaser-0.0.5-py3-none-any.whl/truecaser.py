
import sys
import os
import traceback
import json
import enum
from typing import *
import case
from collections import *
import random
import argparse
import subprocess


def generateTokenSets():

	dirName, fileName = readSettings()	

	dev, training, test = readSentences(fileName)

	with open(dirName + "/dev.tok", "w") as _file:
		_file.write(dev)

	with open(dirName + "/train.tok", "w") as _file:
		_file.write(training)

	with open(dirName + "/test.tok", "w") as _file:
		_file.write(test)


def readSentences(fileName: str) -> tuple:
	training = []
	dev = []
	test = []
	
	with open(fileName, "r") as _file:
		for line in _file:
			num = random.randint(1,10)
			assert(num > 0 and num < 11)
		
			if num == 1:
				dev.append(line)
			elif num == 2:
				test.append(line)	
			else:
				training.append(line)

	dev = "".join(dev)
	training = "".join(training)
	test = "".join(test)

	return dev, training, test


# Stringify enum int value for token cases
def caseConvert(token: str) -> str:
	
	num = case.get_tc(token)[0]
	assert(num >= 0 and num <= 4)

	if num == 0:
		return "DC"
	elif num == 1:
		return "LOWER"
	elif num == 2:
		return "UPPER"
	elif num == 3:
		return "TITLE"
	elif num == 4:
		return "MIXED"

# Print 2D List of strings
def printFeatures(sentence: List[List[str]]):
	for token in sentence:
		print(token)

# Tokenize a sentence
def tokenize(sentence: str) -> List[str]:
	assert(type(sentence) == str)
	return sentence.split()

# Subsitute colons for underscores in word
def subColon(word: str) -> str:
	return word.replace(':','_')

# Substitute colons in sentence
def subColonList(sentence: List[str]) -> List[str]:
	for i in range(len(sentence)):
		word = sentence[i]
		sentence[i] = subColon(word)
	
	return sentence

# Extract features from sentence
def extract(tokens: List[str], includeLabels=True) -> List[List[str]]:
	sentenceFeatures = ""

	tokens = subColonList(tokens)

	for i in range(len(tokens)):
		tokenFeatures = ""
		tokenCase = caseConvert(tokens[i])
		target = "t[0]=" + tokens[i]
		if includeLabels:	
			tokenCase = caseConvert(tokens[i])
			tokenFeatures += tokenCase + "\t" + target + "\t"
		else:
			tokenFeatures += target + "\t"
			

		if i == 0:
			prev = "__BOS__"
		else:
			prev = "t[-1]=" + tokens[i-1]

		if i == len(tokens) - 1:
			post = "__EOS__"
		else:
			post = "t[+1]=" + tokens[i+1]

		if prev == "__BOS__":
			tokenFeatures += prev
		elif post == "__EOS__":
			tokenFeatures += post
		else:
			conjunction = prev + "^" + post
			tokenFeatures += prev + "\t" + post + "\t" + conjunction
	
		tokenFeatures += "\n\n"

		sentenceFeatures += tokenFeatures

	return sentenceFeatures


# Create dict tallying word cases
def createDictionary(fileName: str) -> defaultdict:

	tokens = []

	with open(fileName, "r") as _file:
		for line in _file:
			tokens.extend(line.split())

		conDict = defaultdict(Counter)

		for token in tokens:
			conDict[token.casefold()] = Counter({})

		for key, counter in conDict.items():
			for token in tokens:
				if token.casefold() == key:
					counter[token] += 1
			
	return reduceDict(conDict)




# Reduce tally dict to simple dict
# mapping word to it's most common case
def reduceDict(_dict: dict) -> defaultdict:
	
	simpleDict = {}
	for key, counter in sorted(_dict.items()):
		simpleDict[key] = counter.most_common(1)[0][0]
		
	return simpleDict

# Write dict to json file
def writeJSON(fileName: str, _dict: dict):
	with open(fileName, 'w') as _file:
		_file.write(json.dumps(_dict))

def getSentences(fileName):
	sentences = []
	with open(fileName, "r") as _file:
		for line in _file:
			sentences.append(line)

	return sentences


def getFeatures(sentences, includeLabels=True):
	features = ""
	for sentence in sentences:
		tokens = tokenize(sentence)
		
		feature = extract(tokens, includeLabels)

		features += str(feature) + "\n"

	return features


def writeDictionary():
	
	dirName, fileName = readSettings()	

	fileNameIn = dirName + "/dev.tok"
	mixedCase = createDictionary(fileNameIn)
	fileNameOut = dirName + "/mixedCase.json"
	writeJSON(fileNameOut, mixedCase)


def caseFoldSentences(sentences: str):
	sentences.split
	

def caseUnfoldSentences():
	pass

def caseFoldWord(word: str):
	return word.casefold()

def restoreCaseAll(words: List[str], fileName: str):
	

	with open(fileName, "r") as _file:
		mixedCase = json.load(_file)

	caseRestoredWords = []
	for word in words:
		try:
			trueCase = mixedCase[word]
			caseRestoredWords.append(trueCase)
		except:
			if word == "\n":
				caseRestoredWords.append("\n")
			else:			
				caseRestoredWords.append(word)

		
	return caseRestoredWords

def restoreTokens():
	
	dirName, fileName = readSettings()	

	sentences = []

	with open(dirName + "/test.tok", "r") as _file:
		for line in _file:
			sentences.append(line)


	words = []
	for sentence in sentences:
		splitSentence = sentence.split()
		splitSentence.append("\n")
		words.extend(splitSentence)
			
	for i in range(len(words)):
		words[i] = caseFoldWord(words[i])

	trueCasedWords = restoreCaseAll(words, dirName + "/mixedCase.json")

	with open(dirName + "/test.restored", "w") as _file:
		for word in trueCasedWords:
			if word != "\n":
				_file.write(word + " ")
			else:
				_file.write(word + " ")


def getAccuracy():

	dirName, fileName = readSettings()	

	gold = []
	restored = []

	with open(dirName + "/test.tok", "r") as _file:
		for line in _file:
			gold.append(line)


	with open(dirName + "/test.restored", "r") as _file:
		for line in _file:
			restored.append(line)

	correctTokens = 0
	totalTokens = 0

	for (goldSen, restoredSen) in zip(gold, restored):
		
		goldTokens = goldSen.split()
		restoredTokens = restoredSen.split()
		assert len(goldTokens) == len(restoredTokens), "Mismatched lengths"
		for (goldToken, restoredToken) in zip(goldTokens, restoredTokens):
			totalTokens += 1
			if goldToken == restoredToken:
				correctTokens += 1


	accuracy = round(correctTokens / totalTokens, 3)
	return accuracy



def generateFeatureFiles():

	dirName, fileName = readSettings()	

	fileStems = ["dev", "train", "test"]

	for stem in fileStems:
		tokFile = dirName + "/" + stem + ".tok"
		featuresFile = dirName + "/" + stem + ".features"
		print(tokFile, featuresFile)
		

		sentences = getSentences(tokFile)
		if stem == "test":
			features = getFeatures(sentences, False)
		else:
			features = getFeatures(sentences, True)

		with open(featuresFile, 'w') as _file:
			_file.write(features)


def crfSuiteLearn():

	
	dirName, fileName = readSettings()	

	command = "crfsuite learn "
	command = command + "-p feature.possible_states=1 "
	command = command + "-p feature.possible_transitions=1 "
	command = command + "-m model "
	command = command + "-e2 train.features dev.features"
	print(command)

	process = subprocess.Popen(command,
								shell=True,
								stdout=subprocess.PIPE,
								stderr=subprocess.PIPE,
								cwd=dirName)

	
	readProcess(process)



def readProcess(process):

	while True:
		try:
			outs, errs = process.communicate(timeout=20)
			print(outs.decode(), errs.decode())
			if process.poll() is not None:
				break
		except subprocess.TimeoutExpired:
			process.kill()
			outs, errs = process.communicate()
			print(outs.decode(), errs.decode())
	

def getProcessOutput(process):

	output = ""
	err = ""

	while True:
		try:
			outs, errs = process.communicate(timeout=20)
			output = output + outs.decode()
			err = err + errs.decode()
			if process.poll() is not None:
				break
		except subprocess.TimeoutExpired:
			process.kill()
			outs, errs = process.communicate()
			output = output + outs.decode()
			err = err + errs.decode()
	
	return output, err



def crfSuitePredict():
	
	dirName, fileName = readSettings()	
	
	command = "crfsuite tag -m model "
	command = command + "test.features > test.predictions"
	print(command)

	process = subprocess.Popen(command,
								shell=True,
								stdout=subprocess.PIPE,
								stderr=subprocess.PIPE,
								cwd=dirName)

	readProcess(process)



def configureSettings(dirName: str, fileName: str):

	command = "mkdir config ; "
	command = command + "echo \"" + dirName + "\\n"
	command = command + fileName + "\" > config/config.txt"
	
	process = subprocess.Popen(command,
								shell=True,
								stdout=subprocess.PIPE,
								stderr=subprocess.PIPE)

	readProcess(process)


def readSettings() -> tuple:

	command = "cat config/config.txt"
	process = subprocess.Popen(command,
								shell=True,
								stdout=subprocess.PIPE,
								stderr=subprocess.PIPE)

	outs, errs = getProcessOutput(process)
	
	if len(errs) > 0:
		print(errs)

	return outs.split()
	


def parseArgs() -> dict:
	
	parser = argparse.ArgumentParser(description='Statistical case restoration')
	subparsers = parser.add_subparsers(help='sub-command help', dest='command')
	subparsers.required=True

	setupParser = subparsers.add_parser('configure', help='configure settings')
	setupParser.add_argument('-d', '--source_directory', metavar='', required=True)
	setupParser.add_argument('-f', '--token_file', metavar='', required=True)
	
	
	splitParser = subparsers.add_parser('split', help='split token file')

	featureParser = subparsers.add_parser('features', help='generate features')

	dictionaryParser = subparsers.add_parser('dictionary', help='build dictionary')

	learnParser = subparsers.add_parser('learn', help='train model')

	predictParser = subparsers.add_parser('predict', help='predict case')	
	
	restoreParser = subparsers.add_parser('restore', help='apply model to tokens')

	accuracyParser = subparsers.add_parser('accuracy', help='get prediction accuracy')
	
	return vars(parser.parse_args())

	
