import os
import re
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pyltp import SentenceSplitter, Segmentor, Postagger, NamedEntityRecognizer, Parser
from string import punctuation
from collections import defaultdict
add_punc = '·，。、【 】 “”：；（）《》‘’{}？！⑦()、%^>℃：.”“^-——=&#@￥「」′° —『』'
all_punc = punctuation + add_punc

LTP_DATA_DIR = './models/ltp_data_v3.4.0'  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径
similar_word_file = './data/similar_word.txt'


def token(string):
    return ' '.join(re.findall(r'[\d|\w]+', string))


def cut(string):
    return ' '.join(jieba.cut(string))


def load_similar_word():
    with open(similar_word_file, 'r', encoding='utf-8-sig') as fp:
        return fp.readlines()[0].split(' ')


class AutoExtraction:
    """
    新闻言论自动抽取
    """

    def __init__(self):
        """
        初始化模型
        """
        self.seg_sent = SentenceSplitter()  # 分句
        self.seg = Segmentor()  # 分词
        self.seg.load(cws_model_path)
        self.pos = Postagger()  # 词性标注
        self.pos.load(pos_model_path)
        self.ner = NamedEntityRecognizer()  # 命名实体识别
        self.ner.load(ner_model_path)
        self.par = Parser()  # 依存分析
        self.par.load(par_model_path)
        self.similar_word = load_similar_word()  # 读取相似词列表

    def _sentence_split(self, content):
        sentences = self.seg_sent.split(content)
        return [s for s in sentences if len(s) != 0]

    def _del_punctuation(self, sent):
        """
        1.分词
        2.移除标点符号
        3.再次分词
        """
        sent_seg = self._cut(sent)
        item_list = [item.strip() for item in sent_seg if item.strip() not in all_punc]
        sent_seg = self._cut(''.join(item_list))
        return sent_seg

    def _cut(self, sent):
        return ' '.join(self.seg.segment(sent))

    def _pos(self, sent):
        words = sent.split(' ')
        pos_tags = self.pos.postag(words)
        return list(pos_tags)

    def _ner(self, sent, pos_tags):
        sentence_tag = self.ner.recognize(sent.split(' '), pos_tags)
        return list(sentence_tag)

    def _par(self, sent, sentence_tag):
        arcs = self.par.parse(sent, sentence_tag)
        return [(arc.head, arc.relation) for arc in arcs]

    @classmethod
    def _exist_ner(cls, sentence_tag):
        """
        判断句子的ner结果是否存在实体，并返回实体内容
        """
        # Ni Ns Nhr
        ner_dic = defaultdict(int)
        ner_set = ['S-Ni', 'S-Ns', 'S-Nh', 'B-Ni', 'B-Ns', 'B-Nh', 'I-Ni', 'I-Ns', 'I-Nh', 'E-Ni', 'E-Ns', 'E-Nh']
        i = 0
        while i < len(sentence_tag):
            for j in range(i, len(sentence_tag)):
                if sentence_tag[j] not in ner_set: break
            if j == i:
                i += 1
            else:
                ner_dic[i] = j
                i = j
        return ner_dic

    @classmethod
    def _tf_idf(cls, text_list):
        """
        计算tf-idf
        """
        tf_idf = TfidfVectorizer()
        return tf_idf.fit_transform(text_list)

    @classmethod
    def _cosine_sim(cls, x1, x2):
        """
        文本相似性
        """
        return cosine_similarity(x1, x2)

    def _has_next_sentence(self, x1, x2, threshold):
        """
        判断是否有下一句话
        """
        sim = self._cosine_sim(x1, x2)[0][0]
        if sim > threshold:
            print(sim)
            return True
        return False

    def process(self, content):
        """
        content: 输入的新闻预料
        return: 输出人物和对应言论
        """
        # 1. 分句
        sents = self._sentence_split(content)
        # 2. 分词、去标点
        sents_ = [self._del_punctuation(s) for s in sents]
        # 3. 词性标注
        postags = [self._pos(s) for s in sents_]
        # 4. 命名实体识别
        netags = [self._ner(s, p) for s, p in zip(sents_, postags)]
        # 5. 依存句法分析
        arcs_list = [self._par(w.split(' '), n) for w, n in zip(sents_, netags)]
        # 6. tf-idf
        tf_idf_vec = self._tf_idf(sents_)

        extract_result = []
        for index, netag in enumerate(netags):
            ner_dic = self._exist_ner(netag)
            # print(ner_dic)
            if not ner_dic:  # 判断是否存在实体
                continue

            words = sents_[index].split(' ')
            # print(words)
            subject_verb = defaultdict(int)
            # (i, arc[0]-1)
            for i, arc in enumerate(arcs_list[index]):
                if arc[1] == 'SBV':  # [(subject_index, verb_index),...]
                    if (arc[0] - 1) not in subject_verb.keys():
                        subject_verb[arc[0] - 1] = i
                    else:
                        if i > subject_verb[arc[0] - 1]:
                            subject_verb[arc[0] - 1] = i
                            # print('words:{}\n ner:{}\n arcs:{}\n s_b:{}\n'.format(words,netags[index], arcs,subject_verb))

            for v, s in subject_verb.items():  # 根据句法分析获得的 实体索引 s 和 动词索引 v

                if words[v] in self.similar_word:  # 判断动词是否为相似词
                    # print('s:{},v:{}'.format(s,v))

                    # 如果SBV的 subject 不在实体，则任选一个距离s和v最近的实体作为 subject
                    if s in ner_dic.keys():
                        subject = ''.join(words[s:ner_dic[s]])
                    else:
                        l = [(n[0], n[1], s - n[0]) for n in list(ner_dic.items()) if n[0] < v and n[0] < s]
                        if l:  # 如果前面不存在实体, 则选择非实体词
                            start, end, _ = min(l, key=lambda x: x[2])
                            subject = ''.join(words[start: end])
                        else:
                            subject = words[s]

                    said = words[v]

                    #  判断下一句话是否与当前是同一个语境：1）存在下一句话 2）两句话相似 3）下一句不存在实体
                    speech = sents[index].split(words[v])[1]
                    if index < len(netags) - 1 and self._has_next_sentence(tf_idf_vec[index], tf_idf_vec[index + 1],
                                                                           0.1) and not self._exist_ner(
                            netags[index + 1]):
                        # print('similar:{},{}'.format(sents[index], sents[index + 1]))
                        speech += sents[index + 1]

                    extract_result.append(
                        (subject, said, speech)
                    )

        return extract_result

    def release(self):
        """
        :释放模型
        """
        self.seg.release()
        self.pos.release()
        self.ner.release()
        self.par.release()


if __name__ == '__main__':
    print(token('　　新华社德国杜塞尔多夫６月６日电题：乒乓女球迷　\n　　'))
    test_string = """
    对此，特朗普2小时后也在推特上反击：“告诉贾斯廷⋅特鲁多总理和马克龙总统，他们正在收取美国巨额关税，并制造非货币贸易壁垒。欧盟与美国的贸易顺差为1510亿美元，加拿大影响我们农民的生计。”
    5月31日，特朗普宣布将对加拿大、墨西哥与欧盟开征钢铝进口关税，加拿大、墨西哥随即采取报复性措施，欧盟的反击也箭在弦上，贸易战的恐慌再度引发关注。美国此举让众盟友怨声载道，六国财长纷纷发声要在G7峰会上向特朗普“摊牌”。
    """
    textPro = AutoExtraction()
    extra_res = textPro.process(test_string)
    print(extra_res)
    textPro.release()
