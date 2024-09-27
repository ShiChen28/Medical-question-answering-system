# 创建时间 2022-5-17
# 名称 机器人程序
import gensim
import numpy as np
import jieba
import csv

class Chatbot(object):
    def __init__(self,modelfile = './erke.bin', datafile = '儿科w2v.csv',thre = 0.5,conf = 0.95):
        self.model = [] #Word2Vec模型
        self.Qdata = [] #Qdata为问句的词向量
        self.Adata = [] #Adata为答句
        self.thre = thre #相似度最低阈值
        self.conf = conf #直接输出阈值
        self.model_file = modelfile #文件地址
        self.datafile = datafile
    def load_model(self):
        self.model = gensim.models.KeyedVectors.load_word2vec_format(self.model_file, binary=False)

    def load_QA(self):
        with open(self.datafile, 'r',encoding='gbk',errors='ignore') as f:
            reader = csv.reader(f)
            i = 0
            for row in reader:
                i = i+1
                self.Qdata.append(self.sentence_vector(row[0]))
                self.Adata.append(row[1])

    def answer(self,senten):
        s1 = self.sentence_vector(senten)
        Q = []
        for i in range(len(self.Qdata)):
            s2 = self.Qdata[i]
            sore = np.dot(s1, s2) / (np.linalg.norm(s1) * np.linalg.norm(s2))
            if sore > self.conf:
                return self.Adata[i]
            Q.append(sore)
        Q_max = max(Q)
        if Q_max > self.thre:
            ans = self.Adata[Q.index(Q_max)]
        else:
            ans = '对不起，您的情况我也无能为力呀！'
        return ans

    def sentence_vector(self, s):#计算句子向量
        words = jieba.lcut(s)
        w0 = ' '
        for word in words:
            if word == '，'or word == '？' or word == '。' or word == ',' or word == '，' or word == ':':
                continue
            w0 = w0 + ' ' + word
        words = w0.split()
        v = np.zeros(100)
        for word in words:
            try:
                v += self.model[word]
            except KeyError:
                continue
        if len(words) != 0:
            v = v/len(words)
        return v
