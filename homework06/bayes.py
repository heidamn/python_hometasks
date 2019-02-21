import math
import csv
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

class NaiveBayesClassifier:

    def __init__(self, alpha = 0.05):
        self.alpha = alpha
        self.table = {}
        self.labels = []
        self.labels_part = []

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y.
        X: Данные, которые обрабатываем
        у: Классы, которым принадлежат данные"""
        for i,msg in enumerate(X):
            msg.split()
            self.labels = [i for i in set(y)]
            self.labels_part = [y.count(label) / len(y) for label in self.labels]
            for word in msg:
                if not self.table.get(word):
                    self.table.update({word: [[0 for _i in self.labels], [0 for _i in self.labels]]})
                else:
                    self.table[word][0][self.labels.index(y[i])] += 1
        d = len(self.table)
        n_labels = [0 for _i in self.labels]
        for i in range(len(n_labels)):
            for word in self.table:
                n_labels[i] += self.table[word][0][i]
        print (n_labels, self.labels_part, d, self.labels, self.table['g'], sep="\n")
        for word in self.table:
            for i in range(len(self.table[word][1])):
                self.table[word][1][i] = (self.alpha + self.table[word][0][i]) / (d + n_labels[i])
        print(self.table['q'])



    def predict(self, X):
        """ Perform classification on an array of test vectors X.
        Вычисление класса по входящим данным"""
        y = []
        for msg in X:
            predicted_nums = []
            msg.split()
            for i in range (len(self.labels)):
                predicted_num = math.log(self.labels_part[i])
                for word in msg:
                    if self.table.get(word):
                        predicted_num += math.log(self.table[word][1][i])
                predicted_nums.append(predicted_num)
            y.append(self.labels[predicted_nums.index(max(predicted_nums))])
        return y

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels.
        Проверка вероятности совпадения
        X_test: Данные, которые проверяем
        y_test: Классы, которым должны принадлежать Проверяемые Данные"""
        part = 0
        y = self.predict(X_test)
        for i in range(len(y_test)):
            if y[i] == y_test[i]:
                part += 1
        part /= len(y_test)
        return part

with open("data/SMSSpamCollection") as f:
    data = list(csv.reader(f, delimiter="\t"))
import string


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)
X, y = [], []
for target, msg in data:
    X.append(msg)
    y.append(target)
X = [clean(x).lower() for x in X]
X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]
model = NaiveBayesClassifier()
model.fit(X_train, y_train)
print(model.score(X_test, y_test))
model = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('classifier', MultinomialNB(alpha=0.05)),
])

model.fit(X_train, y_train)
print(model.score(X_test, y_test))