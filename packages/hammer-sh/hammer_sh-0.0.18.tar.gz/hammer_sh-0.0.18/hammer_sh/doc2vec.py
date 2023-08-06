from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from pandas import DataFrame
from typing import List
import numpy as np


def tag_data(df: DataFrame):
    """

    :param df:
    :return:
    """
    tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)])
                   for i, _d in enumerate(df.values().tolist())]
    return tagged_data


def train_model(tagged_data: List[TaggedDocument], max_epochs: int, vec_size: int, alpha: float):
    """

    :param tagged_data:
    :param max_epochs:
    :param vec_size:
    :param alpha:
    :return:
    """
    model = Doc2Vec(size=vec_size,
                    alpha=alpha,
                    min_alpha=0.00025,
                    min_count=1,
                    dm=1)
    model.build_vocab(tagged_data)
    for epoch in range(max_epochs):
        print('iteration {0}'.format(epoch))
        model.train(tagged_data,
                    total_examples=model.corpus_count,
                    epochs=model.iter)
        # decrease the learning rate
        model.alpha -= 0.0002
        # fix the learning rate, no decay
        model.min_alpha = model.alpha
    return model


def get_vector_of_doc(model: Doc2Vec, doc: str):
    """

    :param model:
    :param doc:
    :return:
    """
    doc_data = word_tokenize(doc.lower())
    vector = model.infer_vector(doc_data)
    print(vector)
    return vector


def get_similar_docs(model: Doc2Vec, vector: np.ndarray):
    """

    :param model:
    :param vector:
    :return:
    """
    similar_docs = model.docvecs.most_similar(vector)
    print(similar_docs)
    return similar_docs
