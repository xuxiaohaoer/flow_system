import numpy as np
from sklearn.model_selection import train_test_split
import torch
import torch.utils.data as Data




def pre_data_stand(feature_type, length, dir):
    # base_dir = "f_data_standard"
    base_dir = dir
    d_train_b = np.load("./data_feature/tls/train_black.npy", allow_pickle=True)
    d_train_w = np.load("./data_feature/tls/train_white.npy", allow_pickle=True)
    d_test_b = np.load("./data_feature/tls/test_black.npy", allow_pickle=True)
    d_test_w = np.load("./data_feature/tls/test_white.npy", allow_pickle=True)
    d_train = []
    d_test = []
    for key in d_train_b:
        d_train.append(key)
    for key in d_train_w:
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
    # x, y = pre_data_mix()
    x = []
    y = []

    for key in x_train:
        x.append(key)
    for key in x_test:
        x.append(key)
    for key in y_train:
        y.append(key)
    for key in y_label:
        y.append(key)
    
    x_train, x_test, y_train, y_label = train_test_split(x, y, test_size=0.33, random_state=43)
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
