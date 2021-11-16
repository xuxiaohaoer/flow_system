## 基于分层自编码器的异常网络流量检测HAE
### 模型训练
`hae_dec.py` HAE模型训练和测试的主函数
`model.py` 模型类：HAE、AE、ABAE
`data_process.py` 数据预处理
`tools.py` 工具类：数据读取、模型评估
`/savedModel/`HAE模型保存与加载路径
### 对比实验
`/experiments/`对比模型：ABAE
