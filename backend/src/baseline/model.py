import nltk
import pandas as pd
from deeppavlov.models.tokenizers.nltk_moses_tokenizer import (
    NLTKMosesTokenizer as Tokenizer,
)
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

nltk.download("punkt")
nltk.download("stopwords")

import warnings
from typing import Literal

from nltk.collocations import *
from pymystem3 import Mystem
from tqdm import tqdm

warnings.filterwarnings("ignore", category=RuntimeWarning)

import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import precision_score
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder


class Preprocesser:
    def __init__(self):
        self.stopWords = set(stopwords.words("russian"))
        self.lemmatizer = Mystem()
        self.tokenizer = Tokenizer()

    def preprocess(self, text, custom_bigrams=None):
        text = text.lower()
        text = self.tokenizer([text])[0]
        text = list(filter(str.isalnum, text))
        text = list(
            filter(
                lambda tok: not str.isspace(tok),
                self.lemmatizer.lemmatize(" ".join(text)),
            )
        )
        tokens = list(word for word in text if word not in self.stopWords)
        if custom_bigrams is not None:
            i = 0
            res = []
            while i < len(tokens) - 1:
                bigram = tokens[i] + " " + tokens[i + 1]
                if bigram in custom_bigrams:
                    res += ["_".join(bigram.split())]
                    res += [tokens[i], tokens[i + 1]]
                    i += 2
                else:
                    res += [tokens[i]]
                    i += 1
            if i < len(tokens):
                res += [tokens[-1]]
            tokens = res
        return tokens


def get_custom_bigrams(
    train_df, ranking: Literal["freq", "tscore", "pmi", "llr"] = "freq"
):
    texts_question = []
    preprocesser = Preprocesser()
    for text in tqdm(train_df["question"]):
        text = preprocesser.preprocess(text)
        texts_question.append(" ".join(text))
    texts_content = []
    for text in tqdm(train_df["content"]):
        text = preprocesser.preprocess(text)
        texts_content.append(" ".join(text))
    bm = nltk.collocations.BigramAssocMeasures()
    s = " ".join([" ".join(texts_question), " ".join(texts_content)])
    f = BigramCollocationFinder.from_words(s.split())
    f.apply_freq_filter(5)
    N_best = 100
    if ranking == "freq":
        res = [" ".join(i) for i in f.nbest(bm.raw_freq, N_best)]
    if ranking == "tscore":
        res = [" ".join(i) for i in f.nbest(bm.student_t, N_best)]
    if ranking == "pmi":
        res = [" ".join(i) for i in f.nbest(bm.pmi, N_best)]
    if ranking == "llr":
        res = [" ".join(i) for i in f.nbest(bm.likelihood_ratio, N_best)]
    return set(res)


class ChatbotModel:
    """
    Класс для предсказания ответов на вопросы с использованием моделей TF-IDF и Word2Vec.

    Атрибуты:
    ----------
    data : dict
        Словарь с данными, включающий вопросы, ответы и соответствующие теги.
    tfidf_vectorizer : TfidfVectorizer
        Объект TfidfVectorizer для преобразования текстов в TF-IDF векторы.
    w2v_model : Word2Vec
        Обученная модель Word2Vec для векторизации текстов.
    label_encoder : LabelEncoder
        Объект LabelEncoder для преобразования текстовых ответов в числовые.
    tfidf_matrix : sparse matrix
        Матрица TF-IDF для вопросов в данных.
    """

    def __init__(self, data, label_encoder: LabelEncoder, bigram_ranking="freq"):
        """
        Инициализация модели, включает обучение TF-IDF и Word2Vec моделей, а также кодирование ответов.

        Параметры:
        ----------
        data : dict
            Словарь с данными, включающий вопросы, ответы и соответствующие теги.
        """
        self.data = data
        self.preprocesser = Preprocesser()

        # Векторизация вопросов для TF-IDF
        texts = self.data["question"].tolist()
        self.custom_bigrams = get_custom_bigrams(self.data, bigram_ranking)
        texts = [" ".join(self.preprocess(text)) for text in texts]
        self.tfidf_vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
        self.label_encoder = label_encoder

    def preprocess(self, text):
        return self.preprocesser.preprocess(text, self.custom_bigrams)

    def predict(self, question, method="tfidf"):
        """
        Возвращает предсказанный тег, ответ и оценку схожести для заданного вопроса.

        Параметры:
        ----------
        question : str
            Вопрос, на который нужно получить ответ.
        method : str, optional
            Метод, который будет использоваться для предсказания ('tfidf' или 'w2v'). По умолчанию 'w2v'.

        Возвращает:
        ----------
        tuple
            Предсказанный тег, ответ и оценка схожести.
        """
        if method == "tfidf":
            return self._predict_with_tfidf(question)
        elif method == "w2v":
            return self._predict_with_w2v(question)
        else:
            raise ValueError("Unknown method specified: use 'tfidf' or 'w2v'")

    def _predict_with_tfidf(self, question):
        """
        Предсказывает тег, ответ и оценку схожести с использованием TF-IDF.

        Параметры:
        ----------
        question : str
            Вопрос, на который нужно получить ответ.

        Возвращает:
        ----------
        tuple
            Предсказанный тег, ответ и оценка схожести.
        """
        question_tokens = self.preprocess(question)
        question = " ".join(question_tokens)
        question_tfidf = self.tfidf_vectorizer.transform([question])
        similarities = cosine_similarity(question_tfidf, self.tfidf_matrix)
        most_similar_answer_index = similarities.argmax()
        predicted_answer = self.data["content"].iloc[most_similar_answer_index]
        score = similarities[0][most_similar_answer_index]

        return predicted_answer, score

    def _predict_with_w2v(self, question):
        """
        Предсказывает тег, ответ и оценку схожести с использованием Word2Vec.

        Параметры:
        ----------
        question : str
            Вопрос, на который нужно получить ответ.

        Возвращает:
        ----------
        tuple
            Предсказанный тег, ответ и оценка схожести.
        """
        processed_question = self.preprocess(question)
        question_vector = np.mean(
            [
                self.w2v_model.wv[word]
                for word in processed_question
                if word in self.w2v_model.wv
            ],
            axis=0,
        )

        if question_vector.size == 0 or np.isnan(question_vector).any():
            question_vector = np.zeros(
                self.w2v_model.vector_size
            )  # Возвращаем нулевой вектор

        answer_vectors = []
        for answer in self.data["ответ"]:
            processed_answer = self.preprocess(answer)
            answer_vector = np.mean(
                [
                    self.w2v_model.wv[word]
                    for word in processed_answer
                    if word in self.w2v_model.wv
                ],
                axis=0,
            )
            if answer_vector.size == 0 or np.isnan(answer_vector).any():
                answer_vector = np.zeros(
                    self.w2v_model.vector_size
                )  # Возвращаем нулевой вектор
            answer_vectors.append(answer_vector)

        similarities = cosine_similarity([question_vector], answer_vectors)
        most_similar_answer_index = similarities.argmax()

        predicted_answer = self.data["ответ"][most_similar_answer_index]
        score = similarities[0][most_similar_answer_index]

        return predicted_answer, score

    def evaluate(self, test_questions, target_answers, method="tfidf"):
        """
        Оценивает модель по тестовым вопросам и выводит предсказанные теги, ответы и точность.

        Параметры:
        ----------
        test_questions : list of str
            Список тестовых вопросов.
        real_tags : list of str
            Список реальных тегов для тестовых вопросов.
        method : str, optional
            Метод, который будет использоваться для предсказания ('tfidf' или 'w2v'). По умолчанию 'w2v'.

        Возвращает:
        ----------
        tuple
            Точность модели и DataFrame с предсказаниями.
        """
        predicted_answers = []
        scores = []

        for question in test_questions:
            answer, score = self.predict(question, method=method)
            predicted_answers.append(answer)
            scores.append(score)

        # Кодируем реальные и предсказанные теги в числовой формат
        target_answers_encoded = self.label_encoder.transform(target_answers)
        predicted_answers_encoded = self.label_encoder.transform(predicted_answers)

        # Подсчитываем точность
        precision = precision_score(
            target_answers_encoded,
            predicted_answers_encoded,
            average="macro",
            zero_division=1,
        )

        # Создаем DataFrame для результатов
        results_df = pd.DataFrame(
            {
                "Question": test_questions,
                "Target Answers": target_answers,
                "Predicted Answer ({})".format(method): predicted_answers,
                "Score ({})".format(method): scores,
            }
        )

        return precision, results_df


if __name__ == "__main__":
    df = pd.read_excel("LK_modified.xlsx", sheet_name=1)
    category_counts = df["content"].value_counts()
    small_categories = category_counts[category_counts < 7].index
    df["content"] = df["content"].replace(small_categories, "поддержка")
    train_df, test_df = train_test_split(
        df, test_size=0.15, random_state=42, stratify=df["content"]
    )
    label_encoder = LabelEncoder().fit(df["content"])
    chatbot = ChatbotModel(train_df, label_encoder)
    print("macro-precision ", chatbot.evaluate(test_df["question"], test_df["content"]))
