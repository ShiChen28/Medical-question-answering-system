# 一个小作业
基于MySQL和Word2Vec模型实现一个简单的带机器人对话系统的医疗咨询平台

![teaserfigure](pic.png)

机器人对话的实现仅仅只是利用训练好的Word2Vec模型将语句转成词向量，并利用词向量实现语句相似性计算，利用已经准备好的问答数据集，返回相似性最高的问句对应的回答。

详细项目信息及设计思路说明可见设计文档: `智能医疗问答系统设计文档_Chanser.pdf`。

# 代码文件
`Client.py` 客户端程序

`Server.py` 服务器程序

`dbutil.py` 数据库工具类

`Robot.py` 机器人类

`erke.bin` Word2Vec模型文件(儿科问题相关)


# 数据集
感谢Toyhom提供的Chinese medical dialogue data 中文医疗问答数据集：

https://github.com/Toyhom/Chinese-medical-dialogue-data

# 运行
首先运行`Server.py`，待显示开始开放连接后运行`Client.py`客户端


