import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords   # Requires NLTK in the include path.
import os
import pandas as pd

## List of stopwords
STOPWORDS = stopwords.words('english') # type: list(str)

train_type = "novels"

author_names = ["charles_dickens", "fyodor_dostoevsky", "mark_twain"]

authors = {name: [file for file in os.listdir(os.path.join(os.getcwd(), "data", "train", train_type, name))]
           for name in author_names}

num_novels = sum([len(authors[author]) for author in authors])

texts = []

for author in authors:
    for bookName in authors[author]:
        bookFilepath = os.path.join(os.getcwd(), "data", "train", train_type, author, bookName)
        print(bookFilepath)
        
        # read text in book
        with open(bookFilepath, encoding='utf-8', errors='ignore') as f:
            text = f.read()[1:]
        
        # simple preprocessing, make everything lowercase
        text = text.lower()
        texts += [text]
                
print("Number of novels: {}".format(len(texts)))

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

# extract word counts for each book
def get_tf(texts, vectorizer, transformer, isTestSet):
    features = pd.DataFrame(data=texts)
    
    counts = vectorizer.fit_transform(texts)
    counts = transformer.fit_transform(counts)
    
    return counts

def train_model(model, x_train, y_train):
    ''' TODO: train your model based on the training data '''
    model.fit(x_train, y_train)
    pass

def predict(model, x_test):
    ''' TODO: make your prediction here '''
    return model.predict(x_test)

model = MultinomialNB(fit_prior=False)
# don't include stopwords 
vectorizer = CountVectorizer(token_pattern=r'\b_?[a-z]\w*’?\w*_?\b', stop_words=STOPWORDS)
tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True) 
            
# x_train = array with shape [books, words]
x_train = get_tf(texts, vectorizer, tfidf_transformer, False)

# y_train = books
y_train = []
for author in authors:
    y_train += [author] * len(authors[author])
print(y_train)
train_model(model, x_train, y_train)

from utils.test_runner import *


# only count words that are in known vocab, ignore OOV words
def get_tfidf(queries, vectorizer, transformer):
    # count matrix 
    count_vector=vectorizer.transform(queries) 

    # tf-idf scores 
    tf_idf_vector=transformer.transform(count_vector)
        
    return tf_idf_vector

test_cases = get_all_tests()

tests = pd.Series(test_cases)
x_test = get_tfidf(tests, vectorizer, tfidf_transformer)

output_answers = predict(model, x_test)
check_test_results(output_answers, show_matrix=True)
