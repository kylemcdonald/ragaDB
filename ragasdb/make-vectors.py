import json

def find_ngrams(input_list, n):
  ngrams = zip(*[input_list[i:] for i in range(n)])
  return [''.join(ngram) for ngram in ngrams]

with open('tokens', 'w') as tokens_file, open('words', 'w') as words_file, open('ragas.json') as ragas_file:
	ragas = json.load(ragas_file)
	for raga_name in ragas:
		tokens = set()
		raga = ragas[raga_name]

		# add vadi and samvadi
		if 'vadi' in raga:
			tokens.add(raga['vadi'])
			tokens.add('v_' + raga['vadi'])
		else:
			print('no vadi: ' + raga['vadi'])
		if 'samvadi' in raga:
			tokens.add(raga['samvadi'])
			tokens.add('sv_' + raga['samvadi'])
		else:
			print('no samvadi: ' + raga['samvadi'])

		# use 1-gram (notes), 2-grams, 4-grams
		for n in [1, 2, 4]:
			for notes in find_ngrams(raga['aaroha'], n):
				tokens.add(notes)
				tokens.add('a_' + notes)
			for notes in find_ngrams(raga['avaroha'], n):
				tokens.add(notes)
				tokens.add('d_' + notes)

		words_file.write(raga_name + '\n')
		tokens_file.write('\t'.join(tokens) + '\n')