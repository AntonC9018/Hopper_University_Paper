input_name = 'paper.md'
output_name = 'paper_stripped.txt'

file = open(input_name, 'r')
output = open(output_name, 'w')

line = file.readline()

while line.find('<!-- /TOC -->') == -1:
    line = file.readline()

within_block = False

while True:

    line = file.readline()

    if not line:
        break
    
    if line.find('```') != -1:
        within_block = not within_block
        continue
    
    if within_block:
        continue
    
    output.write(line)

file.close()
output.close()