# Train Word2Vec

### 制作语料库 

1. Wiki语料库：https://dumps.wikimedia.org/zhwiki/20190720/

   **wikiextractor**：https://github.com/attardi/wikiextractor

   0）利用 **wikiextractor** 提取出 json 源文件

   git clone https://github.com/attardi/wikiextractor

   ```
WikiExtractor.py --json -o ../zhwiki20190801 ../zhwiki-20190801-pages-articles-multistream.xml
   ```

   1） 将 json 源文件提取为 text 文件

   2）使用 **hanziconv** 繁体转简体

    **hanziconv**：<https://pypi.org/project/hanziconv/0.2.1/> 

   3）分词、过滤标点符号

2. 新闻语料库：sqlResult_1558435.csv

### 训练词向量

1. Word2vec 模型的增量训练
2. 参数设置


### 利用 **t-SNE** 可视化词向量

   

   

   

   







