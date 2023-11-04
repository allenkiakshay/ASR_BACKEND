import sys,datetime

dirs = sys.argv[1]
language = sys.argv[2]

with open(dirs + '/audio/time_o.txt', 'r') as fr:
    # reading line by line
    lines = fr.readlines()
    lines = lines[:-1]
    # pointer for position
    ptr = 1

    # opening in writing mode
    with open(dirs + '/time.txt', 'w') as fw:
        for line in lines:
            # y = line.replace('created','')
            y = line.replace('.mp3', '_')
            # we want to remove 5th line
            if ptr not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                fw.write(y)
            ptr += 1

file_name = dirs + '/time.txt'
# count=0
time_list = []
with open(file_name, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        # if count==0:
        # count=1
        # continue
        time = line.split("\n")[0].split("_")[2]
        # time = time.replace('created" ','')
        time_list.append(time)
print(len(time_list))

file_name = dirs + "/text.txt"
sentence_list = []
with open(file_name, 'r', encoding='utf-8', errors='ignore') as f:

    for line in f:
        word = line.split("\t")[1].split("\n")[0]
        sentence_list.append(word)
print(len(sentence_list))

file_name = dirs + "/transcript.xml"
wfile = open(file_name, 'w+', encoding='utf-8')
i = 0

wfile.write('<?xml version="1.0" encoding="UTF-8"?>' + "\n")
wfile.write(f'<transcript lang="{language}">' + "\n")
for j in range(len(sentence_list)):
    sentence = sentence_list[j].split(", (")
    time = time_list[j]
    wfile.write("<line timestamp=\"" + str(time) + "\" speaker=\"Speaker_1\">" + "\n")
    # word = sentence.split(" ")
    for k in range(len(sentence)):
        word_line = sentence[k].split(",")
        word = word_line[0].replace("[('", "").replace("'", "").replace(")", "").replace("<s>","")
        if j == 0:
            word_timestamp = word_line[2].replace("[('","").replace("'","").replace(")","").replace("]","")
            word_timestamp = datetime.timedelta(seconds=float(word_timestamp))
        else:
            word_timestamp = word_line[2].replace("[('", "").replace("'", "").replace(")", "").replace("]", "")
            updated_time = time_list[j-1].split(':')
            if len(updated_time) == 2:
                minutes = int(updated_time[0])
                seconds = float(updated_time[1])
                total_seconds = (minutes * 60) + seconds
            else:
                hours = int(updated_time[0])
                minutes = int(updated_time[1])
                seconds = float(updated_time[2])
                total_seconds = (hours * 3600) + (minutes * 60) + seconds

            word_timestamp = float(total_seconds) + float(word_timestamp)
            word_timestamp = datetime.timedelta(seconds= float(word_timestamp))


        wfile.write("<word timestamp=\"" + str(word_timestamp) +"\" is_valid=\"1\">" + str(word) + "</word>" + "\n")
    wfile.write("</line>" + "\n")
wfile.write('</transcript>')
