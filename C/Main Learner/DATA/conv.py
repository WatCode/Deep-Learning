import json

filer = open("CONVRAW.json", "r").read()

raw_dict = json.loads(filer)
freq_dict = {}
conv_list = []

for entry_data in raw_dict:
    dialog = entry_data["dialog"]
    temp_list = []

    for message_data in dialog:
        text = message_data["text"]
        words_raw = [word.lower() for word in text.split(" ")]
        words = []

        for word_raw in words_raw:
            word = ""

            for i in word_raw:
                if i in "abcefghijklmnopqrstuvwxyz'":
                    word += i

            if len(word) > 0:
                if word not in freq_dict:
                    freq_dict[word] = 0

                freq_dict[word] += 1
                words.append(word)
        
        temp_list.append(words)

    conv_list.append(temp_list)

word_dict = {}

for word in freq_dict:
    freq = freq_dict[word]

    if freq not in word_dict:
        word_dict[freq] = []
    
    word_dict[freq].append(word)

rank_dict = {}
counter = 1

for freq in sorted(word_dict)[::-1]:
    word_list = sorted(word_dict[freq])[::-1]

    for word in word_list:
        rank_dict[word] = counter

        counter += 1

filew = open("CONV.txt", "w")

to_write = ""

for dialog in conv_list[:30]:
    for i in range(len(dialog)-1):
        words_in = dialog[i]
        words_out = dialog[i+1]

        temp_in = ""
        temp_out = ""

        for i in range(100):
            if i < len(words_in):
                temp_in += str(rank_dict[words_in[i]])+","
            else:
                temp_in += "0,"
            if i < len(words_out):
                temp_out += str(rank_dict[words_out[i]])+","
            else:
                temp_out += "0,"
        
        to_write += temp_in[:-1]+":"+temp_out[:-1]+"\n"

filew.write(to_write[:-1])
filew.close()