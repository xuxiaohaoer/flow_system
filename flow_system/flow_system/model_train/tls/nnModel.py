
import torch
from torch import nn
import numpy as np
from torch.autograd import Variable
import torch.nn.functional as F
import torch

Max_length = 128
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")



class LSTM(nn.Module):
    """文本分类，RNN模型"""

    def __init__(self, input_size, hidden_num):

        super(LSTM, self).__init__()

        self.input_size = input_size
        self.hidden_size = hidden_num
        # 三个待输入的数据

        # self.attn = nn.Linear(self.hidden_size * 2, self.max_length)
        # self.attn_combine = nn.Linear(self.hidden_size * 2, self.hidden_size)

        self.rnn = nn.LSTM(input_size=self.input_size, hidden_size= self.hidden_size, num_layers=1, batch_first=True)
        # self.rnn = nn.GRU(input_size=64, hidden_size=128, num_layers=2, bidirectional=True)
        # self.f1 = nn.Sequential(nn.Linear(256, 128),
        #                         nn.Dropout(0.8),
        #                         nn.ReLU())
        # self.f1 = nn.Sequential(nn.Linear(128, 2),
        #                         nn.Softmax())

        self.f0 = nn.Dropout(p=0.05)
        self.f1 = nn.Linear(self.hidden_size,84)
        self.f2 = nn.Linear(84, 2)

        # self.f2 = nn.Sigmoid()

    def forward(self, x):
        # attn_weights = F.softmax(
        #     self.attn(torch.cat((x[0], hidden[0]), 1)), dim=1)
        # attn_applied = torch.bmm(attn_weights.unsqueeze(0),
        #                          encoder_outputs.unsqueeze(0))

        # x = x.unsqueeze(2)
        # x = torch.tensor(x, dtype=torch.float32)

        output, (hn, cn)= self.rnn(x)

        output = hn.squeeze(0)

        # s, b, h = output.size()
        # output = output.view(s * b, h)
        # output = output[-1, :, :]
        output = self.f0(output)
        output = F.relu(self.f1(output))
        predict = self.f2(output)
        
        res = predict
        # res = F.softmax(predict, dim=1)


        # result = predict.squeeze(0)
        return res


class attCnn(nn.Module):

    def __init__(self, hidden_size, max_length = Max_length):
        self.hidden_size = hidden_size
        self.max_length = max_length

        super(attCnn, self).__int__()
        self.att = nn.Linear(self.hidden_size*2, self.max_length)
        self.attn_combine = nn.Linear(self.hidden_size*2, self.hidden_size)
        self.f0 = nn.Linear(self.hidden_size, 2)

    def forward(self, input, hidden):
        input = input.view(1,1,-1)
        attn_weights = F.softmax(
            self.att(torch.cat((input[0], hidden[0]), 1)), dim=1)
        atn_applied = torch.bmm(attn_weights.unsqueeze(0),
                                input.unsqueeze(0))
        att_tem = torch.cat((input[0], atn_applied[0]),1)
        att_end = self.attn_combine(att_tem).unsqueeze(0)
        output = self.f0(att_end)
        return output


    def initHidden(self):
        return torch.zeros(1, 1, self.hidden_size, device=device)



class Attention(nn.Module):
    def __init__(self, feature_dim, step_dim, bias=True, **kwargs):
        super(Attention, self).__init__(**kwargs)
        self.supports_masking = True
        self.bias = bias
        self.feature_dim = feature_dim
        self.step_dim = step_dim
        self.features_dim = 0

        weight = torch.zeros(feature_dim, 1)
        nn.init.kaiming_uniform_(weight)
        self.weight = nn.Parameter(weight)

        if bias:
            self.b = nn.Parameter(torch.zeros(step_dim))

    def forward(self, x, mask=None):
        feature_dim = self.feature_dim
        step_dim = self.step_dim

        eij = torch.mm(x.contiguous().view(-1, feature_dim),
                       self.weight).view(-1, step_dim)
        if self.bias:
            eij = eij + self.b
        eij = torch.tanh(eij)
        a = torch.exp(eij)

        if mask is not None:
            a = a * mask
        a = a / (torch.sum(a, 1, keepdim=True) + 1e-10)

        weighted_input = x * torch.unsqueeze(a, -1)
        return torch.sum(weighted_input, 1)

class cnnAtt(nn.Module):
    def __init__(self, feature_num, hidden_length):

        super(cnnAtt, self).__init__()
        num_filters = 128
        self.att = Attention(feature_num, num_filters)
        self.f0 = nn.Dropout(p=0.1)
        self.f1 = nn.Linear(hidden_length, 2)
        self.f2 = nn.Sigmoid()

    def forward(self, input):
        att = self.att(input)
        att = self.f0(att)
        output = self.f1(att)
        output = self.f2(output)
        return output



class mult_att_CNN(nn.Module):
    def __init__(self, input_size, feature_num, hidden_num):
        super(mult_att_CNN, self).__init__()
        self.input_size = input_size
        self.feature_num = feature_num
        self.hidden_num = hidden_num

        self.f0 = nn.Linear(feature_num, feature_num)
        self.multAtt = MultiHeadAttention()
        self.f1 = nn.Linear(feature_num, 2)

    def forward(self, input):

        print(input.shape)
        tem = self.f0(input)
        print(tem.shape)
        context, att = self.multAtt(tem, tem, tem)
        print(context.shape)
        return context



class dot_attention(nn.Module):
    """ 点积注意力机制"""

    def __init__(self, attention_dropout=0.0):
        super(dot_attention, self).__init__()
        self.dropout = nn.Dropout(attention_dropout)
        self.softmax = nn.Softmax(dim=2)

    def forward(self, q, k, v, scale=None, attn_mask=None):
        """
        前向传播
        :param q:
        :param k:
        :param v:
        :param scale:
        :param attn_mask:
        :return: 上下文张量和attention张量。
        """
        attention = torch.bmm(q, k.transpose(1, 2))
        if scale:
            attention = attention * scale        # 是否设置缩放
        if attn_mask:
            attention = attention.masked_fill(attn_mask, -np.inf)     # 给需要mask的地方设置一个负无穷。
        # 计算softmax
        attention = self.softmax(attention)
        # 添加dropout
        attention = self.dropout(attention)
        # 和v做点积。
        context = torch.bmm(attention, v)
        return context, attention



class MultiHeadAttention(nn.Module):
    """ 多头自注意力"""
    def __init__(self, model_dim=256, num_heads=4, dropout=0.0):
        super(MultiHeadAttention, self).__init__()

        self.dim_per_head = model_dim//num_heads   # 每个头的维度
        self.num_heads = num_heads
        self.linear_k = nn.Linear(model_dim, self.dim_per_head * num_heads)
        self.linear_v = nn.Linear(model_dim, self.dim_per_head * num_heads)
        self.linear_q = nn.Linear(model_dim, self.dim_per_head * num_heads)

        self.dot_product_attention = dot_attention(dropout)

        self.linear_final = nn.Linear(model_dim, model_dim)
        self.dropout = nn.Dropout(dropout)
        self.layer_norm = nn.LayerNorm(model_dim)         # LayerNorm 归一化。

    def forward(self, key, value, query, attn_mask=None):
        # 残差连接
        residual = query

        dim_per_head = self.dim_per_head
        num_heads = self.num_heads
        batch_size = key.size(0)

        # 线性映射
        key = self.linear_k(key)
        value = self.linear_v(value)
        query = self.linear_q(query)

        # 按照头进行分割
        key = key.view(batch_size * num_heads, -1, dim_per_head)
        value = value.view(batch_size * num_heads, -1, dim_per_head)
        query = query.view(batch_size * num_heads, -1, dim_per_head)

        if attn_mask:
            attn_mask = attn_mask.repeat(num_heads, 1, 1)

        # 缩放点击注意力机制
        scale = (key.size(-1) // num_heads) ** -0.5
        context, attention = self.dot_product_attention(query, key, value, scale, attn_mask)

        # 进行头合并 concat heads
        context = context.view(batch_size, -1, dim_per_head * num_heads)

        # 进行线性映射
        output = self.linear_final(context)

        # dropout
        output = self.dropout(output)

        # 添加残差层和正则化层。
        output = self.layer_norm(residual + output)

        return output, attention
