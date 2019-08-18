import re
import jieba


def token(string):
    return ' '.join(re.findall(r'[\d|\w]+', string))


def cut(string):
    return ' '.join(jieba.cut(string))


if __name__ == '__main__':
    print(token('　　新华社德国杜塞尔多夫６月６日电题：乒乓女球迷　\n　　'))
