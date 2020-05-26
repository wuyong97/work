import tensorflow as tf
import os
from parse_divorce import get_json_result, get_fact_reasons_result
from init_infer import data_processing
code_path = os.getcwd()
last_path = os.path.abspath(os.path.join(code_path, '..'))
result_path = os.path.join(last_path, 'result')
os.environ["CUDA_VISIBLE_DEVICES"]="0"

class Infer(object):
    """
        ues model to predict classification.
    """
    def __init__(self):
        self.checkpoint_file = tf.train.latest_checkpoint(result_path+'/save_model')
        graph = tf.Graph()
        with graph.as_default():
            session_conf = tf.ConfigProto(allow_soft_placement=True, log_device_placement=False)
            self.sess = tf.Session(config=session_conf)
            with self.sess.as_default():
                # Load the saved meta graph and restore variables
                saver = tf.train.import_meta_graph("{}.meta".format(self.checkpoint_file))
                saver.restore(self.sess, self.checkpoint_file)
                print("Restore model from " + result_path + "/save_model success!")
                # graph = tf.compat.v1.get_default_graph()
                # all_names = [op.name for op in graph.get_operations()]
                # print(all_names)

                # Get the placeholders from the graph by name
                self.text_a = graph.get_operation_by_name("esim_model/text_a").outputs[0]
                self.text_b = graph.get_operation_by_name("esim_model/text_b").outputs[0]
                self.a_length = graph.get_operation_by_name("esim_model/a_length").outputs[0]
                self.b_length = graph.get_operation_by_name("esim_model/b_length").outputs[0]
                self.drop_keep_prob = graph.get_operation_by_name("esim_model/dropout_keep_prob").outputs[0]

                # Tensors we want to evaluate
                self.prediction = graph.get_operation_by_name("esim_model/output/prediction").outputs[0]
                self.score = graph.get_operation_by_name("esim_model/output/score").outputs[0]

    def infer(self, text_a, text_b):
        # transfer to vector
        text_a, length_a, text_b, length_b = data_processing(text_a, text_b)
        feed_dict = {
            self.text_a: text_a,
            self.text_b: text_b,
            self.drop_keep_prob: 1.0,
            self.a_length: length_a,
            self.b_length: length_b
        }
        y, s = self.sess.run([self.prediction, self.score], feed_dict)
        return s


if __name__ == '__main__':
    score23=[]
    text_a = []
    text_b = []
     # passage = "指定辩护人范岩岩，封丘县法律援助中心指派律师。封丘县人民检察院以新封检公诉刑诉〔2019〕172号起诉书指控被告人李祖文犯故意伤害罪，于2019年4月12日向本院提起公诉。本院审查后，于2019年4月12日受理，依法适用简易程序，并依法组成合议庭，公开开庭审理了本案。封丘县人民检察院指派检察员岳凌云、代检察员王凌朝出庭支持公诉，被告人李祖文及其辩护人范岩岩等到庭参加诉讼，现已审理终结。公诉机关指控:2018年9月23日2时许，在封丘县李庄新区水厂大门口北京路上，王某等人于被告人李祖文等人因是否堵车发生争执引起打架，李祖文手持啤酒瓶先将王某头部砸伤，接着李祖文手持烂过的啤酒瓶把儿将李某扎伤。经封丘县公安局物证鉴定室鉴定，王某、李某至损失均属轻伤二级。2018年12月12日被告人李祖文外逃后投案，并如实供述了故意伤害的犯罪事实。2018年12月12日，被告人李祖文与被害人王某、李某达成和解。上述事实，被告人李祖文及其辩护人在开庭审理过程中对公诉机关指控的犯罪事实及罪名均无异议，并有书证被告人李祖文的接处警登记表、抓获（自首）证明、户籍证明、无前科证明、住院病历、调解协议、收到条、谅解书；证人韩某、付某、张某、司某的证言；被害人王某、李某的陈述；被告人李祖文的供述与辩解；封丘县公安局物证鉴定室意见书；现场图、现场照片等证据证实，足以认定。" \
    #           "本院认为，被告人李祖文故意伤害他人身体，致二人轻伤，犯罪事实清楚，证据确实充分，其行为已构成故意伤害罪，公诉机关指控罪名成立，本院予以支持。被告人李祖文外逃后又主动投案，并如实供述其涉嫌的犯罪事实，其行为符合自首的法律构成要件，系自首，依法从轻处罚。被告人李祖文与被害人达成和解，取得被害人的谅解，酌定从轻处罚。根据被告人李祖文的犯罪事实、情节、认罪悔罪表现，犯罪情节较轻，且有悔罪表现，没有再犯罪的危险，宣告缓刑对所居住社区没有重大不良影响，并到其驻所地接受矫正，在此期间应当遵守法律、法规，服从司法行政机关的监督和管理，积极参加公益劳动，做一名有益于社会的公民。" \
    #           "依照《中华人民共和国刑法》第二百三十四条第一款、第六十七条第一款、第七十二条第一款、第七十三条第二、三款之规定，判决如下:被告人李祖文犯故意伤害罪，判处有期徒刑一年零三个月，缓刑二年。（缓刑考验期限，从判决确定之日起计算）"
    passage = "原告:于燕，女，住址山东省威海高区。被告:刘昆，男，住址河南省郸城县。原告于燕与被告刘昆离婚纠纷一案，本院于2019年12月17日立案后，依法适用普通程序，公开开庭进行了审理。原告于燕到庭参加诉讼，被告刘昆经本院公告传唤，无正当理由拒不到庭参加诉讼。本案现已审理终结。于燕向本院提出诉讼请求:一、准予原被告离婚；二婚生女刘紫钰归原告抚养，被告每月支付抚养费2000元。事实和理由:原、被告于2013年12月13日结婚，婚后育有一女刘紫钰。被告于2017年11月离家，并不再与原告联系，导致夫妻感情破裂，故提起诉讼。刘昆未作答辩。本院经审理认定事实如下:原、被告于2013年12月13日登记结婚，婚后于2014年9月1日生育一女刘紫钰。本院认为，原、被告结婚多年并育有一女，应认定双方建立了夫妻感情。原告未提交证据证明夫妻感情确已破裂，故原告要求离婚证据不足，本院不予支持。依照《中华人民共和国婚姻法》第三十二条  、《中华人民共和国民事诉讼法》第一百四十四条 规定，判决如下:不准原告于燕与被告刘昆离婚。案件受理费50元，由原告于燕负担。如不服本判决，可以在判决书送达之日起十五日内，向本院递交上诉状，并按照对方当事人或者代表人的人数提出副本，上诉于山东省威海市中级人民法院。"

    result, law_list, reason_list, fact_list, score12 = get_fact_reasons_result(passage)

    for entry1 in reason_list:
        for entry2 in fact_list:
            text_a.append(entry1)
            text_b.append(entry2)

    infer = Infer()
    score = infer.infer(text_a, text_b) #生成两个句子之间的score
    for i in range(len(score)):
        score23.append(score[i][1])
    #生成JSON文件，并保存在"./result_divorce.json"路径下
    for entry in law_list:
        reason_list.append(entry)
        for _ in fact_list:
            score23.append(0.0)
    dic = get_json_result(result, reason_list, fact_list, score12, score23, 0.5)

