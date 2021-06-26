input_name = 'paper_ro.md'
output_name = 'paper_ro_stripped.md'

file = open(input_name, 'r')
output = open(output_name, 'w')

line = file.readline()

while line:
     

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