import tensorflow as tf
import os
from law2content import get_context_result_law_ques
from parse_intended_harm import get_weights, get_json_result
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
    weight23=[]
    passage = "指定辩护人范岩岩，封丘县法律援助中心指派律师。封丘县人民检察院以新封检公诉刑诉〔2019〕172号起诉书指控被告人李祖文犯故意伤害罪，于2019年4月12日向本院提起公诉。本院审查后，于2019年4月12日受理，依法适用简易程序，并依法组成合议庭，公开开庭审理了本案。封丘县人民检察院指派检察员岳凌云、代检察员王凌朝出庭支持公诉，被告人李祖文及其辩护人范岩岩等到庭参加诉讼，现已审理终结。公诉机关指控:2018年9月23日2时许，在封丘县李庄新区水厂大门口北京路上，王某等人于被告人李祖文等人因是否堵车发生争执引起打架，李祖文手持啤酒瓶先将王某头部砸伤，接着李祖文手持烂过的啤酒瓶把儿将李某扎伤。经封丘县公安局物证鉴定室鉴定，王某、李某至损失均属轻伤二级。2018年12月12日被告人李祖文外逃后投案，并如实供述了故意伤害的犯罪事实。2018年12月12日，被告人李祖文与被害人王某、李某达成和解。上述事实，被告人李祖文及其辩护人在开庭审理过程中对公诉机关指控的犯罪事实及罪名均无异议，并有书证被告人李祖文的接处警登记表、抓获（自首）证明、户籍证明、无前科证明、住院病历、调解协议、收到条、谅解书；证人韩某、付某、张某、司某的证言；被害人王某、李某的陈述；被告人李祖文的供述与辩解；封丘县公安局物证鉴定室意见书；现场图、现场照片等证据证实，足以认定。" \
              "本院认为，被告人李祖文故意伤害他人身体，致二人轻伤，犯罪事实清楚，证据确实充分，其行为已构成故意伤害罪，公诉机关指控罪名成立，本院予以支持。被告人李祖文外逃后又主动投案，并如实供述其涉嫌的犯罪事实，其行为符合自首的法律构成要件，系自首，依法从轻处罚。被告人李祖文与被害人达成和解，取得被害人的谅解，酌定从轻处罚。根据被告人李祖文的犯罪事实、情节、认罪悔罪表现，犯罪情节较轻，且有悔罪表现，没有再犯罪的危险，宣告缓刑对所居住社区没有重大不良影响，并到其驻所地接受矫正，在此期间应当遵守法律、法规，服从司法行政机关的监督和管理，积极参加公益劳动，做一名有益于社会的公民。" \
              "依照《中华人民共和国刑法》第二百三十四条第一款、第六十七条第一款、第七十二条第一款、第七十三条第二、三款之规定，判决如下:被告人李祖文犯故意伤害罪，判处有期徒刑一年零三个月，缓刑二年。（缓刑考验期限，从判决确定之日起计算）"

    #生成的result为判决结果，law_original为原始法条，例如"第二百三十四条",law_list为法条具体内容，与law_original内容一一对应
    context, result, law_original, law_list = get_context_result_law_ques(passage)

    #weight12为判决结果与法条之间权值
    weight12 = get_weights(law_list=law_list, result=result)
    text_a = []
    text_b = []
    #fact_list为事实
    fact_list = context.split('。')[0:-1]
    for entry1 in law_list:
        for entry2 in fact_list:
            text_a.append(entry1)
            text_b.append(entry2)

    infer = Infer()
    score = infer.infer(text_a, text_b) #生成两个句子之间的score
    for i in range(len(score)):
        weight23.append(score[i][1])
    dic = get_json_result(result, law_list, fact_list, weight12, weight23, 0.5)