def bayes_comp(X_train, y_train, X_test, y_test):
    '''simple bayes classifier'''
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.pipeline import Pipeline
    from sklearn.feature_extraction.text import TfidfVectorizer

    model = Pipeline([
        ('vectorizer', TfidfVectorizer()),
        ('classifier', MultinomialNB(alpha=0.05)),
    ])

    model.fit(X_train, y_train)
    print(model.score(X_test, y_test))
    return model.score(X_test, y_test)


def clean(s):
    '''working with data'''
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


if __name__ == '__main__':
    import dispy, logging
    import math
    import csv
    import string
    # bayes
    with open("/home/hei_damn/Documents/python_homeworks/cluster/data/SMSSpamCollection") as f: # change route!
        data = list(csv.reader(f, delimiter="\t"))
    X, y = [], []
    for target, msg in data:
        X.append(msg)
        y.append(target)
        X = [clean(x).lower() for x in X]
    X_train, y_train, X_test, y_test = X[:390], y[:390], X[390:500], y[390:500]
    # cluster. You should choose JobCluster or SharedJobCluster 
    # cluster = dispy.JobCluster(bayes_comp) 
    cluster = dispy.SharedJobCluster(computation=bayes_comp, scheduler_node='192.168.43.54', depends=[sklearn]) # change IP!
    job = cluster.submit(X_train, y_train, X_test, y_test)
    result = job()
    print(result)