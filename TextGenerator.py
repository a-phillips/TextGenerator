#This program analyzes the word frequency in various books.

from Tkinter import Tk
from tkFileDialog import askopenfilename
Tk().withdraw()


import string
import os
import random


print """Hello! This program will generate a random paragraph using 
a chosen text as the base."""


def get_words():

	#Let the user choose the file, then open it
	text_dir = askopenfilename()
	word_list = []
	with open(text_dir,'r') as text_file:
		text_list = text_file.read().splitlines()
	
	#For each line of text, clean the words and add them to the list
	for line in text_list:
		if '-' in line:
			line = line.replace('-',' ')
		word_split = line.split()
		for word in word_split:
			word = word.strip(string.whitespace)
			word_list.append(word)

	return word_list


def make_prefix_dict(word_list,length=1):
	prefix_dict = dict()

	#Loop through the word list and add the following word to the prefix
	for i in xrange(len(word_list)-length):
		prefix = " ".join(word_list[i:i+length])
		word = word_list[i+length]
		prefix_dict[prefix] = prefix_dict.get(prefix,[])
		prefix_dict[prefix].append(word)	
	return prefix_dict


def write_paragraph(length_min):

	#Get word list, and make the prefix dictionaries
	word_list = get_words()
	one_word_prefixes = make_prefix_dict(word_list, length=1)
	two_word_prefixes = make_prefix_dict(word_list, length=2)

	#Get the first two words
	sentence_words = []
	sentence_words.append(raw_input('Enter the first word:\n'))
	if one_word_prefixes.get(sentence_words[0]):
		next_word = random.choice(one_word_prefixes[sentence_words[0]])
	else:
		next_word = random.choice(word_list)
	sentence_words.append(next_word)

	#Write the paragraph, using the two-word prefix if possible.
	#End the program if the length is higher than specified and 
	#the word ends in a punctuation mark.
	while True:
		if len(sentence_words) > length_min:
			if sentence_words[-1][-1] in '.!?':
				print ' '.join(sentence_words)
				break
		prefix = ' '.join(sentence_words[-2:])
		if two_word_prefixes.get(prefix):
			new_word = random.choice(two_word_prefixes[prefix])
		elif one_word_prefixes.get(sentence_words[-1]):
			new_word = random.choice(one_word_prefixes[sentence_words[-1]])
		else:
			new_word = random.choice(word_list)
		sentence_words.append(new_word)
		

if __name__ == '__main__':
	write_paragraph(40)

	
	

	
