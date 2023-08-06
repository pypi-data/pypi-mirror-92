import re
import unicodedata
import nltk
from nltk.corpus import stopwords
import pandas as pd
from sklearn.utils import shuffle

nltk.download('stopwords')


def __unicode_to_ascii(s):
    """

    :param s:
    :return:
    """
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


def __clean_stopwords_shortwords(w):
    """

    :param w:
    :return:
    """
    stopwords_list = stopwords.words('english')
    words = w.split()
    clean_words = [
        word for word in words
        if (word not in stopwords_list) and len(word) > 2
    ]
    return " ".join(clean_words)


def __preprocess_sentence(w):
    """

    :param w:
    :return:
    """
    w = __unicode_to_ascii(w.lower().strip())
    w = re.sub(r'https*\S+', ' ', w)
    w = re.sub(r"([?.!,¿])", r" ", w)
    w = re.sub(r'[" "]+', " ", w)
    w = re.sub(r"[^a-zA-Z?.!,¿]+", " ", w)
    w = __clean_stopwords_shortwords(w)
    w = re.sub(r'@\w+', '', w)
    return w


def clean_dataframe(df):
    """

    :param df:
    :return:
    """
    print('File has {} rows and {} columns'.format(df.shape[0], df.shape[1]))
    df = df.rename(columns={0: "label", 1: "text"})
    # Drop NaN valuues, if any
    df = df.dropna()
    # Reset index after dropping the columns/rows with NaN values
    df = df.reset_index(drop=True)
    # Shuffle the dataset
    df = shuffle(df)
    # Print all the unique labels in the dataset
    print('Available labels: ', df.label.unique())
    # Clean the text column using preprocess_sentence function defined above
    df['text'] = df['text'].map(__preprocess_sentence)
    return df
