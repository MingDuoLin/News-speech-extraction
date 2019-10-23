import os
from gensim.models import Word2Vec
import re
import pickle
import jieba
from functools import partial
from scipy.spatial.distance import cosine
import numpy as np
from pyltp import SentenceSplitter


MODEL_DIR = './models'  # 模型目录的路径
w2v_model_path = os.path.join(MODEL_DIR, 'news.50.model')  # 词向量模型路径
fre_dict_path = os.path.join(MODEL_DIR, 'frequence.dic')   # 词频率


def cut(string): return ' '.join(jieba.cut(string))


def preprocess(text):
    text = text.replace(u'\r\n', u' ')
    text = text.replace(u'\u3000', u' ')
    text = text.replace(u'\\r\\n', u' ')
    text = text.replace(u'\\u3000', u' ')
    return text


def sentence_split_by_pytlp(content):
    sentences = SentenceSplitter.split(content)
    return [s.strip() for s in sentences if len(s) != 0]


def split_sentence(sentence):
    pattern = re.compile('[。，,.]：')
    split = pattern.sub(' ', sentence).split()
    return split


class AutoSummarization:
    """
    新闻自动摘要
    """

    def __init__(self):
        """
        初始化模型
        """
        self.model = Word2Vec.load(w2v_model_path)
        with open(fre_dict_path, "rb") as f:
            self.frequence = pickle.load(f)

    def sentence_embedding(self, sentence):
        # weight = alpah/(alpah + p)
        # alpha is a parameter, 1e-3 ~ 1e-5
        alpha = 1e-4

        max_fre = max(self.frequence.values())

        words = cut(sentence).split()

        sentence_vec = np.zeros_like(self.model.wv['测试'])

        words = [w for w in words if w in self.model]

        for w in words:
            weight = alpha / (alpha + self.frequence.get(w, max_fre))
            sentence_vec += weight * self.model.wv[w]

        sentence_vec /= len(words)
        # Skip the PCA
        return sentence_vec

    def get_corrlations(self, text):
        if isinstance(text, list): text = ' '.join(text)

        sub_sentences = text.split()
        sentence_vector = self.sentence_embedding(text)

        correlations = {}

        for sub_sentence in sub_sentences:
            sub_sen_vec = self.sentence_embedding(sub_sentence)
            correlation = cosine(sentence_vector, sub_sen_vec)
            correlations[sub_sentence] = correlation

        return sorted(correlations.items(), key=lambda x: x[1], reverse=True)

    def get_summarization_simple(self, text, score_fn, constraint=200):
        sub_sentence = sentence_split_by_pytlp(text)

        ranking_sentence = score_fn(sub_sentence)
        selected_text = set()
        current_text = ''

        for sen, _ in ranking_sentence:
            if len(current_text) < constraint:
                current_text += sen
                selected_text.add(sen)
            else:
                break

        summarized = []
        for sen in sub_sentence:
            if sen in selected_text:
                summarized.append(sen)

        return summarized

    def get_summarization_simple_by_sen_embedding(self, text, constraint=200):
        text = preprocess(text)
        return ''.join(self.get_summarization_simple(text, self.get_corrlations, constraint))


if __name__ == '__main__':
    test_string = '''
    \u3000\u30006月21日，A股纳入MSCI指数尘埃落定，但当天被寄予厚望的券商股并未扛起反弹大旗。22日，在222只纳入MSCI指数的A股股票中，银行股全线飘红，
    其中招商银行领涨，涨幅达6.66%。保险股和券商股的表现也可圈可点。在这222只股票中，金融板块的股票数量和总市值占比均位居首位。分析人士指出，银行股股息率高、
    估值低、收益稳定，对于资金量较大、投资期限较长的资金存在相当大的吸引力。从国际经验来看，纳入MSCI指数后，相关股市的投资者风格将更加稳健，更加偏好业绩稳定、
    流动性好、风险低的优质蓝筹股。\r\n\u3000\u3000银行股具估值优势\r\n\u3000\u30006月22日，A股金融股表现强势，板块涨幅达1.19%。据平安证券统计，
    在222只纳入MSCI指数的A股股票中，金融板块市值占比达41.32%，其中银行、证券和保险子板块的市值占比分别为27.30%、7.75%和6.24%。\r\n\u3000\u3000多家券商研究报告认为，
    银行等金融股受到纳入MSCI指数的提振，未来更多境外资金将进入金融股。\r\n\u3000\u3000华泰证券表示，在纳入MSCI指数之后，A股将迎来约850亿元人民币的增量资金。
    其中，考虑到222只股票中，金融股市值占比约42%，并且金融股体量大、流动性强、估值低，符合境外资金偏好，有望迎来超过权重的资金比例。预计金融股有望吸引增量资金约350亿元人民币。
    \r\n\u3000\u3000新富资本证券投资中心研究总监廖云龙认为，银行股脱颖而出的主要原因是低估值。市场预期银行股基本面改善，同时市场整体风格偏保守，偏爱低估值。
    22日银行股的大涨是市场风格的延续，是投资者对龙头股和对低估值的防御性选择。\r\n\u3000\u3000东方财富choice统计的一季度末QFII重仓股数据显示，银行股是QFII关注的重点之一。
    在前五十大重仓股中，北京银行、南京银行、宁波银行、上海银行榜上有名。\r\n
    '''


    auto_sum = AutoSummarization()
    result = auto_sum.get_summarization_simple_by_sen_embedding(test_string)
    print(result)

