from collections import defaultdict
import csv, json, re

with open('nodes.csv', 'rU') as nodes_file, open('edges.csv', 'rU') as edges_file:
	nodes_data = csv.reader(nodes_file, quotechar='\'')
	nodes_data.next()
	nodes = defaultdict(dict)
	for row in nodes_data:
		nodes[row[0]]['type'] = row[1]
		nodes[row[0]]['label'] = row[2]

	edges_data = csv.reader(edges_file, quotechar='\'')
	edges_data.next()
	data = defaultdict(dict)
	for row in edges_data:
		target = row[1]
		if target.isdigit():
			name = nodes[row[0]]['label']
			prop = row[2]
			val = nodes[target]['label']
			data[name][prop] = val

	for key in data.keys():
		raga = data[key]
		raga['a'] = {}
		raga['d'] = {}
		subkeys = []
		for subkey in raga.keys():
			m = re.match('([ad])(\d+)', subkey)
			if m:
				raga[m.group(1)][m.group(2)] = raga[subkey]
				subkeys.append(subkey)
		for subkey in subkeys:
			raga.pop(subkey)
		raga['a'] = [value for key, value in sorted(raga['a'].items())]
		raga['d'] = [value for key, value in sorted(raga['d'].items())]

	print json.dumps(data, sort_keys=True, indent=2)