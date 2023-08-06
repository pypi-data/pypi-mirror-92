
from truecaser import *

args = parseArgs()

if args["command"] == "split":
	print("Generating token files: dev, train, and test...")
	generateTokenSets()
elif args["command"] == "features":
	print("Generating feature files: dev, train, and test...")
	generateFeatureFiles()	
elif args["command"] == "dictionary":
	print("Building mixed case dictionary")
	writeDictionary()
elif args["command"] == "accuracy":
	print(getAccuracy())
elif args["command"] == "learn":
	crfSuiteLearn()
elif args["command"] == "predict":
	crfSuitePredict()
elif args["command"] == "configure":
	try:
		configureSettings(args["source_directory"], args["token_file"], args["crflib"])
	except Exception as e:
		print(e)
elif args["command"] == "restore":
	restoreTokens()




