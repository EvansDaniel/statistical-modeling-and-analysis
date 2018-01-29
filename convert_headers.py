file_name = 'Homework0.ipynb'#input('What is the ipynb file name?')

import json

ipynb = json.load(open(file_name))

cells = ipynb['cells']

def count_hastags(src):
	src = src.strip()
	pass

for i in range(len(cells)):
	if cells[i]['cell_type'] == 'markdown':
		source_array = cells[i]['source']
		for j in range(len(source_array)):
			src = cells[i]['source'][j]
			if src.strip().startswith('#'): # is this a header line
