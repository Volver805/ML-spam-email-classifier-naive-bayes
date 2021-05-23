import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


spam_df = pd.read_csv("emails.csv")
ham_emails = spam_df[spam_df['spam'] == 0]
spam_emails = spam = spam_df[spam_df['spam'] == 1]

# By vectorization the email text we mean that we convert each word and text into tokens with their value and the count
# of their occurrence
vectorizer = CountVectorizer()
countVectorizer = vectorizer.fit_transform(spam_df['text'])

NB_classifier = MultinomialNB()
label = spam_df['spam'].values
NB_classifier.fit(countVectorizer, label)  # train

spam_test = pd.read_csv('email_test.csv')

x = vectorizer.transform(spam_test['text'])
y = spam_test['spam'].values
y_predict_test = NB_classifier.predict(x)
cm = confusion_matrix(y, y_predict_test)
specificity = cm[1, 1] / (cm[1, 0] + cm[1, 1])
accuracy = (cm[0, 0] + cm[1, 1]) / sum(sum(cm))
precision = cm[0, 0] / (cm[0, 0] + cm[1, 1])
print(f'Specificity : {specificity}\nAccuracy : {accuracy}\nPrecision : {precision}')
print(classification_report(y, y_predict_test))


def predictSpam(emails: list) -> list:
    sampleVectorizer = vectorizer.transform(emails)
    return NB_classifier.predict(sampleVectorizer)


