import os
import json
#import jieba
import os
from hanziconv import HanziConv
from string import punctuation


add_punc='·，。、【 】 “”：；（）《》‘’{}？！⑦()、%^>℃：.”“^-——=&#@￥「」′° —『』'
all_punc=punctuation+add_punc

directory = "./zhwiki20190801_text"
file_list = [os.path.join(directory, x) for x in os.listdir(directory)]
out_file = "./zhwiki20190801.txt"

from pyltp import Segmentor
LTP_DATA_DIR = './ltp_data_v3.4.0'  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
segmentor = Segmentor()
segmentor.load(cws_model_path)
def cut(string):
	return segmentor.segment(string)

fp_wr = open(out_file, 'w', encoding = "utf-8")
for i,file in enumerate(file_list):
	# if i == 1: break
	fp_re = open(file,'r', encoding = "utf-8")
	
	for line in fp_re.readlines():
		# 繁体转简体
		line = HanziConv.toSimplified(line)
		# 分词
		line_seg = " ".join(cut(line))
		# 移除标点符号
		item_list = [item.strip() for item in line_seg if item.strip() not in all_punc if not item.strip().isdigit()]
		# 再次分词
		line_seg_ = " ".join(cut(''.join(item_list)))
		fp_wr.write(line_seg_+'\n')
	
	fp_re.close()
	
	print('{}:{} Finish'.format(i, file))
fp_wr.close()
segmentor.release()