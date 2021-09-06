import torch
import torch.nn as nn
import numpy as np

from io import open
import unicodedata
import string
import re
import random

import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
import math
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class BiLSTM_Multi_attention(nn.Module):

    def __init__(self, input_size, hidden_dim, n_layers):
        super(BiLSTM_Multi_attention, self).__init__()
        print(input_size, hidden_dim, n_layers)
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers
        self.input_size = input_size


        self.rnn = nn.LSTM(input_size=input_size,hidden_size=hidden_dim, num_layers=n_layers,batch_first=True,
                           bidirectional=False, dropout=0.1)
        self.f0 = MultiHeadAttention()
        self.fc = nn.Linear(144, 2)
        # self.fc = nn.Linear(hidden_dim * 2, 2)
        self.dropout = nn.Dropout(0.1)

        # x: [batch, seq_len, hidden_dim*2]

    # query : [batch, seq_len, hidden_dim * 2]
    # 软注意力机制 (key=value=x)


    def forward(self, x):
        # [seq_len, batch, embedding_dim]


        # output:[seq_len, batch, hidden_dim*2]
        # hidden/cell:[n_layers*2, batch, hidden_dim]
        x = x.permute(0, 2, 1)
        # print("x:", x.shape)
        output, (final_hidden_state, final_cell_state) = self.rnn(x)
        # print("output:", output.shape)
        # output = output.permute(1, 0, 2)  # [batch, seq_len, hidden_dim*2]
        output = output.permute(0, 2, 1)

        att_output, attention = self.f0(output, output, output)
        # 加入attention机制

        # print("attn_output:", attn_output.shape)

        logit = self.fc(att_output)

        return logit





import torch
import torch.nn as nn
import numpy as np


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
    def __init__(self, model_dim=400, num_heads=4, dropout=0.0):
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

        # 线性映射。
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
