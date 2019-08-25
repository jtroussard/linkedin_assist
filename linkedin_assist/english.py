#!/usr/bin/python3

"""A bunch of functions to facilitate english language rules for string manipulations"""

VOWELS = ['a','e','i','o','u']

def pluralize(word):
	if word.endswith('s') or word.endswith('o'):
		pluralized = "{}es".format(word)

	elif word.endswith('f') or word.endswith('fe'):
		pluralized = "{}ves".format(word)

	elif word.endswith('y'):
		if word[-2] not in VOWELS:
			pluralized = "{}ies".format(word[:-1])
		else:
			pluralized = "{}s".format(word)

	elif word.endswith('us'):
		pluralized = "{}i".format(word[:-2])

	elif word.endswith('is'):
		pluralized = "{}es".format(word[:-2])

	elif word.endswith('on'):
		pluralized = "{}a".format(word[:-2])

	elif word.endswith('man'):
		pluralized = "{}men".format(word[:-3])
	else:
		pluralized = "{}s".format(word)
	return pluralized