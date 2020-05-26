#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import pickle
import config
import jieba
import numpy as np
def get_word2id_id2word_embeddings(data_path):
    # get word2id,id2word,embeddings(already saved from paper'Few-shot')
    with open(os.path.join(data_path, 'word2id.pkl'), 'rb') as read_word2id:
        word2id = pickle.load(read_word2id)
    with open(os.path.join(data_path, 'id2word.pkl'), 'rb') as read_id2word:
        id2word = pickle.load(read_id2word)
    with open(os.path.join(data_path, 'embeddings.pkl'), 'rb') as read_embeddings:
        embeddings = pickle.load(read_embeddings)
    return word2id, id2word, embeddings
def data_processing(text_a, text_b):
    # get some relevant file paths
    code_path = os.getcwd()
    last_path = os.path.abspath(os.path.join(code_path, '..'))
    data_path = os.path.join(last_path, 'data')
    global word2id, id2word, embeddings
    word2id, id2word, embeddings = get_word2id_id2word_embeddings(data_path)
    conf = config.Config()
    length_a = []
    length_b = []
    max_length = conf.max_length

    # processing text_a
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

    # processing text_b
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

    return text_a, length_a, text_b, length_b

if __name__=='__main__':
    sentences = ['被告人唐善济故意伤害他人身体，致人轻伤，其行为已构成故意伤害罪', '【故意伤害罪】故意伤害他人身体的，处三年以下有期徒刑、拘役或者管制']
    text_a, length_a, text_b, length_b = data_processing(sentences)
    print(1)