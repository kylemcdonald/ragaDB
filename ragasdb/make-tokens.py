import json
import argparse

parser = argparse.ArgumentParser(
	description='Generate tokens and words from ragas.json.')
parser.add_argument('-r', '--root', action='store_true', help='Include vadi and samvadi.')
parser.add_argument('-n', '--notes', action='store_true', help='Include notes.')
parser.add_argument('-b', '--bigrams', action='store_true', help='Include bigrams.')
parser.add_argument('-t', '--tetragrams', action='store_true', help='Include tetragrams.')
parser.add_argument('-d', '--direction', action='store_true', help='Include aaroha vs avaroha distinction.')
parser.add_argument('-o', '--octrep', action='store_true', help='Include octave and repeat distinction.')
args = parser.parse_args()

def find_ngrams(input_list, n):
  ngrams = zip(*[input_list[i:] for i in range(n)])
  ngrams = [''.join(ngram) for ngram in ngrams]
  if args.octrep:
  	ngrams = [ngram.replace("'", '') for ngram in ngrams]
  return ngrams

with open('tokens', 'w') as tokens_file, open('words', 'w') as words_file, open('ragas.json') as ragas_file:
	ragas = json.load(ragas_file)
	grams = []
	if args.notes:
		grams.append(1)
	if args.bigrams:
		grams.append(2)
	if args.tetragrams:
		grams.append(4)
	for raga_name in ragas:
		tokens = set()
		raga = ragas[raga_name]

		# add vadi and samvadi
		if args.root:
			tokens.add('v_' + raga['vadi'])
			tokens.add('sv_' + raga['samvadi'])
			if args.notes:
				tokens.add(raga['vadi'])
				tokens.add(raga['samvadi'])

		for n in grams:
			for notes in find_ngrams(raga['aaroha'], n):
				tokens.add(notes)
				if args.direction:
					tokens.add('a_' + notes)
			for notes in find_ngrams(raga['avaroha'], n):
				tokens.add(notes)
				if args.direction:
					tokens.add('d_' + notes)

		words_file.write(raga_name + '\n')
		tokens_file.write('\t'.join(tokens) + '\n')