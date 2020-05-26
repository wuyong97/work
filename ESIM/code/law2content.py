#!/usr/bin/env python
# coding=utf-8
import re
import pickle
import os
def law2content(law, dicc):
    entry = law
    # flag=True
    try:
        if re.compile(r'第.*条第.款及第.款').search(entry.strip()):
            tmp = re.compile(r'第.*条第.款及第.款').search(entry.strip()).group(0)
            tmp_list = tmp.split('及')
            key1 = tmp_list[0]
            key2 = (re.compile(r'第.*条').search(key1).group(0)) + tmp_list[1]
            # print(key1, key2)
            # print("connect")
            return dicc[key1] + "。" + dicc[key2]
        elif re.compile(r'第.*条第.款和第.款').search(entry.strip()):
            tmp = re.compile(r'第.*条第.款和第.款').search(entry.strip()).group(0)
            tmp_list = tmp.split('和')
            key1 = tmp_list[0]
            key2 = (re.compile(r'第.*条').search(key1).group(0)) + tmp_list[1]
            # print(key1, key2)
            # print("connect")
            return dicc[key1] + "。" + dicc[key2]

        elif re.compile(r'第.*条第.款、第.*条之[一|二|三|四|五|六|七|八|九|十]').search(entry.strip()):
            tmp = re.compile(r'第.*条第.款、第.*条之[一|二|三|四|五|六|七|八|九|十]').search(entry.strip()).group(0)
            tmp_list = tmp.split('、')
            key1 = tmp_list[0]
            key2 = tmp_list[1]
            # print(key1, key2)
            # print("connect")
            return dicc[key1] + "。" + dicc[key2]

        elif re.compile(r'第.*条第.款、第.款').search(entry.strip()):
            tmp = re.compile(r'第.*条第.款、第.款').search(entry.strip()).group(0)
            tmp_list = tmp.split('、')
            key1 = tmp_list[0]
            key2 = (re.compile(r'第.*条').search(key1).group(0)) + tmp_list[1]
            # print(key1, key2)
            # print("connect")
            return dicc[key1] + "。" + dicc[key2]

        elif re.compile(r'第.*条第.、.款').search(entry.strip()):
            tmp = re.compile(r'第.*条第.、.款').search(entry.strip()).group(0)
            tmp_list = tmp.split('、')
            key1 = tmp_list[0] + "款"
            key2 = (re.compile(r'第.*条').search(key1).group(0)) + "第" + tmp_list[1]
            # print(key1, key2)
            # print("connect")
            return dicc[key1] + "。" + dicc[key2]
        elif re.compile(r'第.*条第.款，第.款').search(entry.strip()):
            tmp = re.compile(r'第.*条第.款，第.款').search(entry.strip()).group(0)
            tmp_list = tmp.split('，')
            key1 = tmp_list[0]
            key2 = (re.compile(r'第.*条').search(key1).group(0)) + tmp_list[1]
            # print(key1, key2)
            # print("connect")
            return dicc[key1] + "。" + dicc[key2]
        elif re.compile(r'第.*条之[一|二|三|四|五|六|七|八|九|十]').search(entry.strip()):
            tmp = re.compile(r'第.*条之[一|二|三|四|五|六|七|八|九|十]').search(entry.strip()).group(0)
            key1 = tmp
            # print(key1)
            return dicc[key1]
        elif re.compile(r'第.*条第.*款').search(entry.strip()):
            tmp = re.compile(r'第.*条第.*款').search(entry.strip()).group(0)
            key1 = tmp
            # print(key1)
            return dicc[key1]
        elif re.compile(r'第.*条').search(entry.strip()):
            tmp = re.compile(r'第.*条').search(entry.strip()).group(0)
            key1 = tmp
            # print(key1)
            return dicc[key1]

        else:
            # print(entry)
            # flag = False
            return entry
    except:
        print("ERROR:{}".format(entry))

def extract_law_content(passage):
    entry = passage
    law_original= []

    try:
        if re.compile(r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]条第.款及第.款').findall(entry.strip()):
            result_list = re.compile(r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]条第.款及第.款').findall(entry.strip())
            for tmp in result_list:
                law_original.append(tmp)
                # tmp_list = tmp.split('及')
                # key1 = tmp_list[0]
                # key2 = (re.compile(r'第.*条').search(key1).group(0)) + tmp_list[1]
                # law_list.append(key1)
                # law_list.append(key2)
        if re.compile(r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条第.款及第.款').findall(
                entry.strip()):
            result_list = re.compile(
                r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条第.款及第.款').findall(entry.strip())
            for tmp in result_list:
                law_original.append(tmp)
                # tmp_list = tmp.split('及')
                # key1 = tmp_list[0]
                # key2 = (re.compile(r'第.*条').search(key1).group(0)) + tmp_list[1]
                # law_list.append(key1)
                # law_list.append(key2)
        if re.compile(r'第[一|二|三|四|五|六|七|八|九|十]百[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条第.款及第.款').findall(
            entry.strip()):
            result_list = re.compile(
                r'第[一|二|三|四|五|六|七|八|九|十]百[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条第.款及第.款').findall(entry.strip())
            for tmp in result_list:
                law_original.append(tmp)
                # tmp_list = tmp.split('及')
                # key1 = tmp_list[0]
                # key2 = (re.compile(r'第.*条').search(key1).group(0)) + tmp_list[1]
                # law_list.append(key1)
                # law_list.append(key2)

            # print(key1, key2)
            # print("connect")
            # return dicc[key1]+"。"+dicc[key2]
        if re.compile(r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]条第.款和第.款').findall(entry.strip()):
            result_list = re.compile(r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]条第.款和第.款').findall(entry.strip())
            for tmp in result_list:
                law_original.append(tmp)
                # tmp_list = tmp.split('和')
                # key1 = tmp_list[0]
                # key2 = (re.compile(r'第.*条').search(key1).group(0)) + tmp_list[1]
                # law_list.append(key1)
                # law_list.append(key2)
        if re.compile(r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条第.款和第.款').findall(
            entry.strip()):
            result_list = re.compile(
                r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条第.款和第.款').findall(entry.strip())
            for tmp in result_list:
                law_original.append(tmp)
                # tmp_list = tmp.split('和')
                # key1 = tmp_list[0]
                # key2 = (re.compile(r'第.*条').search(key1).group(0)) + tmp_list[1]
                # law_list.append(key1)
                # law_list.append(key2)
        if re.compile(r'第[一|二|三|四|五|六|七|八|九|十]百[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条第.款和第.款').findall(
            entry.strip()):
            result_list = re.compile(
                r'第[一|二|三|四|五|六|七|八|九|十]百[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条第.款和第.款').findall(entry.strip())
            for tmp in result_list:
                law_original.append(tmp)
                # tmp_list = tmp.split('和')
                # key1 = tmp_list[0]
                # key2 = (re.compile(r'第.*条').search(key1).group(0)) + tmp_list[1]
                # law_list.append(key1)
                # law_list.append(key2)
            # print(key1, key2)
            # print("connect")
            # return dicc[key1]+"。"+dicc[key2]



        if re.compile(r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]条第.款、第.款').findall(entry.strip()):
            result_list = re.compile(r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]条第.款、第.款').findall(entry.strip())
            for tmp in result_list:
                law_original.append(tmp)
                # tmp_list = tmp.split('、')
                # key1 = tmp_list[0]
                # key2 = (re.compile(r'第.*条').search(key1).group(0)) + tmp_list[1]
                # law_list.append(key1)
                # law_list.append(key2)
        if re.compile(r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条第.款、第.款').findall(
            entry.strip()):
            result_list = re.compile(
                r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条第.款、第.款').findall(entry.strip())
            for tmp in result_list:
                law_original.append(tmp)
                # tmp_list = tmp.split('、')
                # key1 = tmp_list[0]
                # key2 = (re.compile(r'第.*条').search(key1).group(0)) + tmp_list[1]
                # law_list.append(key1)
                # law_list.append(key2)
        if re.compile(r'第[一|二|三|四|五|六|七|八|九|十]百[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条第.款、第.款').findall(
            entry.strip()):
            result_list = re.compile(
                r'第[一|二|三|四|五|六|七|八|九|十]百[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条第.款、第.款').findall(entry.strip())
            for tmp in result_list:
                law_original.append(tmp)
                # tmp_list = tmp.split('、')
                # key1 = tmp_list[0]
                # key2 = (re.compile(r'第.*条').search(key1).group(0)) + tmp_list[1]
                # law_list.append(key1)
                # law_list.append(key2)

            # print(key1, key2)
            # print("connect")
            # return dicc[key1] + "。"+ dicc[key2]

        if re.compile(r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]条第.、.款').findall(entry.strip()):
            result_list = re.compile(r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]条第.、.款').findall(entry.strip())
            for tmp in result_list:
                law_original.append(tmp)
                # tmp_list = tmp.split('、')
                # key1 = tmp_list[0] + "款"
                # key2 = (re.compile(r'第.*条').search(key1).group(0)) + "第"+ tmp_list[1]
                # law_list.append(key1)
                # law_list.append(key2)
        if re.compile(r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条第.、.款').findall(
            entry.strip()):
            result_list = re.compile(r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条第.、.款').findall(
                entry.strip())
            for tmp in result_list:
                law_original.append(tmp)
                # tmp_list = tmp.split('、')
                # key1 = tmp_list[0] + "款"
                # key2 = (re.compile(r'第.*条').search(key1).group(0)) + "第" + tmp_list[1]
                # law_list.append(key1)
                # law_list.append(key2)
        if re.compile(r'第[一|二|三|四|五|六|七|八|九|十]百[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条第.、.款').findall(
            entry.strip()):
            result_list = re.compile(r'第[一|二|三|四|五|六|七|八|九|十]百[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条第.、.款').findall(
                entry.strip())
            for tmp in result_list:
                law_original.append(tmp)
                # tmp_list = tmp.split('、')
                # key1 = tmp_list[0] + "款"
                # key2 = (re.compile(r'第.*条').search(key1).group(0)) + "第" + tmp_list[1]
                # law_list.append(key1)
                # law_list.append(key2)
            # print(key1, key2)
            # print("connect")
            # return dicc[key1] + "。"+dicc[key2]

        if re.compile(r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]条第.款，第.款').findall(entry.strip()):
            result_list = re.compile(r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]条第.款，第.款').findall(entry.strip())
            for tmp in result_list:
                law_original.append(tmp)
                # tmp_list = tmp.split('，')
                # key1 = tmp_list[0]
                # key2 = (re.compile(r'第.*条').search(key1).group(0)) + tmp_list[1]
                # law_list.append(key1)
                # law_list.append(key2)
        if re.compile(r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条第.款，第.款').findall(
            entry.strip()):
            result_list = re.compile(
                r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条第.款，第.款').findall(entry.strip())
            for tmp in result_list:
                law_original.append(tmp)
                # tmp_list = tmp.split('，')
                # key1 = tmp_list[0]
                # key2 = (re.compile(r'第.*条').search(key1).group(0)) + tmp_list[1]
                # law_list.append(key1)
                # law_list.append(key2)
        if re.compile(r'第[一|二|三|四|五|六|七|八|九|十]百[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条第.款，第.款').findall(
            entry.strip()):
            result_list = re.compile(
                r'第[一|二|三|四|五|六|七|八|九|十]百[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条第.款，第.款').findall(entry.strip())
            for tmp in result_list:
                law_original.append(tmp)
                # tmp_list = tmp.split('，')
                # key1 = tmp_list[0]
                # key2 = (re.compile(r'第.*条').search(key1).group(0)) + tmp_list[1]
                # law_list.append(key1)
                # law_list.append(key2)
            # print(key1, key2)
            # print("connect")
            # return dicc[key1] + "。"+ dicc[key2]

        if re.compile(r'第.*条之[一|二|三|四|五|六|七|八|九|十]').findall(entry.strip()):
            result_list = re.compile(r'第.*条之[一|二|三|四|五|六|七|八|九|十]').findall(entry.strip())
            for tmp in result_list:
                law_original.append(tmp)
                # law_list.append(tmp)

            # print(key1)
            # return dicc[key1]
        if re.compile(r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]条第.款').findall(entry.strip()):
            result_list = re.compile(r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]条第.款').findall(entry.strip())
            for tmp in result_list:
                law_original.append(tmp)
                # law_list.append(tmp)
        if re.compile(r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条第.款').findall(
            entry.strip()):
            result_list = re.compile(r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条第.款').findall(
                entry.strip())
            for tmp in result_list:
                law_original.append(tmp)
                # law_list.append(tmp)
        if re.compile(r'第[一|二|三|四|五|六|七|八|九|十]百[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条第.款').findall(
            entry.strip()):
            result_list = re.compile(r'第[一|二|三|四|五|六|七|八|九|十]百[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条第.款').findall(
                entry.strip())
            for tmp in result_list:
                law_original.append(tmp)
                # law_list.append(tmp)
            # print(key1)
            # return dicc[key1]


        if re.compile(r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]条').findall(entry.strip()):
            result_list = re.compile(r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]条').findall(entry.strip())
            for tmp in result_list:
                law_original.append(tmp)
                # law_list.append(tmp)
        if re.compile(r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]条').findall(entry.strip()):
            result_list = re.compile(r'第[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]条').findall(
                entry.strip())
            for tmp in result_list:
                law_original.append(tmp)
                # law_list.append(tmp)
        if re.compile(r'第[一|二|三|四|五|六|七|八|九|十]百[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条').findall(entry.strip()):
            result_list = re.compile(r'第[一|二|三|四|五|六|七|八|九|十]百[一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十][一|二|三|四|五|六|七|八|九|十]?条').findall(
                entry.strip())
            for tmp in result_list:
                law_original.append(tmp)
                # law_list.append(tmp)

        return law_original

            # print(key1)
            # return dicc[key1]
        # else:
            # print(entry)
            # return entry
    except:

        print("No law found in :{}".format(entry))

def law_list_filter(law_list):
    new_list=[]
    delete_index=[]
    for i in range(len(law_list)):
        for j in range(len(law_list)):
            if i == j:
                pass
            else:
                if law_list[i] in law_list[j]:
                    delete_index.append(i)

    for i in range(len(law_list)):
        if i in delete_index:
            pass
        else:
            new_list.append(law_list[i])
    return new_list

def get_law_content(passage):
    ques=[]
    code_path = os.getcwd()
    last_path = os.path.abspath(os.path.join(code_path, '..'))
    data_path = os.path.join(last_path, 'data')
    with open(data_path+'/new_criminal_law_dic.pkl', "rb") as r:
        dicc = pickle.load(r)
    law_original = extract_law_content(passage)
    law_original = law_list_filter(list(set(law_original)))
    for item in law_original:
        ques.append(law2content(item, dicc))

    return law_original, ques

def get_context_result_law_ques(passage):

    passage_temp = passage[::-1]
    context_s = len(passage) - 4 - passage_temp.find("为认院本")
    context_e = passage.find("判决如下") - 1
    context = passage[context_s:context_e]

    result_s = context_e + 6
    result_e = passage.find("如不服本判决")
    result = passage[result_s:result_e]

    law_original, ques = get_law_content(context)
    return context, result, law_original, ques
