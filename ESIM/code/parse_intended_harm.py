#!/usr/bin/env python
# coding=utf-8
import re
import numpy as np
import json
import os
code_path = os.getcwd()
last_path = os.path.abspath(os.path.join(code_path, '..'))
result_path = os.path.join(last_path, 'result')

def get_tuxing_huanxing(kind, result):

    logit_dic = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10, "1": 1, "2": 2,
                 "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "两": 2}
    if kind =="徒刑":
        tuxing1 = re.compile(r"['徒刑'|'拘役'|'管制'].*月，").findall(result.strip())
        tuxing2 = re.compile(r'徒刑.*年，').findall(result.strip())
        if tuxing1:
            tuxing = tuxing1[0][:-1][2:]
        else:
            tuxing = tuxing2[0][:-1][2:]

    if kind == "缓刑":
        tuxing1 = re.compile(r'缓刑.*月').findall(result.strip())
        tuxing2 = re.compile(r'缓刑.*年').findall(result.strip())
        if tuxing1:
            tuxing = tuxing1[0][2:]
        else:
            tuxing = tuxing2[0][2:]

    year = re.compile(r'[一|二|三|四|五|六|七|八|九|十|两][一|二|三|四|五|六|七|八|九|十|两]?[一|二|三|四|五|六|七|八|九|十|两]?年').findall(tuxing)
    month = re.compile(r'[一|二|三|四|五|六|七|八|九|十|两][一|二|三|四|五|六|七|八|九|十|两]?个月').findall(tuxing)
    year_logit = 0.0
    month_logit = 0.0
    if (year!=[]) and  (month!=[]):

        year_num = list(year[0][:-1])
        if len(year_num) == 1:
            year_logit = logit_dic[year_num[0]]
        if len(year_num) == 2:
            year_logit = 10 + logit_dic[year_num[-1]]
        if len(year_num) == 3:
            year_logit = 10 *logit_dic[year_num[0]]+logit_dic[year_num[2]]
        # print(year_logit)
        month_num = list(month[0][:-1][:-1])
        if len(month_num) == 1:
            month_logit = logit_dic[month_num[0]]
        if len(month_num) == 2:
            month_logit = 11
        # print(month_logit)

    if (year!=[]) and  (month==[]):
        year_num = list(year[0][:-1])
        if len(year_num) == 1:
            year_logit = logit_dic[year_num[0]]
        if len(year_num) == 2:
            year_logit = 10 + logit_dic[year_num[-1]]
        if len(year_num) == 3:
            year_logit = 10 *logit_dic[year_num[0]]+logit_dic[year_num[2]]
        # print(year_logit)

    if (year==[]) and  (month!=[]):
        month_num = list(month[0][:-1][:-1])
        if len(month_num) == 1:
            month_logit = logit_dic[month_num[0]]
        if len(month_num) == 2:
            month_logit = 11
        # print(month_logit)
    tuxing_logit = np.float(year_logit) + np.float(month_logit/12)

    return tuxing_logit

def get_weights(law_list, result):
    charge = re.compile(r'犯.*罪').findall(result.strip())[0][1:]
    huanxing = get_tuxing_huanxing(kind="缓刑", result=result)
    tuixng = get_tuxing_huanxing(kind="徒刑", result=result)
    # print(tuixng, huanxing)

    length = len(law_list)
    weights = [1.0 for i in range(length)]
    for i in range(length):
        if law_list[i].find(charge)!=-1:
            if tuixng >= 3.0:
                weights[i]=0.0
        if law_list[i].find("缓刑考验期限为原判刑期以上五年以下")!=-1:
            if 1.0 <= huanxing < 5.0:
                pass
            else:
                weights[i] = 0.0
    return weights

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
    with open(result_path + "/result_intended_harm.json", 'w', encoding='utf-8') as f:
        json.dump(dic, f, ensure_ascii=False, cls=NpEncoder)
    return dic
# passage="指定辩护人范岩岩，封丘县法律援助中心指派律师。封丘县人民检察院以新封检公诉刑诉〔2019〕172号起诉书指控被告人李祖文犯故意伤害罪，于2019年4月12日向本院提起公诉。本院审查后，于2019年4月12日受理，依法适用简易程序，并依法组成合议庭，公开开庭审理了本案。封丘县人民检察院指派检察员岳凌云、代检察员王凌朝出庭支持公诉，被告人李祖文及其辩护人范岩岩等到庭参加诉讼，现已审理终结。公诉机关指控:2018年9月23日2时许，在封丘县李庄新区水厂大门口北京路上，王某等人于被告人李祖文等人因是否堵车发生争执引起打架，李祖文手持啤酒瓶先将王某头部砸伤，接着李祖文手持烂过的啤酒瓶把儿将李某扎伤。经封丘县公安局物证鉴定室鉴定，王某、李某至损失均属轻伤二级。2018年12月12日被告人李祖文外逃后投案，并如实供述了故意伤害的犯罪事实。2018年12月12日，被告人李祖文与被害人王某、李某达成和解。上述事实，被告人李祖文及其辩护人在开庭审理过程中对公诉机关指控的犯罪事实及罪名均无异议，并有书证被告人李祖文的接处警登记表、抓获（自首）证明、户籍证明、无前科证明、住院病历、调解协议、收到条、谅解书；证人韩某、付某、张某、司某的证言；被害人王某、李某的陈述；被告人李祖文的供述与辩解；封丘县公安局物证鉴定室意见书；现场图、现场照片等证据证实，足以认定。" \
#         "本院认为，被告人李祖文故意伤害他人身体，致二人轻伤，犯罪事实清楚，证据确实充分，其行为已构成故意伤害罪，公诉机关指控罪名成立，本院予以支持。被告人李祖文外逃后又主动投案，并如实供述其涉嫌的犯罪事实，其行为符合自首的法律构成要件，系自首，依法从轻处罚。被告人李祖文与被害人达成和解，取得被害人的谅解，酌定从轻处罚。根据被告人李祖文的犯罪事实、情节、认罪悔罪表现，犯罪情节较轻，且有悔罪表现，没有再犯罪的危险，宣告缓刑对所居住社区没有重大不良影响，并到其驻所地接受矫正，在此期间应当遵守法律、法规，服从司法行政机关的监督和管理，积极参加公益劳动，做一名有益于社会的公民。" \
#         "依照《中华人民共和国刑法》第二百三十四条第一款、第六十七条第一款、第七十二条第一款、第七十三条第二、三款之规定，判决如下:被告人李祖文犯故意伤害罪，判处有期徒刑一年零三个月，缓刑二年。（缓刑考验期限，从判决确定之日起计算）"
# context, result, law_original, law_list = get_context_result_law_ques(passage)
# print("原始裁判文书:{}".format(context))
# print(result)
# print(law_original)
# print(law_list)
# result = "被告人杨金纲犯故意伤害罪，判处有期徒刑三年六个月，缓刑三年。（缓刑考验期限，从判决确定之日起计算）"
# law_list=["【故意伤害罪】故意伤害他人身体的，处三年以下有期徒刑、拘役或者管制", "自首】犯罪以后自动投案，如实供述自己的罪行的，是自首。对于自首的犯罪分子，可以从轻或者减轻处罚。其中，犯罪较轻的，可以免除处罚",
#           "【适用条件】对于被判处拘役、三年以下有期徒刑的犯罪分子，同时符合下列条件的，可以宣告缓刑，对其中不满十八周岁的人、怀孕的妇女和已满七十五周岁的人，应当宣告缓刑：（一）犯罪情节较轻；（二）有悔罪表现；（三）没有再犯罪的危险；（四）宣告缓刑对所居住社区没有重大不良影响",
#           "犯罪嫌疑人虽不具有前两款规定的自首情节，但是如实供述自己罪行的，可以从轻处罚；因其如实供述自己罪行，避免特别严重后果发生的，可以减轻处罚"]
# print("判决结果 与 法条之间 连接权值：{}".format(get_weights(law_list=law_list, result=result)))
# fact_list = context.split('。')[0:-1]
# print(fact_list)




