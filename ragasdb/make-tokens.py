import json
import argparse
import re

parser = argparse.ArgumentParser(
	description='Generate tokens and words from ragas.json.')
parser.add_argument('-v', '--vadi', action='store_true', help='Include vadi and samvadi.')
parser.add_argument('-n', '--notes', action='store_true', help='Include notes.')
parser.add_argument('-b', '--bigrams', action='store_true', help='Include bigrams.')
parser.add_argument('-t', '--tetragrams', action='store_true', help='Include tetragrams.')
parser.add_argument('-d', '--direction', action='store_true', help='Include aaroha vs avaroha distinction.')
parser.add_argument('-o', '--octave', action='store_true', help='Include octave distinction.')
parser.add_argument('-r', '--repeat', action='store_true', help='Include repeat distinction.')
args = parser.parse_args()

repeat_regex = re.compile("'$")
repeat_replace = "x" if args.repeat else ""
octave_regex = re.compile("^'")
octave_replace = "o" if args.octave else ""

def filter_note(note):
	note = repeat_regex.sub(repeat_replace, note)
	note = octave_regex.sub(octave_replace, note)
	return note

def find_ngrams(input_list, n):
	ngrams = zip(*[input_list[i:] for i in range(n)])
	ngrams = [''.join(ngram) for ngram in ngrams]
	return ngrams

with open('tokens', 'w') as tokens_file, open('words', 'w') as words_file, open('ragas.json') as ragas_file:
	ragas = json.load(ragas_file)

	# select which ngrams to use (including individual notes)
	grams = []
	if args.notes:
		grams.append(1)
	if args.bigrams:
		grams.append(2)
	if args.tetragrams:
		grams.append(4)

	for raga_name in ragas:
		tokens = set() # assumes that repetition of ngrams is not significant (likely false)
		raga = ragas[raga_name]

		# add vadi and samvadi
		if args.vadi:
			vadi = filter_note(raga['vadi'])
			samvadi = filter_note(raga['samvadi'])
			tokens.add('v_' + vadi)
			tokens.add('sv_' + samvadi)
			if args.notes:
				if args.direction:
					# treat them as present in both aaroha and avaroha
					tokens.add('a_' + vadi)
					tokens.add('a_' + samvadi)
					tokens.add('d_' + vadi)
					tokens.add('d_' + samvadi)
				else:
					tokens.add(vadi)
					tokens.add(samvadi)

		# add other ngrams (including individual notes)
		aaroha = [filter_note(note) for note in raga['aaroha']]
		avaroha = [filter_note(note) for note in raga['avaroha']]
		for n in grams:
			for notes in find_ngrams(aaroha, n):
				if args.direction:
					tokens.add('a_' + notes)
				else:
					tokens.add(notes)
			for notes in find_ngrams(avaroha, n):
				if args.direction:
					tokens.add('d_' + notes)
				else:
					tokens.add(notes)
					
		words_file.write(raga_name + '\n')
		tokens_file.write('\t'.join(tokens) + '\n')