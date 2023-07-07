# TODO: check that no empty files are created

IN_FILE = "es-100l.txt"
OUT_FILE = "dic_part_"
CHUNK = 25_000
line_num = 0
num_file = 1

f = open(IN_FILE, "r")
copy = open(f"{OUT_FILE}{num_file}", "w")
for line in f:
    if line == None:
        exit
    copy.write(line)
    line_num += 1
    if line_num >= CHUNK:
        num_file += 1
        copy.close()
        copy = open(f"{OUT_FILE}{num_file}", "w")
        line_num = 0
f.close()
copy.close()
