from sklearn.metrics import confusion_matrix, f1_score, classification_report


""" def show_tensorboard():
    %load_ext tensorboard
    %tensorboard --logdir {log_dir} """


class Evaluator:
    def __init__(self, model_trainer):
        """

        :param model_trainer:
        """
        self.model = model_trainer.model
        self.pred_labels =[]
        self.val_inp = model_trainer.val_inp
        self.val_label = model_trainer.val_label
        self.val_mask = model_trainer.val_mask
        self.tokenizer = model_trainer.tokenizer

    def evaluate_model(self):
        """

        :return:
        """
        preds = self.model.predict([self.val_inp, self.val_mask], batch_size=32)
        self.pred_labels = preds.logits.argmax(axis=1)

        f1 = f1_score(self.val_label, self.pred_labels, average='micro')
        print('F1 score', f1)
        print('Classification Report')
        target_names = ['Computer Sience', 'Chemistry', 'Medicine']
        print(classification_report(self.val_label, self.pred_labels, target_names=target_names))

    def show_comparison(self):
        """

        :return:
        """
        lookup = {'0': "Chemistry", '1': "Computer Sience", '2': "Medicine"}
        val_label_list = self.val_label.values.tolist()
        val_inp_list = self.val_inp.values.tolist()
        for idx, label in enumerate(self.pred_labels):

            if label == val_label_list[idx][0]:
                icon = "✔️"
            else:
                icon = "❌"

            print(icon, "Predicted: ", lookup[str(label)], "\t=> Actual: ", lookup[str(val_label_list[idx][0])])
            abstract = self.tokenizer.convert_ids_to_tokens(ids=val_inp_list[idx], skip_special_tokens='False')
            print("Abstract: ", ' '.join(abstract))
            print("\n")