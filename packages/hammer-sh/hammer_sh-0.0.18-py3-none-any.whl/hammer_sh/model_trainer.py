import tensorflow as tf
import pandas as pd
import numpy as np
import tensorflow.keras
from sklearn.model_selection import train_test_split
from transformers import *
from transformers import BertTokenizer, TFBertModel, BertConfig


class ModelTrainer:

    def __init__(self, model_name, save_path, data):
        """

        :param model_name:
        :param save_path:
        :param data:
        """
        self.callbacks = []
        self.input_ids = []
        self.attention_masks = []
        self.labels = []
        self.train_inp = None
        self.val_inp = None
        self.train_label = None
        self.val_label = None
        self.train_mask = None
        self.val_mask = None
        self.history = None
        self.save_path = save_path
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.data = data
        num_classes = len(data.label.unique())
        print("There are " + str(num_classes) + " unique Classes in the Dataset")
        self.model = TFBertForSequenceClassification.from_pretrained(model_name, num_labels=num_classes)

    def auto_train(self):
        """

        :return:
        """
        self.tokenize_data()
        self.train_test_split()
        self.define_model()
        self.train_model()

    def tokenize_data(self, max_length=128):
        """

        :param max_length:
        :return:
        """
        print("Tokenize Data \n")
        self.data['gt'] = self.data['label'].map({
            'Chemistry': 0,
            'Computer Sience': 1,
            'Medicine': 2
        })
        self.data.head()

        sentences = self.data['text']
        self.labels = self.data['gt']

        for sent in sentences:
            tokenizer = self.tokenizer
            bert_inp = tokenizer.encode_plus(sent,add_special_tokens=True,max_length=max_length,return_attention_mask=True)
            self.input_ids.append(bert_inp['input_ids'])
            self.attention_masks.append(bert_inp['attention_mask'])

        self.input_ids = np.asarray(self.input_ids, dtype="object")
        self.attention_masks = np.array(self.attention_masks, dtype="object")
        self.labels = np.array(self.labels)

        self.input_ids = pd.DataFrame(self.input_ids.tolist())
        self.attention_masks = pd.DataFrame(self.attention_masks.tolist())
        self.labels = pd.DataFrame(self.labels.tolist())
        self.input_ids = self.input_ids.fillna(0).astype('int32')
        self.attention_masks = self.attention_masks.fillna(0).astype('int32')
        print('Input shape {} Attention mask shape {} Input label shape {}'.format(self.input_ids.shape,
                                                                                   self.attention_masks.shape,
                                                                                   self.labels.shape))

    def train_test_split(self):
        """

        :return:
        """
        print("Train Test Split \n")
        self.train_inp, self.val_inp, self.train_label, self.val_label, self.train_mask, self.val_mask = train_test_split(
            self.input_ids, self.labels, self.attention_masks, test_size=0.2)

    def define_model(self):
        """

        :return:
        """
        print("Define Model \n")
        log_dir = 'logs/'
        model_save_path = 'logs/bert_model.h5'
        """ self.callbacks = [
            tensorflow.keras.callbacks.ModelCheckpoint(filepath=model_save_path,
                                                       save_weights_only=True,
                                                       monitor='val_loss',
                                                       mode='min',
                                                       save_best_only=True),
            tensorflow.keras.callbacks.TensorBoard(log_dir=log_dir)
        ] """
        print('\nBert Model', self.model.summary())

        loss = tensorflow.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        metric = tensorflow.keras.metrics.SparseCategoricalAccuracy('accuracy')
        optimizer = tensorflow.keras.optimizers.Adam(learning_rate=2e-5, epsilon=1e-08)

        self.model.compile(loss=loss, optimizer=optimizer, metrics=[metric])

    def train_model(self):
        """

        :return:
        """
        print("Train Model \n")
        self.history = self.model.fit([self.train_inp, self.train_mask],
                                      self.train_label,
                                      verbose=1,
                                      batch_size=32,
                                      epochs=4,
                                      callbacks=self.callbacks,
                                      validation_data=([self.val_inp, self.val_mask], self.val_label))
