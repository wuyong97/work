class Config(object):

    def __init__(self):
        self.embedding_size = 100  # 词向量维度
        self.hidden_num = 100  # 隐藏层规模
        self.l2_lambda = 0.0
        self.learning_rate = 0.0001
        self.dropout_keep_prob = 0.5
        self.attn_size = 200
        self.K = 2

        self.epoch = 20
        self.batch_Size = 32
        self.class_num = 2
        self.max_length = 128
