#!/usr/bin/env python
# coding=utf-8
#处理离婚纠纷案件
import re
import os
import json
import numpy as np
code_path = os.getcwd()
last_path = os.path.abspath(os.path.join(code_path, '..'))
result_path = os.path.join(last_path, 'result')
def parse_reason(reason):
    reason = reason[-300:].replace('、《', '，《').replace('以及', '').replace('和《', '，《').replace('相关法律法规', '').replace(
        '、最高人民法院', '，最高人民法院').replace('的规定，《', '，《').replace('规定，《', '，《')
    res = []
    tmp = re.compile(r'依(照|据)(《.+?)(的|之)*(相关)*规定').findall(reason)
    # tmp = re.compile(r'依(照|据)(《.+?)(的|之)*(相关)*规定，').findall(reason)
    for each in tmp:
        if '《' in each[1] and '》' in each[1]:
            cites = each[1]
            # if '依照' in cites or '依据' in cites:
            #     cites=re.compile(r'(依照|依据)+(.+?)$').search(cites).group(2)
            cites = cites.split('，')
            for a in cites:
                if '《' not in a or '》' not in a or (a[-1] != '款' and a[-1] != '条' and a[-1] != '项'):
                    if a == '':
                        del a
                    else:
                        cites = []
                res.append(a)
    return res
def parse_fact(fact):
    res = ''
    same_as_declarartion = re.compile(r'(查明|认定)(.*)(与|同)(.*)一致').search(fact) != None

    # if any(a in fact for a in ['事实如下', '如下事实', '如下情况', '情况如下']):
    try:
        res1= re.compile(r'((事实|情况)如下|(以下|如下)(案件)?(事实|情况))(.*?)(：|，|。)(.+?)(\r|\n|$|本院认为)').search(fact).groups()
        res += res1[5]
        res += res1[6]
        res += res1[7]

    except AttributeError:
        pass

    try:
        res += re.compile(r'经审理查明(.*?)(：|，)(.+?)($|本院认为)').search(fact).groups()[-2]
    except AttributeError:
        pass

    # if '经审理查明' in fact:
    #     res += re.compile(r'经审理查明(.*?)(：|，)(.+?)(\r|\n|$)').search(fact).groups()[-2]
    tmp = re.compile(r'(起诉称：|事实(与|和)理由：)(.+?)(\r|\n|$|以上事实)').search(fact)
    # if tmp != None and (same_as_declarartion or res == ''):
    if res=='' and tmp != None and same_as_declarartion:
        res += tmp.groups()[-2]

    # if res=='':
    #     return ''
    # if '经审理查明，' in fact:
    #     res+=re.compile(r'经审理查明，(.*)\r').search(fact)
    # res=re.compile(r'(认定事实如下(：|，)|经审理查明，|((事实(与|和)理由：).*查明|认定.*与|同.*一致)\r)').split(fact)[-1].strip()
    # tmp = re.compile(r'(另|又|再|还|同时)查明，(.+?)(\r|\n|$)').findall(fact)
    # if tmp != []:
    #     for each in tmp:
    #         res += each[1]
    return res.strip()
# passage="原告:于燕，女，住址山东省威海高区。被告:刘昆，男，住址河南省郸城县。原告于燕与被告刘昆离婚纠纷一案，本院于2019年12月17日立案后，依法适用普通程序，公开开庭进行了审理。原告于燕到庭参加诉讼，被告刘昆经本院公告传唤，无正当理由拒不到庭参加诉讼。本案现已审理终结。于燕向本院提出诉讼请求:一、准予原被告离婚；二婚生女刘紫钰归原告抚养，被告每月支付抚养费2000元。事实和理由:原、被告于2013年12月13日结婚，婚后育有一女刘紫钰。被告于2017年11月离家，并不再与原告联系，导致夫妻感情破裂，故提起诉讼。刘昆未作答辩。本院经审理认定事实如下:原、被告于2013年12月13日登记结婚，婚后于2014年9月1日生育一女刘紫钰。本院认为，原、被告结婚多年并育有一女，应认定双方建立了夫妻感情。原告未提交证据证明夫妻感情确已破裂，故原告要求离婚证据不足，本院不予支持。依照《中华人民共和国婚姻法》第三十二条  、《中华人民共和国民事诉讼法》第一百四十四条 规定，判决如下:不准原告于燕与被告刘昆离婚。案件受理费50元，由原告于燕负担。如不服本判决，可以在判决书送达之日起十五日内，向本院递交上诉状，并按照对方当事人或者代表人的人数提出副本，上诉于山东省威海市中级人民法院。"
def get_fact_reasons_result(passage):
    fact = (parse_fact(fact=passage)).split('。')
    fact_list = [i for i in fact if i != '']
    # fact_list.append('jhhhhhhh')
    passage_temp = passage[::-1]
    context_s = len(passage) - 4 - passage_temp.find("为认院本")
    context_e = passage.find("判决如下") - 1
    context = passage[context_s:context_e]
    result_s = context_e + 6
    result_e = passage.find("如不服本判决")
    result = passage[result_s:result_e]

    laws = parse_reason(context)
    reason_list = context.split('。')[0:-1]
    score12 = [1.0 for i in range(len(reason_list))]
    string=''
    for item in reason_list:
        string += item
    if (result.find('驳回')>=0) or ((result.find('不'))>=0):
        if string.find('不予支持')>=0:
            pass
        else:
            score12 = [0.0 for i in range(len(reason_list))]
    else:
        if string.find('予以支持') >= 0:
            pass
        else:
            score12 = [0.0 for i in range(len(reason_list))]

    for entry in laws:
        score12.append(1.0)

    return result, laws, reason_list, fact_list, score12
# print(1)

# score12 = [1, 2, 3, 4]
# score23 = [0.1, 0.5, 0.2, 0.3, 0.4, 10, 0.88, 0.999]
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

def get_json_result(result, reason_list, fact_list, score12, score23, threshold_vale=0.5):
    length2 = len(reason_list)
    length3 = len(fact_list)

    offspring1 = []
    dic = {}
    dic['id'] = 123456

    for i in range(length2):
        dicc1 = {}
        offspring = []
        if score12[i] >= threshold_vale:
            dicc1['content'] = reason_list[i]
            dicc1['score'] = score12[i]
        else:
            pass
        for j in range(length3):
            dicc2 = {}
            if score23[j + length3 * i] >= threshold_vale:
                dicc2['content'] = fact_list[j]
                dicc2['score'] = score23[j + length3 * i]
                offspring.append(dicc2)
            else:
                pass
        if offspring:
            dicc1['offspring'] = offspring

        offspring1.append(dicc1)
    dic3 = {}
    dic3['content'] = result
    if offspring1:
        dic3['offspring'] = offspring1
    dic['root'] = dic3
    # print(dic)
    with open(result_path + "/result_divorce.json", 'w', encoding='utf-8') as f:
        json.dump(dic, f, ensure_ascii=False, cls=NpEncoder)
    return dic
law_articles = ['《中华人民共和国民事诉讼法》迪一百三十四条、第一百四十二条','《中华人民共和国婚姻法》第三十二条、第三十九条及《最高人民法院关于适用<中华人民共和国民事诉讼法>的解释》第九十条第二款','《最高人民法院关于适用<中华人民共和国婚姻法>若干问题的解释（二）》第十条']
def law_articles_process(law_list):
    law_main = []
    law_other = []
    for law in law_list:
        if law.find('中华人民共和国婚姻法')==-1:
            law_other.append(law)
        else:
            if law.find('及《') == -1:
                print(1)

            else:
                index=law.find('及《')
                law_other.append(law[index:])

    return None
text='《中华人民共和国婚姻法》第三十二条、第三十六条、第三十七条第一款、第三十八条第一款、第二款、第三十九条第一款'
tmp = re.compile(r'依(照|据)(《.+?)(的|之)*(相关)*规定').findall(text)