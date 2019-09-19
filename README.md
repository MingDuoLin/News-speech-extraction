# News-speech-extraction
新闻言论自动提取

**描述**：根据新闻的内容，在线提取言论实体与发表的观点

**工作**：

1. 首先，通过爬虫获取新闻预料，利用Gensim训练300维的新闻词向量。
2. 加载词向量获取“说”的相似词，然后基于广度优先遍历的方法扩充相似词列表，并选取共现频次高的相似词。
3. 利用哈工大的pyltp语言模型对输入的新闻进行分句、分词、命名实体识别，判断新闻是否存在实体，对包含实体的内容进行依存句法分析，若谓语存在相似词列表中，则后面句子为观点内容。
4. 利用 tf-idf 计算句子的相似性，确定观点句子范围。
5. 最后，基于 Flask+Boostrap+Html 搭建 Web 的访问界面。

**todo**：

1. 使用开源词向量，挖掘更多的相似词
2. 解决指代消解、多主体问题
3. 利用 Sentence Embedding 的方法计算句子的相似性

**项目文件**

 data：存放相似词表、语料库

 models：词向量、语言模型

 static：javascript、css、images等

templates：前端 html

views：后端 响应函数

app.py：启动程序



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

1. Flask + Boostrap + Html 搭建 web server

### 测试

![image](https://github.com/MingDuoLin/News-speech-extraction/blob/master/static/images/AutoExtraction.png)

![image](https://github.com/MingDuoLin/News-speech-extraction/blob/master/static/images/result.png)

### 测试与问题

1. 基于句法规则的方法尚无法提取如下语料。```"现任总统马克里出席新闻发布会承认失利"```
2. 如果出现一个动词，前面有多个主体，以最近的主体为准
3. 如果SBV 的 subject 未出现在 实体 中，选择一个 实体 作为 subject


