import sys
import json
import re
import pprint

if len(sys.argv) != 3:
	print('Must provide file name of ipynb to convert headers of and output file')
	sys.exit(1)

file_name = sys.argv[1]
output_file = sys.argv[2]
ipynb_file = open(file_name, 'r+')
ipynb = json.load(ipynb_file)

cells = ipynb['cells']

def count_hastags(src):
	src = src.strip()
	i = 0
	c = 0
	while(src[i] == '#'):
		c += 1
		i += 1
	return [c, i]

# Find every # header in the .ipynb and conver to 
# the corresponding <h{1,2,3,4,5,6}> tag in html
num_headers = 0
for i in range(len(cells)):
	if cells[i]['cell_type'] == 'markdown':
		if 'toc' in cells[i]['metadata'] and not cells[i]['metadata']['toc']:
			continue;
		source_array = cells[i]['source']
		for j in range(len(source_array)):
			# This will remove all \n and \r stuff
			src = cells[i]['source'][j]
			if src.strip().startswith('#'): # is this a header line
				num_headers += 1
				count, last_hashtag_index = count_hastags(src)
				start = '<h' + str(count) 
				a_id = re.sub(r'[\n\r]+', '', src[last_hashtag_index:].strip().replace(' ', '-'))
				replacement = start + ' id='+ a_id +'>' + src[last_hashtag_index:].strip() + start + '/>'
				#ipynb['cells'][i]['source'][j] = replacement

file_to_write = open(output_file, 'w+')
print('Found {} headers. Writing to {}'.format(num_headers, output_file))

# Remove everything from the file, 
# this isn't necessary anymore but oh well
file_to_write.seek(0)
file_to_write.truncate()
file_to_write.write(json.dumps(ipynb))