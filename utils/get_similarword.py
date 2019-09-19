from gensim.models import Word2Vec
from collections import defaultdict

path = '../models/news.50.model'
model = Word2Vec.load(path)
out_file = '../data/similar_word_new.txt'

add_word = ['眼中', '称', '地说', '眼里', '正说', '报道',
            '骂', '要说', '坦承', '提议', '承认', '回击',
            '号召', '反驳', '明确要求', '发表声明', '主张',
            '坚称', '澄清', '暗示', '抛出', '描述', '阐述',
            '强调指出', '反复强调', '明确提出', '时称', '感叹',
            '宣布']


def get_related_words(initial_words, model):
    """
    initial_words: 初始词
    model: Word2Vec
    """
    unseen = initial_words
    seen = defaultdict(int)
    max_size = 500

    while unseen and len(seen) < max_size:
        if len(seen) % 100 == 0:
            print('seen length : {}'.format(len(seen)))
        node = unseen.pop(0)
        new_expanding = [w for w, s in model.most_similar(node, topn=20)]
        unseen += new_expanding
        seen[node] += 1
        # optimal 1: add score function
        # optimal 2: using dynamic programming to reduce computing

    return sorted(seen.items(), key=lambda x: x[1], reverse=True)


def save_similar_word(similar_word, file):
    with open(file, 'w+', encoding='utf-8') as fp:
        fp.write(' '.join([w for w,fre in similar_word if fre>=10]+add_word))


def load_similar_word(file):
    with open(file, 'r', encoding='utf-8-sig') as fp:
        return fp.readlines()[0].split(' ')


if __name__ == '__main__':
    res = get_related_words(['说', '报道', '表示'], model)
    save_similar_word(res, out_file)
    res = load_similar_word(out_file)
    print(res)
