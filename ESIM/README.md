This repository is an Tensorflow_based implementation of ESIM model. Refer to paper "Enhanced LSTM for Natural Language Inference",which, I think,
is a combination of LSTM and Attention Mechanism for contextual inference.
1."/code"
1.1 config.py
Provide some parameters for training, like learning rate, dropout rate...a
1.2 init.py
Mainly make some data preprocessing, including read files, word segmentation, word2vec, turn the label into one-hot for training. Keep in mind that
the original data(train.txt, dev.txt, test.txt) relevant to Law is made by myself for work.
1.3 model.py
An implementation of ESIM model based on tensorflow < 2.1.0. And also refer to others' work.
1.4 train.py
Including train, dev, and test the model.implementation

2. "/data"
the original data: train.txt, dev.txt, test.txt
data from the source code of paper"Few-Shot Charge Prediction with Discriminative Legal Attributes": words.vec, word2id.pkl
id2word.pkl, embeddings.pkl
Other "*pkl" data are generated by "/code/init.py" for quick preparation of data

3. "/result"
Some results of the model, including the saved model and the results of training, dev, test(loss, accuracy, f1_score) in result.txt

4.Run the model
Just run "/code/train.py" and your computer or server will print out the information during training, dev, and test