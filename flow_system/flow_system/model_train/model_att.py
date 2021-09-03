
from __future__ import unicode_literals, print_function, division
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


class LSTM_Attention(nn.Module):

    def __init__(self, word_num, feature_num, hidden_dim, n_layers):
        super(LSTM_Attention, self).__init__()
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers
        self.input_size = feature_num
        self.rnn = nn.LSTM(input_size= self.input_size, hidden_size=hidden_dim, num_layers=n_layers,batch_first=True,
                           bidirectional=False)
        self.fc = nn.Linear(hidden_dim, 2)
        self.linear_q = nn.Linear(self.hidden_dim, self.hidden_dim)
        self.linear_k = nn.Linear(self.hidden_dim, self.hidden_dim)
        self.linear_v = nn.Linear(self.hidden_dim, self.hidden_dim)
        # self.fc = nn.Linear(hidden_dim * 2, 2)
        self.dropout = nn.Dropout(0.1)

        # x: [batch, seq_len, hidden_dim*2]

    # query : [batch, seq_len, hidden_dim * 2]
    # 软注意力机制 (key=value=x)
    def attention_net(self, query, key, value, mask=None):
        d_k = query.size(-1)  # d_k为query的维度

        key = self.linear_k(key)
        value = self.linear_v(value)
        query = self.linear_q(query)
        scores = torch.matmul(query, key.transpose(1, 2)) / math.sqrt(d_k)
        #         print("score: ", scores.shape)  # torch.Size([128, 38, 38])

        # 对最后一个维度 归一化得分
        alpha_n = F.softmax(scores, dim=-1)
        #         print("alpha_n: ", alpha_n.shape)    # torch.Size([128, 38, 38])
        # 对权重化的x求和
        # [batch, seq_len, seq_len]·[batch,seq_len, hidden_dim*2] = [batch,seq_len,hidden_dim*2] -> [batch, hidden_dim*2]
        context = torch.matmul(alpha_n, value).sum(1)

        return context, alpha_n

    def forward(self, x):
        # [seq_len, batch, embedding_dim]


        # output:[seq_len, batch, hidden_dim*2]
        # hidden/cell:[n_layers*2, batch, hidden_dim]
        # x = x.permute(0, 2, 1)
        # print("x:", x.shape)
        output, (final_hidden_state, final_cell_state) = self.rnn(x)


        # output = output.permute(1, 0, 2)  # [batch, seq_len, hidden_dim*2]
        # output = output.permute(0, 2, 1)
        query = self.dropout(output)

        # 加入attention机制
        attn_output, alpha_n = self.attention_net(output, output, output)
        # print("attn_output:", attn_output.shape)

        logit = self.fc(attn_output)

        return logit



