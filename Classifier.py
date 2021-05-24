import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


class Classifier:
    def __init__(self, train_data_file: str):
        spam_df = pd.read_csv(train_data_file)

        # By vectorization the email text we mean that we convert each word and
        # text into tokens with their value and the count of their occurrence
        self.vectorizer = CountVectorizer()
        countVectorizer = self.vectorizer.fit_transform(spam_df['text'])

        self.NB_classifier = MultinomialNB()
        label = spam_df['spam'].values
        self.NB_classifier.fit(countVectorizer, label)  # train

    def testData(self, test_data_file: str):
        spam_test = pd.read_csv(test_data_file)
        x = self.vectorizer.transform(spam_test['text'])
        y = spam_test['spam'].values
        y_predict_test = self.NB_classifier.predict(x)
        print(classification_report(y, y_predict_test))
        
        # cm = confusion_matrix(y, y_predict_test)
        # specificity = cm[1, 1] / (cm[1, 0] + cm[1, 1])#TN/TN+FP
        # accuracy = (cm[0, 0] + cm[1, 1]) / sum(sum(cm))#TP+TN/TP+TN+FP+FN
        # precision = cm[0, 0] / (cm[0, 0] + cm[1, 1])#TP/(TP+FP)
        # recall=cm[0,0]/(cm[0,0]+cm[0,1]) #TP/(TP+TN)
    def predictSpam(self, emails: list) -> list:
        sampleVectorizer = self.vectorizer.transform(emails)
        result = self.NB_classifier.predict(sampleVectorizer)
        return result.tolist()


# classifier = Classifier('emails.csv')
# classifier.testData('email_test.csv')
