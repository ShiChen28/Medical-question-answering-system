# 一个软件工程小作业
基于MySQL和Word2Vec模型实现一个简单的带机器人对话系统的医疗咨询平台

![teaserfigure](pic.png)

机器人对话的实现仅仅只是先由在语料上训练好的Word2Vec模型将语句转成词向量，并利用词向量实现语句相似性计算，利用已经准备好的问答数据集，返回相似性最高的问句对应的回答。

详细项目信息及设计思路说明可见设计文档: `智能医疗问答系统设计文档_Chanser.pdf`。

本项目仅作参考交流，UI界面所用图片来源网络(由于时间过去太久我也忘了是从哪儿找到的)。感谢这些图片作者的贡献！如有侵权请联系我删除：shichen2001x@gmail.com 。

# 代码文件
`Client.py` 客户端程序

`Server.py` 服务器程序

`dbutil.py` 数据库工具类

`Robot.py` 机器人类

`erke.bin` Word2Vec模型文件(儿科问题相关)


# 语料
感谢Toyhom提供的中文医疗问答数据集: [Chinese medical dialogue data](https://github.com/Toyhom/Chinese-medical-dialogue-data)

# 运行
首先运行`Server.py`，待显示开始开放连接后运行`Client.py`客户端


