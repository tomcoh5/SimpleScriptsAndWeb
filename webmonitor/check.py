
import re
file1_path = 'C:/Users/טום/Desktop/dict/neta.txt'
file2_path = 'C:/Users/טום/Desktop/dict/tom.txt'

file1_list = list()
with open(file1_path) as fp:
   line = fp.readline()
   while line:
        line = line.strip()
        file1_list.append(line)
        line = fp.readline()


file3_list = list()
file2_list = list()
with open(file2_path) as fp:
   line = fp.readline()
   cnt = 1
   while line:
        line = line.strip()
        file2_list.append(line)
        line = fp.readline()

for date in file2_list:
    replaced = re.sub("</?p[^>]*>", "", date)
    file3_list.append(replaced)

final_list = file3_list + file1_list
print(final_list)
final_list = set(final_list)
final_list = list(final_list)

f = open(file2_path,"w")
f.close()

with open(file2_path, 'w') as filehandle:
    for dates in final_list:
        filehandle.write("\n")
        filehandle.write( "<p>" +'%s' % dates + "</p>")








