# News-speech-extraction
新闻言论自动提取

### 文本处理

工具： HanLTP （哈工大：https://github.com/HIT-SCIR/pyltp）
其他： Stanford oreNLP （斯坦福：https://stanfordnlp.github.io/CoreNLP/）

1. 分句、分词、去标点

2. 词性标注

3. 命名实体识别：判断句子中是否实体

4. 依存语法分析：检测SBV句法结果，分析subject->verb中，verb是否为相似词

5. 确定言论结束：

   1）可以是以一句话作为停止。但是有的言论是有多句的。

   2）利用tf-idf判断两句话之间的相似性

### 词向量的训练

1. 准备语料库（新闻或Wikipedia语料）
2. 繁体转简体
3. 利用Gensim训练词向量

### 获取相似词

1. 基于词向量和图搜索获取相似词 + 人工添加缺失词
2. optimal 1 ：添加评分函数（option）
3. optimal 2 ：利用DP减少计算时间（option）

### Web部署

1. Flask

### 测试与问题

1. 基于句法规则的方法尚无法提取如下语料。```"现任总统马克里出席新闻发布会承认失利"```
2. 如果出现一个动词，前面有多个主体，以最近的主体为准
3. 如果SBV 的 subject 未出现在 实体 中，选择一个 实体 作为 subject