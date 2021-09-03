import numpy as np
from sklearn.model_selection import train_test_split
import torch
import torch.utils.data as Data

def pre_data():
    """
    截取前144负载
    :return:
    """
    d_train_b = np.load("../datacon/f_data_flow/train_black.npy", allow_pickle=True)
    d_train_w = np.load("../datacon/f_data_flow/train_white.npy", allow_pickle=True)
    d_test_b = np.load("../datacon/f_data_flow/test_black.npy", allow_pickle=True)
    d_test_w = np.load("../datacon/f_data_flow/test_white.npy", allow_pickle=True)
    d_train = np.vstack((d_train_b, d_train_w))
    d_test = np.vstack((d_test_b, d_test_w))
    dataset = np.vstack((d_train, d_test))
    x = []
    y = []
    num_w = 0
    num_b = 0
    for key in dataset:
        # content = []
        # for value in key[0]:
        #     content += value
        # x.append(content)
        x.append(key[0])
        if key[-2] == 'white':
            y.append(1)
            num_w += 1
        else:
            y.append(0)
            num_b += 1
    print(num_w, num_b)
    return x,y

def pre_data_pay():

    base_dir = 'f_data_payload_100'
    d_train_b = np.load("../data/{}/train_black.npy".format(base_dir), allow_pickle=True)
    d_train_w = np.load("../data/{}/train_white.npy".format(base_dir), allow_pickle=True)
    d_test_b = np.load("../data/{}/test_black.npy".format(base_dir), allow_pickle=True)
    d_test_w = np.load("../data/{}/test_white.npy".format(base_dir), allow_pickle=True)
    d_train = np.vstack((d_train_b, d_train_w))
    d_test = np.vstack((d_test_b, d_test_w))
    dataset = np.vstack((d_train, d_test))
    x = []
    y = []
    for key in dataset:
        if (key[1] != 0):
            x.append(key[0])
            if key[-2] == 'white':
                y.append(0)
            else:
                y.append(1)
    print(len(x), len(y))
    return x,y

def pre_data_mix(feature_type):
    """
    位置信息、包大小、负载，对比实验
    :return:
    """
    d_train_b = np.load("../data/f_data_contrast/train_black.npy", allow_pickle=True)
    d_train_w = np.load("../data/f_data_contrast/train_white.npy", allow_pickle=True)
    d_test_b = np.load("../data/f_data_contrast/test_black.npy", allow_pickle=True)
    d_test_w = np.load("../data/f_data_contrast/test_white.npy", allow_pickle=True)
    d_train = np.vstack((d_train_b, d_train_w))
    d_test = np.vstack((d_test_b, d_test_w))
    dataset = np.vstack((d_train, d_test))
    x = []
    y = []

    
    for key in dataset:
        contents = []
        if key[2] != 0:
            
            contents = []
            if feature_type == "packet":
                for i in range(2):
                    contents.append(key[0][i])
                # contents.append(key[0][0])
                # contents.append(key[0][2])
            elif feature_type == "bytes":
                for i in range(1):
                    for value in key[0][i]:
                        contents.append([value])
                # for value in key[0][0]:
                #     contents.append([value])
                # for value in key[0][2]:
                #     contents.append([value])
            x.append(contents)
            if key[-2] == 'white':
                y.append(1)
            else:
                y.append(0)
    return x, y



def pre_data_Image():

    # base_dir = 'f_data_mix'
    base_dir = 'f_data_image'
    d_train_b = np.load("../data/{}/train_black.npy".format(base_dir), allow_pickle=True)
    d_train_w = np.load("../data/{}/train_white.npy".format(base_dir), allow_pickle=True)
    d_test_b = np.load("../data/{}/test_black.npy".format(base_dir), allow_pickle=True)
    d_test_w = np.load("../data/{}/test_white.npy".format(base_dir), allow_pickle=True)
    d_train = np.vstack((d_train_b, d_train_w))
    d_test = np.vstack((d_test_b, d_test_w))
    dataset = np.vstack((d_train, d_test))
    x = []
    y = []
    for key in dataset:
        if (key[1] != 0):
            x.append(key[0])
            if key[-2] == 'white':
                y.append(0)
            else:
                y.append(1)
    print(len(x), len(y))
    return x,y


def pre_data_stand(feature_type, length, dir):
    # base_dir = "f_data_standard"
    base_dir = dir
    d_train_b = np.load("./data_feature/train_black.npy", allow_pickle=True)
    d_train_w = np.load("./data_feature/train_white.npy", allow_pickle=True)
    d_test_b = np.load("./data_feature/test_black.npy", allow_pickle=True)
    d_test_w = np.load("./data_feature/test_white.npy", allow_pickle=True)
    d_train = []
    d_test = []
    for key in d_train_b:
        d_train.append(key)
    for key in d_train_b:
        d_train.append(key)
    for key in d_test_b:
        d_test.append(key)
    for key in d_test_w:
        d_test.append(key)

    
    x_train = []
    y_train = []
    x_test = []
    y_label = []
    y_name = []

    word_num = len(d_train_b[0]["client_hello"])
    word_len = len(d_train_b[0]["client_hello"][0])
    list = ["client_hello",  "server_hello", "certificate"]
    len_list = {"client_hello":20, "server_hello":10, "certificate":25}

    for key in d_train:
        if (key["client_hello"] != [[0]* word_len] * word_num):
            content = []
            for type in list:
                for value in key[type][:len_list[type]]:
                    content.append(value)
                # for value in key[type]:
                #     content.append(value)
            x_train.append(content)
            if key["label"] == 'white':
                y_train.append(0)
            else:
                y_train.append(1)    

    for key in d_test:
        if (key["client_hello"] != [[0]* word_len] * word_num):
            content = []
            for type in list:
                for value in key[type][:len_list[type]]:
                    content.append(value)
                # for value in key[type]:
                #     content.append(value)
            x_test.append(content)
            if key["label"] == 'white':
                y_label.append(0)
            else:
                y_label.append(1)   
            y_name.append(key["name"])
    return x_train, x_test, y_train, y_label, y_name


def pre_dataset(batch_size, feature_type, length, dir):
    # x, y = pre_data_cut()
    if feature_type  in ["client_hello", "server_hello", "certificate", "mix"]:
        x_train, x_test, y_train, y_label, y_name = pre_data_stand(feature_type, length, dir)
    elif feature_type in ["packet", "bytes"]:
        x, y = pre_data_mix(feature_type)
    elif feature_type in ['image']:
        x, y = pre_data_Image()
    elif feature_type in ['payload']:
        x, y = pre_data_pay()
    # x, y = pre_data_mix()
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.2, random_state=42)

    x_train = torch.tensor(x_train)
    x_val = torch.tensor(x_val)
    x_test = torch.tensor(x_test)
    y_label = torch.tensor(y_label)
    y_val = torch.tensor(y_val)
    y_train = torch.tensor(y_train)

    dataloaders_dict = {
        'train': Data.DataLoader(Data.TensorDataset(x_train, y_train), batch_size=batch_size, shuffle=True, num_workers=4),
        'val': Data.DataLoader(Data.TensorDataset(x_val, y_val), batch_size=batch_size, shuffle=False, num_workers=4),
        'test': Data.DataLoader(Data.TensorDataset(x_test, y_label), batch_size=batch_size, shuffle=False, num_workers=4)
        }

    dataset_sizes = {'train': len(x_train),
                     'val': len(x_val),
                     'test': len(x_test)}
    return dataloaders_dict, dataset_sizes, y_name


def cal(sequence):
    # if not sequence:
    if sequence == []:
        return 0, 0, 0, 0
    Max = max(sequence)
    Min = min(sequence)
    seq = np.array(sequence)
    mean = np.mean(seq)
    std = np.std(seq)
    print(Max, Min, mean, std)
    return Max, Min, mean, std

if __name__ == '__main__':
    pre_data_mix("packet")