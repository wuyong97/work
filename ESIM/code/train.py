#!/usr/bin/python
# -*- coding: UTF-8 -*-
import tensorflow as tf
import numpy as np
from model import ESIM_model
from init import load_data_label
import config as config
from tqdm import tqdm
from sklearn.metrics import f1_score
from sklearn import metrics
import os
code_path = os.getcwd()
last_path = os.path.abspath(os.path.join(code_path, '..'))
result_path = os.path.join(last_path, 'result')
con = config.Config()
os.environ["CUDA_VISIBLE_DEVICES"]="1"

class TrainModel(object):
    '''
        训练模型
        保存模型
    '''
    def get_batches(self, text_a_train, length_a_train, text_b_train, length_b_train, y_train):
        num_batch = int(len(text_a_train) / con.batch_Size)
        for i in range(num_batch):
            a = text_a_train[i*con.batch_Size:(i+1)*con.batch_Size]
            length_a = length_a_train[i*con.batch_Size:(i+1)*con.batch_Size]
            b = text_b_train[i*con.batch_Size:(i+1)*con.batch_Size]
            length_b = length_b_train[i * con.batch_Size:(i + 1) * con.batch_Size]
            t = y_train[i*con.batch_Size:(i+1)*con.batch_Size]
            yield a, length_a, b, length_b, t


    def trainModel(self):
        embeddings, text_a_train, length_a_train, text_b_train, length_b_train, y_train, \
        text_a_dev, length_a_dev, text_b_dev, length_b_dev, y_dev, \
        text_a_test, length_a_test, text_b_test, length_b_test, y_test = load_data_label()
        # 定义训练用的循环神经网络模型
        with tf.variable_scope('esim_model', reuse=None):
            # esim model
            model = ESIM_model(True, embeddings, con)

        # 训练模型
        with tf.Session() as sess:
            tf.global_variables_initializer().run()
            saver = tf.train.Saver()
            best_f1 = 0.0
            for time in range(con.epoch):
                print("training " + str(time + 1) + ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                model.is_trainning = True
                loss_all = []
                accuracy_all = []
                for texta, length_a, textb, length_b, tag in tqdm(self.get_batches(text_a_train, length_a_train, text_b_train, length_b_train, y_train)):
                    feed_dict = {
                        model.text_a: texta,
                        model.text_b: textb,
                        model.y: tag,
                        model.dropout_keep_prob: con.dropout_keep_prob,
                        model.a_length: length_a,
                        model.b_length: length_b
                    }
                    _, cost, accuracy = sess.run([model.train_op, model.loss, model.accuracy], feed_dict)
                    loss_all.append(cost)
                    accuracy_all.append(accuracy)
                    print("epoch:" + str((time + 1)) + "\n" + "batch loss：" + str(cost) + "\n" + "Accuracy：" +
                          str(accuracy))
                with open(result_path + "/result.txt", "a+") as f:
                    f.write("Train第" + str((time + 1)) + "次迭代的损失为：" + str(np.mean(np.array(loss_all))) + ";准确率为：" +
                            str(np.mean(np.array(accuracy_all))) + '\n')

                print("第" + str((time + 1)) + "次迭代的损失为：" + str(np.mean(np.array(loss_all))) + ";准确率为：" +
                      str(np.mean(np.array(accuracy_all))))

                def dev_step(time):
                    """
                    Evaluates model on a dev set
                    """
                    loss_all = []
                    accuracy_all = []
                    predictions = []
                    for texta, length_a, textb, length_b, tag in tqdm(self.get_batches(text_a_dev, length_a_dev, text_b_dev, length_b_dev, y_dev)):
                        feed_dict = {
                            model.text_a: texta,
                            model.text_b: textb,
                            model.y: tag,
                            model.dropout_keep_prob: 1.0,
                            model.a_length: length_a,
                            model.b_length: length_b
                        }
                        dev_cost, dev_accuracy, prediction = sess.run([model.loss, model.accuracy,
                                                                       model.prediction], feed_dict)
                        loss_all.append(dev_cost)
                        accuracy_all.append(dev_accuracy)
                        predictions.extend(prediction)
                    y_true = [np.nonzero(x)[0][0] for x in y_dev]
                    y_true = y_true[0:len(loss_all) * con.batch_Size]
                    f1 = f1_score(np.array(y_true), np.array(predictions), average='weighted')
                    print("验证集：loss {:g}, acc {:g}, f1 {:g}\n".format(np.mean(np.array(loss_all)),
                                                                      np.mean(np.array(accuracy_all)), f1))
                    with open(result_path + "/result.txt", "a+") as f:
                        f.write("Dev第" + str((time + 1)) + "次迭代的损失为：" + str(np.mean(np.array(loss_all))) + ";准确率为：" +
                                str(np.mean(np.array(accuracy_all))) + '\n')
                    return f1

                def test_step(time):
                    """
                    Evaluates model on a test set
                    """
                    loss_all = []
                    accuracy_all = []
                    predictions = []
                    for texta, length_a, textb, length_b, tag in tqdm(
                            self.get_batches(text_a_test, length_a_test, text_b_test, length_b_test, y_test)):
                        feed_dict = {
                            model.text_a: texta,
                            model.text_b: textb,
                            model.y: tag,
                            model.dropout_keep_prob: 1.0,
                            model.a_length: length_a,
                            model.b_length: length_b
                        }
                        test_cost, test_accuracy, prediction = sess.run([model.loss, model.accuracy,
                                                                       model.prediction], feed_dict)
                        loss_all.append(test_cost)
                        accuracy_all.append(test_accuracy)
                        predictions.extend(prediction)
                    y_true = [np.nonzero(x)[0][0] for x in y_test]
                    y_true = y_true[0:len(loss_all) * con.batch_Size]
                    f1 = f1_score(np.array(y_true), np.array(predictions), average='weighted')
                    print('分类报告:\n', metrics.classification_report(np.array(y_true), predictions))
                    print("测试集：loss {:g}, acc {:g}, f1 {:g}\n".format(np.mean(np.array(loss_all)),
                                                                      np.mean(np.array(accuracy_all)), f1))
                    with open(result_path + "/result.txt", "a+") as f:
                        f.write("Test第" + str((time + 1)) + "次迭代的损失为：" + str(np.mean(np.array(loss_all))) + ";准确率为：" +
                                str(np.mean(np.array(accuracy_all))) + '\n')
                    return f1

                model.is_trainning = False
                f1 = dev_step(time=time)

                if f1 > best_f1:
                    best_f1 = f1
                    saver.save(sess, result_path + "/save_model/model.ckpt")
                    print("Saved model success\n")
                    print("Start Test!\n")
                    _ = test_step(time=time)


if __name__ == '__main__':
    train = TrainModel()
    train.trainModel()