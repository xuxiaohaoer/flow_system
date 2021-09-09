import sys

from numpy.lib.index_tricks import diag_indices_from
from .model.mult_att_lstm import mult_att_lstm
from .preData import pre_dataset
from sklearn.model_selection import train_test_split
import torch
import torch.utils.data as Data
import torch.nn.functional as F
import copy
import numpy as np
import torch.nn as nn
from torch import optim
from .model_att import LSTM_Attention
from .LSTM_multi_head import BiLSTM_Multi_attention
from . import nnModel
# from nnModel import mult_att_CNN
from .model.mult_att_1d_CNN import  mult_att_CNN
from .model.mult_att_lstm_att import mult_att_lstm_att
from .model.bilstm import BiLSTM
from .model.textcnn import text_cnn
from .model.mult_bilstm import mult_bilstm
from .model.cnn import CNN
from .model.cnn_1d import cnn_1d
import time



from .index import cal_index
from tqdm import tqdm
import os
class DS():
  
    def __init__(self, model_use, feature_type, hidden_num, batch_size, length, dir):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.batch_size = batch_size
        self.model_use = model_use

        self.dataloaders_dict, self.dataset_sizes, self.y_name = pre_dataset(batch_size, feature_type, length, dir)
        word_num =  self.dataloaders_dict["train"].dataset.tensors[0].shape[1]
        word_len = self.dataloaders_dict["test"].dataset.tensors[0].shape[2]

        print("model:", model_use)
        print("word_num:", word_num, "word_len:", word_len)
        if model_use == 'lstm_att':
            self.model = LSTM_Attention(word_num, word_len, hidden_dim=hidden_num, n_layers=1).to(device)
        elif model_use == 'mult_att_cnn':
            self.model = mult_att_CNN(word_num, word_len, out_size=5,kernel_size=3, nums_head=2).to(device)
        elif model_use == "mult_att_lstm":
            self.model = mult_att_lstm(word_num, word_len, hidden_num, nums_head=2).to(device)
        elif model_use =='mult_att_lstm_att':
            self.model = mult_att_lstm_att(word_num, word_len, hidden_num, nums_head=2).to(device)
        elif model_use =='lstm':
            self.model = nnModel.LSTM(word_len, hidden_num=hidden_num).to(device)
        elif model_use =='bilstm':
            self.model = BiLSTM(word_len, hidden_size=hidden_num).to(device)
        elif model_use =='text_cnn':
            self.model = text_cnn(word_num, word_len, out_size = 5).to(device)
        elif model_use =='mult_bilstm':
            self.model = mult_bilstm(word_num, word_len, hidden_num=hidden_num,nums_head=1).to(device)
        elif model_use =='cnn':
            self.model = CNN().to(device)
        elif model_use =='1d_cnn':
            self.model = cnn_1d(word_num, word_len, out_size = 5).to(device)
        self.Loss = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.0001)
        self.best_model_wts = copy.deepcopy(self.model.state_dict())
        self.patience = 20
        self.word_num = word_num
        self.word_len = word_len
      
       

    def train_model(self, save_path, epoch_num=5):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.epoch_num = epoch_num
        best_loss = 100
        flag = True
        for epoch in range(epoch_num):
            result = {'train':{'acc':0, 'loss':0},
                    'val':{'acc':0, 'loss':0}}
            # atts = torch.zeros(55, 55).to(device)
            if not flag:
                break
            for phase in ['train', 'val']:
                if phase == 'train':
                    self.model.train()
                else:
                    self.model.eval()
                runing_loss = 0
                num_correct = 0
                # for step, (x_batch, y_batch) in enumerate(dataloaders_dict[phase]):
                if not flag:
                    break
                for x_batch, y_batch in tqdm(self.dataloaders_dict[phase]):
                    # x_batch = x_batch.unsqueeze(1)
                    x_batch = x_batch.to(device)
                    y_batch = y_batch.to(device)

                    self.optimizer.zero_grad()
                    with torch.set_grad_enabled(phase == 'train'):

                        out = self.model(x_batch)

                        # for i in range(att.shape[0]):
                        #     atts += att[i]
                        # y_oh = F.one_hot(y_batch, 2).to(device)
                        loss = self.Loss(out, y_batch)
                        if phase == 'train':
                            loss.backward()
                            self.optimizer.step()
                        pred = out.argmax(dim=1)
                    runing_loss += loss.item() * x_batch.size(0)
                    num_correct += torch.eq(pred, y_batch).sum().float().item()

                result[phase]['acc'] = num_correct/self.dataset_sizes[phase]
                result[phase]['loss'] = runing_loss/self.dataset_sizes[phase]

                if phase == 'val':
                    if best_loss < result[phase]['loss']:
                        inc_num += 1
                    else:
                        inc_num = 0
                    if inc_num == self.patience:
                        print("Early stop")
                        flag = False
                        break
                    
                if phase == 'val' and result[phase]['loss']<best_loss:
                    best_loss = result[phase]['loss']
                    self.best_model_wts = copy.deepcopy(self.model.state_dict())
                
            print("epoch:{}/{}".format(epoch+1, epoch_num), "train_acc:{:.3}".format(result['train']['acc']), "train_loss:{:.3}".format(result['train']['loss']),
                "val_acc:{:.3}".format(result['val']['acc']), "val_loss:{:.3}".format(result['val']['loss']))
        self.time_now = time.asctime(time.localtime(time.time()))
        torch.save(self.best_model_wts, '{}/{}.pth'.format(save_path, self.time_now))

    def test_model(self, flag, load_path):
        # model  = nnModel.LSTM().to(device)
        # model = LSTM_Attention(3, 256, 1).to(device)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if flag == "load":
            self.model.load_state_dict(torch.load(load_path, map_location='cpu'))
        else:
            self.model.load_state_dict(self.best_model_wts)
        self.model.eval()
        num_correct = 0
        y_label = []
        y_pred = []
        for step, (x_batch, y_batch)in enumerate(self.dataloaders_dict['test']):
            x_batch = x_batch.to(device)
            y_batch = y_batch.to(device)

            with torch.no_grad():
                out = self.model(x_batch)
                pred = out.argmax(dim=1)
            num_correct += torch.eq(pred, y_batch).sum().float().item()
            y_batch = y_batch.cpu().numpy()
            pred = pred.cpu().numpy()
            for i in y_batch:
                y_label.append(i)
            for i in pred:
                y_pred.append(i)

        cal_index(y_label, y_pred)
        for i in range(len(y_pred)):
            from model_test.models import TlsRes
            t = TlsRes(name = self.y_name[i], result = "black" if y_pred[i] else "white")
            t.save()



    # print("test:",  num_correct / dataset_sizes['test'])

def train():
    model_use = "mult_bilstm"
    feature_type = "mix"
    hidden_num = 144
    batch_size = 32
    length = 25
    feature_dir = "f_data_standard"
    system = DS(model_use = model_use, feature_type = feature_type, hidden_num = hidden_num, batch_size = batch_size, length = length, dir = feature_dir)
    base_dir = "./model_save/"
    experiment = feature_type + '_' + model_use
    dir = base_dir + experiment
    if not os.path.exists(dir):
        os.makedirs(dir)
    system.train_model(save_path = dir, epoch_num=3)

   
    with open(dir + "/" + '{}_ill.txt'.format(system.time_now),'w+',encoding='utf-8') as f:
        list = []
        list.append("model_use:{}\n".format(model_use))
        list.append("feature_type:{}\n".format(feature_type))
        list.append("feature_dir:{}\n".format(feature_dir))
        list.append("hidden_num:{}\n".format(hidden_num))
        list.append("batch_size:{}\n".format(batch_size))
        list.append("word_num:{}\n".format(system.word_num))
        list.append("word_len:{}\n".format(system.word_len))
        list.append("client_hello:{}\n".format(20))
        list.append("server_hello:{}\n".format(10))
        list.append("certificate:{}\n".format(25))
        f.writelines(list)
    f.close()

def test():
    model_use = "mult_bilstm"
    feature_type = "mix"
    hidden_num = 144
    batch_size = 32
    length = 25
    feature_dir = "f_data_standard"
    system = DS(model_use = model_use, feature_type = feature_type, hidden_num = hidden_num, batch_size = batch_size, length = length, dir = feature_dir)
    # system.test_model('load', "./model_save/mix_mult_bilstm/Thu Sep  2 03:24:33 2021.pth")
    system.test_model('load', "./model_save/mix_mult_bilstm/Wed Jul 21 15:51:29 2021.pth")


if __name__ == '__main__':
    model_use = "mult_bilstm"
    feature_type = "mix"
    hidden_num = 144
    batch_size = 32
    length = 25
    feature_dir = "f_data_standard"
    system = DS(model_use = model_use, feature_type = feature_type, hidden_num = hidden_num, batch_size = batch_size, length = length, dir = feature_dir)
    base_dir = "model_save/"
    experiment = feature_type + '_' + model_use
    dir = base_dir + experiment
    if not os.path.exists(dir):
        os.makedirs(dir)
    system.train_model(save_path = dir, epoch_num=200)

   
    with open(dir + "/" + '{}_ill.txt'.format(system.time_now),'w+',encoding='utf-8') as f:
        list = []
        list.append("model_use:{}\n".format(model_use))
        list.append("feature_type:{}\n".format(feature_type))
        list.append("feature_dir:{}\n".format(feature_dir))
        list.append("hidden_num:{}\n".format(hidden_num))
        list.append("batch_size:{}\n".format(batch_size))
        list.append("word_num:{}\n".format(system.word_num))
        list.append("word_len:{}\n".format(system.word_len))
        list.append("client_hello:{}\n".format(20))
        list.append("server_hello:{}\n".format(10))
        list.append("certificate:{}\n".format(25))
        f.writelines(list)
    f.close()
    system.test_model("test", "")
    print(time.asctime(time.localtime(time.time())))
    # system.test_model("load", dir + "/Tue Jul 13 21:03:09 2021.pth")








