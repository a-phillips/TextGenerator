#This program analyzes the word frequency in various books.

from Tkinter import Tk
from tkFileDialog import askdirectory
from tkFileDialog import askopenfilename
Tk().withdraw()


import string
import os
import random



def get_texts(single_file=False):
	text_files = []
	
	if single_file == True:
		text_path = askopenfilename()
		text_dir = os.path.split(text_path)[0]
		text_files.append(os.path.split(text_path)[1])
	else:
		text_dir = askdirectory()
		for item in os.listdir(text_dir):
			if item[-4:] == '.txt':
				text_files.append(item)
	
	return text_dir, text_files



def get_words(text_dir, text_files):

	word_list = []
	for item in text_files:
		print 'Processing %s' % item[:-4]

		with open(os.path.join(text_dir, item),'r') as text_file:
			raw_text = text_file.read().splitlines()

		#For each line of text, clean the words and add them to the list
		for line in raw_text:
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


def run():
	print """Hello! This program will generate a random paragraph using 
	a chosen text as the base."""
	print ''
	print """The training data can be made up of one .txt file, or all
	.txt files in a directory of your choice."""
	print ''

	while True:
		choice = raw_input("Please enter 's' to choose a single file, or 'd'							 for a directory.\n")
		if choice == 's':
			single_file = True
			break
		elif choice == 'd':
			single_file = False
			break
		else:
			print 'Please enter a valid value'
	print ''
	text_dir, text_files = get_texts(single_file)

	print 'You chose to train the data based on the following %s texts:' % len(text_files)
	for text in text_files:
		print text[:-4]

	print ''
	word_list = get_words(text_dir, text_files)
	print ''
	print 'The word list has been compiled!'
	print ''
	print 'You can choose to train the data on prefixes of up to 3 words long.'
	print ''

	while True:
		pref_length = int(raw_input('Please enter either 1, 2, or 3\n'))
		if pref_length == 1:
			print 'Making prefix dictionary of length 1...'
			one_word_prefixes = make_prefix_dict(word_list, length=1)
			two_word_prefixes = dict()
			three_word_prefixes = dict()
			break
		elif pref_length == 2:
			print 'Making prefix dictionary of length 1...'
			one_word_prefixes = make_prefix_dict(word_list, length=1)
			print 'Making prefix dictionary of length 2...'
			two_word_prefixes = make_prefix_dict(word_list, length=2)
			three_word_prefixes = dict()
			break
		elif pref_length == 3:
			print 'Making prefix dictionary of length 1...'
			one_word_prefixes = make_prefix_dict(word_list, length=1)
			print 'Making prefix dictionary of length 2...'
			two_word_prefixes = make_prefix_dict(word_list, length=2)
			print 'Making prefix dictionary of length 3...'
			three_word_prefixes = make_prefix_dict(word_list, length=3)
			break
		else:
			print 'Please enter a valid value.'
	
	print ''
	while True:
		try:
			par_length = raw_input('Please enter the minimum length of your paragraph\n')
			par_length = int(par_length)
		except:
			print 'Please enter a number.'
		else:
			if par_length > 0:
				break
			else:
				print 'Please enter a positive integer.'
	
	print ''
	print "You're ready to generate your paragraph!"
	print ''
	sentence_words = write_paragraph(word_list, pref_length, par_length, one_word_prefixes, 
									two_word_prefixes, three_word_prefixes)
	print ''
	print 'Here is your paragraph!'
	print ''
	print ' '.join(sentence_words)
	

def write_paragraph(word_list, pref_length, par_length, one_word_prefixes, 
					two_word_prefixes, three_word_prefixes):

	sentence_words = []
	first_word = raw_input('Please enter the first word to start the paragraph:\n')
	sentence_words.append(first_word)

	print ''
	print 'Here we go!'
	print ''

	#Make the sentence at least 3 words long so loop doesn't fail
	if one_word_prefixes.get(sentence_words[0]):
		next_word = random.choice(one_word_prefixes[sentence_words[0]])
	else:
		next_word = random.choice(word_list)
	sentence_words.append(next_word)

	if two_word_prefixes.get(' '.join(sentence_words)):
		next_word = random.choice(two_word_prefixes[' '.join(sentence_words)])
	elif one_word_prefixes.get(sentence_words[1]):
		next_word = random.choice(one_word_prefixes[sentence_words[1]])
	else:
		next_word = random.choice(word_list)
	sentence_words.append(next_word)
	
	while True:
		if len(sentence_words) > par_length:
			if sentence_words[-1][-1] in '.!?':
				return sentence_words
			elif len(sentence_words) > (5*par_length):
				return sentence_words

		next_word = ''

		if pref_length == 3:
			prefix = ' '.join(sentence_words[-3:])
			if three_word_prefixes.get(prefix):
				next_word = random.choice(three_word_prefixes[prefix])

		if pref_length >= 2 and next_word == '':
			prefix = ' '.join(sentence_words[-2:])
			if two_word_prefixes.get(prefix):
				next_word = random.choice(two_word_prefixes[prefix])

		if next_word == '':
			if one_word_prefixes.get(sentence_words[-1]):
				next_word = random.choice(one_word_prefixes[sentence_words[-1]])
			else:
				next_word = random.choice(word_list)

		sentence_words.append(next_word)

		

if __name__ == '__main__':
	run()
	
	

	
