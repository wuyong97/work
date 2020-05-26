#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import pickle
import jieba
import numpy as np
import random
import config


def get_word2id_id2word_embeddings(data_path):
    # get word2id,id2word,embeddings(already saved from paper'Few-shot')
    with open(os.path.join(data_path, 'word2id.pkl'), 'rb') as read_word2id:
        word2id = pickle.load(read_word2id)
    with open(os.path.join(data_path, 'id2word.pkl'), 'rb') as read_id2word:
        id2word = pickle.load(read_id2word)
    with open(os.path.join(data_path, 'embeddings.pkl'), 'rb') as read_embeddings:
        embeddings = pickle.load(read_embeddings)
    return word2id, id2word, embeddings

def train_data_processing(data_path):
    conf = config.Config()
    path1 = os.path.join(data_path, 'text_a_train.pkl')
    path2 = os.path.join(data_path, 'length_a_train.pkl')
    path3 = os.path.join(data_path, 'text_b_train.pkl')
    path4 = os.path.join(data_path, 'length_b_train.pkl')
    path5 = os.path.join(data_path, 'y_train.pkl')
    train_data_path = os.path.join(data_path, 'train.txt')
    if ((os.path.exists(path1)) & (os.path.exists(path2)) & (os.path.exists(path3)) & (
            os.path.exists(path4)) & (os.path.exists(path5))) == 0:
        text_a = []
        text_b = []
        length_a = []
        length_b = []
        max_length = conf.max_length
        y = []

        with open(train_data_path, 'r', encoding='utf-8') as read_data:
            all_content = read_data.readlines()
            random.shuffle(all_content)
        for content in all_content:
            if content:
                line = content.strip().split('\t')
                text_a.append(line[0])
                text_b.append(line[1])
                y.append(int(line[2]))
        #processing text_a
        for i in range(len(text_a)):
            id_blank = word2id['BLANK']
            ids = [id_blank for _ in range(max_length)]
            content_a = list(jieba.cut(text_a[i], cut_all=False))
            for j in range(len(content_a)):
                if j >= max_length:
                    break
                else:
                    if content_a[j] in word2id:
                        ids[j] = word2id[content_a[j]]
                    else:
                        ids[j] = word2id['UNK']
            length_a.append(min(max_length, len(content_a)))
            text_a[i] = ids
        text_a = np.array(text_a)
        length_a = np.array(length_a)

        #processing text_b
        for i in range(len(text_b)):
            id_blank = word2id['BLANK']
            ids = [id_blank for _ in range(max_length)]
            content_b = list(jieba.cut(text_b[i], cut_all=False))
            for j in range(len(content_b)):
                if j >= max_length:
                    break
                else:
                    if content_b[j] in word2id:
                        ids[j] = word2id[content_b[j]]
                    else:
                        ids[j] = word2id['UNK']
            length_b.append(min(max_length, len(content_b)))
            text_b[i] = ids
        text_b = np.array(text_b)
        length_b = np.array(length_b)

        #processing y
        res = []
        for i in range(len(y)):
            label = [0 for _ in range(conf.class_num)]
            label[y[i]] = 1
            res.append(label)
        y = np.array(res)

        #save files
        with open(path1, 'wb') as save_file:
            pickle.dump(text_a, save_file)
        with open(path2, 'wb') as save_file:
            pickle.dump(length_a, save_file)
        with open(path3, 'wb') as save_file:
            pickle.dump(text_b, save_file)
        with open(path4, 'wb') as save_file:
            pickle.dump(length_b, save_file)
        with open(path5, 'wb') as save_file:
            pickle.dump(y, save_file)

        return text_a, length_a, text_b, length_b, y
    else:
        with open(path1, 'rb') as read_file:
            text_a = pickle.load(read_file)
        with open(path2, 'rb') as read_file:
            length_a = pickle.load(read_file)
        with open(path3, 'rb') as read_file:
            text_b = pickle.load(read_file)
        with open(path4, 'rb') as read_file:
            length_b = pickle.load(read_file)
        with open(path5, 'rb') as read_file:
            y = pickle.load(read_file)

        return text_a, length_a, text_b, length_b, y
def dev_data_processing(data_path):
    conf = config.Config()
    path1 = os.path.join(data_path, 'text_a_dev.pkl')
    path2 = os.path.join(data_path, 'length_a_dev.pkl')
    path3 = os.path.join(data_path, 'text_b_dev.pkl')
    path4 = os.path.join(data_path, 'length_b_dev.pkl')
    path5 = os.path.join(data_path, 'y_dev.pkl')
    dev_data_path = os.path.join(data_path, 'dev.txt')
    if ((os.path.exists(path1)) & (os.path.exists(path2)) & (os.path.exists(path3)) & (
            os.path.exists(path4)) & (os.path.exists(path5))) == 0:
        text_a = []
        text_b = []
        length_a = []
        length_b = []
        max_length = conf.max_length
        y = []

        with open(dev_data_path, 'r', encoding='utf-8') as read_data:
            all_content = read_data.readlines()
            random.shuffle(all_content)
        for content in all_content:
            if content:
                line = content.strip().split('\t')
                text_a.append(line[0])
                text_b.append(line[1])
                y.append(int(line[2]))
        #processing text_a
        for i in range(len(text_a)):
            id_blank = word2id['BLANK']
            ids = [id_blank for _ in range(max_length)]
            content_a = list(jieba.cut(text_a[i], cut_all=False))
            for j in range(len(content_a)):
                if j >= max_length:
                    break
                else:
                    if content_a[j] in word2id:
                        ids[j] = word2id[content_a[j]]
                    else:
                        ids[j] = word2id['UNK']
            length_a.append(min(max_length, len(content_a)))
            text_a[i] = ids
        text_a = np.array(text_a)
        length_a = np.array(length_a)

        #processing text_b
        for i in range(len(text_b)):
            id_blank = word2id['BLANK']
            ids = [id_blank for _ in range(max_length)]
            content_b = list(jieba.cut(text_b[i], cut_all=False))
            for j in range(len(content_b)):
                if j >= max_length:
                    break
                else:
                    if content_b[j] in word2id:
                        ids[j] = word2id[content_b[j]]
                    else:
                        ids[j] = word2id['UNK']
            length_b.append(min(max_length, len(content_b)))
            text_b[i] = ids
        text_b = np.array(text_b)
        length_b = np.array(length_b)

        #processing y
        res = []
        for i in range(len(y)):
            label = [0 for _ in range(conf.class_num)]
            label[y[i]] = 1
            res.append(label)
        y = np.array(res)

        #save files
        with open(path1, 'wb') as save_file:
            pickle.dump(text_a, save_file)
        with open(path2, 'wb') as save_file:
            pickle.dump(length_a, save_file)
        with open(path3, 'wb') as save_file:
            pickle.dump(text_b, save_file)
        with open(path4, 'wb') as save_file:
            pickle.dump(length_b, save_file)
        with open(path5, 'wb') as save_file:
            pickle.dump(y, save_file)

        return text_a, length_a, text_b, length_b, y
    else:
        with open(path1, 'rb') as read_file:
            text_a = pickle.load(read_file)
        with open(path2, 'rb') as read_file:
            length_a = pickle.load(read_file)
        with open(path3, 'rb') as read_file:
            text_b = pickle.load(read_file)
        with open(path4, 'rb') as read_file:
            length_b = pickle.load(read_file)
        with open(path5, 'rb') as read_file:
            y = pickle.load(read_file)

        return text_a, length_a, text_b, length_b, y
def test_data_processing(data_path):
    conf = config.Config()
    path1 = os.path.join(data_path, 'text_a_test.pkl')
    path2 = os.path.join(data_path, 'length_a_test.pkl')
    path3 = os.path.join(data_path, 'text_b_test.pkl')
    path4 = os.path.join(data_path, 'length_b_test.pkl')
    path5 = os.path.join(data_path, 'y_test.pkl')
    test_data_path = os.path.join(data_path, 'test.txt')
    if ((os.path.exists(path1)) & (os.path.exists(path2)) & (os.path.exists(path3)) & (
            os.path.exists(path4)) & (os.path.exists(path5))) == 0:
        text_a = []
        text_b = []
        length_a = []
        length_b = []
        max_length = conf.max_length
        y = []

        with open(test_data_path, 'r', encoding='utf-8') as read_data:
            all_content = read_data.readlines()
            random.shuffle(all_content)
        for content in all_content:
            if content:
                line = content.strip().split('\t')
                text_a.append(line[0])
                text_b.append(line[1])
                y.append(int(line[2]))
        #processing text_a
        for i in range(len(text_a)):
            id_blank = word2id['BLANK']
            ids = [id_blank for _ in range(max_length)]
            content_a = list(jieba.cut(text_a[i], cut_all=False))
            for j in range(len(content_a)):
                if j >= max_length:
                    break
                else:
                    if content_a[j] in word2id:
                        ids[j] = word2id[content_a[j]]
                    else:
                        ids[j] = word2id['UNK']
            length_a.append(min(max_length, len(content_a)))
            text_a[i] = ids
        text_a = np.array(text_a)
        length_a = np.array(length_a)

        #processing text_b
        for i in range(len(text_b)):
            id_blank = word2id['BLANK']
            ids = [id_blank for _ in range(max_length)]
            content_b = list(jieba.cut(text_b[i], cut_all=False))
            for j in range(len(content_b)):
                if j >= max_length:
                    break
                else:
                    if content_b[j] in word2id:
                        ids[j] = word2id[content_b[j]]
                    else:
                        ids[j] = word2id['UNK']
            length_b.append(min(max_length, len(content_b)))
            text_b[i] = ids
        text_b = np.array(text_b)
        length_b = np.array(length_b)

        #processing y
        res = []
        for i in range(len(y)):
            label = [0 for _ in range(conf.class_num)]
            label[y[i]] = 1
            res.append(label)
        y = np.array(res)

        #save files
        with open(path1, 'wb') as save_file:
            pickle.dump(text_a, save_file)
        with open(path2, 'wb') as save_file:
            pickle.dump(length_a, save_file)
        with open(path3, 'wb') as save_file:
            pickle.dump(text_b, save_file)
        with open(path4, 'wb') as save_file:
            pickle.dump(length_b, save_file)
        with open(path5, 'wb') as save_file:
            pickle.dump(y, save_file)

        return text_a, length_a, text_b, length_b, y
    else:
        with open(path1, 'rb') as read_file:
            text_a = pickle.load(read_file)
        with open(path2, 'rb') as read_file:
            length_a = pickle.load(read_file)
        with open(path3, 'rb') as read_file:
            text_b = pickle.load(read_file)
        with open(path4, 'rb') as read_file:
            length_b = pickle.load(read_file)
        with open(path5, 'rb') as read_file:
            y = pickle.load(read_file)

        return text_a, length_a, text_b, length_b, y


def load_data_label():
    # get some relevant file paths
    code_path = os.getcwd()
    last_path = os.path.abspath(os.path.join(code_path, '..'))
    data_path = os.path.join(last_path, 'data')
    global word2id, id2word, embeddings
    word2id, id2word, embeddings = get_word2id_id2word_embeddings(data_path)

    text_a_train, length_a_train, text_b_train, length_b_train, y_train = train_data_processing(data_path)
    text_a_dev, length_a_dev, text_b_dev, length_b_dev, y_dev = dev_data_processing(data_path)
    text_a_test, length_a_test, text_b_test, length_b_test, y_test = test_data_processing(data_path)

    return embeddings, text_a_train, length_a_train, text_b_train, length_b_train, y_train, \
            text_a_dev, length_a_dev, text_b_dev, length_b_dev, y_dev, \
           text_a_test, length_a_test, text_b_test, length_b_test, y_test



if __name__=='__main__':
    load_data_label()