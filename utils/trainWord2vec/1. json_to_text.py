import os
import json
import jieba

directory = "./zhwiki20190801"
dire_list = [os.path.join(directory, x) for x in os.listdir(directory)]
out_dire = "./zhwiki20190801_text"
out_dire_list = [os.path.join(out_dire, x) for x in os.listdir(directory)]


for i, dire in enumerate(dire_list):  # ./extract_wiki/AA

    fp_wr = open(os.path.join(out_dire_list[i]), 'w', encoding='utf-8')
    for file in os.listdir(dire):  # ./extract_wiki/AA/wiki_00
        fp_re = open(os.path.join(dire, file), 'r', encoding='utf-8')

        for line in fp_re.readlines():
            content = json.loads(line)['text'].replace('\n', ' ')
            fp_wr.write(content+'\n')
            #print(json.loads(line)['text'])
        fp_re.close()
    fp_wr.close()
    print('finish:{}'.format(dire))

