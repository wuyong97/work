This repository is an Tensorflow_based implementation of ESIM model. Refer to paper "Enhanced LSTM for Natural Language Inference",which, I think, is a combination of LSTM and Attention Mechanism for contextual inference.

# 1."/code"
## 1.1 `config.py`  
Provide some parameters for training, like learning rate, dropout rate...
## 1.2 `init.py`  
Mainly make some data preprocessing, including read files, word segmentation, word2vec, turn the label into one-hot for training. Keep in mind that the original data(train.txt, dev.txt, test.txt) relevant to Law is made by myself for work. 
## 1.3 `model.py` 
An implementation of ESIM model based on tensorflow < 2.0. And also refer to others' work. 
## 1.4 `train.py`  
Including train, dev, and test the model.  
After every opoch, the model will be verified on `dev` set. If the `f1 score` is getting better, `then` the model will be tested on `test` set. And we can get the finall result on `test` set.  
Make a `Prediction` based on `trained` model.  
## 1.5 `init_infer.py`  
For infering a new passage, mainly including `word segmentation`,  `word2id`. And turn the data into the form the model need.
## 1.6 `parse_intended_harm.py`  
Processing the `故意伤害罪` 裁判文书，mainly including `law extraction`, `fact extraction`, `reason extraction`.  
## 1.7 `infer_intended_harm.py`  
Accordin to the `故意伤害罪` 裁判文书, make an inference based on the trained mdoel.  
## 1.8 `parse_divorce.py`  
Processing the `离婚纠纷` 裁判文书，mainly including `law extraction`, `fact extraction`, `reason extraction`.  
## 1.7 `infer_divorce.py`  
Accordin to the `离婚纠纷` 裁判文书, make an inference based on the trained mdoel. 


# 2."/data"  
the `original` data: `train.txt`, `dev.txt`, `test.txt`.  
data from the source code of paper"Few-Shot Charge Prediction with Discriminative Legal Attributes": words.vec, `word2id.pkl`
id2word.pkl, `embeddings.pkl`. However, `these data` are too big to upload.If you need them, PLZ publish a issue and give me your email.  
Other "*pkl" data are generated by `"/code/init.py"` for quick preparation of data.

# 3."/result"  
Some results of the model, including the saved model and the results of training, dev, test(loss, accuracy, f1_score) in `result.txt`.  
And the `json` files are the results generated by infering.

# 4.Run the model  
Just run `"/code/train.py"` and your computer or server will print out the information during training, dev, and test.
