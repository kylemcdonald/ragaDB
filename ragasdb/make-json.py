from collections import defaultdict
import csv, json, re

with open('ragas.csv', 'r') as ragas_file:
	ragas_data = csv.reader(ragas_file, quotechar='"')
	ragas_data.next()
	ragas = {}
	for row in ragas_data:
		raga = {}
		raga['thaat'] = row[1]
		raga['time'] = row[2]
		raga['aaroha'] = filter(None, row[3].split(','))
		raga['avaroha'] = filter(None, row[4].split(','))
		raga['vadi'] = row[5]
		raga['samvadi'] = row[6]
		raga['pakad'] = filter(None, row[7].split(' '))
		raga['jati'] = row[8]
		ragas[row[0]] = raga

	print json.dumps(ragas, sort_keys=True, indent=2)